import Foundation

// Codable mirrors of what `pcci search`, `pcci fetch` and `pcci paste` put on stdout.
// Field names match the engine's JSON exactly; CodingKeys does the mapping so the wire
// format stays the engine's and nothing here has to be kept in step by hand.

/// A site that contributed to a search result, and what it contributed.
struct MatchSource: Codable, Hashable, Identifiable {
    var provider: String
    var name: String
    var url: String?
    var supplies: [String]

    var id: String { "\(provider)-\(url ?? name)" }
}

/// One row in the search results.
struct SongMatch: Codable, Hashable, Identifiable {
    var ref: String
    var title: String
    var artist: String?
    var album: String?
    var year: Int?
    var artworkURL: String?
    var artworkThumbURL: String?
    var artworkProvider: String?
    var chartURL: String?
    var chartKind: String
    var rating: Double?
    var votes: Int?
    var key: String?
    var ccliNumber: String?
    var copyright: String?
    var sources: [MatchSource]

    var id: String { ref }

    enum CodingKeys: String, CodingKey {
        case ref
        case title
        case artist
        case album
        case year
        case artworkURL = "artwork_url"
        case artworkThumbURL = "artwork_thumb_url"
        case artworkProvider = "artwork_provider"
        case chartURL = "chart_url"
        case chartKind = "chart_kind"
        case rating
        case votes
        case key
        case ccliNumber = "ccli_number"
        case copyright
        case sources
    }

    /// Whether there is anything here to turn into a presentation.
    var importable: Bool { chartURL != nil && chartKind != "none" }

    var hasChords: Bool { chartKind == "chords" || chartKind == "tab" }

    /// `Parish Choir · Hymns, Volume One · 2019`, as much of it as is known.
    var subtitle: String {
        var parts: [String] = []
        if let artist, !artist.isEmpty { parts.append(artist) }
        if let album, !album.isEmpty, album != artist { parts.append(album) }
        if let year { parts.append(String(year)) }
        return parts.joined(separator: " · ")
    }

    var sourceNames: String {
        sources.map(\.name).joined(separator: ", ")
    }

    /// What the row promises: chords, just the words, or nothing importable.
    var wordsLabel: String {
        switch chartKind {
        case "chords", "tab": return "Chords"
        case "lyrics": return "Lyrics"
        default: return "No words"
        }
    }

    var thumbnail: URL? { artworkThumbURL.flatMap(URL.init(string:)) }
}

/// Everything one search produced, including what went wrong on the way.
struct SearchOutcome: Codable {
    var query: String
    var isURL: Bool
    var results: [SongMatch]
    var notes: [String]
    /// How many matched before the list was cut to the requested size.
    var totalFound: Int

    enum CodingKeys: String, CodingKey {
        case query
        case isURL = "is_url"
        case results
        case notes
        case totalFound = "total_found"
    }

    var hasMore: Bool { totalFound > results.count }
}

/// What `fetch` and `paste` report: a chart now sitting on disk.
struct ImportedChart: Codable {
    var path: String
    var title: String
    var artist: String?
    var chartKind: String
    var hasChords: Bool
    var source: MatchSource
    var notes: [String]

    enum CodingKeys: String, CodingKey {
        case path
        case title
        case artist
        case chartKind = "chart_kind"
        case hasChords = "has_chords"
        case source
        case notes
    }

    var url: URL { URL(fileURLWithPath: path) }
}
