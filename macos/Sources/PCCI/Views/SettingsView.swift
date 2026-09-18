import SwiftUI

/// The settings window, on ⌘, where a Mac user looks for it.
///
/// Until now these were fixed in code: notes *and* a chord chart, chords aligned under
/// the words. Those are still the defaults, and they are still the right ones for most
/// people — but the route that feeds ProPresenter's own Chords element can only be
/// chosen deliberately, so there has to be somewhere to choose it.
@MainActor
struct SettingsView: View {
    @Environment(AppState.self) private var state

    var body: some View {
        @Bindable var state = state
        Form {
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
        .formStyle(.grouped)
        .frame(width: 460)
        .fixedSize(horizontal: false, vertical: true)
    }
}
