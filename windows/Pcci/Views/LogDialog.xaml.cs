using System.Linq;
using Microsoft.UI.Xaml.Controls;
using Pcci.ViewModels;
using Windows.ApplicationModel.DataTransfer;

namespace Pcci;

public sealed partial class LogDialog : ContentDialog
{
    private readonly AppState _state;

    public LogDialog(AppState state)
    {
        InitializeComponent();
        _state = state;
        Lines.ItemsSource = state.LogLines;
    }

    private void OnCopy(ContentDialog sender, ContentDialogButtonClickEventArgs args)
    {
        args.Cancel = true; // keep the dialog open after copying
        var package = new DataPackage();
        package.SetText(string.Join("\n", _state.LogLines.Select(line => line.Display)));
        Clipboard.SetContent(package);
    }
}
