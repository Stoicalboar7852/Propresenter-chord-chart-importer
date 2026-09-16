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
    [ObservableProperty] private string chordPlacement = "chords_inline";
    [ObservableProperty] private string batchStatus = "";
    [ObservableProperty] private bool isBatchRunning;

    public ObservableCollection<ChartDocument> Documents { get; } = new();
    public ObservableCollection<EngineLogLine> LogLines { get; } = new();

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
