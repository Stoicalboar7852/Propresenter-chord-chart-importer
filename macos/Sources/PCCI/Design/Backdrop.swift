import AppKit
import SwiftUI

/// The window's own translucency.
///
/// `NSVisualEffectView` in `.behindWindow` mode is what makes a Mac window genuinely
/// transparent: the desktop and whatever is sitting behind it blur through, rather than
/// the app painting a grey that merely resembles blur. It has worked the same way since
/// 10.10, which is why the glass here rests on it rather than on anything newer -
/// `glassEffect` exists only on macOS 26, and this has to look deliberate on 14 too.
struct VisualEffectBackground: NSViewRepresentable {
    var material: NSVisualEffectView.Material = .underWindowBackground
    var blending: NSVisualEffectView.BlendingMode = .behindWindow

    func makeNSView(context: Context) -> NSVisualEffectView {
        let view = NSVisualEffectView()
        view.material = material
        view.blendingMode = blending
        // Keep blurring when the window is not frontmost. A window that goes flat grey
        // the moment you click ProPresenter would be the opposite of the point.
        view.state = .active
        view.isEmphasized = true
        return view
    }

    func updateNSView(_ view: NSVisualEffectView, context: Context) {
        view.material = material
        view.blendingMode = blending
    }
}

/// Colour behind the glass.
///
/// Glass with nothing behind it is grey. These are the app icon's two oranges thrown
/// across the window as soft radial washes at low opacity, so the material has
/// something warm to pick up and refract. They are deliberately weak: this is a tint
/// on the desktop showing through, not a painted background that would put the
/// transparency back where it started.
struct AppBackdrop: View {
    var body: some View {
        ZStack {
            VisualEffectBackground()

            RadialGradient(
                colors: [Theme.washWarm.opacity(0.34), Theme.washWarm.opacity(0.0)],
                center: .topLeading,
                startRadius: 0,
                endRadius: 620
            )
            RadialGradient(
                colors: [Theme.washDeep.opacity(0.30), Theme.washDeep.opacity(0.0)],
                center: .bottomTrailing,
                startRadius: 0,
                endRadius: 660
            )
            RadialGradient(
                colors: [Theme.washCool.opacity(0.18), Theme.washCool.opacity(0.0)],
                center: .init(x: 0.15, y: 0.95),
                startRadius: 0,
                endRadius: 420
            )
        }
        .ignoresSafeArea()
    }
}

extension View {
    /// Translucency, with the app's colour washed across it.
    func appBackdrop() -> some View {
        background(AppBackdrop())
    }
}
