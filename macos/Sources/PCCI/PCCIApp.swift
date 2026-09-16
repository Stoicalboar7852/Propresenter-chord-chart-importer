import AppKit
import SwiftUI

/// Closing the window quits, rather than leaving an empty app sitting in the Dock.
/// PCCI converts a chart and is done; there is nothing for it to do with no window.
@MainActor
final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationShouldTerminateAfterLastWindowClosed(_ application: NSApplication) -> Bool {
        true
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
            }
            CommandGroup(after: .toolbar) {
                Toggle("Show Engine Log", isOn: Binding(
                    get: { state.showLog },
                    set: { state.showLog = $0 }
                ))
                .keyboardShortcut("l", modifiers: [.command, .shift])
            }
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
