import SwiftUI

/// Liquid Glass, with a deliberate fallback.
///
/// macOS 26 introduced `glassEffect(_:in:)`, `GlassEffectContainer` and
/// `.buttonStyle(.glass)`. Those symbols do not exist in the macOS 14 SDK this package
/// declares as its deployment target, and a `#available` check alone is not enough —
/// the compiler still has to *see* the symbol, which means building against the macOS
/// 26 SDK.
///
/// So the glass path is behind a compilation condition as well as an availability
/// check. Build with `-D PCCI_LIQUID_GLASS` on a machine with the macOS 26 SDK to get
/// real Liquid Glass; without it the app uses `.ultraThinMaterial`, which is what every
/// macOS version from 14 onwards has and which still looks deliberate rather than
/// unfinished.
///
/// The exact Liquid Glass signatures should be checked against the installed SDK
/// before enabling the flag — they are the one thing in this project that could not be
/// verified against a real toolchain.
struct GlassPanel: ViewModifier {
    var cornerRadius: CGFloat = 16
    var tint: Color? = nil

    @ViewBuilder
    func body(content: Content) -> some View {
        #if PCCI_LIQUID_GLASS
        if #available(macOS 26, *) {
            content
                .glassEffect(
                    tint.map { .regular.tint($0) } ?? .regular,
                    in: .rect(cornerRadius: cornerRadius)
                )
        } else {
            fallback(content)
        }
        #else
        fallback(content)
        #endif
    }

    @ViewBuilder
    private func fallback(_ content: Content) -> some View {
        // The tint is painted over the material rather than dropped, which it used to
        // be: without it every tinted panel on macOS 14 came out the same flat grey and
        // a tinted button lost the only thing making it look like a button.
        content
            .background {
                let shape = RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                shape
                    .fill(.ultraThinMaterial)
                    .overlay(shape.fill(tint ?? .clear))
                    .overlay(
                        shape.strokeBorder(
                            LinearGradient(
                                colors: [
                                    Color.white.opacity(0.28),
                                    Theme.separator.opacity(0.45),
                                ],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 1
                        )
                    )
            }
    }
}

extension View {
    /// A panel that reads as glass on macOS 26 and as a material everywhere else.
    func glassPanel(cornerRadius: CGFloat = 16, tint: Color? = nil) -> some View {
        modifier(GlassPanel(cornerRadius: cornerRadius, tint: tint))
    }
}

/// The app's primary button: Golden Gate orange, as glass rather than as paint.
///
/// The tint is heavy enough to carry white text over whatever is behind the window -
/// a bright desktop included - and light enough that the button still reads as glass
/// rather than a coloured rectangle.
struct GoldenGateButtonStyle: ButtonStyle {
    var prominent: Bool = true

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 13, weight: .semibold))
            .padding(.horizontal, 18)
            .padding(.vertical, 9)
            .foregroundStyle(prominent ? Color.white : Theme.primaryText)
            .glassPanel(cornerRadius: 10, tint: tint(pressed: configuration.isPressed))
            .contentShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
            .scaleEffect(configuration.isPressed ? 0.975 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }

    private func tint(pressed: Bool) -> Color {
        guard prominent else {
            return Theme.primaryText.opacity(pressed ? 0.16 : 0.08)
        }
        return pressed
            ? Theme.accentWarm.opacity(0.92)
            : Theme.effectiveAccent.opacity(0.78)
    }
}
