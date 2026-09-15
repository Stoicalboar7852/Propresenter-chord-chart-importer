import Foundation
import Observation
import SwiftUI
import UniformTypeIdentifiers

/// One file the user dropped, and everything known about it.
@Observable
final class ChartDocument: Identifiable {
    enum Stage: Equatable {
        case queued
        case analysing
        case review
        case exporting
        case exported(URL)
        case failed(String)
    }

    let id = UUID()
    let url: URL
    var stage: Stage = .queued
    var song: Song?
    var plan: SlidePlan?
    var result: ConversionResult?
    var error: EngineError?

    init(url: URL) {
        self.url = url
    }

    var name: String { url.lastPathComponent }

    var statusText: String {
        switch stage {
        case .queued: return "Waiting"
        case .analysing: return "Reading…"
        case .review: return plan.map { "\($0.slideCount) slides" } ?? "Ready"
        case .exporting: return "Exporting…"
        case .exported: return "Exported"
        case .failed: return "Failed"
        }
    }

    var statusColour: Color {
        switch stage {
        case .failed: return Theme.guessed
        case .exported: return Theme.confident
        default: return Theme.secondaryText
        }
    }
}

/// The whole app's state. Everything the views read lives here, and every engine call
/// goes through it so no view ever touches a process.
@MainActor
@Observable
final class AppState {
    var documents: [ChartDocument] = []
    var selectedID: ChartDocument.ID?
    var config = EngineConfig(
        linesPerSlide: 4,
        balanceLastSlide: true,
        chordDelivery: .both,
        chordPlacement: .chordsOnly
    )
    var writeChordPro = false
    var logLines: [EngineLogLine] = []
    var showLog = false
    var banner: EngineError?
    var isBusy = false

    /// File types the drop target accepts, kept in step with the engine's readers.
    /// `nonisolated` because deciding whether a path looks convertible is a pure
    /// function of its extension, and the drop handler asks before it reaches the
    /// main actor.
    nonisolated static let acceptedExtensions: Set<String> = [
        "txt", "text", "md", "markdown", "pdf", "docx", "rtf", "odt", "fodt",
        "html", "htm", "xhtml", "cho", "chopro", "chordpro", "crd", "pro"
    ]

    var selected: ChartDocument? {
        documents.first { $0.id == selectedID }
    }

    // MARK: Queue

    func add(urls: [URL]) {
        let fresh = urls
            .filter { Self.acceptedExtensions.contains($0.pathExtension.lowercased()) }
            .filter { url in !documents.contains { $0.url == url } }
            .map(ChartDocument.init(url:))
        documents.append(contentsOf: fresh)
        if selectedID == nil { selectedID = fresh.first?.id ?? documents.first?.id }
        for document in fresh {
            Task { await analyse(document) }
        }
    }

    func remove(_ document: ChartDocument) {
        documents.removeAll { $0.id == document.id }
        if selectedID == document.id { selectedID = documents.first?.id }
    }

    nonisolated static func accepts(_ url: URL) -> Bool {
        acceptedExtensions.contains(url.pathExtension.lowercased())
    }

    // MARK: Engine

    func analyse(_ document: ChartDocument) async {
        document.stage = .analysing
        document.error = nil
        await withEngine(document) { engine in
            let data = try await engine.planJSON(document.url, config: self.config)
            let plan = try EngineClient.decodePlan(data)
            document.song = plan.song
            document.plan = plan
            document.stage = .review
        }
    }

    /// Re-plan after the user changed the lines-per-slide stepper or edited a section.
    ///
    /// The corrected song goes back to the engine rather than being re-chunked here, so
    /// the preview can never drift from what `build` will write.
    func replan(_ document: ChartDocument) async {
        guard let song = document.song else { return }
        await withEngine(document) { engine in
            let songData = try JSONEncoder().encode(song)
            let data = try await engine.planJSON(song: songData, config: self.config)
            let plan = try EngineClient.decodePlan(data)
            document.plan = plan
            document.stage = .review
        }
    }

    func export(_ document: ChartDocument, to destination: URL) async {
        guard var plan = document.plan, let song = document.song else { return }
        document.stage = .exporting
        await withEngine(document) { engine in
            // Send the corrected song, not the one the parser first produced.
            let songData = try JSONEncoder().encode(song)
            plan.raw["song"] = try JSONSerialization.jsonObject(with: songData)
            let planData = try JSONSerialization.data(withJSONObject: plan.raw)
            let data = try await engine.buildJSON(
                plan: planData,
                to: destination,
                writeChordPro: self.writeChordPro
            )
            let result = try JSONDecoder().decode(ConversionResult.self, from: data)
            document.result = result
            document.stage = .exported(URL(fileURLWithPath: result.output))
        }
    }

    private func withEngine(
        _ document: ChartDocument,
        _ body: (EngineClient) async throws -> Void
    ) async {
        isBusy = true
        defer { isBusy = false }
        do {
            let engine = try EngineClient()
            try await body(engine)
            logLines = await engine.log
            banner = nil
        } catch let error as EngineError {
            document.stage = .failed(error.userMessage)
            document.error = error
            banner = error
        } catch {
            let wrapped = EngineError.local(
                "Something went wrong.",
                detail: error.localizedDescription
            )
            document.stage = .failed(wrapped.userMessage)
            document.error = wrapped
            banner = wrapped
        }
    }

    // MARK: Section editing — the review screen's whole point

    func setType(_ type: SectionType, forSectionAt index: Int, in document: ChartDocument) {
        guard var song = document.song, song.sections.indices.contains(index) else { return }
        song.sections[index].type = type
        song.sections[index].confidence = 1.0
        document.song = song
        Task { await replan(document) }
    }

    func setNumber(_ number: Int?, forSectionAt index: Int, in document: ChartDocument) {
        guard var song = document.song, song.sections.indices.contains(index) else { return }
        song.sections[index].number = number
        document.song = song
        Task { await replan(document) }
    }

    func delete(sectionAt index: Int, in document: ChartDocument) {
        guard var song = document.song, song.sections.indices.contains(index) else { return }
        song.sections.remove(at: index)
        document.song = song
        Task { await replan(document) }
    }

    func move(sectionsAt offsets: IndexSet, to destination: Int, in document: ChartDocument) {
        guard var song = document.song else { return }
        song.sections.move(fromOffsets: offsets, toOffset: destination)
        document.song = song
        Task { await replan(document) }
    }

    /// Merge a section into the one above it.
    func mergeUp(sectionAt index: Int, in document: ChartDocument) {
        guard var song = document.song, index > 0, song.sections.indices.contains(index) else {
            return
        }
        let moving = song.sections.remove(at: index)
        song.sections[index - 1].lines.append(contentsOf: moving.lines)
        document.song = song
        Task { await replan(document) }
    }

    /// Split a section in two at a line, giving the second half the same type.
    func split(sectionAt index: Int, atLine line: Int, in document: ChartDocument) {
        guard
            var song = document.song,
            song.sections.indices.contains(index),
            line > 0,
            line < song.sections[index].lines.count
        else { return }
        var section = song.sections[index]
        let tail = Array(section.lines[line...])
        section.lines = Array(section.lines[..<line])
        var newSection = section
        newSection.lines = tail
        newSection.confidence = 1.0
        song.sections[index] = section
        song.sections.insert(newSection, at: index + 1)
        document.song = song
        Task { await replan(document) }
    }

    func setLinesPerSlide(_ value: Int, for document: ChartDocument) {
        config.linesPerSlide = value
        Task { await replan(document) }
    }
}
