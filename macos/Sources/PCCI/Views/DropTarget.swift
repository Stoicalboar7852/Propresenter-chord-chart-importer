import AppKit
import SwiftUI
import UniformTypeIdentifiers

/// The first pane: a full-window drop target that validates on hover.
struct DropTarget: View {
    @Environment(AppState.self) private var state
    @State private var isTargeted = false
    @State private var rejected = false

    var body: some View {
        VStack(spacing: 18) {
            Image(systemName: isTargeted ? "square.and.arrow.down.fill" : "square.and.arrow.down")
                .font(.system(size: 54, weight: .light))
                .foregroundStyle(borderColour)
            Text("Drop a chord chart here")
                .font(.title2.weight(.semibold))
                .foregroundStyle(Theme.primaryText)
            Text(rejected ? "That file type is not one PCCI can read." : supportedList)
                .font(.callout)
                .foregroundStyle(rejected ? Theme.guessed : Theme.secondaryText)
                .multilineTextAlignment(.center)
                .frame(maxWidth: 460)
            Button("Choose files…") { openPanel() }
                .buttonStyle(GoldenGateButtonStyle())
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .padding(48)
        .background {
            RoundedRectangle(cornerRadius: 22)
                .strokeBorder(
                    borderColour,
                    style: StrokeStyle(lineWidth: isTargeted ? 2.5 : 1.5, dash: [9, 7])
                )
                .padding(28)
        }
        .glassPanel(cornerRadius: 22, tint: isTargeted ? Theme.accentWarm.opacity(0.16) : nil)
        .padding(20)
        .animation(.easeOut(duration: 0.15), value: isTargeted)
        .onDrop(of: [.fileURL], isTargeted: $isTargeted) { providers in
            handle(providers)
            return true
        }
    }

    private var supportedList: String {
        "Word, PDF, plain text, Markdown, RTF, OpenDocument, HTML or ChordPro."
    }

    private var borderColour: Color {
        if rejected { return Theme.guessed }
        return isTargeted ? Theme.accentWarm : Theme.separator
    }

    private func handle(_ providers: [NSItemProvider]) {
        rejected = false
        Task {
            var urls: [URL] = []
            for provider in providers {
                if let url = await provider.loadFileURL() {
                    urls.append(url)
                }
            }
            let accepted = urls.filter(AppState.accepts)
            await MainActor.run {
                if accepted.isEmpty, !urls.isEmpty {
                    rejected = true
                } else {
                    state.add(urls: accepted)
                }
            }
        }
    }

    private func openPanel() {
        let panel = NSOpenPanel()
        panel.allowsMultipleSelection = true
        panel.canChooseDirectories = false
        if panel.runModal() == .OK {
            state.add(urls: panel.urls)
        }
    }
}

extension NSItemProvider {
    /// Load a dropped file URL, without blocking whatever called us.
    func loadFileURL() async -> URL? {
        await withCheckedContinuation { continuation in
            _ = loadObject(ofClass: URL.self) { url, _ in
                continuation.resume(returning: url)
            }
        }
    }
}
