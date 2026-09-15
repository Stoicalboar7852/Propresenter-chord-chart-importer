using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Pcci.ViewModels;
using Windows.ApplicationModel.DataTransfer;

namespace Pcci;

public sealed partial class FailureView : UserControl
{
    private AppState? _state;
    private ChartDocument? _document;

    public FailureView() => InitializeComponent();

    public void Initialise(AppState state) => _state = state;

    public void Show(ChartDocument document)
    {
        if (!document.IsFailed) return;
        _document = document;
        MessageText.Text = document.Error?.UserMessage ?? "That chart could not be read.";
        DetailText.Text = document.Error?.TechnicalDetail ?? "";
        DetailExpander.Visibility = string.IsNullOrWhiteSpace(DetailText.Text)
            ? Visibility.Collapsed
            : Visibility.Visible;
    }

    private void OnCopyDetail(object sender, RoutedEventArgs args)
    {
        var package = new DataPackage();
        package.SetText(DetailText.Text);
        Clipboard.SetContent(package);
    }

    private async void OnRetry(object sender, RoutedEventArgs args)
    {
        if (_state is null || _document is null) return;
        await _state.AnalyseAsync(_document);
    }
}
