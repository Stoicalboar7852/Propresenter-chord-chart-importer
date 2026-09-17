import AppKit
import SwiftUI

/// Finding a song online, and the results it found.
///
/// One field does both jobs the user asked for: type a song name and it searches every
/// source; paste a link out of a browser and it describes that page instead. The
/// engine works out which of the two it has been given, so there is no mode to pick
/// and no second box to explain.
@MainActor
struct SearchPane: View {
    @Environment(AppState.self) private var state
    @FocusState private var fieldFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            field
            if state.isSearching {
                HStack(spacing: 8) {
                    ProgressView().controlSize(.small)
                    Text("Asking every source\u{2026}")
                        .font(.callout)
                        .foregroundStyle(Theme.secondaryText)
                }
            } else if !state.searchResults.isEmpty {
                results
            } else if let query = state.searchedFor {
                Text("Nothing came back for \u{201C}\(query)\u{201D}.")
                    .font(.callout)
                    .foregroundStyle(Theme.secondaryText)
            }
            notes
        }
        .onAppear { fieldFocused = true }
    }

    private var field: some View {
        @Bindable var state = state
        return HStack(spacing: 8) {
            Image(systemName: "magnifyingglass")
                .foregroundStyle(Theme.secondaryText)
            TextField("Search for a song, or paste a link", text: $state.searchQuery)
                .textFieldStyle(.plain)
                .focused($fieldFocused)
                .onSubmit { Task { await state.runSearch() } }
                .accessibilityLabel("Search for a song, or paste a link")
            if !state.searchQuery.isEmpty {
                Button {
                    state.clearSearch()
                    fieldFocused = true
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(Theme.secondaryText)
                }
                .buttonStyle(.borderless)
                .help("Clear the search")
            }
            Button("Search") { Task { await state.runSearch() } }
                .buttonStyle(GoldenGateButtonStyle())
                .disabled(state.searchQuery.trimmed.isEmpty || state.isSearching)
            Button {
                Task { await state.importFromClipboard() }
            } label: {
                Label("Paste", systemImage: "doc.on.clipboard")
                    .labelStyle(.titleAndIcon)
            }
            .help("Import a chart you have copied from somewhere else (\u{2318}\u{21E7}V)")
            .disabled(state.isBusy)
        }
        .padding(10)
        .glassPanel(cornerRadius: 12)
    }

    private var results: some View {
        ScrollView {
            LazyVStack(spacing: 8) {
                ForEach(state.searchResults) { match in
                    SearchResultRow(match: match)
                }
            }
            .padding(.bottom, 4)
        }
        .frame(maxHeight: 420)
    }

    @ViewBuilder
    private var notes: some View {
        if !state.searchNotes.isEmpty || !state.importNotes.isEmpty {
            VStack(alignment: .leading, spacing: 4) {
                ForEach(state.importNotes + state.searchNotes, id: \.self) { note in
                    HStack(alignment: .top, spacing: 6) {
                        Image(systemName: "info.circle")
                            .foregroundStyle(Theme.uncertain)
                        Text(note)
                            .font(.caption)
                            .foregroundStyle(Theme.secondaryText)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
            }
            .padding(.top, 2)
        }
    }
}

/// One song: its cover, its credits, where the words would come from.
@MainActor
struct SearchResultRow: View {
    @Environment(AppState.self) private var state
    let match: SongMatch

    private var isImporting: Bool { state.importingRef == match.ref }

    var body: some View {
        HStack(spacing: 12) {
            artwork
            VStack(alignment: .leading, spacing: 3) {
                Text(match.title)
                    .font(.body.weight(.semibold))
                    .foregroundStyle(Theme.primaryText)
                    .lineLimit(1)
                if !match.subtitle.isEmpty {
                    Text(match.subtitle)
                        .font(.caption)
                        .foregroundStyle(Theme.secondaryText)
                        .lineLimit(1)
                }
                HStack(spacing: 6) {
                    badge
                    Text("via \(match.sourceNames)")
                        .font(.caption2)
                        .foregroundStyle(Theme.secondaryText)
                        .lineLimit(1)
                }
            }
            Spacer(minLength: 8)
            if isImporting {
                ProgressView().controlSize(.small)
            } else {
                Button("Import") { Task { await state.importMatch(match) } }
                    .buttonStyle(GoldenGateButtonStyle())
                    // A song Apple knows about and nobody has the words for is worth
                    // showing - it confirms pcci found the right song - but there is
                    // nothing behind the button, so there is no button.
                    .disabled(!match.importable || state.isBusy)
                    .help(
                        match.importable
                            ? "Download this and add it to the list"
                            : "No source pcci can read has the words for this one"
                    )
            }
        }
        .padding(10)
        .glassPanel(cornerRadius: 12, tint: match.importable ? nil : Theme.separator.opacity(0.10))
        .opacity(match.importable ? 1.0 : 0.72)
    }

    private var artwork: some View {
        // AsyncImage does the fetching; the engine only ever hands over the address.
        // A cover that fails to load is a placeholder, never an error worth telling
        // anybody about - the song still imports perfectly well without its picture.
        AsyncImage(url: match.thumbnail) { phase in
            switch phase {
            case .success(let image):
                image.resizable().aspectRatio(contentMode: .fill)
            default:
                ZStack {
                    Rectangle().fill(Theme.surfaceRaised)
                    Image(systemName: "music.note")
                        .foregroundStyle(Theme.secondaryText)
                }
            }
        }
        .frame(width: 48, height: 48)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .strokeBorder(Theme.separator.opacity(0.6))
        )
    }

    private var badge: some View {
        Text(match.wordsLabel)
            .font(.caption2.weight(.semibold))
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(
                Capsule().fill(
                    match.hasChords
                        ? Theme.confident.opacity(0.22)
                        : match.importable
                            ? Theme.uncertain.opacity(0.22)
                            : Theme.separator.opacity(0.30)
                )
            )
            .foregroundStyle(
                match.hasChords
                    ? Theme.confident
                    : match.importable ? Theme.uncertain : Theme.secondaryText
            )
    }
}

extension String {
    var trimmed: String { trimmingCharacters(in: .whitespacesAndNewlines) }
}
