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
        content
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: cornerRadius))
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .strokeBorder(Theme.separator.opacity(0.6), lineWidth: 1)
            )
    }
}

extension View {
    /// A panel that reads as glass on macOS 26 and as a material everywhere else.
    func glassPanel(cornerRadius: CGFloat = 16, tint: Color? = nil) -> some View {
        modifier(GlassPanel(cornerRadius: cornerRadius, tint: tint))
    }
}

/// The app's primary button: Golden Gate orange, warming when pressed.
struct GoldenGateButtonStyle: ButtonStyle {
    var prominent: Bool = true

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 13, weight: .semibold))
            .padding(.horizontal, 18)
            .padding(.vertical, 9)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .fill(background(pressed: configuration.isPressed))
            )
            .foregroundStyle(prominent ? Color.white : Theme.primaryText)
            .contentShape(RoundedRectangle(cornerRadius: 10))
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }

    private func background(pressed: Bool) -> Color {
        guard prominent else {
            return pressed ? Theme.surfaceRaised : Theme.surface
        }
        return pressed ? Theme.accentWarm : Theme.effectiveAccent
    }
}
