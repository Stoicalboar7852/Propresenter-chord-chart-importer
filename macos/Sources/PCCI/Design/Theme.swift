import AppKit
import SwiftUI

/// The Golden Gate palette: a deep charcoal ground with International Orange for
/// anything interactive.
///
/// Colours are defined in code rather than an asset catalogue so the app builds with
/// the Swift toolchain alone — `actool`, which compiles asset catalogues, ships with
/// Xcode. Each colour still carries a light and a dark variant and resolves through
/// the system appearance, which is what an asset catalogue would have given us.
enum Theme {

    // MARK: Ground

    static let background = dynamic(light: Color(hex: 0xF2F1EF), dark: Color(hex: 0x1C1C1E))
    static let surface = dynamic(light: Color(hex: 0xFFFFFF), dark: Color(hex: 0x252528))
    static let surfaceRaised = dynamic(light: Color(hex: 0xFAFAF8), dark: Color(hex: 0x2E2E32))
    static let separator = dynamic(light: Color(hex: 0xD8D6D2), dark: Color(hex: 0x3A3A3E))

    // MARK: Ink

    static let primaryText = dynamic(light: Color(hex: 0x1C1C1E), dark: Color(hex: 0xF5F4F2))
    static let secondaryText = dynamic(light: Color(hex: 0x5B5B60), dark: Color(hex: 0xA0A0A6))

    // MARK: Golden Gate

    /// International Orange, the colour the bridge is actually painted.
    static let accent = dynamic(light: Color(hex: 0xC0362C), dark: Color(hex: 0xC0362C))
    /// The warmer end, used for hover and pressed states.
    static let accentWarm = dynamic(light: Color(hex: 0xE8603C), dark: Color(hex: 0xE8603C))

    // MARK: Confidence

    static let confident = dynamic(light: Color(hex: 0x2E7D51), dark: Color(hex: 0x4CC38A))
    static let uncertain = dynamic(light: Color(hex: 0xB4791B), dark: Color(hex: 0xE8B339))
    static let guessed = dynamic(light: Color(hex: 0xB03A2E), dark: Color(hex: 0xE8603C))

    /// The accent to use: the person's own system accent when they have chosen one,
    /// otherwise Golden Gate orange.
    static var effectiveAccent: Color {
        if UserDefaults.standard.object(forKey: "AppleAccentColor") != nil {
            return Color.accentColor
        }
        return accent
    }

    static func confidenceColour(_ confidence: Double) -> Color {
        switch confidence {
        case 0.9...: return confident
        case 0.5..<0.9: return uncertain
        default: return guessed
        }
    }

    private static func dynamic(light: Color, dark: Color) -> Color {
        Color(nsColor: NSColor(name: nil) { appearance in
            let isDark = appearance.bestMatch(from: [.aqua, .darkAqua]) == .darkAqua
            return NSColor(isDark ? dark : light)
        })
    }
}

extension Color {
    init(hex: UInt32) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255.0,
            green: Double((hex >> 8) & 0xFF) / 255.0,
            blue: Double(hex & 0xFF) / 255.0,
            opacity: 1.0
        )
    }
}
