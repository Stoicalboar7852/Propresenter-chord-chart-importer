import SwiftUI

/// Lines per slide: a box you can type into, with a stepper beside it.
///
/// The value commits on Return or when the field loses focus, never per keystroke, so
/// typing "10" does not re-plan the song at "1" on the way past. Anything out of range
/// is clamped rather than refused — typing 99 gives you the maximum instead of silently
/// doing nothing — and anything that is not a number puts the real value back.
@MainActor
struct LinesPerSlideField: View {
    @Binding var value: Int
    var range: ClosedRange<Int> = 1...10

    @State private var text: String = ""
    @FocusState private var isFocused: Bool

    var body: some View {
        HStack(spacing: 8) {
            Text("Lines per slide")
                .foregroundStyle(Theme.secondaryText)

            TextField("", text: $text)
                .textFieldStyle(.plain)
                .multilineTextAlignment(.center)
                .font(.body.monospacedDigit().weight(.semibold))
                .frame(width: 34)
                .padding(.vertical, 3)
                .background(
                    RoundedRectangle(cornerRadius: 6, style: .continuous)
                        .fill(Theme.surfaceRaised)
                        .overlay(
                            RoundedRectangle(cornerRadius: 6, style: .continuous)
                                .strokeBorder(isFocused ? Theme.accent : Theme.separator)
                        )
                )
                .focused($isFocused)
                .onSubmit(commit)
                .accessibilityLabel("Lines per slide")

            Stepper("", value: $value, in: range)
                .labelsHidden()
        }
        .onAppear { text = String(value) }
        .onChange(of: value) { _, updated in
            if Int(text) != updated { text = String(updated) }
        }
        .onChange(of: isFocused) { _, focused in
            if !focused { commit() }
        }
    }

    private func commit() {
        guard let typed = Int(text.trimmingCharacters(in: .whitespaces)) else {
            text = String(value)
            return
        }
        let clamped = min(max(typed, range.lowerBound), range.upperBound)
        if clamped != value { value = clamped }
        text = String(clamped)
    }
}
