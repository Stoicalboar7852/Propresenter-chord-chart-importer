using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Pcci.Services;

/// <summary>
/// What the app remembers between launches.
///
/// A small JSON file beside the engine's own cache and logs. Nothing here is worth an
/// error message: a missing or unreadable file means "use the defaults", and a failed
/// write means the next launch starts from the defaults again. Neither is worth
/// interrupting somebody setting up for a Sunday.
/// </summary>
public sealed class Preferences
{
    [JsonPropertyName("export_target")] public string ExportTarget { get; set; } = "propresenter";
    [JsonPropertyName("chord_delivery")] public string ChordDelivery { get; set; } = "inline";
    [JsonPropertyName("chord_placement")] public string ChordPlacement { get; set; } = "chords_only";
    [JsonPropertyName("chords_on_slide")] public bool ChordsOnSlide { get; set; }
    [JsonPropertyName("write_chordpro")] public bool WriteChordPro { get; set; }
    [JsonPropertyName("lines_per_slide")] public int LinesPerSlide { get; set; } = 4;

    /// <summary>
    /// Whether an export stops to show these first. On until somebody says otherwise,
    /// because the settings decide what reaches a stage screen and the first export is
    /// the moment to find that out - not the Sunday after.
    /// </summary>
    [JsonPropertyName("ask_before_export")] public bool AskBeforeExport { get; set; } = true;

    public static string FilePath
    {
        get
        {
            var root = Environment.GetEnvironmentVariable("LOCALAPPDATA");
            if (string.IsNullOrEmpty(root))
            {
                root = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            }
            return Path.Combine(root, "PCCI", "settings.json");
        }
    }

    public static Preferences Load()
    {
        try
        {
            if (!File.Exists(FilePath)) return new Preferences();
            var text = File.ReadAllText(FilePath);
            return JsonSerializer.Deserialize<Preferences>(text) ?? new Preferences();
        }
        catch (Exception)
        {
            return new Preferences();
        }
    }

    public void Save()
    {
        try
        {
            var directory = Path.GetDirectoryName(FilePath);
            if (!string.IsNullOrEmpty(directory)) Directory.CreateDirectory(directory);
            var options = new JsonSerializerOptions { WriteIndented = true };
            // Through a temporary file: an interrupted write must not leave a settings
            // file that cannot be read, which would silently reset everything.
            var temporary = FilePath + ".tmp";
            File.WriteAllText(temporary, JsonSerializer.Serialize(this, options));
            File.Move(temporary, FilePath, overwrite: true);
        }
        catch (Exception)
        {
            // Settings that do not survive a restart are a nuisance, not a failure.
        }
    }
}
