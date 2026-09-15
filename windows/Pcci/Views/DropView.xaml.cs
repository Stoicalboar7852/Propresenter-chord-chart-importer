// `using System;` is load-bearing: the awaiter for a WinRT IAsyncOperation comes from
// WindowsRuntimeSystemExtensions in the System namespace, so without it every
// `await picker...Async()` fails to compile with CS4036.
using System;
using System.Linq;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Pcci.ViewModels;
using Windows.Storage.Pickers;
using WinRT.Interop;

namespace Pcci;

public sealed partial class DropView : UserControl
{
    private AppState? _state;

    public DropView() => InitializeComponent();

    public void Initialise(AppState state) => _state = state;

    private async void OnChoose(object sender, RoutedEventArgs args)
    {
        if (_state is null) return;
        var window = (App.Current as App)?.MainWindowInstance;
        if (window is null) return;

        var picker = new FileOpenPicker { ViewMode = PickerViewMode.List };
        InitializeWithWindow.Initialize(picker, WindowNative.GetWindowHandle(window));
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
            await _state.AddAsync(files.Select(file => file.Path));
        }
    }
}
