"""ChordPro: the clean-room path.

ChordPro states its structure explicitly — ``{start_of_verse}``, ``[C]`` — so this
ingester never guesses. It is also the reference implementation for what the rest of
the pipeline is trying to reconstruct from visual layout, which makes it the best test
bed in the project.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

from pcci.errors import UnsupportedFormatError
from pcci.ingest.base import build_document, read_text, register, split_lines
from pcci.ir import (
    ChordPlacement,
    Line,
    PositionedLine,
    RawDocument,
    Section,
    SectionType,
    Song,
    SourceFormat,
)
from pcci.parse.chords import parse_chord
from pcci.parse.sections import (
    CONFIDENCE_DIRECTIVE,
    CONFIDENCE_FALLBACK,
    assign_section_numbers,
    parse_section_label,
)

_DIRECTIVE_RE: Final[re.Pattern[str]] = re.compile(r"^\s*\{\s*([^:}]+?)\s*(?::\s*(.*?))?\s*\}\s*$")
_CHORD_RE: Final[re.Pattern[str]] = re.compile(r"\[([^\]]*)\]")

_ENVIRONMENT_STARTS: Final[dict[str, SectionType]] = {
    "start_of_verse": SectionType.VERSE,
    "sov": SectionType.VERSE,
    "start_of_chorus": SectionType.CHORUS,
    "soc": SectionType.CHORUS,
    "start_of_bridge": SectionType.BRIDGE,
    "sob": SectionType.BRIDGE,
    "start_of_part": SectionType.MISC,
    "sop": SectionType.MISC,
    "start_of_tab": SectionType.INSTRUMENTAL,
    "sot": SectionType.INSTRUMENTAL,
    "start_of_grid": SectionType.INSTRUMENTAL,
    "sog": SectionType.INSTRUMENTAL,
}

_ENVIRONMENT_ENDS: Final[frozenset[str]] = frozenset(
    {
        "end_of_verse",
        "eov",
        "end_of_chorus",
        "eoc",
        "end_of_bridge",
        "eob",
        "end_of_part",
        "eop",
        "end_of_tab",
        "eot",
        "end_of_grid",
        "eog",
    }
)

_TITLE_KEYS: Final[frozenset[str]] = frozenset({"title", "t"})
_ARTIST_KEYS: Final[frozenset[str]] = frozenset({"artist", "composer", "subtitle", "st"})
_KEY_KEYS: Final[frozenset[str]] = frozenset({"key"})
_TEMPO_KEYS: Final[frozenset[str]] = frozenset({"tempo", "bpm"})
_CCLI_KEYS: Final[frozenset[str]] = frozenset({"ccli", "ccli_song_id", "songid"})
_COPYRIGHT_KEYS: Final[frozenset[str]] = frozenset({"copyright", "footer"})
_COMMENT_KEYS: Final[frozenset[str]] = frozenset({"comment", "c", "ci", "cf", "comment_italic"})


class ChordProIngester:
    """Reads ``.cho``/``.chopro``/``.chordpro``/``.crd``/``.pro`` ChordPro text."""

    extensions: tuple[str, ...] = (".cho", ".chopro", ".chordpro", ".crd", ".pro")
    source_format: SourceFormat = "chordpro"

    def load(self, path: Path) -> RawDocument:
        _reject_propresenter_binary(path)
        text, warnings = read_text(path)
        lines = [
            PositionedLine(text=line, y=float(index), page=1)
            for index, line in enumerate(split_lines(text))
        ]
        return build_document(
            path,
            "chordpro",
            lines,
            monospace=True,
            warnings=warnings,
        )


def _reject_propresenter_binary(path: Path) -> None:
    """``.pro`` is ChordPro to some tools and ProPresenter to others. Tell them apart.

    A ProPresenter presentation starts with field 1 (``application_info``) as a
    length-delimited message: byte ``0x0A``. No ChordPro file starts that way.
    """
    if path.suffix.lower() != ".pro":
        return
    try:
        head = path.read_bytes()[:1]
    except OSError:
        return
    if head == b"\x0a":
        raise UnsupportedFormatError(
            f"{path.name} is a ProPresenter presentation, not a ChordPro chart. "
            "pcci creates .pro files; it does not read them yet.",
            "file begins with protobuf field 1, wire type 2",
            context={"path": str(path)},
        )


def _split_chords(text: str) -> tuple[str, list[ChordPlacement]]:
    """Strip ``[C]`` markers out of a line, recording where each one landed."""
    lyrics: list[str] = []
    placements: list[ChordPlacement] = []
    position = 0
    for match in _CHORD_RE.finditer(text):
        lyrics.append(text[position : match.start()])
        token = match.group(1).strip()
        if token:
            chord = parse_chord(token)
            placements.append(
                ChordPlacement(
                    chord=chord.normalised if chord else token,
                    char_index=sum(len(part) for part in lyrics),
                    raw=token,
                )
            )
        position = match.end()
    lyrics.append(text[position:])
    return "".join(lyrics), placements


def parse_chordpro(document: RawDocument) -> Song:
    """Turn a ChordPro ``RawDocument`` into a ``Song``. No heuristics involved."""
    metadata: dict[str, str] = {}
    sections: list[Section] = []
    warnings: list[str] = list(document.warnings)
    current: Section | None = None

    pending_annotations: list[str] = []

    def section_for(
        section_type: SectionType,
        label: str,
        confidence: float,
        number: int | None = None,
        variant: str = "",
    ) -> Section:
        nonlocal current
        current = Section(
            type=section_type,
            number=number,
            variant=variant,
            raw_label=label,
            confidence=confidence,
        )
        while pending_annotations:
            current.lines.append(Line(annotation=pending_annotations.pop(0)))
        sections.append(current)
        return current

    for positioned in document.lines:
        raw_line = positioned.text
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            continue

        directive = _DIRECTIVE_RE.match(raw_line)
        if directive:
            name = directive.group(1).strip().lower().replace("-", "_")
            value = (directive.group(2) or "").strip()

            if name in _ENVIRONMENT_STARTS:
                label = value or name.replace("start_of_", "").replace("so", "")
                parsed = parse_section_label(value) if value else None
                if parsed is not None:
                    section_for(
                        parsed.type, value, CONFIDENCE_DIRECTIVE, parsed.number, parsed.variant
                    )
                else:
                    section_for(_ENVIRONMENT_STARTS[name], label, CONFIDENCE_DIRECTIVE)
                continue
            if name in _ENVIRONMENT_ENDS:
                current = None
                continue
            if name in _TITLE_KEYS:
                metadata["title"] = value
                continue
            if name in _ARTIST_KEYS:
                metadata.setdefault("artist", value)
                continue
            if name in _KEY_KEYS:
                metadata["key"] = value
                continue
            if name in _TEMPO_KEYS:
                metadata["tempo"] = value
                continue
            if name in _CCLI_KEYS:
                metadata["ccli"] = value
                continue
            if name in _COPYRIGHT_KEYS:
                metadata["copyright"] = value
                continue
            if name in _COMMENT_KEYS:
                parsed = parse_section_label(value)
                if parsed is not None:
                    section_for(
                        parsed.type, value, parsed.confidence, parsed.number, parsed.variant
                    )
                elif value:
                    # An annotation outside any environment belongs with the section it
                    # follows ("Hold G X 8 BARS" after a verse), not in a section of
                    # its own. Before the first section, hold it until one opens.
                    target = current or (sections[-1] if sections else None)
                    if target is None:
                        pending_annotations.append(value)
                    else:
                        target.lines.append(Line(annotation=value))
                continue
            # Anything else (define, capo, columns, x_ extensions) is not ours to use.
            continue

        if not stripped:
            continue

        # A bare section header inside a ChordPro file: some exporters write them.
        label = parse_section_label(stripped)
        if label is not None and "[" not in stripped:
            section_for(label.type, label.raw_label, label.confidence, label.number, label.variant)
            continue

        lyrics, placements = _split_chords(raw_line)
        lyrics = lyrics.strip()
        if current is None:
            # Content before any environment directive. Treat it the way the heuristic
            # path treats an unlabelled stanza rather than inventing a "Misc" group.
            current = section_for(SectionType.VERSE, "", CONFIDENCE_FALLBACK)
        if not lyrics and placements:
            current.lines.append(
                Line(
                    chords=[
                        ChordPlacement(chord=p.chord, char_index=0, raw=p.raw) for p in placements
                    ]
                )
            )
        elif lyrics:
            leading = len(raw_line) - len(raw_line.lstrip())
            adjusted = [
                ChordPlacement(
                    chord=placement.chord,
                    char_index=min(max(placement.char_index - leading, 0), len(lyrics)),
                    raw=placement.raw,
                )
                for placement in placements
            ]
            current.lines.append(Line(lyrics=lyrics, chords=adjusted))

    sections = [section for section in sections if section.lines]
    assign_section_numbers(sections)

    title = metadata.get("title") or document.source_path.stem
    if not metadata.get("title"):
        warnings.append("No {title} directive; the file name was used as the song title.")

    tempo: int | None = None
    if metadata.get("tempo"):
        digits = re.search(r"\d+", metadata["tempo"])
        if digits:
            tempo = int(digits.group())

    return Song(
        title=title,
        artist=metadata.get("artist") or None,
        ccli_number=metadata.get("ccli") or None,
        copyright=metadata.get("copyright") or None,
        key=metadata.get("key") or None,
        tempo=tempo,
        sections=sections,
        warnings=warnings,
        source_path=document.source_path,
        source_format="chordpro",
    )


CHORDPRO_INGESTER = register(ChordProIngester())
