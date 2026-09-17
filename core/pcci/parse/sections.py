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
from enum import StrEnum
from typing import Final

from pcci.ir import PositionedLine, RawDocument, Section, SectionType
from pcci.parse.chords import (
    LineClass,
    classify_line,
    find_inline_lyric_start,
    is_chord_token,
)

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
    # Seen in the real charts: [TURN 1], [END]
    "turn": SectionType.INSTRUMENTAL,
    "end": SectionType.ENDING,
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
    [>*\u2022\-]*\s*                       # decoration such as ">>>[CHORUS 1]"
    [\[\(]?\s*
    (?P<word>Intro|Verse|Chorus|Pre[\s\-]?Chorus|Post[\s\-]?Chorus|Bridge|Tag|Outro|
       Ending|End|Interlude|Instrumental|Refrain|Vamp|Turnaround|Turn|Coda|Breakdown|
       Hook|Solo|Reprise|Channel|Link)
    \s*
    (?P<number>[0-9]+[A-Za-z]?|[IVX]{1,4}|[A-Z])?
    \s*[\]\)]?\s*:?\s*
    (?P<trailer>\[\s*[xX]\s*\d+\s*\]|\(\s*[xX]\s*\d+\s*\)|[xX]\s*\d+)?
    \s*$""",
    re.VERBOSE | re.IGNORECASE,
)

_ROMAN_VALUES: Final[dict[str, int]] = {"I": 1, "V": 5, "X": 10}

_ABBREVIATION_RE: Final[re.Pattern[str]] = re.compile(
    r"^\s*[\[\(]?\s*(?P<word>[A-Za-z]{1,4})\s*(?P<number>\d{1,2})?\s*[\]\)]?\s*:?\s*$"
)

_TRAILING_REPEAT_RE: Final[re.Pattern[str]] = re.compile(r"[\[\(]?\s*[xX]\s*\d+\s*[\]\)]?\s*$")

#: A chord fingering, which chord sites print in brackets above the chart:
#: ``[F - x33210]``, ``[Am - x02210]``, ``[x33210]``. It is bracketed and it is short,
#: which is everything an unrecognised section label looks like - and a presentation
#: with a group called "F - X33210" is how you find out the difference.
_CHORD_DIAGRAM_RE: Final[re.Pattern[str]] = re.compile(
    r"""^\s*
    (?:[A-G][#b\u266f\u266d]?[A-Za-z0-9+\u00b0\u00f8/]*   # an optional chord name
       \s*[-\u2013\u2014:=]\s*)?                          #   and its separator
    [xX0-9]{4,8}                                     # the fret positions themselves
    \s*$""",
    re.VERBOSE,
)


def looks_like_chord_diagram(text: str) -> bool:
    """Whether some bracketed text is a fingering rather than a section name."""
    return bool(_CHORD_DIAGRAM_RE.match(text))


#: ``[Verse 1: A Singer]``, ``[Chorus: A Singer & Another]`` - how lyrics sites label a
#: section when they also say who sings it. The name is not part of the section, and
#: keeping it means the group is called "Verse 1: A Singer", never matches the other
#: verses, and loses its colour. Everything after the colon has to be people, though:
#: ``[Chorus: x2]`` is a repeat count and belongs to the label.
_PERFORMER_SUFFIX_RE: Final[re.Pattern[str]] = re.compile(
    r"^(?P<label>[^:]{1,24}):\s*(?P<performer>[A-Za-z][A-Za-z0-9 .,&+'\u2019\-]{0,40})$"
)


def without_performer(inner: str) -> str | None:
    """``Verse 1`` from ``Verse 1: A Singer``, or None if there is no name to drop."""
    match = _PERFORMER_SUFFIX_RE.match(inner.strip())
    if match is None:
        return None
    performer = match.group("performer").strip()
    # "x2", "X 4" and friends are repeat counts, which the label parser wants to keep.
    if re.fullmatch(r"[xX]\s*\d+", performer):
        return None
    # A performer is a name, and names are capitalised. That is what separates
    # "[Build: Absolutely]", where the second half is who sings it, from
    # "[Talking: to the band]", where the whole thing is the label.
    if not performer[:1].isupper():
        return None
    return match.group("label").strip() or None


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


def _roman_to_int(text: str) -> int | None:
    """``II`` -> 2. Returns ``None`` for anything that is not a roman numeral."""
    total = 0
    previous = 0
    for character in reversed(text.upper()):
        value = _ROMAN_VALUES.get(character)
        if value is None:
            return None
        total = total - value if value < previous else total + value
        previous = max(previous, value)
    return total or None


def _number_from(text: str | None) -> int | None:
    if not text:
        return None
    digits = re.match(r"\d+", text)
    if digits:
        return int(digits.group())
    candidate = text.strip().upper()
    # "Verse II" is roman; "Verse B" is a letter variant. Roman wins when it can.
    roman = _roman_to_int(candidate)
    if roman is not None:
        return roman
    if len(candidate) == 1 and candidate.isalpha():
        return ord(candidate) - ord("A") + 1
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

    # "[Verse 1: A Singer]" is a verse. Try again without the name, and only believe
    # the answer if it came back as a real section type rather than the catch-all -
    # otherwise "[Talking: to the band]" would quietly become a section called
    # "Talking" instead of being kept whole.
    if stripped.startswith("[") and stripped.endswith("]"):
        shortened = without_performer(stripped[1:-1])
        if shortened is not None:
            inner_label = parse_section_label(
                f"[{shortened}]",
                allow_abbreviations=allow_abbreviations,
                allow_bare_words=allow_bare_words,
            )
            if inner_label is not None:
                # Keep the shortened wording even when the type is the catch-all:
                # "[Build: Absolutely]" is a section called Build, and carrying the
                # singer's name into the group label helps nobody.
                return SectionLabel(
                    type=inner_label.type,
                    number=inner_label.number,
                    raw_label=shortened if inner_label.type is SectionType.MISC else stripped,
                    confidence=inner_label.confidence,
                    repeat=inner_label.repeat,
                    variant=inner_label.variant,
                )

    # A bracketed label we do not recognise is still a label: keep the user's words.
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1].strip()
        if inner and len(inner) <= 30 and not looks_like_chord_diagram(inner):
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


# ---------------------------------------------------------------------------
# Detection: which lines are headers, which are chords, which are lyrics
# ---------------------------------------------------------------------------

#: Words that mark a performance instruction rather than something to project.
_INSTRUCTION_WORDS: Final[frozenset[str]] = frozenset(
    {
        "repeat",
        "hold",
        "bar",
        "bars",
        "beat",
        "beats",
        "tacet",
        "build",
        "drop",
        "cue",
        "spontaneous",
        "spont",
        "acappella",
        "cappella",
        "rit",
        "fermata",
        "until",
        "til",
        "click",
        "break",
        "stop",
        "times",
        "downbeat",
        "instrumental",
        "modulate",
        "key change",
        "no click",
    }
)

_TRAILING_PAREN_RE: Final[re.Pattern[str]] = re.compile(r"\s+\(([^()]{1,30})\)\s*$")
_TRAILING_COUNT_RE: Final[re.Pattern[str]] = re.compile(r"\s+([xX]\s?\d{1,2})\s*$")
_WRAPPED_RE: Final[re.Pattern[str]] = re.compile(r"^\s*[\(\[]([^()\[\]]{1,40})[\)\]]\s*$")

MAX_HEADER_LENGTH: Final[int] = 32
#: How many certain chord lines make a document "a chord chart" for evidence 4.
MIN_CHORD_LINES_FOR_DENSITY: Final[int] = 3


class LineKind(StrEnum):
    """What a line turned out to be, after context was taken into account."""

    HEADER = "header"
    CHORD = "chord"
    LYRIC = "lyric"
    ANNOTATION = "annotation"
    BLANK = "blank"
    #: Internal only: an ambiguous line before the second pass decides what it is.
    AMBIGUOUS_PLACEHOLDER = "ambiguous"


@dataclass(slots=True)
class ClassifiedLine:
    """One source line, with the decision made about it."""

    index: int
    line: PositionedLine
    kind: LineKind
    label: SectionLabel | None = None
    lyric_text: str = ""
    annotation: str = ""


def is_instruction(text: str) -> bool:
    """A performance note ("Hold G X 8 BARS"), not a lyric and not a chord."""
    stripped = text.strip()
    if not stripped:
        return False
    wrapped = _WRAPPED_RE.match(stripped)
    if wrapped:
        stripped = wrapped.group(1).strip()
    words = re.findall(r"[A-Za-z]+", stripped.lower())
    if not words or len(words) > 8:
        return False
    if not any(word in _INSTRUCTION_WORDS for word in words):
        return False
    # "Bars of gold" is a lyric; an instruction is short and mostly not prose.
    return len(stripped) <= 40


def split_trailing_instruction(text: str) -> tuple[str, str]:
    """Peel a trailing ``(HOLD)`` or ``x4`` off a lyric line.

    Real charts write these next to the words. Projected to a congregation they read
    as part of the song, so they move to the line's annotation instead.
    """
    annotation_parts: list[str] = []
    body = text.rstrip()
    while True:
        count = _TRAILING_COUNT_RE.search(body)
        if count:
            annotation_parts.insert(0, count.group(1).strip())
            body = body[: count.start()].rstrip()
            continue
        paren = _TRAILING_PAREN_RE.search(body)
        if paren:
            annotation_parts.insert(0, paren.group(1).strip())
            body = body[: paren.start()].rstrip()
            continue
        break
    return body, " ".join(annotation_parts)


def _bold_marks_chords(document: RawDocument) -> bool:
    """Does this document use bold for chord lines? The reference Word charts do."""
    bold_chords = plain_chords = bold_lyrics = plain_lyrics = 0
    for line in document.lines:
        text = line.text.strip()
        if not text:
            continue
        structural = classify_line(text)
        if structural is LineClass.CHORD:
            bold_chords += line.bold
            plain_chords += not line.bold
        elif structural is LineClass.LYRIC and len(text.split()) > 3:
            bold_lyrics += line.bold
            plain_lyrics += not line.bold
    if bold_chords + plain_chords < 3 or bold_lyrics + plain_lyrics < 3:
        return False
    return bold_chords > plain_chords and plain_lyrics > bold_lyrics


def classify_document(document: RawDocument) -> list[ClassifiedLine]:
    """Classify every line, resolving ambiguity with its neighbours.

    Three passes, because each one needs the previous one's answers:

    1. The unambiguous decisions — blank, header, annotation, definite chord line.
    2. The ambiguous ones ("A" alone), resolved against the kinds decided in pass 1.
       Headers and blank lines act as boundaries here, which is the whole point: a
       lone "A" directly under ``[Verse 1]`` and directly above a lyric is a chord.
    3. Formatting-based headers, which can only be judged once chord lines are known.
    """
    bold_is_chords = _bold_marks_chords(document)
    structural = [classify_line(line.text) for line in document.lines]
    classified: list[ClassifiedLine] = []

    for index, line in enumerate(document.lines):
        text = line.text.strip()
        if not text:
            classified.append(ClassifiedLine(index, line, LineKind.BLANK))
            continue

        label = parse_section_label(text)
        if label is not None and structural[index] is not LineClass.CHORD:
            classified.append(ClassifiedLine(index, line, LineKind.HEADER, label=label))
            continue

        # "Hold G X 8 BARS" is an instruction; "I won't turn back  (HOLD)" is a lyric
        # with one attached. Peel the trailing note off before judging the line, or
        # every lyric ending in a cue reads as an instruction and never reaches a slide.
        body, trailing = split_trailing_instruction(text)
        if structural[index] is not LineClass.CHORD and (not body or is_instruction(body)):
            classified.append(ClassifiedLine(index, line, LineKind.ANNOTATION, annotation=text))
            continue

        if structural[index] is LineClass.CHORD:
            classified.append(ClassifiedLine(index, line, LineKind.CHORD))
            continue

        if structural[index] is LineClass.AMBIGUOUS:
            classified.append(ClassifiedLine(index, line, LineKind.AMBIGUOUS_PLACEHOLDER))
            continue

        # "A  Bm    I have decided": chords and their lyric share one line. It reads as
        # a lyric line by proportion, but projecting it verbatim would put chord names
        # on the screen, so it is handled as a chord line and split during pairing.
        if find_inline_lyric_start(text) is not None:
            classified.append(ClassifiedLine(index, line, LineKind.CHORD))
            continue

        classified.append(
            ClassifiedLine(index, line, LineKind.LYRIC, lyric_text=body, annotation=trailing)
        )

    chord_line_count = sum(1 for item in classified if item.kind is LineKind.CHORD)
    _resolve_ambiguous(classified, bold_is_chords, chord_line_count)
    _promote_formatting_headers(classified, document)
    return classified


def _neighbour_kind(classified: list[ClassifiedLine], position: int, step: int) -> LineKind | None:
    """The kind of the nearest non-blank line in one direction."""
    index = position + step
    while 0 <= index < len(classified):
        kind = classified[index].kind
        if kind is not LineKind.BLANK:
            return kind
        index += step
    return None


def _resolve_ambiguous(
    classified: list[ClassifiedLine], bold_is_chords: bool, chord_line_count: int
) -> None:
    """Turn each placeholder into a chord line or a lyric line.

    Evidence, in the order it is worth trusting:

    1. This document marks chord lines bold, and this line's weight agrees.
    2. A neighbour is definitely a chord line — chords cluster together.
    3. The line above is a header or the start of the section and the line below is a
       lyric, which is exactly the shape of a chord sitting over its words.
    4. The document is full of chord lines and this one sits directly above a lyric.
       In a chart with three or more unambiguous chord lines, a lone "A" on its own
       line above a lyric is a chord; a lyric line consisting only of the word "A"
       essentially does not occur.
    """
    for position, item in enumerate(classified):
        if item.kind is not LineKind.AMBIGUOUS_PLACEHOLDER:
            continue
        if bold_is_chords:
            is_chord = item.line.bold
        else:
            is_chord = _ambiguous_reads_as_chord(classified, position, chord_line_count)

        if is_chord:
            item.kind = LineKind.CHORD
        else:
            body, annotation = split_trailing_instruction(item.line.text.strip())
            item.kind = LineKind.LYRIC
            item.lyric_text = body
            item.annotation = annotation


def _ambiguous_reads_as_chord(
    classified: list[ClassifiedLine], position: int, chord_line_count: int
) -> bool:
    """Apply evidence 2 to 4 from ``_resolve_ambiguous`` to one line."""
    above = _neighbour_kind(classified, position, -1)
    below = _neighbour_kind(classified, position, 1)
    if LineKind.CHORD in (above, below):
        return True
    if below is not LineKind.LYRIC:
        return False
    if above in (LineKind.HEADER, LineKind.ANNOTATION, None):
        return True
    # A chart with several unmistakable chord lines is a chart where a lone "A" above
    # a lyric is a chord, not the article.
    return chord_line_count >= MIN_CHORD_LINES_FOR_DENSITY


def _promote_formatting_headers(classified: list[ClassifiedLine], document: RawDocument) -> None:
    """Priority 3: a short, standalone, emphasised line that is not a chord line."""
    for position, item in enumerate(classified):
        if item.kind is not LineKind.LYRIC:
            continue
        text = item.line.text.strip()
        if len(text) > MAX_HEADER_LENGTH or len(text.split()) > 4:
            continue
        if is_chord_token(text):
            continue
        # "F - X33210" is a fingering, and it clears every other bar here: it is short,
        # it is three words, and .isupper() is true of it because the only letters in
        # it are F and X. A real Shivers import came out with that as its first group.
        if looks_like_chord_diagram(text):
            continue
        # A line wrapped in brackets is a backing vocal or an aside, not a heading.
        # "(I, I, I)" passes every other bar here - it is short, and .isupper() is
        # true of it because its only letter is I - and it was stealing whole
        # sections, because a heading immediately after a heading leaves the real
        # section with no lines at all and it gets dropped.
        if _WRAPPED_RE.match(text):
            continue
        emphasised = item.line.heading or item.line.bold or (text.isupper() and len(text) > 1)
        if not emphasised:
            continue
        before = classified[position - 1].kind if position else LineKind.BLANK
        after = classified[position + 1].kind if position + 1 < len(classified) else LineKind.BLANK
        # Directly under a heading is the first line of that section, never a heading
        # of its own. Promoting it leaves the section above with nothing in it, and a
        # section with nothing in it is thrown away.
        if before is LineKind.HEADER:
            continue
        if before is not LineKind.BLANK and after is not LineKind.BLANK:
            continue
        word = re.sub(r"[^a-z]", "", text.lower())
        section_type = _TYPE_BY_KEYWORD.get(word, SectionType.MISC)
        if section_type is SectionType.MISC and not document.monospace:
            continue
        item.kind = LineKind.HEADER
        item.label = SectionLabel(
            type=section_type,
            number=None,
            raw_label=text,
            confidence=CONFIDENCE_FORMATTING,
        )
