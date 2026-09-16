import AppKit
import SwiftUI

/// The window: a queue on the left, the three-step flow on the right.
@MainActor
struct ContentView: View {
    @Environment(AppState.self) private var state

    var body: some View {
        @Bindable var state = state
        NavigationSplitView {
            QueueSidebar()
                .navigationSplitViewColumnWidth(min: 220, ideal: 260, max: 320)
        } detail: {
            detail
        }
        .appBackdrop()
        .toolbar {
            ToolbarItem(placement: .principal) {
                if let document = state.selected {
                    Text(document.plan?.song.title ?? document.name)
                        .font(.headline)
                        .foregroundStyle(Theme.primaryText)
                }
            }
            ToolbarItem(placement: .primaryAction) {
                // Title and icon, not icon alone: an icon-only toolbar button is easy
                // to miss, and an SF Symbol the running system does not have draws
                // nothing at all.
                Button {
                    state.chooseFolderAndConvertAll()
                } label: {
                    Label("Convert All", systemImage: "tray.and.arrow.down")
                        .labelStyle(.titleAndIcon)
                }
                .disabled(state.documents.isEmpty || state.isBusy)
                .help("Convert every chart in the list into one folder")
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
@MainActor
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
        .safeAreaInset(edge: .bottom) {
            VStack(alignment: .leading, spacing: 8) {
                // The same setting the review screen shows: one value for the queue,
                // so what you set here is what a Convert All writes.
                LinesPerSlideField(
                    value: Binding(
                        get: { state.config.linesPerSlide },
                        set: { state.setLinesPerSlide($0) }
                    )
                )
                .font(.caption)

                Button {
                    state.chooseFolderAndConvertAll()
                } label: {
                    Text("Convert All\u{2026}")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(GoldenGateButtonStyle())
                .disabled(state.documents.isEmpty || state.isBusy)
                .help("Convert every chart in the list into one folder")

                HStack(spacing: 8) {
                    if let progress = state.batchProgress {
                        ProgressView(value: Double(progress.done), total: Double(progress.total))
                            .frame(width: 70)
                        Text(progress.label)
                            .font(.caption)
                            .foregroundStyle(Theme.secondaryText)
                    } else {
                        Text(countLabel)
                            .font(.caption)
                            .foregroundStyle(Theme.secondaryText)
                    }
                    Spacer()
                    Button("Clear") { state.clear() }
                        .buttonStyle(.borderless)
                        .disabled(state.documents.isEmpty || state.batchProgress != nil)
                        .help("Empty the list. Files already exported are left where they are.")
                }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(.ultraThinMaterial.opacity(0.7))
        }
    }

    private var countLabel: String {
        switch state.documents.count {
        case 0: return "Nothing loaded"
        case 1: return "1 chart"
        case let count: return "\(count) charts"
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
@MainActor
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

@MainActor
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

@MainActor
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

@MainActor
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
