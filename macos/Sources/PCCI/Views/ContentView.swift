import AppKit
import SwiftUI

/// The window: a queue on the left, the three-step flow on the right.
struct ContentView: View {
    @Environment(AppState.self) private var state

    var body: some View {
        @Bindable var state = state
        NavigationSplitView {
            QueueSidebar()
                .navigationSplitViewColumnWidth(min: 220, ideal: 260, max: 320)
        } detail: {
            detail
                .background(Theme.background)
        }
        .background(Theme.background)
        .toolbar {
            ToolbarItem(placement: .principal) {
                if let document = state.selected {
                    Text(document.plan?.song.title ?? document.name)
                        .font(.headline)
                        .foregroundStyle(Theme.primaryText)
                }
            }
            ToolbarItem(placement: .primaryAction) {
                Button {
                    state.showLog.toggle()
                } label: {
                    Label("Engine log", systemImage: "text.alignleft")
                }
                .help("Show what the conversion engine reported")
            }
        }
        .sheet(isPresented: $state.showLog) {
            LogConsole()
        }
    }

    @ViewBuilder
    private var detail: some View {
        VStack(spacing: 0) {
            if let error = state.banner {
                ErrorBanner(error: error) { state.banner = nil }
            }
            if let document = state.selected {
                DocumentDetail(document: document)
            } else {
                DropTarget()
            }
        }
    }
}

/// The queue of dropped files.
struct QueueSidebar: View {
    @Environment(AppState.self) private var state

    var body: some View {
        @Bindable var state = state
        List(selection: $state.selectedID) {
            Section("Charts") {
                ForEach(state.documents) { document in
                    HStack(spacing: 10) {
                        Image(systemName: icon(for: document))
                            .foregroundStyle(document.statusColour)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(document.name)
                                .lineLimit(1)
                                .truncationMode(.middle)
                            Text(document.statusText)
                                .font(.caption)
                                .foregroundStyle(Theme.secondaryText)
                        }
                    }
                    .tag(document.id)
                    .contextMenu {
                        Button("Remove", role: .destructive) { state.remove(document) }
                    }
                }
            }
        }
        .listStyle(.sidebar)
        .overlay {
            if state.documents.isEmpty {
                ContentUnavailableView(
                    "No charts yet",
                    systemImage: "music.note.list",
                    description: Text("Drop a chart onto the window, or press \u{2318}O.")
                )
            }
        }
    }

    private func icon(for document: ChartDocument) -> String {
        switch document.stage {
        case .failed: return "exclamationmark.triangle.fill"
        case .exported: return "checkmark.circle.fill"
        case .analysing, .exporting: return "clock"
        default: return "doc.text"
        }
    }
}

/// Which of the three panes a document is currently showing.
struct DocumentDetail: View {
    @Environment(AppState.self) private var state
    let document: ChartDocument

    var body: some View {
        switch document.stage {
        case .queued, .analysing:
            LoadingPane(name: document.name)
        case .review, .exporting:
            ReviewPane(document: document)
        case .exported(let url):
            ExportedPane(document: document, output: url)
        case .failed:
            FailurePane(document: document)
        }
    }
}

struct LoadingPane: View {
    let name: String

    var body: some View {
        VStack(spacing: 14) {
            ProgressView()
            Text("Reading \(name)")
                .foregroundStyle(Theme.secondaryText)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct FailurePane: View {
    @Environment(AppState.self) private var state
    let document: ChartDocument

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 40))
                .foregroundStyle(Theme.guessed)
            Text(document.error?.userMessage ?? "That chart could not be read.")
                .font(.title3)
                .multilineTextAlignment(.center)
                .frame(maxWidth: 520)
            if let detail = document.error?.technicalDetail, !detail.isEmpty {
                DisclosureGroup("Technical detail") {
                    HStack(alignment: .top) {
                        Text(detail)
                            .font(.system(.caption, design: .monospaced))
                            .textSelection(.enabled)
                        Spacer()
                        Button {
                            NSPasteboard.general.clearContents()
                            NSPasteboard.general.setString(detail, forType: .string)
                        } label: {
                            Image(systemName: "doc.on.doc")
                        }
                        .buttonStyle(.borderless)
                        .help("Copy")
                    }
                    .padding(.top, 6)
                }
                .frame(maxWidth: 520)
            }
            Button("Try again") {
                Task { await state.analyse(document) }
            }
            .buttonStyle(GoldenGateButtonStyle())
        }
        .padding(40)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct ErrorBanner: View {
    let error: EngineError
    var dismiss: () -> Void

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: "exclamationmark.circle.fill")
                .foregroundStyle(Theme.guessed)
            VStack(alignment: .leading, spacing: 4) {
                Text(error.userMessage)
                    .foregroundStyle(Theme.primaryText)
                if !error.technicalDetail.isEmpty {
                    Text(error.technicalDetail)
                        .font(.caption)
                        .foregroundStyle(Theme.secondaryText)
                        .textSelection(.enabled)
                }
            }
            Spacer()
            Button {
                dismiss()
            } label: {
                Image(systemName: "xmark")
            }
            .buttonStyle(.borderless)
        }
        .padding(12)
        .glassPanel(cornerRadius: 12, tint: Theme.guessed.opacity(0.18))
        .padding([.horizontal, .top], 12)
    }
}
