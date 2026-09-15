using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace Pcci.Models;

// Mirrors of the engine's JSON. Property names come from the engine, not from C#
// convention, so JsonPropertyName does the mapping and the wire format stays the
// engine's business.

public sealed class ChordPlacement
{
    [JsonPropertyName("chord")] public string Chord { get; set; } = "";
    [JsonPropertyName("char_index")] public int CharIndex { get; set; }
    [JsonPropertyName("raw")] public string Raw { get; set; } = "";
}

public sealed class SongLine
{
    [JsonPropertyName("lyrics")] public string Lyrics { get; set; } = "";
    [JsonPropertyName("chords")] public List<ChordPlacement> Chords { get; set; } = new();
    [JsonPropertyName("annotation")] public string? Annotation { get; set; }

    /// <summary>The chord row, rebuilt the way the engine rebuilds it for slide notes.</summary>
    [JsonIgnore]
    public string ChordRow
    {
        get
        {
            var row = new StringBuilder();
            foreach (var placement in Chords)
            {
                var target = placement.CharIndex;
                if (target < row.Length)
                {
                    target = row.Length + 1;
                }
                row.Append(' ', System.Math.Max(0, target - row.Length));
                row.Append(placement.Chord);
            }
            return row.ToString();
        }
    }

    [JsonIgnore] public bool HasChords => Chords.Count > 0;
    [JsonIgnore] public bool HasLyrics => !string.IsNullOrEmpty(Lyrics);
    [JsonIgnore] public bool HasAnnotation => !string.IsNullOrWhiteSpace(Annotation);
}

public sealed class SongSection
{
    [JsonPropertyName("type")] public string Type { get; set; } = "Verse";
    [JsonPropertyName("number")] public int? Number { get; set; }
    [JsonPropertyName("variant")] public string Variant { get; set; } = "";
    [JsonPropertyName("raw_label")] public string RawLabel { get; set; } = "";
    [JsonPropertyName("lines")] public List<SongLine> Lines { get; set; } = new();
    [JsonPropertyName("confidence")] public double Confidence { get; set; } = 1.0;

    [JsonIgnore]
    public string Label
    {
        get
        {
            if (Type == "Misc" && !string.IsNullOrEmpty(RawLabel)) return RawLabel;
            return Number is null ? Type : $"{Type} {Number}{Variant}";
        }
    }

    [JsonIgnore] public bool WasGuessed => Confidence < 0.9;
}

public sealed class Song
{
    [JsonPropertyName("title")] public string Title { get; set; } = "";
    [JsonPropertyName("artist")] public string? Artist { get; set; }
    [JsonPropertyName("ccli_number")] public string? CcliNumber { get; set; }
    [JsonPropertyName("copyright")] public string? Copyright { get; set; }
    [JsonPropertyName("key")] public string? Key { get; set; }
    [JsonPropertyName("tempo")] public int? Tempo { get; set; }
    [JsonPropertyName("sections")] public List<SongSection> Sections { get; set; } = new();
    [JsonPropertyName("warnings")] public List<string> Warnings { get; set; } = new();
    [JsonPropertyName("source_path")] public string? SourcePath { get; set; }
    [JsonPropertyName("source_format")] public string? SourceFormat { get; set; }
}

public sealed class PlannedSlide
{
    [JsonPropertyName("section_index")] public int SectionIndex { get; set; }
    [JsonPropertyName("section_label")] public string SectionLabel { get; set; } = "";
    [JsonPropertyName("section_type")] public string SectionType { get; set; } = "";
    [JsonPropertyName("ordinal")] public int Ordinal { get; set; }
    [JsonPropertyName("total_in_section")] public int TotalInSection { get; set; }
    [JsonPropertyName("lines")] public List<SongLine> Lines { get; set; } = new();

    [JsonIgnore]
    public string Label => TotalInSection == 1 ? SectionLabel : $"{SectionLabel} ({Ordinal})";

    [JsonIgnore] public string LineCountText => $"{Lines.Count} lines";
}

public sealed class EngineConfig
{
    [JsonPropertyName("lines_per_slide")] public int LinesPerSlide { get; set; } = 4;
    [JsonPropertyName("balance_last_slide")] public bool BalanceLastSlide { get; set; } = true;
    [JsonPropertyName("chord_delivery")] public string ChordDelivery { get; set; } = "both";
    [JsonPropertyName("chord_placement")] public string ChordPlacement { get; set; } = "chords_only";
}

public sealed class ConversionResult
{
    [JsonPropertyName("output")] public string Output { get; set; } = "";
    [JsonPropertyName("slides")] public int Slides { get; set; }
    [JsonPropertyName("sections")] public int Sections { get; set; }
    [JsonPropertyName("title")] public string Title { get; set; } = "";
    [JsonPropertyName("chart_pages")] public List<string> ChartPages { get; set; } = new();
    [JsonPropertyName("chordpro")] public string? ChordPro { get; set; }
    [JsonPropertyName("checks")] public int Checks { get; set; }
    [JsonPropertyName("warnings")] public List<string> Warnings { get; set; } = new();
}

/// <summary>A typed failure from the engine.</summary>
public sealed class EngineError
{
    [JsonPropertyName("kind")] public string Kind { get; set; } = "internal";
    [JsonPropertyName("user_message")] public string UserMessage { get; set; } = "";
    [JsonPropertyName("technical_detail")] public string TechnicalDetail { get; set; } = "";

    public static EngineError Local(string message, string detail = "") =>
        new() { Kind = "app", UserMessage = message, TechnicalDetail = detail };
}

public sealed class EngineErrorEnvelope
{
    [JsonPropertyName("error")] public EngineError? Error { get; set; }
}

public sealed class EngineException : System.Exception
{
    public EngineError Error { get; }

    public EngineException(EngineError error) : base(error.UserMessage) => Error = error;
}

public sealed class EngineLogLine
{
    [JsonPropertyName("level")] public string Level { get; set; } = "info";
    [JsonPropertyName("msg")] public string Message { get; set; } = "";
    [JsonPropertyName("ts")] public string Timestamp { get; set; } = "";

    [JsonIgnore] public string Display => $"{Level.ToUpperInvariant(),-8}{Message}";
}

/// <summary>
/// The plan as the app holds it: typed where the UI needs it, plus the original JSON so
/// an edited plan goes back to the engine whole rather than being re-modelled here.
/// </summary>
public sealed class SlidePlan
{
    public Song Song { get; set; } = new();
    public List<PlannedSlide> Slides { get; set; } = new();
    public EngineConfig Config { get; set; } = new();
    public List<string> Warnings { get; set; } = new();
    public System.Text.Json.Nodes.JsonNode? Raw { get; set; }

    public int SlideCount => Slides.Count;
}

public static class SectionTypes
{
    /// <summary>Kept in step with SectionType in the engine's ir.py.</summary>
    public static readonly string[] All =
    {
        "Intro", "Verse", "Pre-Chorus", "Chorus", "Post-Chorus", "Bridge", "Tag",
        "Outro", "Instrumental", "Interlude", "Vamp", "Breakdown", "Refrain",
        "Ending", "Misc"
    };
}
