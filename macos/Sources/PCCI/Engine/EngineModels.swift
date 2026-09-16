import Foundation

// Codable mirrors of the engine's JSON. Field names match the Python models exactly;
// where Swift would rather spell something differently, CodingKeys does the mapping so
// the wire format stays the engine's.

struct ChordPlacement: Codable, Hashable, Identifiable {
    var chord: String
    var charIndex: Int
    var raw: String

    var id: String { "\(chord)-\(charIndex)-\(raw)" }

    enum CodingKeys: String, CodingKey {
        case chord
        case charIndex = "char_index"
        case raw
    }
}

struct SongLine: Codable, Hashable, Identifiable {
    var lyrics: String
    var chords: [ChordPlacement]
    var annotation: String?

    var id: String { "\(lyrics)-\(chords.map(\.id).joined())-\(annotation ?? "")" }

    /// The chord row, rebuilt the way the engine rebuilds it for slide notes.
    var chordRow: String {
        var row = ""
        for placement in chords {
            var target = placement.charIndex
            if target < row.count { target = row.count + 1 }
            row += String(repeating: " ", count: max(0, target - row.count))
            row += placement.chord
        }
        return row
    }
}

enum SectionType: String, Codable, CaseIterable, Identifiable {
    case intro = "Intro"
    case verse = "Verse"
    case preChorus = "Pre-Chorus"
    case chorus = "Chorus"
    case postChorus = "Post-Chorus"
    case bridge = "Bridge"
    case tag = "Tag"
    case outro = "Outro"
    case instrumental = "Instrumental"
    case interlude = "Interlude"
    case vamp = "Vamp"
    case breakdown = "Breakdown"
    case refrain = "Refrain"
    case ending = "Ending"
    case misc = "Misc"

    var id: String { rawValue }
}

struct SongSection: Codable, Hashable, Identifiable {
    var type: SectionType
    var number: Int?
    var variant: String
    var rawLabel: String
    var lines: [SongLine]
    var confidence: Double

    let id = UUID()

    enum CodingKeys: String, CodingKey {
        case type
        case number
        case variant
        case rawLabel = "raw_label"
        case lines
        case confidence
    }

    var label: String {
        if type == .misc, !rawLabel.isEmpty { return rawLabel }
        guard let number else { return type.rawValue }
        return "\(type.rawValue) \(number)\(variant)"
    }

    var lyricCount: Int { lines.filter { !$0.lyrics.isEmpty }.count }
    var wasGuessed: Bool { confidence < 0.9 }
}

struct Song: Codable, Hashable {
    var title: String
    var artist: String?
    var ccliNumber: String?
    var copyright: String?
    var key: String?
    var tempo: Int?
    var sections: [SongSection]
    var warnings: [String]
    var sourcePath: String?
    var sourceFormat: String?

    enum CodingKeys: String, CodingKey {
        case title
        case artist
        case ccliNumber = "ccli_number"
        case copyright
        case key
        case tempo
        case sections
        case warnings
        case sourcePath = "source_path"
        case sourceFormat = "source_format"
    }
}

struct PlannedSlide: Codable, Hashable, Identifiable {
    var sectionIndex: Int
    var sectionLabel: String
    var sectionType: SectionType
    var ordinal: Int
    var totalInSection: Int
    var lines: [SongLine]

    let id = UUID()

    enum CodingKeys: String, CodingKey {
        case sectionIndex = "section_index"
        case sectionLabel = "section_label"
        case sectionType = "section_type"
        case ordinal
        case totalInSection = "total_in_section"
        case lines
    }

    var label: String {
        totalInSection == 1 ? sectionLabel : "\(sectionLabel) (\(ordinal))"
    }
}

enum ChordDelivery: String, Codable, CaseIterable, Identifiable {
    case none, notes, chart, both
    var id: String { rawValue }

    var title: String {
        switch self {
        case .none: return "No chords"
        case .notes: return "Slide notes"
        case .chart: return "Chord chart"
        case .both: return "Notes and chart"
        }
    }
}

enum ChordPlacementStyle: String, Codable, CaseIterable, Identifiable {
    case chordsInline = "chords_inline"
    case chordsOnly = "chords_only"
    case above
    case below

    var id: String { rawValue }

    var title: String {
        switch self {
        case .chordsInline: return "Chords in one row"
        case .chordsOnly: return "Chords, aligned to the words"
        case .above: return "Chords above the lyric"
        case .below: return "Chords below the lyric"
        }
    }

    var explanation: String {
        switch self {
        case .chordsInline:
            return "Every chord on one horizontal line. Largest on screen, but nothing lines up."
        case .chordsOnly:
            return "One row per lyric line, each chord over the word it is played on."
        case .above, .below:
            return "The chart in full. Repeats the lyrics already on the slide."
        }
    }
}

struct EngineConfig: Codable, Hashable {
    var linesPerSlide: Int
    var balanceLastSlide: Bool
    var chordDelivery: ChordDelivery
    var chordPlacement: ChordPlacementStyle

    enum CodingKeys: String, CodingKey {
        case linesPerSlide = "lines_per_slide"
        case balanceLastSlide = "balance_last_slide"
        case chordDelivery = "chord_delivery"
        case chordPlacement = "chord_placement"
    }
}

/// The plan, decoded loosely: the engine owns the full schema, and the app only needs
/// the parts it displays. `raw` keeps the original JSON so an edited plan can be sent
/// back without the app having to model every field the engine might add later.
struct SlidePlan {
    var song: Song
    var slides: [PlannedSlide]
    var config: EngineConfig
    var warnings: [String]
    var raw: [String: Any]

    var slideCount: Int { slides.count }
}

struct ConversionResult: Codable {
    var output: String
    var slides: Int
    var sections: Int
    var title: String
    var chartPages: [String]
    var chordpro: String?
    var checks: Int
    var warnings: [String]

    enum CodingKeys: String, CodingKey {
        case output
        case slides
        case sections
        case title
        case chartPages = "chart_pages"
        case chordpro
        case checks
        case warnings
    }
}

/// A typed failure from the engine. `userMessage` is what the banner shows;
/// `technicalDetail` sits behind the disclosure triangle.
struct EngineError: Codable, Error, LocalizedError {
    var kind: String
    var userMessage: String
    var technicalDetail: String

    enum CodingKeys: String, CodingKey {
        case kind
        case userMessage = "user_message"
        case technicalDetail = "technical_detail"
    }

    var errorDescription: String? { userMessage }

    static func local(_ message: String, detail: String = "") -> EngineError {
        EngineError(kind: "app", userMessage: message, technicalDetail: detail)
    }
}

struct EngineLogLine: Identifiable, Hashable {
    let id = UUID()
    var level: String
    var message: String
    var timestamp: String
}
