using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.UI.Composition.SystemBackdrops;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Pcci.ViewModels;
using Windows.ApplicationModel.DataTransfer;
using Windows.Storage;
using Windows.Storage.Pickers;
using WinRT.Interop;

namespace Pcci;

public sealed partial class MainWindow : Window
{
    public AppState State { get; } = new();

    public MainWindow()
    {
        InitializeComponent();

        Title = "ProPresenter Chord Chart Importer";
        // Mica Alt: the Fluent backdrop for a window with a navigation pane. Not
        // acrylic, and not an imitation of the Mac app's glass.
        SystemBackdrop = new MicaBackdrop { Kind = MicaKind.BaseAlt };
        ExtendsContentIntoTitleBar = true;
        SetTitleBar(TitleBarArea);
        SetWindowIcon();

        Navigation.MenuItemsSource = State.Documents;
        State.PropertyChanged += (_, args) =>
        {
            if (args.PropertyName is nameof(AppState.Selected) or nameof(AppState.Banner)
                or nameof(AppState.IsBusy) or nameof(AppState.BatchStatus)
                or nameof(AppState.IsBatchRunning) or nameof(AppState.LinesPerSlide)
                or nameof(AppState.IsSearching))
            {
                UpdatePanes();
            }
        };
        State.Documents.CollectionChanged += (_, _) => UpdatePanes();
        State.SearchResults.CollectionChanged += (_, _) => UpdatePanes();

        SearchPane.Initialise(State);
        DropPane.Initialise(State);
        ReviewPane.Initialise(State);
        ExportedPane.Initialise(State);
        FailurePane.Initialise(State);
        UpdatePanes();
    }

    /// <summary>
    /// The icon the window and the taskbar draw. ApplicationIcon only covers the .exe
    /// as Explorer sees it; an unpackaged WinUI window asks separately. A missing file
    /// is not worth failing a launch over, so it is simply skipped.
    /// </summary>
    private void SetWindowIcon()
    {
        var icon = System.IO.Path.Combine(AppContext.BaseDirectory, "Assets", "AppIcon.ico");
        if (System.IO.File.Exists(icon)) AppWindow.SetIcon(icon);
    }

    private void UpdatePanes()
    {
        var document = State.Selected;
        TitleText.Text = document?.Title ?? "";

        Banner.IsOpen = State.Banner is not null;
        Banner.Title = State.Banner?.UserMessage ?? "";
        Banner.Message = State.Banner?.TechnicalDetail ?? "";

        BusyRing.IsActive = State.IsBusy;
        BusyRing.Visibility = State.IsBusy ? Visibility.Visible : Visibility.Collapsed;

        var count = State.Documents.Count;
        QueueStatusText.Text = State.BatchStatus.Length > 0
            ? State.BatchStatus
            : count switch { 0 => "Nothing loaded", 1 => "1 chart", _ => $"{count} charts" };
        ConvertAllButton.IsEnabled = count > 0 && !State.IsBatchRunning;
        ClearButton.IsEnabled = count > 0 && !State.IsBatchRunning;
        if (QueueLinesPerSlide.Value != State.LinesPerSlide)
        {
            QueueLinesPerSlide.Value = State.LinesPerSlide;
        }

        // Both ways in are on screen at once with nothing loaded, because they answer
        // different questions - "I have this file" and "I need this song" - and the
        // user knows which of those they have before they open the app. The drop
        // target steps aside while results are showing so the list has the room.
        var atStart = document is null;
        var showingResults = State.SearchResults.Count > 0 || State.IsSearching;
        SearchPane.Visibility = atStart ? Visibility.Visible : Visibility.Collapsed;
        DropPane.Visibility = atStart && !showingResults ? Visibility.Visible : Visibility.Collapsed;
        ReviewPane.Visibility = document?.IsReview == true ? Visibility.Visible : Visibility.Collapsed;
        ExportedPane.Visibility = document?.IsExported == true ? Visibility.Visible : Visibility.Collapsed;
        FailurePane.Visibility = document?.IsFailed == true ? Visibility.Visible : Visibility.Collapsed;

        if (document is not null)
        {
            ReviewPane.Show(document);
            ExportedPane.Show(document);
            FailurePane.Show(document);
        }
    }

    private void OnQueueSelectionChanged(NavigationView sender, NavigationViewSelectionChangedEventArgs args)
    {
        if (args.IsSettingsSelected)
        {
            _ = new SettingsDialog(State) { XamlRoot = RootGrid.XamlRoot }.ShowAsync();
            return;
        }
        if (args.SelectedItem is ChartDocument document)
        {
            State.Selected = document;
        }
    }

    private async void OnOpenFiles(object sender, RoutedEventArgs args)
    {
        var picker = new FileOpenPicker { ViewMode = PickerViewMode.List };
        InitializeWithWindow.Initialize(picker, WindowNative.GetWindowHandle(this));
        foreach (var extension in new[]
                 {
                     ".docx", ".pdf", ".txt", ".md", ".rtf", ".odt", ".html", ".htm",
                     ".cho", ".chopro", ".chordpro", ".crd"
                 })
        {
            picker.FileTypeFilter.Add(extension);
        }

        var files = await picker.PickMultipleFilesAsync();
        if (files.Count > 0)
        {
            await State.AddAsync(files.Select(file => file.Path));
        }
    }

    private async void OnConvertAll(object sender, RoutedEventArgs args)
    {
        if (State.Documents.Count == 0) return;

        var picker = new FolderPicker { SuggestedStartLocation = PickerLocationId.DocumentsLibrary };
        // A FolderPicker with no filter returns nothing at all, which looks like a
        // cancelled dialog. "*" means every folder is selectable.
        picker.FileTypeFilter.Add("*");
        InitializeWithWindow.Initialize(picker, WindowNative.GetWindowHandle(this));

        var folder = await picker.PickSingleFolderAsync();
        if (folder is null) return;
        await State.ConvertAllAsync(folder.Path);
    }

    private void OnClear(object sender, RoutedEventArgs args) => State.Clear();

    private async void OnQueueLinesPerSlideChanged(NumberBox sender, NumberBoxValueChangedEventArgs args)
    {
        if (double.IsNaN(args.NewValue)) return;
        await State.SetLinesPerSlideAsync((int)args.NewValue);
    }

    private void OnShowLog(object sender, RoutedEventArgs args)
    {
        _ = new LogDialog(State) { XamlRoot = RootGrid.XamlRoot }.ShowAsync();
    }

    private void OnDragOver(object sender, DragEventArgs args)
    {
        args.AcceptedOperation = args.DataView.Contains(StandardDataFormats.StorageItems)
            ? DataPackageOperation.Copy
            : DataPackageOperation.None;
        args.DragUIOverride.Caption = "Add to PCCI";
        args.DragUIOverride.IsCaptionVisible = true;
    }

    private async void OnDrop(object sender, DragEventArgs args)
    {
        if (!args.DataView.Contains(StandardDataFormats.StorageItems)) return;
        var deferral = args.GetDeferral();
        try
        {
            var items = await args.DataView.GetStorageItemsAsync();
            var paths = items.OfType<StorageFile>().Select(file => file.Path).ToList();
            var accepted = paths.Where(AppState.Accepts).ToList();
            if (accepted.Count == 0 && paths.Count > 0)
            {
                Banner.IsOpen = true;
                Banner.Title = "PCCI cannot read that file type.";
                Banner.Message = string.Join(", ", paths.Select(System.IO.Path.GetFileName));
                return;
            }
            await State.AddAsync(accepted);
        }
        finally
        {
            deferral.Complete();
        }
    }

    /// <summary>Where the export should go. Returns null if the user cancelled.</summary>
    public async System.Threading.Tasks.Task<string?> PickDestinationAsync(string suggestedName)
    {
        var picker = new FileSavePicker
        {
            SuggestedFileName = suggestedName,
            SuggestedStartLocation = PickerLocationId.DocumentsLibrary
        };
        picker.FileTypeChoices.Add("ProPresenter presentation", new List<string> { ".pro" });
        InitializeWithWindow.Initialize(picker, WindowNative.GetWindowHandle(this));
        var file = await picker.PickSaveFileAsync();
        return file?.Path;
    }
}
