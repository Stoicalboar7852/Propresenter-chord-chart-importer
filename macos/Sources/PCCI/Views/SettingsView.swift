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
                Text(state.config.chordDelivery.explanation)
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
                    .fixedSize(horizontal: false, vertical: true)

                if let caution = state.config.chordDelivery.caution {
                    Label(caution, systemImage: "exclamationmark.triangle.fill")
                        .font(.caption)
                        .foregroundStyle(Theme.uncertain)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.top, 2)
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
