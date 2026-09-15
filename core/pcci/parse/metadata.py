"""Title, artist, CCLI number, copyright, key and tempo.

Chord charts carry this information in whatever shape the person who typed them felt
like. The rules here are ordered by how much they can be trusted, and every one of them
falls back to something rather than failing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Final

from pcci.ir import RawDocument
from pcci.parse.chords import LineClass, classify_line, is_chord_token, tokenise

_CCLI_RE: Final[re.Pattern[str]] = re.compile(
    r"CCLI\s*(?:Song)?\s*(?:#|No\.?|Number)?\s*[:\-]?\s*(\d{4,9})", re.IGNORECASE
)
_COPYRIGHT_RE: Final[re.Pattern[str]] = re.compile(r"(?:©|\(c\)|copyright)\s*(.+)", re.IGNORECASE)
_KEY_RE: Final[re.Pattern[str]] = re.compile(
    r"\bkey\s*(?:of)?\s*[:\-]?\s*([A-G][#b]?m?(?:aj|in)?)\b", re.IGNORECASE
)
_TEMPO_RE: Final[re.Pattern[str]] = re.compile(
    r"\b(?:bpm|tempo)\s*[:\-]?\s*(\d{2,3})\b|\b(\d{2,3})\s*bpm\b", re.IGNORECASE
)
_TITLE_LABEL_RE: Final[re.Pattern[str]] = re.compile(r"^\s*title\s*[:\-]\s*(.+)$", re.IGNORECASE)
_ARTIST_LABEL_RE: Final[re.Pattern[str]] = re.compile(
    r"^\s*(?:artist|by|writer|writers|author)\s*[:\-]\s*(.+)$", re.IGNORECASE
)
#: "Watch Your Mouth By: Josiah Queen" — the credit sits on the title line.
_INLINE_BY_RE: Final[re.Pattern[str]] = re.compile(r"^(.+?)\s+by\s*[:\-]\s*(.+)$", re.IGNORECASE)
#: "WASHED- ELEVATION" and "The Prodigal  Josiah Queen".
_INLINE_DASH_RE: Final[re.Pattern[str]] = re.compile(r"^(.+?)\s*[\u2013\u2014-]\s+(.+)$")
_INLINE_GAP_RE: Final[re.Pattern[str]] = re.compile(r"^(.+?)\s{2,}(.+)$")

#: Minimum gap that separates a title from a chord run typed on the same line.
TITLE_CHORD_GAP: Final[int] = 3

#: How far into the document metadata is worth looking for.
HEADER_SCAN_LINES: Final[int] = 12


@dataclass(slots=True)
class Metadata:
    """Everything scraped from the top of a chart."""

    title: str = ""
    artist: str | None = None
    ccli_number: str | None = None
    copyright: str | None = None
    key: str | None = None
    tempo: int | None = None
    title_chords: str = ""
    consumed_indices: set[int] = field(default_factory=set)
    warnings: list[str] = field(default_factory=list)


def extract_metadata(document: RawDocument, *, header_indices: set[int]) -> Metadata:
    """Scrape metadata, recording which line indices it used up.

    ``header_indices`` are lines already known to be section headers; the title is
    never one of those.
    """
    metadata = Metadata()

    for index, line in enumerate(document.lines):
        text = line.text.strip()
        if not text:
            continue
        if match := _CCLI_RE.search(text):
            metadata.ccli_number = metadata.ccli_number or match.group(1)
            metadata.consumed_indices.add(index)
        if match := _COPYRIGHT_RE.search(text):
            metadata.copyright = metadata.copyright or match.group(1).strip()
            metadata.consumed_indices.add(index)
        if match := _KEY_RE.search(text):
            metadata.key = metadata.key or match.group(1)
            metadata.consumed_indices.add(index)
        if match := _TEMPO_RE.search(text):
            metadata.tempo = metadata.tempo or int(match.group(1) or match.group(2))
            metadata.consumed_indices.add(index)
        if match := _TITLE_LABEL_RE.match(text):
            metadata.title = metadata.title or match.group(1).strip()
            metadata.consumed_indices.add(index)
        if match := _ARTIST_LABEL_RE.match(text):
            metadata.artist = metadata.artist or match.group(1).strip()
            metadata.consumed_indices.add(index)

    if not metadata.title:
        _title_from_first_line(document, header_indices, metadata)

    if not metadata.title:
        metadata.title = document.source_path.stem
        metadata.warnings.append("No title was found in the document, so the file name was used.")
    return metadata


def split_title_chords(text: str) -> tuple[str, str]:
    """Separate ``IN THE RIVER      A   F#m   C#m   E`` into title and chord run.

    Charts often put the intro chords on the title line. Left alone they end up in the
    presentation's name.
    """
    tokens = tokenise(text)
    if len(tokens) < 2:
        return text, ""
    first_chord: int | None = None
    for position in range(len(tokens) - 1, -1, -1):
        token, column = tokens[position]
        if not is_chord_token(token):
            break
        previous_token, previous_column = tokens[position - 1] if position else ("", 0)
        gap = column - (previous_column + len(previous_token))
        if position and gap >= TITLE_CHORD_GAP and not is_chord_token(previous_token):
            first_chord = position
            break
        first_chord = position
    if first_chord is None or first_chord == 0:
        return text, ""
    boundary = tokens[first_chord][1]
    title = text[:boundary].strip()
    chords = text[boundary:].strip()
    if not title or len(chords.split()) < 2:
        return text, ""
    return title, chords


def split_title_artist(text: str) -> tuple[str, str | None]:
    """Separate a credit typed on the title line."""
    for pattern in (_INLINE_BY_RE, _INLINE_GAP_RE, _INLINE_DASH_RE):
        match = pattern.match(text)
        if not match:
            continue
        title, artist = match.group(1).strip(), match.group(2).strip()
        if title and artist and len(artist.split()) <= 6:
            return title, artist
    return text, None


def _title_from_first_line(
    document: RawDocument, header_indices: set[int], metadata: Metadata
) -> None:
    """The first real line of page 1, above every section, that is not a chord line.

    Stopping at the first section header matters: a chart with no title line at all
    should fall back to its file name rather than promote its opening lyric.
    """
    limit = min([*header_indices, HEADER_SCAN_LINES, len(document.lines)])
    for index, line in enumerate(document.lines[:limit]):
        text = line.text.strip()
        if not text or index in metadata.consumed_indices:
            continue
        if line.page != 1 or classify_line(text) is not LineClass.LYRIC:
            continue
        title, chords = split_title_chords(text)
        title, artist = split_title_artist(title)
        metadata.title = title
        metadata.title_chords = chords
        if artist and not metadata.artist:
            metadata.artist = artist
        metadata.consumed_indices.add(index)
        if not metadata.artist:
            _artist_from_next_line(document, index, header_indices, metadata)
        return


def _artist_from_next_line(
    document: RawDocument, title_index: int, header_indices: set[int], metadata: Metadata
) -> None:
    """A short line straight under the title, before any section, is the artist."""
    if metadata.artist:
        return
    for index in range(title_index + 1, min(title_index + 3, len(document.lines))):
        text = document.lines[index].text.strip()
        if not text:
            return
        if index in header_indices or index in metadata.consumed_indices:
            return
        if classify_line(text) is not LineClass.LYRIC or len(text) > 60:
            return
        # An artist credit reads as a name, not as a sentence of lyrics.
        if len(text.split()) <= 6 and (text.isupper() or "&" in text or "," in text):
            metadata.artist = text
            metadata.consumed_indices.add(index)
        return
