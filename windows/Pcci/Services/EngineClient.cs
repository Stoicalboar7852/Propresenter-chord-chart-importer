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
        config.BalanceLastSlide ? "--balance" : "--no-balance",
        "--chords", config.ChordDelivery,
        "--chord-placement", config.ChordPlacement
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

    private async Task<string> RunAsync(IEnumerable<string> arguments)
    {
        Log.Clear();
        var info = new ProcessStartInfo
        {
            FileName = _executable,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            StandardOutputEncoding = Encoding.UTF8,
            StandardErrorEncoding = Encoding.UTF8
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
