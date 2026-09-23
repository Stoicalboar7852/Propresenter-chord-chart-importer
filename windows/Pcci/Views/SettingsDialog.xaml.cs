using System.Linq;
using System.Threading.Tasks;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Pcci.Services;
using Pcci.ViewModels;

namespace Pcci;

public sealed partial class SettingsDialog : ContentDialog
{
    private readonly AppState _state;
    private readonly bool _beforeExport;
    private bool _loading = true;

    /// <param name="beforeExport">
    /// True when this is the stop on the way to an export rather than the Settings
    /// menu. The settings are the same either way; what changes is that there is
    /// something to cancel, and that the switch offers to stop asking rather than to
    /// start.
    /// </param>
    public SettingsDialog(AppState state, bool beforeExport = false)
    {
        InitializeComponent();
        _state = state;
        _beforeExport = beforeExport;

        if (beforeExport)
        {
            Title = "Check these before exporting";
            PrimaryButtonText = "Export";
            CloseButtonText = "Cancel";
            DefaultButton = ContentDialogButton.Primary;
            AskToggle.Header = "Use these every time";
            AskNote.Text = "Exporting will not stop to ask again. You can turn it back "
                           + "on in Settings whenever you like.";
            // Not settings for an export: how the app looks, and where its engine is.
            ThemeCombo.Visibility = Visibility.Collapsed;
            EngineText.Visibility = Visibility.Collapsed;
        }
        else
        {
            AskNote.Text = "The settings decide what reaches your stage screen, so an "
                           + "export offers them one last time before it writes anything.";
        }

        Select(ExportTargetCombo, state.ExportTarget);
        Select(ChordDeliveryCombo, state.ChordDelivery);
        ChordsOnSlideToggle.IsOn = state.ChordsOnSlide;
        UpdateInlineWarning();
        Select(ChordPlacementCombo, state.ChordPlacement);
        ChordProToggle.IsOn = state.WriteChordPro;
        // In the Settings menu the switch says whether the app asks; on the way to an
        // export it offers to stop, so it starts off and reads the other way round.
        AskToggle.IsOn = beforeExport ? !state.AskBeforeExport : state.AskBeforeExport;
        Select(ThemeCombo, "default");

        EngineText.Text = EngineClient.FindEngine() is { } path
            ? $"Engine: {path}"
            : "Engine: not found. PCCI cannot convert anything until it is reinstalled.";
        _loading = false;
    }

    /// <summary>
    /// Show the settings on the way to an export. True means go ahead; false means the
    /// user cancelled and nothing should be written.
    /// </summary>
    public static async Task<bool> ConfirmAsync(AppState state, XamlRoot root)
    {
        if (!state.AskBeforeExport) return true;
        var dialog = new SettingsDialog(state, beforeExport: true) { XamlRoot = root };
        var answer = await dialog.ShowAsync();
        if (answer != ContentDialogResult.Primary) return false;
        // Only once the export is actually going ahead: somebody who ticks the box and
        // then cancels has not agreed to anything.
        if (dialog.AskToggle.IsOn) state.AskBeforeExport = false;
        return true;
    }

    private void OnAskToggled(object sender, RoutedEventArgs args)
    {
        if (_loading || _beforeExport) return;
        _state.AskBeforeExport = AskToggle.IsOn;
    }

    private static void Select(ComboBox combo, string tag)
    {
        combo.SelectedItem = combo.Items
            .OfType<ComboBoxItem>()
            .FirstOrDefault(item => (string?)item.Tag == tag) ?? combo.Items.FirstOrDefault();
    }

    private static string TagOf(ComboBox combo) =>
        (combo.SelectedItem as ComboBoxItem)?.Tag as string ?? "";

    private void OnExportTargetChanged(object sender, SelectionChangedEventArgs args)
    {
        UpdateInlineWarning();
        if (_loading) return;
        _state.ExportTarget = TagOf(ExportTargetCombo);
        // The target is baked into the plan an export sends back, like everything else
        // here, so a chart already read has to be re-planned.
        _ = _state.ReplanAllAsync();
    }

    private void OnChordDeliveryChanged(object sender, SelectionChangedEventArgs args)
    {
        UpdateInlineWarning();
        if (_loading) return;
        _state.ChordDelivery = TagOf(ChordDeliveryCombo);
        // Chord delivery is baked into the plan an export sends back, so a chart
        // already read has to be re-planned or the change simply will not apply.
        _ = _state.ReplanAllAsync();
    }

    private void UpdateInlineWarning()
    {
        var delivery = TagOf(ChordDeliveryCombo);
        var target = TagOf(ExportTargetCombo);
        var freeshow = target == "freeshow";
        var inline = delivery is "inline" or "inline+notes";

        ExportTargetNote.Text = freeshow
            ? "A .show file for FreeShow, with the same groups and the chords on its own "
              + "Chords stage element. FreeShow has no chord-chart element, so that one "
              + "route has nothing to write there."
            : "A .pro presentation: named groups, an arrangement, and the chords on the "
              + "stage screen.";

        // FreeShow keeps no per-slide chart image, so a route that asks for one leaves
        // the stage with nothing on it.
        var unsupported = freeshow && delivery is "chart" or "both";
        UnsupportedRoute.IsOpen = unsupported;
        UnsupportedRoute.Message = delivery == "chart"
            ? "FreeShow has no chord-chart element, so nothing would reach the stage. "
              + "Pick one of the other routes."
            : "Only the notes half of this reaches FreeShow: it has no chord-chart element.";

        InlineInfo.Message =
            $"The chords are stored on the words, which is what {AppState.NameFor(target)}'s "
            + "Chords stage element reads. Turn the Chords element on in the stage layout "
            + "editor to see them.";

        InlinePanel.Visibility = inline ? Visibility.Visible : Visibility.Collapsed;
        AudienceWarning.IsOpen = inline && ChordsOnSlideToggle.IsOn;
    }

    private void OnChordsOnSlideToggled(object sender, RoutedEventArgs args)
    {
        UpdateInlineWarning();
        if (_loading) return;
        _state.ChordsOnSlide = ChordsOnSlideToggle.IsOn;
        // Baked into the plan an export sends back, like the delivery route itself.
        _ = _state.ReplanAllAsync();
    }

    private void OnChordPlacementChanged(object sender, SelectionChangedEventArgs args)
    {
        if (_loading) return;
        _state.ChordPlacement = TagOf(ChordPlacementCombo);
        _ = _state.ReplanAllAsync();
    }

    private void OnChordProToggled(object sender, RoutedEventArgs args)
    {
        if (_loading) return;
        _state.WriteChordPro = ChordProToggle.IsOn;
    }

    private void OnThemeChanged(object sender, SelectionChangedEventArgs args)
    {
        if (_loading) return;
        if (XamlRoot?.Content is FrameworkElement root)
        {
            root.RequestedTheme = TagOf(ThemeCombo) switch
            {
                "light" => ElementTheme.Light,
                "dark" => ElementTheme.Dark,
                _ => ElementTheme.Default
            };
        }
    }
}
