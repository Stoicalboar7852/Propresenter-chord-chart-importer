"""Putting chords where they belong in the lyric beneath them.

Two sources of truth, in order of preference:

* **Real coordinates.** When the ingester supplied ``char_x`` (PDFs do), the chord's x
  position is compared against the lyric's actual glyph positions. Font, kerning and
  proportional spacing stop mattering.
* **Columns.** In a monospaced source the column index *is* the position, so the
  chord's column is the lyric's character index.

Both clamp to the lyric's length: a chord hanging past the end of a line anchors to the
final character rather than being dropped.
"""

from __future__ import annotations

import bisect

from pcci.ir import ChordPlacement, PositionedLine
from pcci.parse.chords import find_inline_lyric_start, parse_any_chord, tokenise


def _placement(token: str, char_index: int) -> ChordPlacement:
    chord = parse_any_chord(token)
    return ChordPlacement(
        chord=chord.normalised if chord else token,
        char_index=char_index,
        raw=token,
    )


def char_index_for_x(lyric: PositionedLine, x: float) -> int:
    """Index of the lyric character sitting at or before ``x``."""
    if not lyric.char_x:
        return 0
    # A chord positioned past the end of the line anchors at len(text), exactly as the
    # monospaced path clamps an over-long column. Without this, positional and column
    # alignment disagree by one character on every chord that hangs off the end.
    if x > lyric.char_x[-1]:
        return len(lyric.text)
    index = bisect.bisect_right(lyric.char_x, x + 0.01) - 1
    return max(0, min(index, len(lyric.text)))


def align_chords(
    chord_line: PositionedLine,
    lyric_line: PositionedLine | None,
    *,
    monospace: bool,
) -> list[ChordPlacement]:
    """Anchor every chord on ``chord_line`` to a character of ``lyric_line``.

    With no lyric line the chords describe an instrumental bar, and the spec is
    explicit: they all sit at index 0 and the line carries no lyrics.
    """
    tokens = tokenise(chord_line.text)
    if lyric_line is None or not lyric_line.text:
        return [_placement(token, 0) for token, _ in tokens]

    limit = len(lyric_line.text)
    placements: list[ChordPlacement] = []
    use_positions = bool(chord_line.char_x and lyric_line.char_x)

    for token, column in tokens:
        if use_positions and column < len(chord_line.char_x):
            index = char_index_for_x(lyric_line, chord_line.char_x[column])
        elif monospace or not chord_line.char_x:
            index = min(column, limit)
        else:
            index = min(column, limit)
        placements.append(_placement(token, min(max(index, 0), limit)))
    return placements


def split_inline_line(line: PositionedLine) -> tuple[str, list[ChordPlacement]] | None:
    """Handle a line that carries its chords and its lyric together.

    ``A  Bm    I have decided`` becomes the lyric ``I have decided`` with A and Bm
    anchored at its start, in source order.
    """
    start = find_inline_lyric_start(line.text)
    if start is None:
        return None
    lyric = line.text[start:].strip()
    chords = [
        _placement(token, 0) for token, column in tokenise(line.text[:start]) if column < start
    ]
    if not lyric or not chords:
        return None
    return lyric, chords
