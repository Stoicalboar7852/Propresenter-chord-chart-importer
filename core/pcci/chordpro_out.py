"""Writing a ``Song`` back out as ChordPro.

Useful in three places: as a sidecar next to the ``.pro``, as the source for the chord
chart pages, and as a debugging aid — a ChordPro round-trip through ``ingest`` and
``parse_chordpro`` should return the song it started from.
"""

from __future__ import annotations

from pcci.ir import Line, Section, SectionType, Song

_ENVIRONMENTS: dict[SectionType, str] = {
    SectionType.VERSE: "verse",
    SectionType.CHORUS: "chorus",
    SectionType.BRIDGE: "bridge",
}


def line_to_chordpro(line: Line) -> str:
    """Put ``[C]`` markers back into a lyric at their character positions."""
    if not line.lyrics:
        return " ".join(f"[{placement.chord}]" for placement in line.chords)
    pieces: list[str] = []
    position = 0
    for placement in sorted(line.chords, key=lambda p: p.char_index):
        index = min(max(placement.char_index, 0), len(line.lyrics))
        pieces.append(line.lyrics[position:index])
        pieces.append(f"[{placement.chord}]")
        position = index
    pieces.append(line.lyrics[position:])
    return "".join(pieces)


def section_to_chordpro(section: Section) -> list[str]:
    environment = _ENVIRONMENTS.get(section.type)
    lines: list[str] = []
    if environment:
        lines.append(f"{{start_of_{environment}: {section.label}}}")
    else:
        lines.append(f"{{comment: {section.label}}}")
    for line in section.lines:
        if line.annotation and not line.lyrics and not line.chords:
            lines.append(f"{{comment: {line.annotation}}}")
            continue
        lines.append(line_to_chordpro(line))
        if line.annotation:
            lines.append(f"{{comment: {line.annotation}}}")
    if environment:
        lines.append(f"{{end_of_{environment}}}")
    lines.append("")
    return lines


def song_to_chordpro(song: Song) -> str:
    """The whole song as ChordPro text."""
    lines: list[str] = [f"{{title: {song.title}}}"]
    if song.artist:
        lines.append(f"{{artist: {song.artist}}}")
    if song.key:
        lines.append(f"{{key: {song.key}}}")
    if song.tempo:
        lines.append(f"{{tempo: {song.tempo}}}")
    if song.ccli_number:
        lines.append(f"{{ccli: {song.ccli_number}}}")
    if song.copyright:
        lines.append(f"{{copyright: {song.copyright}}}")
    lines.append("")
    for section in song.sections:
        lines.extend(section_to_chordpro(section))
    return "\n".join(lines).rstrip() + "\n"
