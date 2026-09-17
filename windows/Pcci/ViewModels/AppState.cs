using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using Pcci.Models;
using Pcci.Services;

namespace Pcci.ViewModels;

public enum DocumentStage
{
    Queued,
    Analysing,
    Review,
    Exporting,
    Exported,
    Failed
}

/// <summary>One chart the user dropped, and everything known about it.</summary>
public sealed partial class ChartDocument : ObservableObject
{
    [ObservableProperty] private DocumentStage stage = DocumentStage.Queued;
    [ObservableProperty] private Song? song;
    [ObservableProperty] private SlidePlan? plan;
    [ObservableProperty] private ConversionResult? result;
    [ObservableProperty] private EngineError? error;

    public ChartDocument(string path) => Path = path;

    public string Path { get; }
    public string Name => System.IO.Path.GetFileName(Path);

    public string StatusText => Stage switch
    {
        DocumentStage.Queued => "Waiting",
        DocumentStage.Analysing => "Reading…",
        DocumentStage.Review => Plan is null ? "Ready" : $"{Plan.SlideCount} slides",
        DocumentStage.Exporting => "Exporting…",
        DocumentStage.Exported => "Exported",
        _ => "Failed"
    };

    partial void OnStageChanged(DocumentStage value)
    {
        OnPropertyChanged(nameof(StatusText));
        OnPropertyChanged(nameof(IsReview));
        OnPropertyChanged(nameof(IsExported));
        OnPropertyChanged(nameof(IsFailed));
        OnPropertyChanged(nameof(IsBusyStage));
    }

    partial void OnPlanChanged(SlidePlan? value)
    {
        OnPropertyChanged(nameof(StatusText));
        OnPropertyChanged(nameof(Sections));
        OnPropertyChanged(nameof(Slides));
        OnPropertyChanged(nameof(Title));
        OnPropertyChanged(nameof(Summary));
    }

    public bool IsReview => Stage is DocumentStage.Review or DocumentStage.Exporting;
    public bool IsExported => Stage == DocumentStage.Exported;
    public bool IsFailed => Stage == DocumentStage.Failed;
    public bool IsBusyStage => Stage is DocumentStage.Queued or DocumentStage.Analysing;

    public string Title => Song?.Title ?? Name;

    public IReadOnlyList<SongSection> Sections => Song?.Sections ?? new List<SongSection>();
    public IReadOnlyList<PlannedSlide> Slides => Plan?.Slides ?? new List<PlannedSlide>();

    public string Summary
    {
        get
        {
            if (Plan is null) return "";
            var guessed = Plan.Song.Sections.Count(section => section.WasGuessed);
            var text = $"{Plan.SlideCount} slides in {Plan.Song.Sections.Count} sections";
            return guessed == 0 ? text : $"{text} · {guessed} guessed, worth a look";
        }
    }
}

/// <summary>
/// The application's state. Views bind to this; nothing else starts a process.
/// </summary>
public sealed partial class AppState : ObservableObject
{
    private static readonly HashSet<string> Accepted = new(StringComparer.OrdinalIgnoreCase)
    {
        ".txt", ".text", ".md", ".markdown", ".pdf", ".docx", ".rtf", ".odt", ".fodt",
        ".html", ".htm", ".xhtml", ".cho", ".chopro", ".chordpro", ".crd", ".pro"
    };

    [ObservableProperty] private ChartDocument? selected;
    [ObservableProperty] private EngineError? banner;
    [ObservableProperty] private bool isBusy;
    [ObservableProperty] private bool writeChordPro;
    [ObservableProperty] private int linesPerSlide = 4;
    [ObservableProperty] private string chordDelivery = "both";
    [ObservableProperty] private string chordPlacement = "chords_only";
    [ObservableProperty] private string batchStatus = "";
    [ObservableProperty] private bool isBatchRunning;

    // Finding songs online. The query box takes a song name or a link pasted out of a
    // browser; the engine works out which, so the user never has to say.
    [ObservableProperty] private string searchQuery = "";
    [ObservableProperty] private bool isSearching;
    /// <summary>The query the current results belong to, so "nothing found" can name it.</summary>
    [ObservableProperty] private string? searchedFor;
    /// <summary>The result being downloaded, so its own row can show the progress.</summary>
    [ObservableProperty] private string? importingRef;
    // Narrowing, for a title a hundred other songs share.
    [ObservableProperty] private string searchArtist = "";
    [ObservableProperty] private string searchAlbum = "";
    [ObservableProperty] private string searchYear = "";
    /// <summary>How many rows to ask for. Grows when the user asks to see more.</summary>
    [ObservableProperty] private int searchLimit = 20;
    /// <summary>How many matched altogether, so the list can offer the rest.</summary>
    [ObservableProperty] private int searchTotal;

    public bool HasMoreResults => SearchTotal > SearchResults.Count;
    public bool HasSearchFilters =>
        !string.IsNullOrWhiteSpace(SearchArtist)
        || !string.IsNullOrWhiteSpace(SearchAlbum)
        || !string.IsNullOrWhiteSpace(SearchYear);

    public ObservableCollection<ChartDocument> Documents { get; } = new();
    public ObservableCollection<EngineLogLine> LogLines { get; } = new();
    public ObservableCollection<SongMatch> SearchResults { get; } = new();
    /// <summary>What the sources had to say for themselves, and what an import warned.</summary>
    public ObservableCollection<string> SearchNotes { get; } = new();

    public static bool Accepts(string path) => Accepted.Contains(Path.GetExtension(path));

    public EngineConfig Config => new()
    {
        LinesPerSlide = LinesPerSlide,
        BalanceLastSlide = true,
        ChordDelivery = ChordDelivery,
        ChordPlacement = ChordPlacement
    };

    public async Task AddAsync(IEnumerable<string> paths)
    {
        var fresh = paths
            .Where(Accepts)
            .Where(path => Documents.All(document => document.Path != path))
            .Select(path => new ChartDocument(path))
            .ToList();

        foreach (var document in fresh)
        {
            Documents.Add(document);
        }
        Selected ??= Documents.FirstOrDefault();

        foreach (var document in fresh)
        {
            await AnalyseAsync(document);
        }
    }

    public void Remove(ChartDocument document)
    {
        Documents.Remove(document);
        if (Selected == document) Selected = Documents.FirstOrDefault();
    }

    /// <summary>
    /// Empty the list and go back to the drop target. Files already exported are left
    /// where they are: this clears the list, not anybody's disk.
    /// </summary>
    public void Clear()
    {
        Documents.Clear();
        Selected = null;
        Banner = null;
    }

    /// <summary>
    /// Lines per slide is one setting for the whole queue, so changing it re-plans every
    /// chart already read. The previews and a Convert All then cannot disagree about
    /// what a slide holds.
    /// </summary>
    public async Task SetLinesPerSlideAsync(int value)
    {
        if (value == LinesPerSlide) return;
        LinesPerSlide = value;
        await ReplanAllAsync();
    }

    /// <summary>
    /// Re-plan every chart already read.
    ///
    /// Not optional after a settings change: an export sends the plan back to the
    /// engine and the plan carries the settings it was made with, so without this a
    /// setting changed after a chart was read would not apply to it.
    /// </summary>
    public async Task ReplanAllAsync()
    {
        foreach (var document in Documents.ToList())
        {
            if (document.Song is not null) await ReplanAsync(document);
        }
    }

    /// <summary>
    /// Export every chart in the queue into one folder with the current settings.
    /// Anything not read yet is read first, and each chart keeps the corrections already
    /// made to it. A chart that fails is left marked failed and the rest still convert.
    /// </summary>
    public async Task ConvertAllAsync(string directory)
    {
        var queue = Documents.ToList();
        if (queue.Count == 0) return;

        var used = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        IsBatchRunning = true;
        try
        {
            for (var index = 0; index < queue.Count; index++)
            {
                var document = queue[index];
                BatchStatus = $"Converting {index + 1} of {queue.Count}";
                if (document.Song is null) await AnalyseAsync(document);
                if (document.Song is null || document.Plan is null) continue;

                var name = Path.GetFileNameWithoutExtension(document.Path);
                await ExportAsync(document, FreePath(directory, name, used));
            }
        }
        finally
        {
            IsBatchRunning = false;
            BatchStatus = "";
        }
    }

    /// <summary>
    /// <c>directory\name.pro</c>, numbered rather than overwritten. Two folders of
    /// charts can easily each hold a Great Are You Lord, and a batch that quietly wrote
    /// one over the other would be worse than no batch at all.
    /// </summary>
    public static string FreePath(string directory, string name, HashSet<string> used)
    {
        var candidate = name;
        var counter = 2;
        while (used.Contains(candidate) || File.Exists(Path.Combine(directory, candidate + ".pro")))
        {
            candidate = $"{name} {counter}";
            counter++;
        }
        used.Add(candidate);
        return Path.Combine(directory, candidate + ".pro");
    }

    public async Task AnalyseAsync(ChartDocument document)
    {
        document.Stage = DocumentStage.Analysing;
        document.Error = null;
        await WithEngineAsync(document, async engine =>
        {
            var plan = await engine.PlanAsync(document.Path, Config);
            document.Song = plan.Song;
            document.Plan = plan;
            document.Stage = DocumentStage.Review;
        });
    }

    /// <summary>Re-plan after a section edit or a change to lines per slide.</summary>
    public async Task ReplanAsync(ChartDocument document)
    {
        if (document.Song is null) return;
        await WithEngineAsync(document, async engine =>
        {
            var plan = await engine.PlanAsync(document.Song, Config);
            document.Plan = plan;
            document.Stage = DocumentStage.Review;
        });
    }

    public async Task ExportAsync(ChartDocument document, string destination)
    {
        if (document.Plan is null || document.Song is null) return;
        document.Stage = DocumentStage.Exporting;
        await WithEngineAsync(document, async engine =>
        {
            // Send the corrected song, not the one the parser first produced.
            var songNode = JsonSerializer.SerializeToNode(document.Song);
            if (document.Plan.Raw is JsonObject raw && songNode is not null)
            {
                raw["song"] = songNode;
            }
            var result = await engine.BuildAsync(document.Plan, destination, WriteChordPro);
            document.Result = result;
            document.Stage = DocumentStage.Exported;
        });
    }

    // Songs from the web.

    /// <summary>Search, or describe a pasted link. The engine decides which this is.</summary>
    public async Task SearchAsync(bool startingOver = true)
    {
        var query = SearchQuery.Trim();
        if (query.Length == 0 || IsSearching) return;

        if (startingOver) SearchLimit = 20;
        IsSearching = true;
        SearchedFor = query;
        try
        {
            var outcome = await WithEngineValueAsync(engine => engine.SearchAsync(
                query, SearchLimit, SearchArtist.Trim(), SearchAlbum.Trim(), SearchYear.Trim()));
            SearchResults.Clear();
            SearchNotes.Clear();
            SearchTotal = 0;
            if (outcome is null) return;
            foreach (var match in outcome.Results) SearchResults.Add(match);
            foreach (var note in outcome.Notes) SearchNotes.Add(note);
            SearchTotal = outcome.TotalFound;
            OnPropertyChanged(nameof(HasMoreResults));
        }
        finally
        {
            IsSearching = false;
        }
    }

    /// <summary>
    /// Ask for the next batch. The list is capped so the first search stays quick; a
    /// song further down was simply unreachable before this existed.
    /// </summary>
    public async Task ShowMoreResultsAsync()
    {
        if (!HasMoreResults || IsSearching) return;
        SearchLimit = Math.Min(SearchLimit + 20, 60);
        await SearchAsync(startingOver: false);
    }

    public void ClearSearch()
    {
        SearchQuery = "";
        SearchArtist = "";
        SearchAlbum = "";
        SearchYear = "";
        SearchLimit = 20;
        SearchedFor = null;
        SearchTotal = 0;
        SearchResults.Clear();
        SearchNotes.Clear();
    }

    /// <summary>Download a result and queue it, ready to review like any other chart.</summary>
    public async Task ImportMatchAsync(SongMatch match)
    {
        if (string.IsNullOrEmpty(match.ChartUrl)) return;
        ImportingRef = match.Ref;
        try
        {
            await ImportLinkAsync(match.ChartUrl!);
        }
        finally
        {
            ImportingRef = null;
        }
    }

    public async Task ImportLinkAsync(string url)
    {
        var imported = await WithEngineValueAsync(engine => engine.FetchAsync(url));
        if (imported is not null) await AdoptAsync(imported);
    }

    /// <summary>
    /// Text copied from somewhere else, as a chart.
    ///
    /// The same door as a link: some words, possibly some chords, and no file. This is
    /// the way in for every site that will not let a program read it - open the page
    /// yourself, select the chart, copy, and come back here.
    /// </summary>
    public async Task ImportPastedAsync(string pasted)
    {
        if (string.IsNullOrWhiteSpace(pasted))
        {
            Banner = EngineError.Local(
                "There is no text on the clipboard to import.",
                "the clipboard held no text");
            return;
        }
        var imported = await WithEngineValueAsync(engine => engine.PasteAsync(pasted));
        if (imported is not null) await AdoptAsync(imported);
    }

    /// <summary>Put a freshly imported chart in the list and select it.</summary>
    private async Task AdoptAsync(ImportedChart imported)
    {
        SearchNotes.Clear();
        foreach (var note in imported.Notes) SearchNotes.Add(note);

        var existing = Documents.FirstOrDefault(
            document => string.Equals(document.Path, imported.Path, StringComparison.OrdinalIgnoreCase));
        if (existing is not null)
        {
            // Re-importing the same song overwrites the file it was written to, so the
            // row already in the list is stale. Read it again rather than adding a
            // second row pointing at the same path.
            Selected = existing;
            await AnalyseAsync(existing);
        }
        else
        {
            await AddAsync(new[] { imported.Path });
            Selected = Documents.FirstOrDefault(
                document => string.Equals(document.Path, imported.Path, StringComparison.OrdinalIgnoreCase))
                ?? Selected;
        }
        SearchResults.Clear();
        SearchedFor = null;
    }

    /// <summary>
    /// Run something against the engine that is about no particular document.
    ///
    /// A search has no chart to mark as failed, so a failure here is a banner and a
    /// null, rather than the document-shaped error path the conversion flow uses.
    /// </summary>
    private async Task<T?> WithEngineValueAsync<T>(Func<EngineClient, Task<T>> body) where T : class
    {
        IsBusy = true;
        try
        {
            var engine = new EngineClient();
            var value = await body(engine);
            LogLines.Clear();
            foreach (var line in engine.Log) LogLines.Add(line);
            Banner = null;
            return value;
        }
        catch (EngineException exception)
        {
            Banner = exception.Error;
            return null;
        }
        catch (Exception exception)
        {
            Banner = EngineError.Local("Something went wrong.", exception.Message);
            return null;
        }
        finally
        {
            IsBusy = false;
        }
    }

    private async Task WithEngineAsync(ChartDocument document, Func<EngineClient, Task> body)
    {
        IsBusy = true;
        try
        {
            var engine = new EngineClient();
            await body(engine);
            LogLines.Clear();
            foreach (var line in engine.Log) LogLines.Add(line);
            Banner = null;
        }
        catch (EngineException exception)
        {
            document.Error = exception.Error;
            document.Stage = DocumentStage.Failed;
            Banner = exception.Error;
        }
        catch (Exception exception)
        {
            var error = EngineError.Local("Something went wrong.", exception.Message);
            document.Error = error;
            document.Stage = DocumentStage.Failed;
            Banner = error;
        }
        finally
        {
            IsBusy = false;
        }
    }

    // Section editing — the review screen's whole point.

    public async Task SetSectionTypeAsync(ChartDocument document, int index, string type)
    {
        if (document.Song is null || index < 0 || index >= document.Song.Sections.Count) return;
        document.Song.Sections[index].Type = type;
        document.Song.Sections[index].Confidence = 1.0;
        await ReplanAsync(document);
    }

    public async Task SetSectionNumberAsync(ChartDocument document, int index, int? number)
    {
        if (document.Song is null || index < 0 || index >= document.Song.Sections.Count) return;
        document.Song.Sections[index].Number = number;
        await ReplanAsync(document);
    }

    public async Task DeleteSectionAsync(ChartDocument document, int index)
    {
        if (document.Song is null || index < 0 || index >= document.Song.Sections.Count) return;
        document.Song.Sections.RemoveAt(index);
        await ReplanAsync(document);
    }

    public async Task MoveSectionAsync(ChartDocument document, int index, int offset)
    {
        if (document.Song is null) return;
        var target = index + offset;
        if (index < 0 || index >= document.Song.Sections.Count) return;
        if (target < 0 || target >= document.Song.Sections.Count) return;
        var section = document.Song.Sections[index];
        document.Song.Sections.RemoveAt(index);
        document.Song.Sections.Insert(target, section);
        await ReplanAsync(document);
    }

    public async Task MergeUpAsync(ChartDocument document, int index)
    {
        if (document.Song is null || index <= 0 || index >= document.Song.Sections.Count) return;
        var moving = document.Song.Sections[index];
        document.Song.Sections.RemoveAt(index);
        document.Song.Sections[index - 1].Lines.AddRange(moving.Lines);
        await ReplanAsync(document);
    }

    public async Task SplitAsync(ChartDocument document, int index)
    {
        if (document.Song is null || index < 0 || index >= document.Song.Sections.Count) return;
        var section = document.Song.Sections[index];
        if (section.Lines.Count < 2) return;
        var at = section.Lines.Count / 2;
        var tail = section.Lines.GetRange(at, section.Lines.Count - at);
        section.Lines.RemoveRange(at, section.Lines.Count - at);
        document.Song.Sections.Insert(index + 1, new SongSection
        {
            Type = section.Type,
            Number = section.Number,
            Variant = section.Variant,
            RawLabel = section.RawLabel,
            Confidence = 1.0,
            Lines = tail
        });
        await ReplanAsync(document);
    }

    partial void OnLinesPerSlideChanged(int value)
    {
        if (Selected is { } document)
        {
            _ = ReplanAsync(document);
        }
    }
}
