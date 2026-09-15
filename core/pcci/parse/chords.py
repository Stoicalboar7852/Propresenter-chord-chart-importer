"""Chord token grammar, normalisation, and chord-line classification.

The grammar is deliberately strict: a token is a chord only if the whole token is
consumed by it. That matters because the alternative — matching a prefix — turns
half the English language into chords ("Ate" would match "A").

Classification of a whole *line* as a chord line is a separate, softer question. It
uses the proportion of chord-shaped tokens, their length, and a guard list of words
that are simultaneously valid chords and ordinary English. Context (what the
surrounding lines look like) resolves the rest, in ``sections.py``.
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

# Unicode accidentals and look-alike characters that appear in charts copied from the web.
UNICODE_ACCIDENTALS: Final[dict[str, str]] = {
    "♭": "b",  # ♭
    "♯": "#",  # ♯
    "ᴒb": "bb",  # 𝄫
    "ᴒa": "##",  # 𝄪
    "–": "-",  # en dash
    "—": "-",  # em dash
    "−": "-",  # minus sign
}

ROOTS: Final[frozenset[str]] = frozenset("ABCDEFG")
#: Nashville number charts write the degree instead of the letter: "1 5/7 6m 4".
NASHVILLE_ROOTS: Final[frozenset[str]] = frozenset("1234567")

# Qualities, longest first so that "maj" wins over "m" and "min" over "m".
_QUALITY_ALIASES: Final[list[tuple[str, str]]] = [
    ("maj", "maj"),
    ("Maj", "maj"),
    ("MAJ", "maj"),
    ("min", "m"),
    ("Min", "m"),
    ("MIN", "m"),
    ("dim", "dim"),
    ("Dim", "dim"),
    ("aug", "aug"),
    ("Aug", "aug"),
    ("sus", "sus"),  # handled as an alteration, listed here so "Asus" parses
    ("add", "add"),
    ("M", "maj"),
    ("m", "m"),
    ("o", "dim"),
    ("°", "dim"),  # °
    ("ø", "m7b5"),  # ø, half-diminished
    ("+", "aug"),
    ("-", "m"),
]

_EXTENSIONS: Final[tuple[str, ...]] = ("13", "11", "9", "7", "6", "5", "4", "2")

_ALTERATIONS: Final[tuple[str, ...]] = (
    "sus2",
    "sus4",
    "sus",
    "add9",
    "add11",
    "add13",
    "add2",
    "add4",
    "b5",
    "#5",
    "b9",
    "#9",
    "#11",
    "b13",
    "b6",
)

# Tokens that are legitimate on a chord line without being chords.
NON_CHORD_TOKENS: Final[frozenset[str]] = frozenset(
    {"N.C.", "NC", "n.c.", "%", "|", "||", ":||", "||:", "|:", ":|", "-", "/", "//"}
)

_REPEAT_RE: Final[re.Pattern[str]] = re.compile(r"^[xX]\d{1,2}$|^\d{1,2}[xX]$")

# Words that parse as chords but are overwhelmingly English in a lyric line.
AMBIGUOUS_WORDS: Final[frozenset[str]] = frozenset(
    {"A", "a", "Am", "am", "Be", "be", "Do", "do", "Dad", "dad", "Add", "add", "Bad", "bad"}
)


@dataclass(frozen=True, slots=True)
class Chord:
    """A parsed chord. ``raw`` keeps the spelling exactly as the chart had it."""

    root: str
    accidental: str = ""
    quality: str = ""
    extension: str = ""
    alterations: tuple[str, ...] = ()
    bass: str = ""
    raw: str = ""
    nashville: bool = False

    @property
    def normalised(self) -> str:
        parts = [self.root, self.accidental, self.quality, self.extension, *self.alterations]
        text = "".join(parts)
        if self.bass:
            text += f"/{self.bass}"
        return text

    def __str__(self) -> str:
        return self.normalised


def normalise_accidentals(text: str) -> str:
    """Replace ♭/♯ and dash look-alikes with their ASCII equivalents."""
    for source, target in UNICODE_ACCIDENTALS.items():
        text = text.replace(source, target)
    return text


def _parse_root(token: str, index: int, *, nashville: bool = False) -> tuple[str, str, int] | None:
    """Read a root note (or a Nashville degree) plus any accidental."""
    allowed = NASHVILLE_ROOTS if nashville else ROOTS
    if index >= len(token) or token[index] not in allowed:
        return None
    root = token[index]
    index += 1
    accidental = ""
    for candidate in ("##", "bb", "#", "b"):
        if token.startswith(candidate, index):
            accidental = candidate
            index += len(candidate)
            break
    return root, accidental, index


def parse_chord(token: str, *, nashville: bool = False) -> Chord | None:
    """Parse one whitespace-delimited token. Returns ``None`` if it is not a chord.

    The whole token must be consumed — a trailing comma or a stray letter means this
    is a word, not a chord. With ``nashville=True`` the root is a scale degree
    (``1``..``7``, optionally preceded by an accidental) instead of a letter.
    """
    if not token:
        return None
    raw = token
    token = normalise_accidentals(token).strip()
    if not token:
        return None

    prefix = ""
    if nashville and token[:1] in ("b", "#"):
        prefix, token = token[0], token[1:]

    parsed_root = _parse_root(token, 0, nashville=nashville)
    if parsed_root is None:
        return None
    root, accidental, index = parsed_root
    root = prefix + root

    quality = ""
    for alias, canonical in _QUALITY_ALIASES:
        if alias in ("sus", "add"):
            continue  # these are alterations; leave them for the alteration pass
        if token.startswith(alias, index):
            quality = canonical
            index += len(alias)
            break

    extension = ""
    for candidate in _EXTENSIONS:
        if token.startswith(candidate, index):
            extension = candidate
            index += len(candidate)
            break

    alterations: list[str] = []
    while index < len(token):
        for candidate in _ALTERATIONS:
            if token.startswith(candidate, index):
                alterations.append(candidate)
                index += len(candidate)
                break
        else:
            break

    # A quality can follow an alteration too, as in "Csus4maj7" or "A7sus4".
    if index < len(token) and not quality:
        for alias, canonical in _QUALITY_ALIASES:
            if alias in ("sus", "add"):
                continue
            if token.startswith(alias, index):
                quality = canonical
                index += len(alias)
                break
        if not extension:
            for candidate in _EXTENSIONS:
                if token.startswith(candidate, index):
                    extension = candidate
                    index += len(candidate)
                    break

    bass = ""
    if index < len(token) and token[index] == "/":
        parsed_bass = _parse_root(token, index + 1, nashville=nashville)
        if parsed_bass is None:
            return None
        bass_root, bass_accidental, index = parsed_bass
        bass = bass_root + bass_accidental

    if index != len(token):
        return None

    return Chord(
        root=root,
        accidental=accidental,
        quality=quality,
        extension=extension,
        alterations=tuple(alterations),
        bass=bass,
        raw=raw,
        nashville=nashville,
    )


def parse_any_chord(token: str) -> Chord | None:
    """Parse a letter chord, falling back to Nashville number notation."""
    return parse_chord(token) or parse_chord(token, nashville=True)


def normalise_chord(token: str) -> str | None:
    """``"CM7"`` -> ``"Cmaj7"``. ``None`` when the token is not a chord."""
    chord = parse_any_chord(token)
    return chord.normalised if chord else None


def is_chord_token(token: str) -> bool:
    """True for a chord, a bar line, ``N.C.``, or a repeat marker such as ``x2``."""
    if not token:
        return False
    stripped = token.strip().strip(",")
    if not stripped:
        return False
    if stripped in NON_CHORD_TOKENS or _REPEAT_RE.match(stripped):
        return True
    return parse_any_chord(stripped) is not None


def tokenise(text: str) -> list[tuple[str, int]]:
    """Split into ``(token, column)`` pairs, keeping the column of each token."""
    return [(match.group(), match.start()) for match in re.finditer(r"\S+", text)]


CHORD_LINE_MIN_RATIO: Final[float] = 0.75
CHORD_LINE_MAX_MEDIAN_LENGTH: Final[int] = 6
INLINE_LYRIC_GAP: Final[int] = 2


class LineClass(StrEnum):
    """What a line looks like on its own, before context is considered."""

    CHORD = "chord"
    AMBIGUOUS = "ambiguous"
    LYRIC = "lyric"
    BLANK = "blank"


def chord_line_score(text: str) -> float:
    """Fraction of tokens on the line that look like chords, 0..1."""
    tokens = [token for token, _ in tokenise(text)]
    if not tokens:
        return 0.0
    return sum(1 for token in tokens if is_chord_token(token)) / len(tokens)


def classify_line(text: str) -> LineClass:
    """Classify a line structurally. Context is somebody else's job.

    ``AMBIGUOUS`` is the important state: a line reading just ``A`` is both a perfectly
    ordinary chord line and an English word. The reference charts are full of the
    former, real lyrics are full of the latter, and only the surrounding lines can
    tell them apart — see ``sections.py``.
    """
    tokens = [token for token, _ in tokenise(text)]
    if not tokens:
        return LineClass.BLANK
    if chord_line_score(text) < CHORD_LINE_MIN_RATIO:
        return LineClass.LYRIC
    if statistics.median(len(token) for token in tokens) > CHORD_LINE_MAX_MEDIAN_LENGTH:
        return LineClass.LYRIC
    if all(token.strip(",") in AMBIGUOUS_WORDS for token in tokens):
        return LineClass.AMBIGUOUS
    return LineClass.CHORD


def looks_like_chord_line(text: str) -> bool:
    """True only for lines that are unambiguously chords."""
    return classify_line(text) is LineClass.CHORD


def find_inline_lyric_start(text: str) -> int | None:
    """Column where a lyric begins on a line that starts with chords.

    Charts written by hand often put both on one line::

        A  Bm    I have decided

    Returns the column of the lyric's first character, or ``None`` when the line is
    not of that shape. The rule is: one or more leading chord tokens, then a gap of at
    least two spaces, then a remainder that is not itself chord-shaped.
    """
    tokens = tokenise(text)
    if len(tokens) < 2:
        return None
    leading = 0
    while leading < len(tokens) and is_chord_token(tokens[leading][0]):
        leading += 1
    if leading == 0 or leading == len(tokens):
        return None

    last_chord_token, last_chord_column = tokens[leading - 1]
    lyric_column = tokens[leading][1]
    if lyric_column - (last_chord_column + len(last_chord_token)) < INLINE_LYRIC_GAP:
        return None

    remainder = text[lyric_column:]
    if classify_line(remainder) is LineClass.CHORD:
        return None
    return lyric_column
