"""From a ``RawDocument`` to a ``Song``.

This is where the detection ladder in the spec actually runs:

1. ChordPro directives, when the source is ChordPro — no heuristics at all.
2. Bracketed and labelled headers.
3. Formatting signals — a short, bold, standalone line.
4. Blank-line stanzas, as a last resort.

Chord lines are then paired with the lyric line beneath them and aligned, and anything
that is neither (performance instructions such as "Hold G X 8 BARS") is kept as an
annotation so it never reaches the audience screen.
"""

from __future__ import annotations

from pathlib import Path

from pcci.errors import NoSectionsDetectedError
from pcci.ingest import ingest
from pcci.ingest.chordpro import parse_chordpro
from pcci.ir import Line, PositionedLine, RawDocument, Section, SectionType, Song
from pcci.parse.align import align_chords, split_inline_line
from pcci.parse.chords import is_chord_token
from pcci.parse.metadata import extract_metadata
from pcci.parse.sections import (
    CONFIDENCE_FALLBACK,
    CONFIDENCE_FORMATTING,
    CONFIDENCE_LABEL,
    ClassifiedLine,
    LineKind,
    SectionLabel,
    assign_section_numbers,
    classify_document,
)


def analyze(path: Path) -> Song:
    """Read any supported chart and parse it into a ``Song``."""
    return build_song(ingest(path))


def build_song(document: RawDocument) -> Song:
    """Turn ingested lines into a parsed song."""
    if document.source_format == "chordpro":
        return parse_chordpro(document)

    classified = classify_document(document)
    # Only *labelled* headers block a line from being the title. A line promoted to a
    # header purely because it is bold and short is exactly what a song title looks
    # like, and the reference charts open with one.
    labelled = {
        item.index
        for item in classified
        if item.kind is LineKind.HEADER
        and item.label is not None
        and item.label.confidence >= CONFIDENCE_LABEL
    }
    metadata = extract_metadata(document, header_indices=labelled)

    usable = [item for item in classified if item.index not in metadata.consumed_indices]
    sections = _build_sections(usable)
    if not sections:
        sections = _fallback_sections(usable)
    sections = [section for section in sections if section.lines]
    _prepend_title_line_chords(sections, metadata.title_chords)

    if not sections:
        raise NoSectionsDetectedError(
            f"No song sections could be found in {document.source_path.name}.",
            "every detection route produced zero sections",
            context={"path": str(document.source_path)},
        )

    assign_section_numbers(sections)

    warnings = list(document.warnings) + metadata.warnings
    unrecognised = _unrecognised_chords(sections)
    if unrecognised:
        # Kept, not corrected. A chart that says "Dmd/E" has a typo in it and the band
        # can see what was written; guessing at what was meant would be worse, and
        # calling it a lyric would put it on the audience screen.
        warnings.append(
            "These are not chords pcci recognises, and were kept exactly as the chart "
            "wrote them: " + ", ".join(unrecognised) + "."
        )
    low_confidence = [s.label for s in sections if s.confidence < 0.9]
    if low_confidence:
        warnings.append(
            "These sections were guessed rather than read from a label: "
            + ", ".join(low_confidence)
            + ". Check them before exporting."
        )

    return Song(
        title=metadata.title,
        artist=metadata.artist,
        ccli_number=metadata.ccli_number,
        copyright=metadata.copyright,
        key=metadata.key,
        tempo=metadata.tempo,
        sections=sections,
        warnings=warnings,
        source_path=document.source_path,
        source_format=document.source_format,
    )


def _unrecognised_chords(sections: list[Section]) -> list[str]:
    """Chord tokens that were kept on a chord line without parsing as chords."""
    found = {
        placement.raw
        for section in sections
        for line in section.lines
        for placement in line.chords
        if not is_chord_token(placement.raw)
    }
    return sorted(found)


def _prepend_title_line_chords(sections: list[Section], chord_text: str) -> None:
    """Keep the chords some charts type next to the song title.

    ``IN THE RIVER      A   F#m   C#m   E`` is a title and an intro. The title goes to
    the presentation name; without this the intro would simply vanish. It only applies
    when the chart has no intro of its own, and it is marked as a guess.
    """
    if not chord_text:
        return
    if any(section.type is SectionType.INTRO for section in sections):
        return
    chords = align_chords(PositionedLine(text=chord_text), None)
    if len(chords) < 2:
        return
    sections.insert(
        0,
        Section(
            type=SectionType.INTRO,
            raw_label=chord_text,
            confidence=CONFIDENCE_FORMATTING,
            lines=[Line(chords=chords)],
        ),
    )


def _new_section(label: SectionLabel) -> Section:
    return Section(
        type=label.type,
        number=label.number,
        variant=label.variant,
        raw_label=label.raw_label,
        confidence=label.confidence,
    )


def _build_sections(classified: list[ClassifiedLine]) -> list[Section]:
    """Split at headers and fill each section with paired chord/lyric lines."""
    sections: list[Section] = []
    current: Section | None = None
    buffer: list[ClassifiedLine] = []

    def flush() -> None:
        nonlocal buffer
        if current is not None and buffer:
            current.lines.extend(_pair_lines(buffer))
        buffer = []

    for item in classified:
        if item.kind is LineKind.HEADER and item.label is not None:
            flush()
            current = _new_section(item.label)
            sections.append(current)
            continue
        if current is None:
            continue
        buffer.append(item)
    flush()
    return sections


def _fallback_sections(classified: list[ClassifiedLine]) -> list[Section]:
    """Last resort: blank-line stanzas.

    The first stanza becomes an Intro only if it is chords with no words; otherwise
    stanzas are Verse 1, Verse 2, … at low confidence so the UI flags them.
    """
    stanzas: list[list[ClassifiedLine]] = []
    current: list[ClassifiedLine] = []
    for item in classified:
        if item.kind is LineKind.BLANK:
            if current:
                stanzas.append(current)
                current = []
            continue
        current.append(item)
    if current:
        stanzas.append(current)

    sections: list[Section] = []
    for position, stanza in enumerate(stanzas):
        lines = _pair_lines(stanza)
        if not lines:
            continue
        instrumental = all(not line.lyrics for line in lines)
        if position == 0 and instrumental:
            section_type = SectionType.INTRO
        elif instrumental:
            section_type = SectionType.INSTRUMENTAL
        else:
            section_type = SectionType.VERSE
        section = Section(
            type=section_type,
            raw_label="",
            confidence=CONFIDENCE_FALLBACK,
            lines=lines,
        )
        sections.append(section)
    return sections


def _pair_lines(items: list[ClassifiedLine]) -> list[Line]:
    """Pair each chord line with the lyric beneath it."""
    lines: list[Line] = []
    pending_annotations: list[str] = []
    index = 0

    def attach_annotations(line: Line) -> Line:
        if pending_annotations:
            existing = [line.annotation] if line.annotation else []
            line = Line(
                lyrics=line.lyrics,
                chords=line.chords,
                annotation=" / ".join([*existing, *pending_annotations]),
            )
            pending_annotations.clear()
        return line

    while index < len(items):
        item = items[index]
        if item.kind is LineKind.BLANK:
            index += 1
            continue

        if item.kind is LineKind.ANNOTATION:
            if lines:
                lines[-1] = _with_annotation(lines[-1], item.annotation)
            else:
                pending_annotations.append(item.annotation)
            index += 1
            continue

        if item.kind is LineKind.CHORD:
            inline = split_inline_line(item.line)
            if inline is not None:
                lyric_text, chords = inline
                lines.append(attach_annotations(Line(lyrics=lyric_text, chords=chords)))
                index += 1
                continue
            lyric_item = _next_content(items, index + 1)
            if lyric_item is not None and lyric_item.kind is LineKind.LYRIC:
                offset = _lyric_offset(lyric_item)
                lyric_line = PositionedLine(
                    text=lyric_item.lyric_text or lyric_item.line.text.strip(),
                    char_x=_shifted_char_x(lyric_item),
                )
                chords = align_chords(item.line, lyric_line, lyric_offset=offset)
                line = Line(
                    lyrics=lyric_line.text,
                    chords=chords,
                    annotation=lyric_item.annotation or None,
                )
                lines.append(attach_annotations(line))
                index = items.index(lyric_item) + 1
                continue
            chords = align_chords(item.line, None)
            lines.append(attach_annotations(Line(chords=chords)))
            index += 1
            continue

        text = item.lyric_text or item.line.text.strip()
        if text:
            lines.append(attach_annotations(Line(lyrics=text, annotation=item.annotation or None)))
        index += 1

    if pending_annotations and lines:
        lines[-1] = _with_annotation(lines[-1], " / ".join(pending_annotations))
    elif pending_annotations:
        lines.append(Line(annotation=" / ".join(pending_annotations)))
    return lines


def _with_annotation(line: Line, annotation: str) -> Line:
    joined = " / ".join(filter(None, [line.annotation, annotation]))
    return Line(lyrics=line.lyrics, chords=line.chords, annotation=joined or None)


def _next_content(items: list[ClassifiedLine], start: int) -> ClassifiedLine | None:
    for item in items[start:]:
        if item.kind is not LineKind.BLANK:
            return item
    return None


def _lyric_offset(item: ClassifiedLine) -> int:
    """How many characters were trimmed from the front of this line's lyric.

    Every chord column on the line above is measured from the same left edge, so this
    is what has to come off them before they mean anything as an index into the lyric.
    """
    original = item.line.text
    kept = item.lyric_text or original.strip()
    if not kept or kept not in original:
        return 0
    return original.index(kept)


def _shifted_char_x(item: ClassifiedLine) -> list[float]:
    """Character positions for the lyric text after leading whitespace was stripped."""
    if not item.line.char_x:
        return []
    kept = item.lyric_text or item.line.text.strip()
    offset = _lyric_offset(item)
    return item.line.char_x[offset : offset + len(kept)]
