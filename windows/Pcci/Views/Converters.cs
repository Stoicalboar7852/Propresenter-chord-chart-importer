using System;
using Microsoft.UI;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;
using Windows.UI;

namespace Pcci;

/// <summary>Confidence to the dot colour beside a section: green, amber, red.</summary>
public sealed class ConfidenceToBrushConverter : IValueConverter
{
    private static readonly SolidColorBrush Confident = new(Color.FromArgb(255, 0x4C, 0xC3, 0x8A));
    private static readonly SolidColorBrush Uncertain = new(Color.FromArgb(255, 0xE8, 0xB3, 0x39));
    private static readonly SolidColorBrush Guessed = new(Color.FromArgb(255, 0xE8, 0x60, 0x3C));

    public object Convert(object value, Type targetType, object parameter, string language)
    {
        var confidence = value is double number ? number : 1.0;
        return confidence switch
        {
            >= 0.9 => Confident,
            >= 0.5 => Uncertain,
            _ => Guessed
        };
    }

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}


/// <summary>Bool to Visibility, spelled out rather than relying on x:Bind's implicit conversion.</summary>
public sealed class BoolToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, string language) =>
        value is true ? Microsoft.UI.Xaml.Visibility.Visible : Microsoft.UI.Xaml.Visibility.Collapsed;

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        value is Microsoft.UI.Xaml.Visibility.Visible;
}
