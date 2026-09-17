using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;

namespace Pcci.Models;

// Mirrors of what `pcci search`, `pcci fetch` and `pcci paste` put on stdout. Property
// names come from the engine, not from C# convention, so JsonPropertyName does the
// mapping and the wire format stays the engine's business.

/// <summary>A site that contributed to a search result, and what it contributed.</summary>
public sealed class MatchSource
{
    [JsonPropertyName("provider")] public string Provider { get; set; } = "";
    [JsonPropertyName("name")] public string Name { get; set; } = "";
    [JsonPropertyName("url")] public string? Url { get; set; }
    [JsonPropertyName("supplies")] public List<string> Supplies { get; set; } = new();
}

/// <summary>One row in the search results.</summary>
public sealed class SongMatch
{
    [JsonPropertyName("ref")] public string Ref { get; set; } = "";
    [JsonPropertyName("title")] public string Title { get; set; } = "";
    [JsonPropertyName("artist")] public string? Artist { get; set; }
    [JsonPropertyName("album")] public string? Album { get; set; }
    [JsonPropertyName("year")] public int? Year { get; set; }
    [JsonPropertyName("artwork_url")] public string? ArtworkUrl { get; set; }
    [JsonPropertyName("artwork_thumb_url")] public string? ArtworkThumbUrl { get; set; }
    [JsonPropertyName("artwork_provider")] public string? ArtworkProvider { get; set; }
    [JsonPropertyName("chart_url")] public string? ChartUrl { get; set; }
    [JsonPropertyName("chart_kind")] public string ChartKind { get; set; } = "none";
    [JsonPropertyName("rating")] public double? Rating { get; set; }
    [JsonPropertyName("votes")] public int? Votes { get; set; }
    [JsonPropertyName("key")] public string? Key { get; set; }
    [JsonPropertyName("ccli_number")] public string? CcliNumber { get; set; }
    [JsonPropertyName("copyright")] public string? Copyright { get; set; }
    [JsonPropertyName("sources")] public List<MatchSource> Sources { get; set; } = new();

    /// <summary>Whether there is anything here to turn into a presentation.</summary>
    [JsonIgnore]
    public bool Importable => !string.IsNullOrEmpty(ChartUrl) && ChartKind != "none";

    [JsonIgnore]
    public bool HasChords => ChartKind is "chords" or "tab";

    /// <summary>Parish Choir · Hymns, Volume One · 2019, as much of it as is known.</summary>
    [JsonIgnore]
    public string Subtitle
    {
        get
        {
            var parts = new List<string>();
            if (!string.IsNullOrWhiteSpace(Artist)) parts.Add(Artist!);
            if (!string.IsNullOrWhiteSpace(Album) && Album != Artist) parts.Add(Album!);
            if (Year is { } year) parts.Add(year.ToString());
            return string.Join(" · ", parts);
        }
    }

    [JsonIgnore]
    public string SourceNames => string.Join(", ", Sources.Select(source => source.Name));

    /// <summary>What the row promises: chords, just the words, or nothing importable.</summary>
    [JsonIgnore]
    public string WordsLabel => ChartKind switch
    {
        "chords" or "tab" => "Chords",
        "lyrics" => "Lyrics",
        _ => "No words"
    };

    [JsonIgnore]
    public Uri? ThumbnailUri =>
        Uri.TryCreate(ArtworkThumbUrl ?? "", UriKind.Absolute, out var uri) ? uri : null;
}

/// <summary>Everything one search produced, including what went wrong on the way.</summary>
public sealed class SearchOutcome
{
    [JsonPropertyName("query")] public string Query { get; set; } = "";
    [JsonPropertyName("is_url")] public bool IsUrl { get; set; }
    [JsonPropertyName("results")] public List<SongMatch> Results { get; set; } = new();
    [JsonPropertyName("notes")] public List<string> Notes { get; set; } = new();
    /// <summary>How many matched before the list was cut to the requested size.</summary>
    [JsonPropertyName("total_found")] public int TotalFound { get; set; }

    [JsonIgnore]
    public bool HasMore => TotalFound > Results.Count;
}

/// <summary>What fetch and paste report: a chart now sitting on disk.</summary>
public sealed class ImportedChart
{
    [JsonPropertyName("path")] public string Path { get; set; } = "";
    [JsonPropertyName("title")] public string Title { get; set; } = "";
    [JsonPropertyName("artist")] public string? Artist { get; set; }
    [JsonPropertyName("chart_kind")] public string ChartKind { get; set; } = "lyrics";
    [JsonPropertyName("has_chords")] public bool HasChords { get; set; }
    [JsonPropertyName("source")] public MatchSource Source { get; set; } = new();
    [JsonPropertyName("notes")] public List<string> Notes { get; set; } = new();
}
