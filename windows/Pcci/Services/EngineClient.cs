using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading.Tasks;
using Pcci.Models;

namespace Pcci.Services;

/// <summary>
/// Talks to the pcci engine, which ships beside the app as engine\pcci.exe.
///
/// The contract is the engine's: with --json, stdout carries exactly one JSON object
/// and stderr carries JSON Lines. Nothing here parses human-readable text, and every
/// call is awaited off the UI thread.
/// </summary>
public sealed class EngineClient
{
    private readonly string _executable;

    public List<EngineLogLine> Log { get; } = new();

    public EngineClient(string? executable = null)
    {
        _executable = executable ?? FindEngine()
            ?? throw new EngineException(EngineError.Local(
                "The conversion engine is missing from this copy of PCCI.",
                "no pcci.exe found beside the application or on PATH"));
    }

    /// <summary>engine\pcci.exe beside the app, a development build, or PATH.</summary>
    public static string? FindEngine()
    {
        var baseDirectory = AppContext.BaseDirectory;
        var candidates = new[]
        {
            Path.Combine(baseDirectory, "engine", "pcci.exe"),
            Path.Combine(baseDirectory, "engine", "pcci"),
            Path.Combine(baseDirectory, "pcci.exe"),
            Path.GetFullPath(Path.Combine(baseDirectory, "..", "..", "..", "..", "..", "build", "engine", "pcci", "pcci.exe"))
        };
        foreach (var candidate in candidates)
        {
            if (File.Exists(candidate)) return candidate;
        }

        var path = Environment.GetEnvironmentVariable("PATH") ?? "";
        foreach (var directory in path.Split(Path.PathSeparator))
        {
            if (string.IsNullOrWhiteSpace(directory)) continue;
            var candidate = Path.Combine(directory, "pcci.exe");
            if (File.Exists(candidate)) return candidate;
        }
        return null;
    }

    public Task<JsonNode?> DoctorAsync() => RunJsonAsync(new[] { "doctor", "--json" });

    public async Task<SlidePlan> PlanAsync(string sourcePath, EngineConfig config)
    {
        var arguments = new List<string> { "plan", sourcePath, "--json" };
        arguments.AddRange(ConfigArguments(config));
        return DecodePlan(await RunAsync(arguments));
    }

    /// <summary>
    /// Re-plan from a song the user corrected. The chunking rules stay in the engine so
    /// the preview and the exported file can never disagree.
    /// </summary>
    public async Task<SlidePlan> PlanAsync(Song song, EngineConfig config)
    {
        var temporary = WriteTemporary(JsonSerializer.SerializeToUtf8Bytes(song), "song");
        try
        {
            var arguments = new List<string> { "plan", "--song", temporary, "--json" };
            arguments.AddRange(ConfigArguments(config));
            return DecodePlan(await RunAsync(arguments));
        }
        finally
        {
            TryDelete(temporary);
        }
    }

    // Songs from the web. Each of these ends at an ordinary file on disk, which the
    // existing Plan/Build calls then work on exactly as they would on a dropped file.

    /// <summary>
    /// Search every source. The artist is a filter and part of the question both: a
    /// bare title is a thousand songs on any source, a title with an artist is one.
    /// </summary>
    public async Task<SearchOutcome> SearchAsync(
        string query, int limit = 20, string artist = "", string album = "", string year = "")
    {
        var arguments = new List<string> { "search", query, "--limit", limit.ToString(), "--json" };
        if (!string.IsNullOrWhiteSpace(artist)) { arguments.Add("--artist"); arguments.Add(artist); }
        if (!string.IsNullOrWhiteSpace(album)) { arguments.Add("--album"); arguments.Add(album); }
        if (!string.IsNullOrWhiteSpace(year)) { arguments.Add("--year"); arguments.Add(year); }
        var output = await RunAsync(arguments);
        return JsonSerializer.Deserialize<SearchOutcome>(output)
            ?? throw new EngineException(EngineError.Local("The search returned nothing readable."));
    }

    /// <summary>Download the chart at a link. The engine picks where to keep it.</summary>
    public async Task<ImportedChart> FetchAsync(string url)
    {
        var output = await RunAsync(new[] { "fetch", url, "--json" });
        return JsonSerializer.Deserialize<ImportedChart>(output)
            ?? throw new EngineException(EngineError.Local("The download returned nothing readable."));
    }

    /// <summary>
    /// Hand the engine text copied from somewhere else.
    ///
    /// It goes over stdin rather than a temporary file so a chart copied out of an
    /// email never lands on disk as a file nobody asked for; the engine writes it out
    /// itself, once, under a name taken from the song.
    /// </summary>
    public async Task<ImportedChart> PasteAsync(string text)
    {
        var output = await RunAsync(new[] { "paste", "--json" }, input: text);
        return JsonSerializer.Deserialize<ImportedChart>(output)
            ?? throw new EngineException(EngineError.Local("The pasted chart could not be read."));
    }

    public async Task<ConversionResult> BuildAsync(SlidePlan plan, string destination, bool writeChordPro)
    {
        var payload = Encoding.UTF8.GetBytes(plan.Raw?.ToJsonString() ?? "{}");
        var temporary = WriteTemporary(payload, "plan");
        try
        {
            var arguments = new List<string>
            {
                "build", "--plan", temporary, "-o", destination, "--json"
            };
            if (writeChordPro) arguments.Add("--chordpro");
            var output = await RunAsync(arguments);
            return JsonSerializer.Deserialize<ConversionResult>(output)
                ?? throw new EngineException(EngineError.Local("The engine returned nothing."));
        }
        finally
        {
            TryDelete(temporary);
        }
    }

    private static IEnumerable<string> ConfigArguments(EngineConfig config) => new[]
    {
        "-n", config.LinesPerSlide.ToString(),
        "--target", config.ExportTarget,
        config.BalanceLastSlide ? "--balance" : "--no-balance",
        "--chords", config.ChordDelivery,
        "--chord-placement", config.ChordPlacement,
        config.ChordsOnSlide ? "--chords-on-slide" : "--no-chords-on-slide"
    };

    public static SlidePlan DecodePlan(string json)
    {
        var root = JsonNode.Parse(json)
            ?? throw new EngineException(EngineError.Local("The engine returned an empty plan."));
        return new SlidePlan
        {
            Song = root["song"].Deserialize<Song>() ?? new Song(),
            Slides = root["slides"].Deserialize<List<PlannedSlide>>() ?? new List<PlannedSlide>(),
            Config = root["config"].Deserialize<EngineConfig>() ?? new EngineConfig(),
            Warnings = root["warnings"].Deserialize<List<string>>() ?? new List<string>(),
            Raw = root
        };
    }

    private async Task<JsonNode?> RunJsonAsync(IEnumerable<string> arguments) =>
        JsonNode.Parse(await RunAsync(arguments));

    private async Task<string> RunAsync(IEnumerable<string> arguments, string? input = null)
    {
        Log.Clear();
        var info = new ProcessStartInfo
        {
            FileName = _executable,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            RedirectStandardInput = input is not null,
            UseShellExecute = false,
            CreateNoWindow = true,
            StandardOutputEncoding = Encoding.UTF8,
            StandardErrorEncoding = Encoding.UTF8,
            // Explicitly UTF-8 with no byte-order mark. The default here is the
            // console's code page, which on a Windows machine is whatever ANSI
            // codepage that machine happens to use - and a chart pasted from a web
            // page is full of characters that do not survive one.
            StandardInputEncoding = input is null ? null : new UTF8Encoding(false)
        };
        foreach (var argument in arguments)
        {
            info.ArgumentList.Add(argument);
        }

        using var process = new Process { StartInfo = info };
        try
        {
            process.Start();
        }
        catch (Exception exception)
        {
            throw new EngineException(EngineError.Local(
                "PCCI could not start its conversion engine.",
                $"{_executable}: {exception.Message}"));
        }

        var stdoutTask = process.StandardOutput.ReadToEndAsync();
        var stderrTask = process.StandardError.ReadToEndAsync();
        if (input is not null)
        {
            // Written after the readers are started and closed straight after: the
            // engine reads stdin to the end before it answers, so writing it with
            // nobody draining stdout would deadlock on a long chart.
            await process.StandardInput.WriteAsync(input);
            process.StandardInput.Close();
        }
        await process.WaitForExitAsync();
        var stdout = await stdoutTask;
        var stderr = await stderrTask;

        Log.AddRange(ParseLog(stderr));

        if (process.ExitCode != 0)
        {
            throw new EngineException(DecodeError(stdout, process.ExitCode));
        }
        return stdout;
    }

    public static List<EngineLogLine> ParseLog(string stderr)
    {
        var lines = new List<EngineLogLine>();
        foreach (var line in stderr.Split('\n'))
        {
            var trimmed = line.Trim();
            if (trimmed.Length == 0) continue;
            try
            {
                var parsed = JsonSerializer.Deserialize<EngineLogLine>(trimmed);
                if (parsed is not null) lines.Add(parsed);
            }
            catch (JsonException)
            {
                // Not JSON: the contract says logs are JSON Lines, so anything else is
                // noise from a crashing interpreter. Keep it — it is exactly what a bug
                // report needs.
                lines.Add(new EngineLogLine { Level = "raw", Message = trimmed });
            }
        }
        return lines;
    }

    public static EngineError DecodeError(string stdout, int exitCode)
    {
        try
        {
            var envelope = JsonSerializer.Deserialize<EngineErrorEnvelope>(stdout);
            if (envelope?.Error is { } error) return error;
        }
        catch (JsonException)
        {
            // fall through to the generic message
        }
        return EngineError.Local(
            "The conversion did not finish.",
            $"engine exited with status {exitCode}");
    }

    private static string WriteTemporary(byte[] payload, string prefix)
    {
        var path = Path.Combine(Path.GetTempPath(), $"pcci-{prefix}-{Guid.NewGuid():N}.json");
        File.WriteAllBytes(path, payload);
        return path;
    }

    private static void TryDelete(string path)
    {
        try
        {
            File.Delete(path);
        }
        catch (IOException)
        {
            // A leftover temp file is not worth failing a conversion over.
        }
    }
}
