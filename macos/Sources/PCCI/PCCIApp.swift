import AppKit
import SwiftUI

/// Closing the window quits, rather than leaving an empty app sitting in the Dock.
/// PCCI converts a chart and is done; there is nothing for it to do with no window.
@MainActor
final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationShouldTerminateAfterLastWindowClosed(_ application: NSApplication) -> Bool {
        true
    }

    /// Let the desktop through.
    ///
    /// The visual effect view behind the content does the blurring, but an opaque
    /// window with a solid background colour paints over it first, which is why the
    /// app looked like flat panels rather than glass. A transparent titlebar then
    /// stops a grey strip cutting across the top of it.
    func applicationDidFinishLaunching(_ notification: Notification) {
        for window in NSApplication.shared.windows {
            window.isOpaque = false
            window.backgroundColor = .clear
            window.titlebarAppearsTransparent = true
        }
    }
}

@main
@MainActor
struct PCCIApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    @State private var state = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(state)
                .frame(minWidth: 980, minHeight: 640)
                .tint(Theme.effectiveAccent)
        }
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified(showsTitle: true))
        .commands {
            CommandGroup(replacing: .newItem) {
                Button("Open Chart…") { openPanel() }
                    .keyboardShortcut("o")
                // The same shortcut ProPresenter uses for its own clipboard import, so
                // anyone who already does this there does not have to learn a second one.
                Button("Import from Clipboard") {
                    Task { await state.importFromClipboard() }
                }
                .keyboardShortcut("v", modifiers: [.command, .shift])
                Button("Convert All…") { state.beginConvertAll() }
                    .keyboardShortcut("e", modifiers: [.command, .shift])
                    .disabled(state.documents.isEmpty)
            }
            CommandGroup(after: .toolbar) {
                Toggle("Show Engine Log", isOn: Binding(
                    get: { state.showLog },
                    set: { state.showLog = $0 }
                ))
                .keyboardShortcut("l", modifiers: [.command, .shift])
            }
        }

        // Cmd-comma, where a Mac user looks for it. Chord delivery used to be fixed
        // in code, which was fine while there were three sensible routes and one
        // right answer. The route that feeds ProPresenter's own Chords element has to
        // be chosen deliberately, so there has to be somewhere to choose it.
        Settings {
            SettingsView()
                .environment(state)
                .tint(Theme.effectiveAccent)
        }
    }

    private func openPanel() {
        let panel = NSOpenPanel()
        panel.allowsMultipleSelection = true
        panel.canChooseDirectories = false
        panel.message = "Choose one or more chord charts"
        if panel.runModal() == .OK {
            state.add(urls: panel.urls)
        }
    }
}
