"""Section labels and section detection.

This module owns two things:

``parse_section_label``
    Given a candidate line, decide whether it is a section header and what section it
    names. Used by every path, including ChordPro, so that ``[Verse 1]``, ``V1``,
    ``{start_of_verse: Verse 1}`` and **VERSE 1** all land on the same ``SectionType``.

``detect_sections``
    The heuristic ladder for sources with no explicit structure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

from pcci.ir import Section, SectionType

#: Confidence attached to each detection route, per the spec's priority ladder.
CONFIDENCE_DIRECTIVE: Final[float] = 1.0
CONFIDENCE_LABEL: Final[float] = 0.95
CONFIDENCE_FORMATTING: Final[float] = 0.7
CONFIDENCE_FALLBACK: Final[float] = 0.3

_TYPE_BY_KEYWORD: Final[dict[str, SectionType]] = {
    "intro": SectionType.INTRO,
    "verse": SectionType.VERSE,
    "prechorus": SectionType.PRE_CHORUS,
    "postchorus": SectionType.POST_CHORUS,
    "chorus": SectionType.CHORUS,
    "bridge": SectionType.BRIDGE,
    "tag": SectionType.TAG,
    "outro": SectionType.OUTRO,
    "ending": SectionType.ENDING,
    "interlude": SectionType.INTERLUDE,
    "instrumental": SectionType.INSTRUMENTAL,
    "refrain": SectionType.REFRAIN,
    "vamp": SectionType.VAMP,
    "turnaround": SectionType.INSTRUMENTAL,
    "coda": SectionType.OUTRO,
    "breakdown": SectionType.BREAKDOWN,
    "hook": SectionType.POST_CHORUS,
    "solo": SectionType.INSTRUMENTAL,
    "reprise": SectionType.MISC,
    "channel": SectionType.MISC,
    "link": SectionType.MISC,
}

#: Short forms that appear as bare labels in hand-written charts.
_TYPE_BY_ABBREVIATION: Final[dict[str, SectionType]] = {
    "v": SectionType.VERSE,
    "c": SectionType.CHORUS,
    "ch": SectionType.CHORUS,
    "pc": SectionType.PRE_CHORUS,
    "prec": SectionType.PRE_CHORUS,
    "b": SectionType.BRIDGE,
    "br": SectionType.BRIDGE,
    "i": SectionType.INTRO,
    "in": SectionType.INTRO,
    "o": SectionType.OUTRO,
    "t": SectionType.TAG,
    "inst": SectionType.INSTRUMENTAL,
    "int": SectionType.INTERLUDE,
}

_LABEL_RE: Final[re.Pattern[str]] = re.compile(
    r"""^\s*
    [\[\(]?\s*
    (?P<word>Intro|Verse|Chorus|Pre[\s\-]?Chorus|Post[\s\-]?Chorus|Bridge|Tag|Outro|
       Ending|Interlude|Instrumental|Refrain|Vamp|Turnaround|Coda|Breakdown|Hook|Solo|
       Reprise|Channel|Link)
    \s*
    (?P<number>[0-9]+[A-Za-z]?|[A-Z])?
    \s*[\]\)]?\s*:?\s*
    (?P<trailer>\(\s*[xX]\s*\d+\s*\)|[xX]\s*\d+)?
    \s*$""",
    re.VERBOSE | re.IGNORECASE,
)

_ABBREVIATION_RE: Final[re.Pattern[str]] = re.compile(
    r"^\s*[\[\(]?\s*(?P<word>[A-Za-z]{1,4})\s*(?P<number>\d{1,2})?\s*[\]\)]?\s*:?\s*$"
)

_TRAILING_REPEAT_RE: Final[re.Pattern[str]] = re.compile(r"\(?\s*[xX]\s*\d+\s*\)?\s*$")


@dataclass(frozen=True, slots=True)
class SectionLabel:
    """What a header line names."""

    type: SectionType
    number: int | None
    raw_label: str
    confidence: float
    repeat: int = 1
    variant: str = ""

    @property
    def is_misc(self) -> bool:
        return self.type is SectionType.MISC


def _variant_from(text: str | None) -> str:
    """The letter half of a label like ``2A``."""
    if not text:
        return ""
    match = re.match(r"\d+([A-Za-z])$", text.strip())
    return match.group(1).upper() if match else ""


def _number_from(text: str | None) -> int | None:
    if not text:
        return None
    digits = re.match(r"\d+", text)
    if digits:
        return int(digits.group())
    # A bare letter suffix: "Verse A" -> 1, "Verse B" -> 2.
    letter = text.strip().upper()
    if len(letter) == 1 and letter.isalpha():
        return ord(letter) - ord("A") + 1
    return None


def _repeat_from(text: str | None) -> int:
    if not text:
        return 1
    digits = re.search(r"\d+", text)
    return int(digits.group()) if digits else 1


def parse_section_label(
    text: str,
    *,
    allow_abbreviations: bool = True,
    allow_bare_words: bool = True,
) -> SectionLabel | None:
    """Parse a line as a section header, or return ``None``.

    ``allow_bare_words`` covers labels with no brackets or colon (a line reading just
    ``Chorus``); ``allow_abbreviations`` covers ``V1``, ``CH``, ``PC``.
    """
    stripped = text.strip()
    if not stripped or len(stripped) > 40:
        return None

    bracketed = stripped.startswith(("[", "(")) or stripped.endswith((":",))
    match = _LABEL_RE.match(stripped)
    if match:
        if not bracketed and not allow_bare_words:
            return None
        word = re.sub(r"[\s\-]", "", match.group("word")).lower()
        section_type = _TYPE_BY_KEYWORD.get(word, SectionType.MISC)
        return SectionLabel(
            type=section_type,
            number=_number_from(match.group("number")),
            raw_label=stripped,
            confidence=CONFIDENCE_LABEL,
            repeat=_repeat_from(match.group("trailer")),
            variant=_variant_from(match.group("number")),
        )

    if allow_abbreviations:
        trailing_repeat = _TRAILING_REPEAT_RE.search(stripped)
        repeat = _repeat_from(trailing_repeat.group()) if trailing_repeat else 1
        core = _TRAILING_REPEAT_RE.sub("", stripped).strip()
        abbreviation = _ABBREVIATION_RE.match(core)
        if abbreviation:
            word = abbreviation.group("word").lower()
            abbreviated_type = _TYPE_BY_ABBREVIATION.get(word)
            if abbreviated_type is not None:
                # "CH" or "PC" on their own are safe: no lyric line looks like that.
                # A bare single letter is not — "I" and "B" are ordinary words — so
                # those need a number or a bracket before we believe them.
                has_marker = core.startswith(("[", "(")) or core.endswith(":")
                if abbreviation.group("number") or has_marker or len(word) > 1:
                    return SectionLabel(
                        type=abbreviated_type,
                        number=_number_from(abbreviation.group("number")),
                        raw_label=stripped,
                        confidence=CONFIDENCE_LABEL if has_marker else CONFIDENCE_FORMATTING,
                        repeat=repeat,
                    )

    # A bracketed label we do not recognise is still a label: keep the user's words.
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1].strip()
        if inner and len(inner) <= 30:
            return SectionLabel(
                type=SectionType.MISC,
                number=None,
                raw_label=inner,
                confidence=CONFIDENCE_LABEL,
                repeat=1,
            )
    return None


def _section_fingerprint(section: Section) -> tuple[str, ...]:
    """Content identity: the lyrics, or the chords when there are none."""
    parts: list[str] = []
    for line in section.lines:
        if line.lyrics:
            parts.append(line.lyrics.casefold())
        elif line.chords:
            parts.append("|".join(chord.chord for chord in line.chords))
        elif line.annotation:
            parts.append(f"!{line.annotation.casefold()}")
    return tuple(parts)


def assign_section_numbers(sections: list[Section]) -> None:
    """Number repeated section types in place, the way ProPresenter groups them.

    Two rules, taken from how the reference presentation is organised:

    * A section whose content matches an earlier section of the same type is the *same*
      section again. It keeps that section's number, so the writer can point both at one
      group preset and let the arrangement repeat it.
    * A section with new content gets the next number for its type — two unnumbered
      verses become Verse 1 and Verse 2.

    A type that occurs exactly once keeps ``number = None`` and shows as plain
    "Chorus", matching how people label charts.
    """
    explicit: dict[SectionType, set[int]] = {}
    for section in sections:
        if section.number is not None:
            explicit.setdefault(section.type, set()).add(section.number)

    # Count *distinct* contents per type, not occurrences: a chorus sung three times
    # is still one chorus and should stay plain "Chorus".
    distinct: dict[SectionType, set[tuple[str, ...]]] = {}
    for section in sections:
        distinct.setdefault(section.type, set()).add(_section_fingerprint(section))

    seen: dict[tuple[SectionType, tuple[str, ...]], int | None] = {}
    next_number: dict[SectionType, int] = {}

    for section in sections:
        fingerprint = (section.type, _section_fingerprint(section))
        if section.number is not None:
            seen.setdefault(fingerprint, section.number)
            continue
        if fingerprint in seen:
            section.number = seen[fingerprint]
            continue
        if len(distinct[section.type]) == 1 and not explicit.get(section.type):
            seen[fingerprint] = None
            continue
        candidate = next_number.get(section.type, 0) + 1
        used = explicit.get(section.type, set())
        while candidate in used:
            candidate += 1
        next_number[section.type] = candidate
        section.number = candidate
        seen[fingerprint] = candidate
