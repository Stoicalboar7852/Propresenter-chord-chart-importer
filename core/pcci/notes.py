"""Rendering chords over (or under) lyrics as a monospaced block.

This is the text an operator reads on a stage screen, and the same text that gets
rasterised into a chord-chart page. It is deliberately plain: a chord row and a lyric
row, aligned by character, exactly like the charts musicians already read.
"""

from __future__ import annotations

from pcci.config import ChordPlacementStyle
from pcci.ir import Line, Section, Song


def chord_row(line: Line) -> str:
    """The chord row for a line: each chord at its character index.

    Two chords that resolve to the same index are kept in source order, separated by a
    single space, rather than one overwriting the other.
    """
    row = ""
    for placement in line.chords:
        target = placement.char_index
        if target < len(row):
            target = len(row) + 1
        row = row.ljust(target) + placement.chord
    return row


def render_line(line: Line, placement: ChordPlacementStyle) -> list[str]:
    """One song line as one or two rows of text.

    In ``CHORDS_ONLY`` mode a line with no chords still produces an empty row, so row
    *n* of the block is always chord row *n* of the slide.
    """
    rows: list[str] = []
    chords = chord_row(line)
    if not placement.includes_lyrics:
        rows = [chords]
    elif line.lyrics:
        rows = (
            [chords, line.lyrics]
            if placement is ChordPlacementStyle.ABOVE
            else [line.lyrics, chords]
        )
        if not chords.strip():
            rows = [line.lyrics]
    elif chords.strip():
        rows = [chords]
    if line.annotation:
        rows.append(f"({line.annotation})")
    return rows


#: Separates one lyric line's chords from the next on an inline row.
#:
#: Plain spaces, deliberately. A middle dot reads better but has to travel through RTF
#: as a \uNNNN escape, and if the reader that renders it disagrees the operator gets a
#: literal "?" on the stage screen mid-song. A pipe would render, but a pipe means a
#: bar line on a chord chart and these groups are lyric lines, not bars. The notes use
#: a fixed-pitch font, so four spaces against one is an obvious gap.
INLINE_SEPARATOR = "    "


def render_inline(lines: list[Line]) -> str:
    """Every chord on the slide in one horizontal row.

    A wider gap separates one lyric line's chords from the next, so an operator can
    still see which chords belong together, and a line with no chords contributes
    nothing rather than leaving a hole in the row.
    """
    groups: list[str] = []
    annotations: list[str] = []
    for line in lines:
        chords = " ".join(placement.chord for placement in line.chords)
        if chords:
            groups.append(chords)
        if line.annotation:
            annotations.append(line.annotation)
    row = INLINE_SEPARATOR.join(groups)
    if annotations:
        note = " / ".join(annotations)
        row = f"{row}{INLINE_SEPARATOR}({note})" if row else f"({note})"
    return row


def render_lines(
    lines: list[Line],
    placement: ChordPlacementStyle = ChordPlacementStyle.CHORDS_ONLY,
) -> str:
    """A block of chord/lyric rows for a slide."""
    if placement is ChordPlacementStyle.CHORDS_INLINE:
        return render_inline(lines)
    rows: list[str] = []
    for line in lines:
        rows.extend(render_line(line, placement))
    return "\n".join(rows).rstrip()


def render_section(
    section: Section,
    placement: ChordPlacementStyle = ChordPlacementStyle.ABOVE,
) -> str:
    """A whole section, with its label as a heading."""
    body = render_lines(section.lines, placement)
    return f"[{section.label}]\n{body}" if body else f"[{section.label}]"


def render_song(
    song: Song,
    placement: ChordPlacementStyle = ChordPlacementStyle.ABOVE,
) -> str:
    """The whole chart as plain text: what gets rasterised into chart pages."""
    parts: list[str] = [song.title]
    credits = " · ".join(filter(None, [song.artist, song.key and f"Key of {song.key}"]))
    if credits:
        parts.append(credits)
    parts.append("")
    for section in song.sections:
        parts.append(render_section(section, placement))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"
