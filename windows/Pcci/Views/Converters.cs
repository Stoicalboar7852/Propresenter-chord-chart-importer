using System;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Media.Imaging;
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


/// <summary>
/// A cover-art address to something an Image can show.
///
/// The engine only ever hands over a URL; the download happens here, in the framework,
/// which already knows how to do it off the UI thread and cache the result. A song
/// with no cover, or a cover that fails to load, is a null and an empty frame - never
/// an error, because the import works perfectly well without a picture.
/// </summary>
public sealed class UriToImageSourceConverter : IValueConverter
{
    // An empty BitmapImage rather than null: the interface promises a non-null object,
    // and one with no UriSource simply draws nothing, which is the wanted result.
    public object Convert(object value, Type targetType, object parameter, string language) =>
        value is Uri uri ? new BitmapImage(uri) : new BitmapImage();

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}
