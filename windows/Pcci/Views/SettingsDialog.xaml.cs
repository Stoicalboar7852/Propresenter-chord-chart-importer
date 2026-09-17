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
        var inline = delivery is "inline" or "inline+notes";
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
