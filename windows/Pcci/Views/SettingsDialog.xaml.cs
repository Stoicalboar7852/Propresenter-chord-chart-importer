using System.Linq;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Pcci.Services;
using Pcci.ViewModels;

namespace Pcci;

public sealed partial class SettingsDialog : ContentDialog
{
    private readonly AppState _state;
    private bool _loading = true;

    public SettingsDialog(AppState state)
    {
        InitializeComponent();
        _state = state;

        Select(ExportTargetCombo, state.ExportTarget);
        Select(ChordDeliveryCombo, state.ChordDelivery);
        ChordsOnSlideToggle.IsOn = state.ChordsOnSlide;
        UpdateInlineWarning();
        Select(ChordPlacementCombo, state.ChordPlacement);
        ChordProToggle.IsOn = state.WriteChordPro;
        Select(ThemeCombo, "default");

        EngineText.Text = EngineClient.FindEngine() is { } path
            ? $"Engine: {path}"
            : "Engine: not found. PCCI cannot convert anything until it is reinstalled.";
        _loading = false;
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
