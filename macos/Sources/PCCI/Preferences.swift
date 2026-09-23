import Foundation

/// What the app remembers between launches.
///
/// `UserDefaults`, because that is where a Mac app's settings belong and the whole of
/// it is seven small values. Nothing here is worth an error message: a key that is
/// missing or holds something unexpected means "use the default", which is also what a
/// first launch sees.
struct Preferences {
    var exportTarget: ExportTarget = .propresenter
    var chordDelivery: ChordDelivery = .inline
    var chordPlacement: ChordPlacementStyle = .chordsOnly
    var chordsOnSlide = false
    var writeChordPro = false
    var linesPerSlide = 4

    /// Whether an export stops to show the settings first. On until somebody says
    /// otherwise: these settings decide what reaches a stage screen, and an export is
    /// the moment to find that out rather than the Sunday after.
    var askBeforeExport = true

    private enum Key {
        static let exportTarget = "exportTarget"
        static let chordDelivery = "chordDelivery"
        static let chordPlacement = "chordPlacement"
        static let chordsOnSlide = "chordsOnSlide"
        static let writeChordPro = "writeChordPro"
        static let linesPerSlide = "linesPerSlide"
        static let askBeforeExport = "askBeforeExport"
    }

    static func load(from defaults: UserDefaults = .standard) -> Preferences {
        var preferences = Preferences()
        if let raw = defaults.string(forKey: Key.exportTarget),
            let value = ExportTarget(rawValue: raw)
        {
            preferences.exportTarget = value
        }
        if let raw = defaults.string(forKey: Key.chordDelivery),
            let value = ChordDelivery(rawValue: raw)
        {
            preferences.chordDelivery = value
        }
        if let raw = defaults.string(forKey: Key.chordPlacement),
            let value = ChordPlacementStyle(rawValue: raw)
        {
            preferences.chordPlacement = value
        }
        preferences.chordsOnSlide = defaults.bool(forKey: Key.chordsOnSlide)
        preferences.writeChordPro = defaults.bool(forKey: Key.writeChordPro)
        // A missing integer reads as zero, which is not a legal number of lines.
        let lines = defaults.integer(forKey: Key.linesPerSlide)
        preferences.linesPerSlide = (1...10).contains(lines) ? lines : 4
        if defaults.object(forKey: Key.askBeforeExport) != nil {
            preferences.askBeforeExport = defaults.bool(forKey: Key.askBeforeExport)
        }
        return preferences
    }

    func save(to defaults: UserDefaults = .standard) {
        defaults.set(exportTarget.rawValue, forKey: Key.exportTarget)
        defaults.set(chordDelivery.rawValue, forKey: Key.chordDelivery)
        defaults.set(chordPlacement.rawValue, forKey: Key.chordPlacement)
        defaults.set(chordsOnSlide, forKey: Key.chordsOnSlide)
        defaults.set(writeChordPro, forKey: Key.writeChordPro)
        defaults.set(linesPerSlide, forKey: Key.linesPerSlide)
        defaults.set(askBeforeExport, forKey: Key.askBeforeExport)
    }
}
