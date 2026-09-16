import AppKit
import SwiftUI

/// The screen that matters: what the parser guessed, and the chance to fix it.
///
/// Left: the detected sections, each editable. Right: exactly what each slide will
/// contain, chords over lyrics in a monospaced face. Changing lines per slide re-plans
/// through the engine, so the preview is never an approximation of the output.
@MainActor
struct ReviewPane: View {
    @Environment(AppState.self) private var state
    let document: ChartDocument

    var body: some View {
        VStack(spacing: 0) {
            header
            Divider().overlay(Theme.separator)
            HSplitView {
                SectionList(document: document)
                    .frame(minWidth: 280, idealWidth: 340)
                SlidePreview(document: document)
                    .frame(minWidth: 380)
            }
        }
    }

    private var header: some View {
        HStack(spacing: 20) {
            VStack(alignment: .leading, spacing: 2) {
                Text(document.plan?.song.title ?? document.name)
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(Theme.primaryText)
                if let plan = document.plan {
                    Text(summary(plan))
                        .font(.caption)
                        .foregroundStyle(Theme.secondaryText)
                }
            }
            Spacer()

            LinesPerSlideField(
                value: Binding(
                    get: { state.config.linesPerSlide },
                    set: { state.setLinesPerSlide($0) }
                )
            )
            .padding(.horizontal, 12)
            .padding(.vertical, 7)
            .glassPanel(cornerRadius: 10)

            Button("Export…") { exportPanel() }
                .buttonStyle(GoldenGateButtonStyle())
                .disabled(state.isBusy || document.plan == nil)
        }
        .padding(16)
    }

    private func summary(_ plan: SlidePlan) -> String {
        let guessed = plan.song.sections.filter(\.wasGuessed).count
        let base = "\(plan.slideCount) slides in \(plan.song.sections.count) sections"
        return guessed == 0 ? base : "\(base) · \(guessed) guessed, worth a look"
    }

    private func exportPanel() {
        let panel = NSSavePanel()
        panel.nameFieldStringValue = (document.plan?.song.title ?? document.url.deletingPathExtension().lastPathComponent) + ".pro"
        panel.message = "Where should the ProPresenter file go?"
        panel.canCreateDirectories = true
        if panel.runModal() == .OK, let url = panel.url {
            Task { await state.export(document, to: url) }
        }
    }
}

/// The detected sections, reorderable and editable.
@MainActor
struct SectionList: View {
    @Environment(AppState.self) private var state
    let document: ChartDocument

    var body: some View {
        List {
            Section {
                ForEach(Array(sections.enumerated()), id: \.element.id) { index, section in
                    SectionRow(document: document, index: index, section: section)
                }
                .onMove { offsets, destination in
                    state.move(sectionsAt: offsets, to: destination, in: document)
                }
            } header: {
                Text("Detected sections")
            } footer: {
                if sections.contains(where: \.wasGuessed) {
                    Label(
                        "Sections with an amber or red dot were guessed. Correct them here.",
                        systemImage: "info.circle"
                    )
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
                }
            }
        }
        .listStyle(.inset)
    }

    private var sections: [SongSection] {
        document.song?.sections ?? []
    }
}

@MainActor
struct SectionRow: View {
    @Environment(AppState.self) private var state
    let document: ChartDocument
    let index: Int
    let section: SongSection

    var body: some View {
        HStack(spacing: 10) {
            Circle()
                .fill(Theme.confidenceColour(section.confidence))
                .frame(width: 9, height: 9)
                .help(confidenceHelp)

            Picker("", selection: typeBinding) {
                ForEach(SectionType.allCases) { type in
                    Text(type.rawValue).tag(type)
                }
            }
            .labelsHidden()
            .frame(width: 140)

            TextField("—", text: numberText)
                .frame(width: 44)
                .textFieldStyle(.roundedBorder)
                .help("Section number. Leave blank for a section that appears once.")

            Spacer(minLength: 4)

            Text("\(section.lines.count)")
                .font(.caption.monospacedDigit())
                .foregroundStyle(Theme.secondaryText)
                .help("\(section.lines.count) lines, \(section.lyricCount) with words")

            Menu {
                Button("Merge into section above") {
                    state.mergeUp(sectionAt: index, in: document)
                }
                .disabled(index == 0)
                Button("Split in half") {
                    state.split(
                        sectionAt: index,
                        atLine: max(1, section.lines.count / 2),
                        in: document
                    )
                }
                .disabled(section.lines.count < 2)
                Divider()
                Button("Delete section", role: .destructive) {
                    state.delete(sectionAt: index, in: document)
                }
            } label: {
                Image(systemName: "ellipsis.circle")
            }
            .menuStyle(.borderlessButton)
            .frame(width: 24)
        }
        .padding(.vertical, 3)
    }

    private var confidenceHelp: String {
        switch section.confidence {
        case 0.9...: return "Read from a label in the chart"
        case 0.5..<0.9: return "Inferred from the chart's formatting — worth checking"
        default: return "Guessed from blank lines — please check"
        }
    }

    private var typeBinding: Binding<SectionType> {
        Binding(
            get: { section.type },
            set: { state.setType($0, forSectionAt: index, in: document) }
        )
    }

    /// An empty field means "no number", which is how a section that appears once is
    /// labelled. `TextField(value:format:)` cannot express that, so this maps text.
    private var numberText: Binding<String> {
        Binding(
            get: { section.number.map(String.init) ?? "" },
            set: { text in
                let trimmed = text.trimmingCharacters(in: .whitespaces)
                state.setNumber(trimmed.isEmpty ? nil : Int(trimmed), forSectionAt: index, in: document)
            }
        )
    }
}

/// What each slide will actually contain.
@MainActor
struct SlidePreview: View {
    let document: ChartDocument

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                ForEach(document.plan?.slides ?? []) { slide in
                    SlideCard(slide: slide)
                }
            }
            .padding(16)
        }
        .background(Theme.background)
    }
}

@MainActor
struct SlideCard: View {
    let slide: PlannedSlide

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(slide.label)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(Theme.accent)
                Spacer()
                Text("\(slide.lines.count) lines")
                    .font(.caption)
                    .foregroundStyle(Theme.secondaryText)
            }
            VStack(alignment: .leading, spacing: 2) {
                ForEach(slide.lines) { line in
                    if !line.chordRow.trimmingCharacters(in: .whitespaces).isEmpty {
                        Text(line.chordRow)
                            .font(.system(.caption, design: .monospaced))
                            .foregroundStyle(Theme.accentWarm)
                    }
                    if !line.lyrics.isEmpty {
                        Text(line.lyrics)
                            .font(.system(.body, design: .monospaced))
                            .foregroundStyle(Theme.primaryText)
                    }
                    if let annotation = line.annotation, !annotation.isEmpty {
                        Text(annotation)
                            .font(.caption.italic())
                            .foregroundStyle(Theme.secondaryText)
                    }
                }
            }
            .textSelection(.enabled)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(14)
        .glassPanel(cornerRadius: 14)
    }
}
