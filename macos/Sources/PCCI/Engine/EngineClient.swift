import Foundation

/// Talks to the `pcci` engine, which ships inside the app bundle as a sidecar binary.
///
/// The contract is the one the engine documents: with `--json`, stdout carries exactly
/// one JSON object and stderr carries JSON Lines. Nothing here parses human-readable
/// text, and nothing here runs on the main actor — every call is `async` and the
/// process is waited on off the main thread.
actor EngineClient {

    /// Log lines the engine wrote to stderr during the most recent call.
    private(set) var log: [EngineLogLine] = []

    private let executableURL: URL

    init(executableURL: URL? = nil) throws {
        if let executableURL {
            self.executableURL = executableURL
            return
        }
        guard let bundled = EngineClient.bundledEngineURL() else {
            throw EngineError.local(
                "The conversion engine is missing from this copy of PCCI.",
                detail: "no engine found in Contents/Resources/engine or on PATH"
            )
        }
        self.executableURL = bundled
    }

    /// `Contents/Resources/engine/pcci`, or a development build, or `pcci` on PATH.
    static func bundledEngineURL() -> URL? {
        let candidates: [URL?] = [
            Bundle.main.resourceURL?.appendingPathComponent("engine/pcci"),
            Bundle.main.resourceURL?.appendingPathComponent("engine/pcci.exe"),
            URL(fileURLWithPath: "../core/.venv/bin/pcci"),
            URL(fileURLWithPath: "/usr/local/bin/pcci"),
            URL(fileURLWithPath: "/opt/homebrew/bin/pcci")
        ]
        for case let candidate? in candidates
        where FileManager.default.isExecutableFile(atPath: candidate.path) {
            return candidate
        }
        return nil
    }

    // MARK: Commands

    func doctorJSON() async throws -> Data {
        try await runRaw(["doctor", "--json"])
    }

    /// Every call returns raw JSON. Decoding happens on the caller's side, which keeps
    /// values that are not `Sendable` — a decoded plan holds the engine's own JSON
    /// dictionary — from crossing the actor boundary.
    func analyzeJSON(_ url: URL) async throws -> Data {
        try await runRaw(["analyze", url.path, "--json"])
    }

    func planJSON(_ url: URL, config: EngineConfig) async throws -> Data {
        try await runRaw(["plan", url.path, "--json"] + configArguments(config))
    }

    /// Re-plan from a song the user has corrected in the review screen.
    ///
    /// The chunking rules stay in the engine: the app sends the corrected song back
    /// rather than re-implementing slide planning in Swift, so the two can never drift.
    func planJSON(song: Data, config: EngineConfig) async throws -> Data {
        let temporary = try Self.writeTemporary(song, prefix: "pcci-song")
        defer { try? FileManager.default.removeItem(at: temporary) }
        return try await runRaw(
            ["plan", "--song", temporary.path, "--json"] + configArguments(config)
        )
    }

    // MARK: Songs from the web

    /// Search every online source the engine knows.
    ///
    /// The artist is a filter *and* part of the question: a bare title is a thousand
    /// songs on any source, and a title with an artist is usually one.
    func searchJSON(
        _ query: String,
        limit: Int = 20,
        artist: String = "",
        album: String = "",
        year: String = ""
    ) async throws -> Data {
        var arguments = ["search", query, "--limit", String(limit), "--json"]
        if !artist.isEmpty { arguments += ["--artist", artist] }
        if !album.isEmpty { arguments += ["--album", album] }
        if !year.isEmpty { arguments += ["--year", year] }
        return try await runRaw(arguments)
    }

    /// Download the chart at a link. The engine picks where to keep it and says where.
    func fetchJSON(url: String) async throws -> Data {
        try await runRaw(["fetch", url, "--json"])
    }

    /// Hand the engine text copied from somewhere else.
    ///
    /// It goes over stdin rather than a temporary file so a chart the user copied out
    /// of an email never touches the disk as a file nobody asked for; the engine
    /// writes it out itself, once, under a name taken from the song.
    func pasteJSON(text: String) async throws -> Data {
        try await runRaw(["paste", "--json"], input: Data(text.utf8))
    }

    /// Build from a plan the user has reviewed and possibly edited.
    func buildJSON(plan: Data, to destination: URL, writeChordPro: Bool) async throws -> Data {
        let temporary = try Self.writeTemporary(plan, prefix: "pcci-plan")
        defer { try? FileManager.default.removeItem(at: temporary) }
        var arguments = ["build", "--plan", temporary.path, "-o", destination.path, "--json"]
        if writeChordPro { arguments.append("--chordpro") }
        return try await runRaw(arguments)
    }

    private static func writeTemporary(_ payload: Data, prefix: String) throws -> URL {
        let url = FileManager.default.temporaryDirectory
            .appendingPathComponent("\(prefix)-\(UUID().uuidString).json")
        try payload.write(to: url)
        return url
    }

    private func configArguments(_ config: EngineConfig) -> [String] {
        [
            "-n", String(config.linesPerSlide),
            config.balanceLastSlide ? "--balance" : "--no-balance",
            "--chords", config.chordDelivery.rawValue,
            "--chord-placement", config.chordPlacement.rawValue
        ]
    }

    // MARK: Plan decoding

    /// Decode a plan, keeping the original JSON so an edited plan round-trips whole.
    static func decodePlan(_ data: Data) throws -> SlidePlan {
        guard let raw = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            throw EngineError.local(
                "The engine returned something PCCI could not read.",
                detail: "plan payload was not a JSON object"
            )
        }
        let decoder = JSONDecoder()
        let songData = try JSONSerialization.data(withJSONObject: raw["song"] ?? [:])
        let slidesData = try JSONSerialization.data(withJSONObject: raw["slides"] ?? [])
        let configData = try JSONSerialization.data(withJSONObject: raw["config"] ?? [:])
        return SlidePlan(
            song: try decoder.decode(Song.self, from: songData),
            slides: try decoder.decode([PlannedSlide].self, from: slidesData),
            config: try decoder.decode(EngineConfig.self, from: configData),
            warnings: raw["warnings"] as? [String] ?? [],
            raw: raw
        )
    }

    // MARK: Decoding

    /// Decode any of the engine's payloads, saying which one failed rather than
    /// letting a `DecodingError` reach the user as a wall of Swift.
    static func decode<T: Decodable>(_ type: T.Type, from data: Data, what: String) throws -> T {
        do {
            return try JSONDecoder().decode(type, from: data)
        } catch {
            throw EngineError.local(
                "PCCI could not read what the engine said about \(what).",
                detail: "\(error)"
            )
        }
    }

    // MARK: Process plumbing

    /// Run the engine and return stdout, turning a non-zero exit into a typed error.
    private func runRaw(_ arguments: [String], input: Data? = nil) async throws -> Data {
        log.removeAll()
        let process = Process()
        process.executableURL = executableURL
        process.arguments = arguments

        let outPipe = Pipe()
        let errPipe = Pipe()
        process.standardOutput = outPipe
        process.standardError = errPipe
        let inPipe = input.map { _ in Pipe() }
        if let inPipe { process.standardInput = inPipe }

        do {
            try process.run()
        } catch {
            throw EngineError.local(
                "PCCI could not start its conversion engine.",
                detail: "\(executableURL.path): \(error.localizedDescription)"
            )
        }

        // Written off the calling thread and closed straight after: the engine reads
        // stdin to the end before it answers, so writing it inline would deadlock as
        // soon as the text outgrew a pipe buffer.
        if let inPipe, let input {
            DispatchQueue.global(qos: .userInitiated).async {
                inPipe.fileHandleForWriting.write(input)
                try? inPipe.fileHandleForWriting.close()
            }
        }

        let outData = try await Self.readToEnd(outPipe)
        let errData = try await Self.readToEnd(errPipe)
        await Self.wait(for: process)

        log = Self.parseLog(errData)

        guard process.terminationStatus == 0 else {
            throw Self.decodeError(from: outData, exitCode: process.terminationStatus, log: log)
        }
        return outData
    }

    private static func readToEnd(_ pipe: Pipe) async throws -> Data {
        try await withCheckedThrowingContinuation { continuation in
            DispatchQueue.global(qos: .userInitiated).async {
                let data = pipe.fileHandleForReading.readDataToEndOfFile()
                continuation.resume(returning: data)
            }
        }
    }

    private static func wait(for process: Process) async {
        await withCheckedContinuation { continuation in
            DispatchQueue.global(qos: .userInitiated).async {
                process.waitUntilExit()
                continuation.resume()
            }
        }
    }

    static func parseLog(_ data: Data) -> [EngineLogLine] {
        String(decoding: data, as: UTF8.self)
            .split(separator: "\n")
            .compactMap { line in
                guard
                    let payload = try? JSONSerialization.jsonObject(
                        with: Data(line.utf8)
                    ) as? [String: Any]
                else {
                    return nil
                }
                return EngineLogLine(
                    level: payload["level"] as? String ?? "info",
                    message: payload["msg"] as? String ?? "",
                    timestamp: payload["ts"] as? String ?? ""
                )
            }
    }

    static func decodeError(from data: Data, exitCode: Int32, log: [EngineLogLine]) -> EngineError {
        if
            let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
            let error = payload["error"],
            let errorData = try? JSONSerialization.data(withJSONObject: error),
            let decoded = try? JSONDecoder().decode(EngineError.self, from: errorData)
        {
            return decoded
        }
        let tail = log.suffix(3).map(\.message).joined(separator: "; ")
        return EngineError.local(
            "The conversion did not finish.",
            detail: "engine exited with status \(exitCode). \(tail)"
        )
    }
}
