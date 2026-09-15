import AppKit
import SwiftUI

/// The success screen: what was written, and what to do next.
struct ExportedPane: View {
    @Environment(AppState.self) private var state
    let document: ChartDocument
    let output: URL

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 48))
                .foregroundStyle(Theme.confident)

            VStack(spacing: 6) {
                Text(document.result?.title ?? output.deletingPathExtension().lastPathComponent)
                    .font(.title2.weight(.semibold))
                if let result = document.result {
                    Text("\(result.slides) slides in \(result.sections) sections · \(result.checks) checks passed")
                        .foregroundStyle(Theme.secondaryText)
                }
            }

            VStack(alignment: .leading, spacing: 10) {
                FileRow(label: "Presentation", url: output)
                ForEach(document.result?.chartPages ?? [], id: \.self) { page in
                    FileRow(label: "Chord chart page", url: URL(fileURLWithPath: page))
                }
                if let chordpro = document.result?.chordpro {
                    FileRow(label: "ChordPro", url: URL(fileURLWithPath: chordpro))
                }
            }
            .padding(16)
            .glassPanel(cornerRadius: 14)
            .frame(maxWidth: 560)

            if let warnings = document.result?.warnings, !warnings.isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(warnings, id: \.self) { warning in
                        Label(warning, systemImage: "info.circle")
                            .font(.caption)
                            .foregroundStyle(Theme.secondaryText)
                    }
                }
                .frame(maxWidth: 560, alignment: .leading)
            }

            HStack(spacing: 12) {
                Button("Reveal in Finder") {
                    NSWorkspace.shared.activateFileViewerSelecting([output])
                }
                .buttonStyle(GoldenGateButtonStyle(prominent: false))

                Button("Set up my stage screen") {
                    openStageGuide()
                }
                .buttonStyle(GoldenGateButtonStyle(prominent: false))

                Button("Back to review") {
                    document.stage = .review
                }
                .buttonStyle(GoldenGateButtonStyle())
            }

            Text("The chords are in each slide's notes, and the chart pages are beside the presentation. Neither shows on the audience output.")
                .font(.caption)
                .foregroundStyle(Theme.secondaryText)
                .multilineTextAlignment(.center)
                .frame(maxWidth: 520)
        }
        .padding(40)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func openStageGuide() {
        let bundled = Bundle.main.resourceURL?.appendingPathComponent("STAGE_SETUP.md")
        if let bundled, FileManager.default.fileExists(atPath: bundled.path) {
            NSWorkspace.shared.open(bundled)
            return
        }
        if let url = URL(string: "https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/blob/main/docs/STAGE_SETUP.md") {
            NSWorkspace.shared.open(url)
        }
    }
}

struct FileRow: View {
    let label: String
    let url: URL

    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: "doc")
                .foregroundStyle(Theme.secondaryText)
            VStack(alignment: .leading, spacing: 1) {
                Text(label)
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
                Text(url.lastPathComponent)
                    .foregroundStyle(Theme.primaryText)
                    .lineLimit(1)
                    .truncationMode(.middle)
            }
            Spacer()
            Button {
                NSWorkspace.shared.activateFileViewerSelecting([url])
            } label: {
                Image(systemName: "arrow.right.circle")
            }
            .buttonStyle(.borderless)
            .help("Show in Finder")
        }
    }
}
