using System;
using System.Linq;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Pcci.Models;
using Pcci.ViewModels;

namespace Pcci;

public sealed partial class ReviewView : UserControl
{
    private AppState? _state;
    private ChartDocument? _document;
    private bool _updating;

    public ReviewView()
    {
        InitializeComponent();
        TypeCombo.ItemsSource = SectionTypes.All;
    }

    public void Initialise(AppState state)
    {
        _state = state;
        SectionList.SelectionChanged += (_, _) => SyncEditor();
    }

    public void Show(ChartDocument document)
    {
        if (!document.IsReview) return;
        _document = document;
        _updating = true;

        TitleText.Text = document.Title;
        SummaryText.Text = document.Summary;
        LinesPerSlideBox.Value = _state?.LinesPerSlide ?? 4;

        var selectedIndex = SectionList.SelectedIndex;
        SectionList.ItemsSource = document.Sections;
        SlideList.ItemsSource = document.Slides;
        if (selectedIndex >= 0 && selectedIndex < document.Sections.Count)
        {
            SectionList.SelectedIndex = selectedIndex;
        }

        GuessBar.IsOpen = document.Sections.Any(section => section.WasGuessed);
        _updating = false;
        SyncEditor();
    }

    private void SyncEditor()
    {
        if (_updating) return;
        var section = SectionList.SelectedItem as SongSection;
        _updating = true;
        TypeCombo.SelectedItem = section?.Type;
        SectionNumberBox.Value = section?.Number ?? double.NaN;
        TypeCombo.IsEnabled = section is not null;
        SectionNumberBox.IsEnabled = section is not null;
        _updating = false;
    }

    private int SelectedIndex => SectionList.SelectedIndex;

    private async void OnTypeChanged(object sender, SelectionChangedEventArgs args)
    {
        if (_updating || _state is null || _document is null) return;
        if (TypeCombo.SelectedItem is not string type) return;
        await _state.SetSectionTypeAsync(_document, SelectedIndex, type);
        Show(_document);
    }

    private async void OnNumberChanged(NumberBox sender, NumberBoxValueChangedEventArgs args)
    {
        if (_updating || _state is null || _document is null) return;
        int? number = double.IsNaN(args.NewValue) ? null : (int)args.NewValue;
        await _state.SetSectionNumberAsync(_document, SelectedIndex, number);
        Show(_document);
    }

    private async void OnLinesPerSlideChanged(NumberBox sender, NumberBoxValueChangedEventArgs args)
    {
        if (_updating || _state is null || double.IsNaN(args.NewValue)) return;
        // Re-plan, not just remember. Setting the number alone left the preview and the
        // export running on the plan the parser first produced.
        await _state.SetLinesPerSlideAsync((int)args.NewValue);
        if (_document is not null) Show(_document);
    }

    private async void OnMoveUp(object sender, RoutedEventArgs args) => await MoveAsync(-1);

    private async void OnMoveDown(object sender, RoutedEventArgs args) => await MoveAsync(1);

    private async System.Threading.Tasks.Task MoveAsync(int offset)
    {
        if (_state is null || _document is null) return;
        var index = SelectedIndex;
        await _state.MoveSectionAsync(_document, index, offset);
        Show(_document);
        SectionList.SelectedIndex = Math.Clamp(index + offset, 0, _document.Sections.Count - 1);
    }

    private async void OnMergeUp(object sender, RoutedEventArgs args)
    {
        if (_state is null || _document is null) return;
        await _state.MergeUpAsync(_document, SelectedIndex);
        Show(_document);
    }

    private async void OnSplit(object sender, RoutedEventArgs args)
    {
        if (_state is null || _document is null) return;
        await _state.SplitAsync(_document, SelectedIndex);
        Show(_document);
    }

    private async void OnDelete(object sender, RoutedEventArgs args)
    {
        if (_state is null || _document is null) return;
        await _state.DeleteSectionAsync(_document, SelectedIndex);
        Show(_document);
    }

    private async void OnExport(object sender, RoutedEventArgs args)
    {
        if (_state is null || _document is null) return;
        var window = (App.Current as App)?.MainWindowInstance;
        if (window is null) return;
        // The settings decide what reaches a stage screen, so they get one last look
        // before anything is written - unless the user has said not to ask.
        if (!await SettingsDialog.ConfirmAsync(_state, XamlRoot)) return;
        var suggested = SanitiseFileName(_document.Title);
        var destination = await window.PickDestinationAsync(suggested);
        if (destination is null) return;
        await _state.ExportAsync(_document, destination);
    }

    private static string SanitiseFileName(string name)
    {
        var invalid = System.IO.Path.GetInvalidFileNameChars();
        var cleaned = new string(name.Where(character => !invalid.Contains(character)).ToArray());
        return string.IsNullOrWhiteSpace(cleaned) ? "Song" : cleaned;
    }
}
