"""Chord grammar, normalisation and line classification."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pcci.parse.chords import (
    LineClass,
    classify_line,
    find_inline_lyric_start,
    is_chord_token,
    normalise_chord,
    parse_chord,
    tokenise,
)


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("A", "A"),
        ("Bb", "Bb"),
        ("F#m", "F#m"),
        ("C#m7/G#", "C#m7/G#"),
        ("Cmaj7", "Cmaj7"),
        ("CM7", "Cmaj7"),
        ("Cmin7", "Cm7"),
        ("C-7", "Cm7"),
        ("Co", "Cdim"),
        ("C+", "Caug"),
        ("Caug", "Caug"),
        ("Asus", "Asus"),
        ("Asus4", "Asus4"),
        ("A4", "A4"),
        ("Aadd9", "Aadd9"),
        ("E7sus4", "E7sus4"),
        ("Bm7b5", "Bm7b5"),
        ("Bbmaj7/D", "Bbmaj7/D"),
        ("G/B", "G/B"),
        ("Dbb", "Dbb"),
        ("F##m", "F##m"),
    ],
)
def test_chords_parse_and_normalise(token: str, expected: str) -> None:
    assert normalise_chord(token) == expected


@pytest.mark.parametrize(
    "token",
    ["man", "sorrows", "Ate", "Hello", "I", "the", "Praise", "grace", "H", "Am7extra", "A/H"],
)
def test_non_chords_are_rejected(token: str) -> None:
    assert parse_chord(token) is None


def test_unicode_accidentals_are_normalised() -> None:
    assert normalise_chord("B♭") == "Bb"
    assert normalise_chord("F♯m7") == "F#m7"


def test_raw_spelling_is_preserved() -> None:
    chord = parse_chord("CM7")
    assert chord is not None
    assert chord.raw == "CM7"
    assert chord.normalised == "Cmaj7"


@pytest.mark.parametrize("token", ["N.C.", "NC", "%", "|", "||", ":||", "x2", "X4", "-"])
def test_chord_line_furniture_counts_as_a_chord_token(token: str) -> None:
    assert is_chord_token(token)


def test_the_lyric_line_that_must_not_be_a_chord_line() -> None:
    # From the spec: this line is 25% chord-shaped and must never classify as chords.
    assert classify_line("A man of sorrows") is LineClass.LYRIC


@pytest.mark.parametrize(
    "line",
    [
        "Amazing grace how sweet the sound",
        "I won't waste another minute in my old ways",
        "Praise the Lord, I've been born again",
        "REPEAT V1 HOLD G",
        "Hold G X 8 BARS",
    ],
)
def test_real_lyric_lines_are_not_chord_lines(line: str) -> None:
    assert classify_line(line) is not LineClass.CHORD


@pytest.mark.parametrize(
    "line",
    [
        "D          E         F#m",
        "Bm                                                 E",
        "A/C#",
        "Asus",
        "G   D/F#   Em7   C",
    ],
)
def test_real_chord_lines_are_chord_lines(line: str) -> None:
    assert classify_line(line) is LineClass.CHORD


@pytest.mark.parametrize("line", ["A", "Am", "Do"])
def test_single_ambiguous_words_defer_to_context(line: str) -> None:
    assert classify_line(line) is LineClass.AMBIGUOUS


def test_lower_case_root_is_not_a_chord() -> None:
    # Chord roots are upper case; a lone "a" is the English article.
    assert classify_line("a") is LineClass.LYRIC


def test_blank_lines_are_blank() -> None:
    assert classify_line("") is LineClass.BLANK
    assert classify_line("    ") is LineClass.BLANK


def test_inline_lyric_detection() -> None:
    assert find_inline_lyric_start("A  Bm    I have decided") == 9
    assert find_inline_lyric_start("A  Bm    To follow Jesus") == 9
    assert find_inline_lyric_start("D          E         F#m") is None
    assert find_inline_lyric_start("Goodbye yesterday") is None
    # A single space is ordinary spacing, not a chords-then-lyric split.
    assert find_inline_lyric_start("A yesterday") is None


def test_tokenise_reports_columns() -> None:
    assert tokenise("  A   Bm") == [("A", 2), ("Bm", 6)]


ROOTS = st.sampled_from("ABCDEFG")
ACCIDENTALS = st.sampled_from(["", "#", "b", "##", "bb"])
QUALITIES = st.sampled_from(["", "m", "maj", "dim", "aug"])
EXTENSIONS = st.sampled_from(["", "2", "4", "5", "6", "7", "9", "11", "13"])
ALTERATIONS = st.sampled_from(["", "sus2", "sus4", "add9", "b5", "#5", "b9", "#9", "#11", "b13"])


@given(ROOTS, ACCIDENTALS, QUALITIES, EXTENSIONS, ALTERATIONS, ROOTS, ACCIDENTALS)
def test_generated_chords_round_trip(
    root: str,
    accidental: str,
    quality: str,
    extension: str,
    alteration: str,
    bass_root: str,
    bass_accidental: str,
) -> None:
    """parse -> normalise -> parse -> normalise is a fixed point."""
    token = f"{root}{accidental}{quality}{extension}{alteration}/{bass_root}{bass_accidental}"
    first = normalise_chord(token)
    if first is None:
        return
    assert normalise_chord(first) == first
