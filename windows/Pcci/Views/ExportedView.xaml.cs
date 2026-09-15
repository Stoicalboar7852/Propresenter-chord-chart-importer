using System.Diagnostics;
using System.IO;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Pcci.ViewModels;

namespace Pcci;

public sealed partial class ExportedView : UserControl
{
    private AppState? _state;
    private ChartDocument? _document;

    public ExportedView() => InitializeComponent();

    public void Initialise(AppState state) => _state = state;

    public void Show(ChartDocument document)
    {
        if (!document.IsExported || document.Result is not { } result) return;
        _document = document;

        TitleText.Text = result.Title;
        SummaryText.Text =
            $"{result.Slides} slides in {result.Sections} sections · {result.Checks} checks passed";

        FileList.Children.Clear();
        AddFileRow("Presentation", result.Output);
        foreach (var page in result.ChartPages)
        {
            AddFileRow("Chord chart page", page);
        }
        if (!string.IsNullOrEmpty(result.ChordPro))
        {
            AddFileRow("ChordPro", result.ChordPro!);
        }

        WarningList.Children.Clear();
        WarningList.Visibility = result.Warnings.Count > 0 ? Visibility.Visible : Visibility.Collapsed;
        foreach (var warning in result.Warnings)
        {
            WarningList.Children.Add(new TextBlock
            {
                Text = warning,
                TextWrapping = TextWrapping.Wrap,
                Style = (Style)Application.Current.Resources["CaptionTextBlockStyle"]
            });
        }
    }

    private void AddFileRow(string label, string path)
    {
        var panel = new StackPanel { Spacing = 1 };
        panel.Children.Add(new TextBlock
        {
            Text = label,
            Style = (Style)Application.Current.Resources["CaptionTextBlockStyle"]
        });
        panel.Children.Add(new TextBlock
        {
            Text = Path.GetFileName(path),
            TextTrimming = TextTrimming.CharacterEllipsis
        });
        FileList.Children.Add(panel);
    }

    private void OnShowInExplorer(object sender, RoutedEventArgs args)
    {
        if (_document?.Result is not { } result) return;
        Process.Start(new ProcessStartInfo("explorer.exe", $"/select,\"{result.Output}\"")
        {
            UseShellExecute = true
        });
    }

    private void OnOpenGuide(object sender, RoutedEventArgs args)
    {
        var bundled = Path.Combine(System.AppContext.BaseDirectory, "STAGE_SETUP.md");
        var target = File.Exists(bundled)
            ? bundled
            : "https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/blob/main/docs/STAGE_SETUP.md";
        Process.Start(new ProcessStartInfo(target) { UseShellExecute = true });
    }

    private void OnBackToReview(object sender, RoutedEventArgs args)
    {
        if (_document is not null)
        {
            _document.Stage = DocumentStage.Review;
        }
    }
}
