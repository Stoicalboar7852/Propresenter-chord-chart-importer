using Microsoft.UI.Xaml;

namespace Pcci;

public partial class App : Application
{
    /// <summary>The one window, so views can parent file pickers and dialogs to it.</summary>
    public MainWindow? MainWindowInstance { get; private set; }

    public App() => InitializeComponent();

    protected override void OnLaunched(LaunchActivatedEventArgs args)
    {
        MainWindowInstance = new MainWindow();
        MainWindowInstance.Activate();
    }
}
