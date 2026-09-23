import AppKit
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
/// An export that has been asked for and is waiting on the settings screen.
enum PendingExport: Equatable {
    case single(ChartDocument.ID)
    case all
}

@MainActor
@Observable
final class AppState {
    var documents: [ChartDocument] = []
    var selectedID: ChartDocument.ID?
    // Chords into the slide text, which is what both programs' Chords stage element
    // reads. Stage-only: the switch that would draw them on the audience screen is
    // `chordsOnSlide`, and it is off. Overwritten from the saved settings at launch.
    var config = EngineConfig(
        linesPerSlide: 4,
        balanceLastSlide: true,
        chordDelivery: .inline,
        chordPlacement: .chordsOnly
    ) {
        didSet { remember() }
    }
    var writeChordPro = false {
        didSet { remember() }
    }
    /// Whether an export stops to show the settings first.
    var askBeforeExport = true {
        didSet { remember() }
    }
    /// The export waiting on that screen, or nil when nothing is waiting.
    var pendingExport: PendingExport?
    var logLines: [EngineLogLine] = []
    var showLog = false
    var banner: EngineError?
    var isBusy = false
    /// How far a Convert All has got, or nil when no batch is running.
    var batchProgress: BatchProgress?

    // MARK: Finding songs online

    /// What is in the search box. A song name, or a link pasted out of a browser -
    /// the engine works out which, so the user does not have to tell it.
    var searchQuery = ""
    var searchResults: [SongMatch] = []
    /// What the sources had to say for themselves: one of them down, a page with no
    /// chart in it, a search that found nothing.
    var searchNotes: [String] = []
    var isSearching = false
    /// The query the current results belong to, so "nothing found" can name it.
    var searchedFor: String?
    /// Narrowing, for a title a hundred other songs share.
    var searchArtist = ""
    var searchAlbum = ""
    var searchYear = ""
    /// How many rows to ask for. Grows when the user asks to see more.
    var searchLimit = 20
    /// How many matched altogether, so the list can offer the rest.
    var searchTotal = 0

    var hasMoreResults: Bool { searchTotal > searchResults.count }
    var hasFilters: Bool {
        !searchArtist.isEmpty || !searchAlbum.isEmpty || !searchYear.isEmpty
    }
    /// The result being downloaded, so its own row can show the progress.
    var importingRef: String?
    /// Anything the import wants to warn about, once it has happened.
    var importNotes: [String] = []

    struct BatchProgress: Equatable {
        var done: Int
        var total: Int
        var failed: Int

        var label: String { "Converting \(done + 1) of \(total)" }
    }

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

    /// Go back to the start screen without losing the list.
    ///
    /// The search box and the drop target only appear when nothing is selected, so
    /// until this existed the only way to add a second song was to clear the first.
    func showAddSong() {
        selectedID = nil
        banner = nil
    }

    /// Empty the queue and go back to the drop target. Exported files are left alone:
    /// this clears the list, not anybody's disk.
    func clear() {
        documents.removeAll()
        selectedID = nil
        banner = nil
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

    init() {
        let saved = Preferences.load()
        loadingPreferences = true
        config.exportTarget = saved.exportTarget
        config.chordDelivery = saved.chordDelivery
        config.chordPlacement = saved.chordPlacement
        config.chordsOnSlide = saved.chordsOnSlide
        config.linesPerSlide = saved.linesPerSlide
        writeChordPro = saved.writeChordPro
        askBeforeExport = saved.askBeforeExport
        loadingPreferences = false
    }

    /// Guards the setters above while the saved settings are being read in, so that
    /// loading does not immediately write back what it just read.
    private var loadingPreferences = false

    private func remember() {
        guard !loadingPreferences else { return }
        Preferences(
            exportTarget: config.exportTarget,
            chordDelivery: config.chordDelivery,
            chordPlacement: config.chordPlacement,
            chordsOnSlide: config.chordsOnSlide,
            writeChordPro: writeChordPro,
            linesPerSlide: config.linesPerSlide,
            askBeforeExport: askBeforeExport
        ).save()
    }

    /// Lines per slide is one setting for the whole queue, not a per-chart one, so
    /// changing it re-plans every chart already read. Previews and a batch export then
    /// cannot disagree about what a slide holds.
    func setLinesPerSlide(_ value: Int) {
        guard value != config.linesPerSlide else { return }
        config.linesPerSlide = value
        replanEverything()
    }

    func setChordDelivery(_ value: ChordDelivery) {
        guard value != config.chordDelivery else { return }
        config.chordDelivery = value
        replanEverything()
    }

    func setExportTarget(_ value: ExportTarget) {
        guard value != config.exportTarget else { return }
        config.exportTarget = value
        replanEverything()
    }

    func setChordsOnSlide(_ value: Bool) {
        guard value != config.chordsOnSlide else { return }
        config.chordsOnSlide = value
        replanEverything()
    }

    func setChordPlacement(_ value: ChordPlacementStyle) {
        guard value != config.chordPlacement else { return }
        config.chordPlacement = value
        replanEverything()
    }

    /// Re-plan every chart already read.
    ///
    /// Not optional after a settings change: an export sends the plan back to the
    /// engine, and the plan carries the settings it was made with. Without this, a
    /// setting changed after a chart was read would simply not apply to it.
    private func replanEverything() {
        for document in documents where document.song != nil {
            Task { await replan(document) }
        }
    }

    // MARK: Converting the whole queue

    // MARK: Exporting

    /// Start an export of one chart: the settings first, if they are being asked for.
    func beginExport(_ document: ChartDocument) {
        guard askBeforeExport else {
            chooseDestinationAndExport(document)
            return
        }
        pendingExport = .single(document.id)
    }

    /// The same for the whole queue.
    func beginConvertAll() {
        guard !documents.isEmpty else { return }
        guard askBeforeExport else {
            chooseFolderAndConvertAll()
            return
        }
        pendingExport = .all
    }

    /// The settings screen was accepted. `remember` is the user asking not to be
    /// stopped again, and is only acted on here - somebody who ticks the box and then
    /// cancels has agreed to nothing.
    func confirmPendingExport(remember: Bool) {
        let pending = pendingExport
        pendingExport = nil
        if remember { askBeforeExport = false }
        guard let pending else { return }
        // On the next turn of the run loop: a modal panel opened while the sheet is
        // still going away gets a window that is on its way out.
        Task { @MainActor in
            switch pending {
            case .single(let id):
                guard let document = documents.first(where: { $0.id == id }) else { return }
                chooseDestinationAndExport(document)
            case .all:
                chooseFolderAndConvertAll()
            }
        }
    }

    func cancelPendingExport() {
        pendingExport = nil
    }

    /// Ask where one presentation should go, then write it.
    ///
    /// The panel lives here rather than in a view for the same reason the folder one
    /// does: more than one place offers the action, and the file name and the message
    /// both depend on settings this object owns.
    func chooseDestinationAndExport(_ document: ChartDocument) {
        let target = config.exportTarget
        let panel = NSSavePanel()
        let name =
            document.plan?.song.title ?? document.url.deletingPathExtension().lastPathComponent
        panel.nameFieldStringValue = "\(name).\(target.fileExtension)"
        panel.message = "Where should the \(target.title) file go?"
        panel.canCreateDirectories = true
        guard panel.runModal() == .OK, let url = panel.url else { return }
        Task { await export(document, to: url) }
    }

    /// Ask where the batch should go, then convert the whole queue into it.
    ///
    /// The panel lives here rather than in a view because two places offer this same
    /// action - the toolbar and the button under the list - and neither should own a
    /// private copy of it.
    func chooseFolderAndConvertAll() {
        guard !documents.isEmpty else { return }
        let panel = NSOpenPanel()
        panel.canChooseDirectories = true
        panel.canChooseFiles = false
        panel.canCreateDirectories = true
        panel.allowsMultipleSelection = false
        panel.prompt = "Convert Here"
        panel.message = documents.count == 1
            ? "Where should the presentation go?"
            : "Where should the \(documents.count) presentations go?"
        guard panel.runModal() == .OK, let directory = panel.url else { return }
        Task { await convertAll(into: directory) }
    }

    /// Export every chart in the queue into one folder with the current settings.
    ///
    /// Anything not read yet is read first, and each chart keeps whatever corrections
    /// have already been made to it. A chart that fails is left marked failed and the
    /// rest still convert: one bad file in a service folder should not cost the others.
    func convertAll(into directory: URL) async {
        let queue = documents
        guard !queue.isEmpty else { return }
        var used: Set<String> = []
        var failed = 0
        for (index, document) in queue.enumerated() {
            batchProgress = BatchProgress(done: index, total: queue.count, failed: failed)
            if document.song == nil {
                await analyse(document)
            }
            guard document.song != nil, document.plan != nil else {
                failed += 1
                continue
            }
            let destination = Self.freePath(
                in: directory,
                named: document.url.deletingPathExtension().lastPathComponent,
                extension: config.exportTarget.fileExtension,
                alreadyUsed: &used
            )
            await export(document, to: destination)
            if case .failed = document.stage { failed += 1 }
        }
        batchProgress = nil
        banner = nil
    }

    /// `<directory>/<name>.<extension>`, numbered rather than overwritten.
    ///
    /// Two folders of charts can easily each hold a Great Are You Lord, and a batch
    /// that quietly wrote one over the other would be worse than no batch at all.
    static func freePath(
        in directory: URL,
        named name: String,
        extension fileExtension: String,
        alreadyUsed: inout Set<String>
    ) -> URL {
        var candidate = name
        var counter = 2
        while alreadyUsed.contains(candidate.lowercased())
            || FileManager.default.fileExists(
                atPath: directory.appendingPathComponent(candidate).appendingPathExtension(
                    fileExtension
                ).path
            )
        {
            candidate = "\(name) \(counter)"
            counter += 1
        }
        alreadyUsed.insert(candidate.lowercased())
        return directory.appendingPathComponent(candidate).appendingPathExtension(fileExtension)
    }

    // MARK: Songs from the web

    /// Search, or describe a pasted link. The engine decides which this is.
    func runSearch(startingOver: Bool = true) async {
        let query = searchQuery.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !query.isEmpty, !isSearching else { return }
        if startingOver { searchLimit = 20 }
        isSearching = true
        defer { isSearching = false }
        searchedFor = query

        let limit = searchLimit
        let artist = searchArtist.trimmed
        let album = searchAlbum.trimmed
        let year = searchYear.trimmed
        guard
            let outcome = await withEngineValue({ engine in
                try EngineClient.decode(
                    SearchOutcome.self,
                    from: await engine.searchJSON(
                        query, limit: limit, artist: artist, album: album, year: year
                    ),
                    what: "the search"
                )
            })
        else {
            searchResults = []
            searchTotal = 0
            return
        }
        searchResults = outcome.results
        searchNotes = outcome.notes
        searchTotal = outcome.totalFound
    }

    /// Ask for the next batch. The list is capped so the first search stays quick;
    /// a song further down was simply unreachable before this existed.
    func showMoreResults() async {
        guard hasMoreResults, !isSearching else { return }
        searchLimit = min(searchLimit + 20, 60)
        await runSearch(startingOver: false)
    }

    func clearSearch() {
        searchQuery = ""
        searchArtist = ""
        searchAlbum = ""
        searchYear = ""
        searchLimit = 20
        searchResults = []
        searchNotes = []
        searchedFor = nil
        searchTotal = 0
        importNotes = []
    }

    /// Download a result and put it in the queue, ready to review like any other chart.
    func importMatch(_ match: SongMatch) async {
        guard let link = match.chartURL else { return }
        importingRef = match.ref
        defer { importingRef = nil }
        await importLink(link)
    }

    func importLink(_ link: String) async {
        guard
            let imported = await withEngineValue({ engine in
                try EngineClient.decode(
                    ImportedChart.self, from: await engine.fetchJSON(url: link), what: "the download"
                )
            })
        else { return }
        adopt(imported)
    }

    /// Whatever is on the clipboard, as a chart.
    ///
    /// The same door as a link: some words, possibly some chords, and no file. This is
    /// the way in for every site that will not let a program read it - open the page
    /// yourself, select the chart, copy, and come back here.
    func importFromClipboard() async {
        let pasted = NSPasteboard.general.string(forType: .string) ?? ""
        guard !pasted.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            banner = EngineError.local(
                "There is no text on the clipboard to import.",
                detail: "the pasteboard held no string"
            )
            return
        }
        guard
            let imported = await withEngineValue({ engine in
                try EngineClient.decode(
                    ImportedChart.self,
                    from: await engine.pasteJSON(text: pasted),
                    what: "the pasted chart"
                )
            })
        else { return }
        adopt(imported)
    }

    /// Put a freshly imported chart in the queue and select it.
    private func adopt(_ imported: ImportedChart) {
        importNotes = imported.notes
        if let existing = documents.first(where: { $0.url == imported.url }) {
            // Re-importing the same song overwrites the file it was written to, so the
            // one already in the list is stale. Read it again rather than adding a
            // second row pointing at the same path.
            selectedID = existing.id
            Task { await analyse(existing) }
        } else {
            add(urls: [imported.url])
            selectedID = documents.first { $0.url == imported.url }?.id ?? selectedID
        }
        searchResults = []
        searchedFor = nil
        searchTotal = 0
    }

    /// Run something against the engine that is about no particular document.
    ///
    /// A search has no chart to mark as failed, so a failure here is a banner and a
    /// nil, rather than the document-shaped error path the conversion flow uses.
    private func withEngineValue<T>(_ body: (EngineClient) async throws -> T) async -> T? {
        isBusy = true
        defer { isBusy = false }
        do {
            let engine = try EngineClient()
            let value = try await body(engine)
            logLines = await engine.log
            banner = nil
            return value
        } catch let error as EngineError {
            banner = error
            return nil
        } catch {
            banner = EngineError.local("Something went wrong.", detail: error.localizedDescription)
            return nil
        }
    }
}
