import AppKit
import SwiftUI

/// What the engine said, as it said it. Collapsed by default; useful when something
/// goes wrong and the user needs to send us something concrete.
@MainActor
struct LogConsole: View {
    @Environment(AppState.self) private var state
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Text("Engine log")
                    .font(.headline)
                Spacer()
                Button("Copy") {
                    NSPasteboard.general.clearContents()
                    NSPasteboard.general.setString(plainText, forType: .string)
                }
                .buttonStyle(GoldenGateButtonStyle(prominent: false))
                Button("Done") { dismiss() }
                    .buttonStyle(GoldenGateButtonStyle())
            }
            .padding(14)

            Divider().overlay(Theme.separator)

            ScrollView {
                LazyVStack(alignment: .leading, spacing: 3) {
                    ForEach(state.logLines) { line in
                        HStack(alignment: .firstTextBaseline, spacing: 8) {
                            Text(line.level.uppercased())
                                .font(.system(size: 10, weight: .semibold, design: .monospaced))
                                .foregroundStyle(colour(for: line.level))
                                .frame(width: 54, alignment: .leading)
                            Text(line.message)
                                .font(.system(.caption, design: .monospaced))
                                .foregroundStyle(Theme.primaryText)
                                .textSelection(.enabled)
                        }
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(14)
            }
            .overlay {
                if state.logLines.isEmpty {
                    Text("Nothing logged yet.")
                        .foregroundStyle(Theme.secondaryText)
                }
            }
        }
        .frame(width: 640, height: 420)
        .background(Theme.surface)
    }

    private var plainText: String {
        state.logLines.map { "\($0.timestamp) \($0.level) \($0.message)" }.joined(separator: "\n")
    }

    private func colour(for level: String) -> Color {
        switch level {
        case "error", "critical": return Theme.guessed
        case "warning": return Theme.uncertain
        default: return Theme.secondaryText
        }
    }
}
