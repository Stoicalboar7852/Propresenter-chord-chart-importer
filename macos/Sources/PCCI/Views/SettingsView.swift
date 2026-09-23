import SwiftUI

/// Everything that decides what a conversion writes.
///
/// Sections rather than a whole screen, because two places show them: the settings
/// window, and the screen an export stops at on its way to the file panel. One copy of
/// them means the two cannot drift apart.
@MainActor
struct ConversionSettingsSections: View {
    @Environment(AppState.self) private var state

    var body: some View {
        @Bindable var state = state
        Group {
            Section("Export") {
                Picker(
                    "Write files for",
                    selection: Binding(
                        get: { state.config.exportTarget },
                        set: { state.setExportTarget($0) }
                    )
                ) {
                    ForEach(ExportTarget.allCases) { target in
                        Text(target.title).tag(target)
                    }
                }
                Text(state.config.exportTarget.explanation)
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
                    .fixedSize(horizontal: false, vertical: true)
            }

            Section("Chords") {
                Picker(
                    "Reach the stage screen by",
                    selection: Binding(
                        get: { state.config.chordDelivery },
                        set: { state.setChordDelivery($0) }
                    )
                ) {
                    ForEach(ChordDelivery.allCases) { delivery in
                        Text(delivery.title).tag(delivery)
                    }
                }
                Text(state.config.chordDelivery.explanation(for: state.config.exportTarget))
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
                    .fixedSize(horizontal: false, vertical: true)

                if !state.config.chordDelivery.isSupported(by: state.config.exportTarget) {
                    Label(
                        "\(state.config.exportTarget.title) cannot do this. The chords "
                            + "will not reach the stage screen until you pick another route.",
                        systemImage: "exclamationmark.triangle.fill"
                    )
                    .font(.caption)
                    .foregroundStyle(Theme.guessed)
                    .fixedSize(horizontal: false, vertical: true)
                }

                if let caution = state.config.chordDelivery.caution(for: state.config.exportTarget) {
                    Label(caution, systemImage: "info.circle")
                        .font(.caption)
                        .foregroundStyle(Theme.secondaryText)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.top, 2)
                }

                if state.config.chordDelivery.isExperimental {
                    Toggle(
                        "Draw them on the slide",
                        isOn: Binding(
                            get: { state.config.chordsOnSlide },
                            set: { state.setChordsOnSlide($0) }
                        )
                    )
                    Label(
                        "This paints the chords onto the lyric text, which puts them on "
                            + "the audience screen as well as the stage. Off is what you "
                            + "want unless the congregation is meant to see them.",
                        systemImage: "exclamationmark.triangle.fill"
                    )
                    .font(.caption)
                    .foregroundStyle(state.config.chordsOnSlide ? Theme.guessed : Theme.secondaryText)
                    .fixedSize(horizontal: false, vertical: true)
                }
            }

            Section("Slide notes") {
                Picker(
                    "Notes contain",
                    selection: Binding(
                        get: { state.config.chordPlacement },
                        set: { state.setChordPlacement($0) }
                    )
                ) {
                    ForEach(ChordPlacementStyle.allCases) { placement in
                        Text(placement.title).tag(placement)
                    }
                }
                .disabled(!state.config.chordDelivery.writesNotes)
                Text(
                    state.config.chordDelivery.writesNotes
                        ? "The notes block a stage layout shows on Current Slide Notes."
                        : "Nothing to set: the chords are not going into the notes."
                )
                .font(.caption)
                .foregroundStyle(Theme.secondaryText)
                .fixedSize(horizontal: false, vertical: true)
            }

            Section("Files") {
                Toggle("Also write a ChordPro (.cho) file", isOn: $state.writeChordPro)
                Text("A plain-text copy of the chart beside each presentation.")
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
            }
        }
    }
}

/// The settings window, on ⌘, where a Mac user looks for it.
@MainActor
struct SettingsView: View {
    @Environment(AppState.self) private var state

    var body: some View {
        @Bindable var state = state
        Form {
            ConversionSettingsSections()

            Section("Exporting") {
                Toggle("Ask for these before every export", isOn: $state.askBeforeExport)
                Text(
                    "These settings decide what reaches your stage screen, so an export "
                        + "offers them one last time before it writes anything."
                )
                .font(.caption)
                .foregroundStyle(Theme.secondaryText)
                .fixedSize(horizontal: false, vertical: true)
            }
        }
        .formStyle(.grouped)
        .frame(width: 460)
        .fixedSize(horizontal: false, vertical: true)
    }
}

/// The same settings, on the way to an export.
///
/// The point of stopping here is that the settings are invisible the rest of the time
/// and they decide what a congregation sees. Anyone who would rather not be stopped
/// says so with one switch, and can say the opposite again in Settings.
@MainActor
struct ExportSettingsSheet: View {
    @Environment(AppState.self) private var state
    @State private var remember = false

    var body: some View {
        VStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 4) {
                Text("Check these before exporting")
                    .font(.headline)
                Text(title)
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 20)
            .padding(.top, 20)
            .padding(.bottom, 8)

            Form {
                ConversionSettingsSections()
            }
            .formStyle(.grouped)

            Divider()

            HStack(spacing: 12) {
                Toggle("Use these every time", isOn: $remember)
                    .help("Export without stopping here again. Settings can turn it back on.")
                Spacer()
                Button("Cancel") { state.cancelPendingExport() }
                    .keyboardShortcut(.cancelAction)
                Button("Export\u{2026}") { state.confirmPendingExport(remember: remember) }
                    .keyboardShortcut(.defaultAction)
                    .buttonStyle(GoldenGateButtonStyle())
            }
            .padding(16)
        }
        .frame(width: 520, height: 640)
    }
}

extension ExportSettingsSheet {
    /// What is about to be written, so the screen is about this export and not settings
    /// in the abstract.
    private var title: String {
        switch state.pendingExport {
        case .all:
            let count = state.documents.count
            return count == 1 ? "One song" : "\(count) songs"
        case .single(let id):
            return state.documents.first { $0.id == id }?.name ?? "One song"
        case nil:
            return ""
        }
    }
}
