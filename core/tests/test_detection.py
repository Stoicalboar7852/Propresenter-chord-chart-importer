"""Section detection, chord alignment and cross-format agreement."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pcci.ingest import ingest
from pcci.ir import PositionedLine, SectionType, Song
from pcci.parse.align import align_chords, split_inline_line
from pcci.parse.metadata import split_title_artist, split_title_chords
from pcci.parse.pipeline import analyze
from pcci.parse.sections import (
    LineKind,
    classify_document,
    is_instruction,
    parse_section_label,
    split_trailing_instruction,
)

SAME_SONG_FORMATS = [
    "GOODBYE YESTERDAY A.docx",
    "text/goodbye_yesterday.txt",
    "text/goodbye_yesterday.md",
    "html/goodbye_yesterday.html",
    "html/goodbye_yesterday_no_pre.html",
    "rtf/goodbye_yesterday.rtf",
    "odt/goodbye_yesterday.odt",
    "pdf/goodbye_yesterday.pdf",
    "pdf/goodbye_yesterday_2col.pdf",
]


@pytest.fixture(scope="module")
def goodbye(fixtures_dir: Path) -> Song:
    return analyze(fixtures_dir / "GOODBYE YESTERDAY A.docx")


def test_the_real_chart_is_read_entirely_from_labels(goodbye: Song) -> None:
    assert goodbye.title == "GOODBYE YESTERDAY"
    assert len(goodbye.sections) == 14
    assert all(section.confidence >= 0.95 for section in goodbye.sections)
    assert [section.label for section in goodbye.sections][:5] == [
        "Verse 1",
        "Chorus 1",
        "Verse 2",
        "Chorus 2A",
        "Interlude",
    ]


def test_chords_land_on_the_right_characters(goodbye: Song) -> None:
    chorus = next(s for s in goodbye.sections if s.label == "Chorus 2A")
    line = chorus.lines[0]
    assert line.lyrics == "Again and again and again and again"
    assert [(c.chord, c.char_index) for c in line.chords] == [("D", 0), ("E", 11), ("F#m", 21)]


def test_lone_chord_above_a_lyric_is_not_projected(goodbye: Song) -> None:
    """A line reading just "A" is a chord, not the article."""
    verse = goodbye.sections[0]
    assert verse.lines[0].lyrics == "Goodbye yesterday"
    assert [c.chord for c in verse.lines[0].chords] == ["A"]
    assert all(line.lyrics != "A" for section in goodbye.sections for line in section.lines)


def test_performance_instructions_never_become_lyrics(goodbye: Song) -> None:
    lyrics = [line.lyrics for section in goodbye.sections for line in section.lines]
    assert "Hold G X 8 BARS" not in lyrics
    annotations = [
        line.annotation for section in goodbye.sections for line in section.lines if line.annotation
    ]
    assert any("Hold G X 8 BARS" in annotation for annotation in annotations)


def test_chords_and_lyric_on_one_line_are_separated(goodbye: Song) -> None:
    bridge = next(s for s in goodbye.sections if s.label == "Bridge 1")
    line = bridge.lines[0]
    assert line.lyrics == "I have decided"
    assert [c.chord for c in line.chords] == ["A", "Bm"]


@pytest.mark.parametrize("fixture", SAME_SONG_FORMATS)
def test_every_format_detects_the_same_song(fixtures_dir: Path, fixture: str) -> None:
    reference = analyze(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    song = analyze(fixtures_dir / fixture)
    assert [s.label for s in song.sections] == [s.label for s in reference.sections]
    assert [[line.lyrics for line in section.lines] for section in song.sections] == [
        [line.lyrics for line in section.lines] for section in reference.sections
    ]


@pytest.mark.parametrize("fixture", SAME_SONG_FORMATS)
def test_chord_placements_agree_across_formats(fixtures_dir: Path, fixture: str) -> None:
    """Positional sources must land chords in the same place as monospaced ones."""
    reference = analyze(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    song = analyze(fixtures_dir / fixture)
    for produced, expected in zip(song.sections, reference.sections, strict=True):
        for line_produced, line_expected in zip(produced.lines, expected.lines, strict=True):
            assert [(c.chord, c.char_index) for c in line_produced.chords] == [
                (c.chord, c.char_index) for c in line_expected.chords
            ], f"{fixture}: {line_expected.lyrics!r}"


def test_charts_with_no_headers_fall_back_to_stanzas(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "adversarial" / "no_headers.txt")
    assert [s.label for s in song.sections] == ["Verse 1", "Verse 2"]
    assert all(section.confidence == 0.3 for section in song.sections)
    assert any("guessed" in warning for warning in song.warnings)


def test_the_lyric_line_that_must_survive(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "adversarial" / "no_headers.txt")
    lyrics = [line.lyrics for section in song.sections for line in section.lines]
    assert "A man of sorrows, and acquainted with grief" in lyrics


def test_abbreviated_labels(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "adversarial" / "abbreviations.txt")
    assert [s.type for s in song.sections] == [
        SectionType.VERSE,
        SectionType.PRE_CHORUS,
        SectionType.CHORUS,
        SectionType.VERSE,
    ]
    assert all(section.confidence == 0.7 for section in song.sections)


def test_chord_only_intro_is_instrumental(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "adversarial" / "chord_only_intro.txt")
    intro = song.sections[0]
    assert intro.type is SectionType.INTRO
    assert all(line.is_instrumental for line in intro.lines)


def test_nashville_numbers_are_chords_not_lyrics(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "adversarial" / "nashville.txt")
    lyrics = [line.lyrics for section in song.sections for line in section.lines]
    assert "Great is your faithfulness to me" in lyrics
    assert "1        5/7      6m       4" not in lyrics
    verse = song.sections[0]
    assert [c.chord for c in verse.lines[0].chords] == ["1", "5/7", "6m", "4"]


def test_title_and_artist_on_one_line(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "PRODIGAL.docx")
    assert song.title == "The Prodigal"
    assert song.artist == "Josiah Queen"


def test_title_line_chords_become_an_intro(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "IN THE RIVER.docx")
    assert song.title == "IN THE RIVER"
    intro = song.sections[0]
    assert intro.type is SectionType.INTRO
    assert intro.confidence == 0.7
    assert [c.chord for c in intro.lines[0].chords] == ["A", "F#m", "C#m", "E"]


def test_chart_without_a_title_line_uses_the_file_name(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "GRATITUDE E.docx")
    assert song.title == "GRATITUDE E"
    # The opening lyric must stay a lyric.
    lyrics = [line.lyrics for section in song.sections for line in section.lines]
    assert "All my words fall short" in lyrics


def test_repeated_sections_share_an_identity(fixtures_dir: Path) -> None:
    song = analyze(fixtures_dir / "ONE WAY.docx")
    choruses = [s for s in song.sections if s.type is SectionType.CHORUS]
    assert len(choruses) == 2
    assert choruses[0].label == choruses[1].label


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hold G X 8 BARS", True),
        ("REPEAT V1 HOLD “G”", True),
        ("AX 1 BAR", True),
        ("(repeat)", True),
        ("Goodbye yesterday", False),
        ("I have decided", False),
        ("The world behind, the cross before", False),
        # A label, with nobody doing anything: a note.
        ("Drum break", True),
        ("Repeat until fade", True),
        ("Key change", True),
        ("Key change to D", True),
        ("Tacet", True),
        # A sentence, whatever word it happens to contain: a line of the song. Each of
        # these was read as a performance note once, and never reached a slide.
        ("We break the silence with a song", False),
        ("Hold me in the storm", False),
        ("Nothing can stop this joy", False),
        ("Break every chain", False),
        ("Times of refreshing", False),
        # Upper case is how charts write notes, but it cannot outvote a sentence: some
        # charts are typed entirely in capitals.
        ("WE BREAK THE SILENCE WITH A SONG", False),
    ],
)
def test_instruction_detection(text: str, expected: bool) -> None:
    assert is_instruction(text) is expected


def test_a_lyric_with_an_instruction_word_still_reaches_the_slide() -> None:
    """The bug this guards: one word off the list took a whole line off the screen."""
    chart = (
        "Hymn\n\n"
        "Verse 1\n"
        "G              C\n"
        "We break the silence with a song\n"
        "         D\n"
        "Hold me in the storm\n"
    )
    song = _song_from(chart)
    lyrics = [line.lyrics for section in song.sections for line in section.lines]
    assert lyrics == ["We break the silence with a song", "Hold me in the storm"]
    assert all(line.annotation is None for section in song.sections for line in section.lines)


def test_a_mistyped_chord_never_becomes_a_lyric() -> None:
    """A real chart wrote "Dmd/E" where every other line of the section had a chord."""
    chart = (
        "Hymn\n\n"
        "Verse 1\n"
        "            Dm\n"
        "Amazing grace how sweet the sound\n"
        "           Dmd/E\n"
        "That saved a wretch like me\n"
    )
    song = _song_from(chart)
    lyrics = [line.lyrics for section in song.sections for line in section.lines]
    assert lyrics == ["Amazing grace how sweet the sound", "That saved a wretch like me"]

    chords = [
        placement.chord
        for section in song.sections
        for line in section.lines
        for placement in line.chords
    ]
    assert chords == ["Dm", "Dmd/E"], "kept exactly as the chart wrote it"
    assert any("Dmd/E" in warning for warning in song.warnings), "and said so"


def _song_from(chart: str) -> Song:
    """Parse a chart written inline, the way a text ingester would hand it over."""
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "chart.txt"
        path.write_text(chart, encoding="utf-8")
        return analyze(path)


def test_trailing_instructions_are_split_off_lyrics() -> None:
    assert split_trailing_instruction("Praise the Lord Oh my soul  x4") == (
        "Praise the Lord Oh my soul",
        "x4",
    )
    assert split_trailing_instruction("I won't turn back     (HOLD)") == (
        "I won't turn back",
        "HOLD",
    )
    assert split_trailing_instruction("Goodbye yesterday") == ("Goodbye yesterday", "")


def test_title_helpers() -> None:
    assert split_title_chords("ONE WAY    G   Em   D   C") == ("ONE WAY", "G   Em   D   C")
    assert split_title_chords("GOODBYE YESTERDAY") == ("GOODBYE YESTERDAY", "")
    assert split_title_artist("Watch Your Mouth By: Josiah Queen") == (
        "Watch Your Mouth",
        "Josiah Queen",
    )


def test_an_indented_chart_keeps_its_chords_over_the_right_words() -> None:
    """A chart written inside a Word text box carries the same indent on every line.

    The lyric loses that indent when it is read; the chord columns are measured before
    it does. Subtracting one from the other is the whole fix, and getting it wrong
    pushes every chord past the end of the line and piles them on the last character,
    which is what these charts used to do.
    """
    indent = " " * 64
    chords = align_chords(
        PositionedLine(text=f"{indent}G                                      Gsus"),
        PositionedLine(text="I was headed for hell until He rescued me"),
        lyric_offset=len(indent),
    )
    assert [c.char_index for c in chords] == [0, 39]
    # 39 is "me": the word the Gsus actually falls on.
    lyric = "I was headed for hell until He rescued me"
    assert lyric[39:] == "me"


def test_an_indented_chart_reads_the_same_as_an_unindented_one() -> None:
    """Indenting a whole chart must not move a single chord."""
    chord_text = "D          E         F#m"
    lyric_text = "Again and again and again and again"
    plain = align_chords(PositionedLine(text=chord_text), PositionedLine(text=lyric_text))
    indented = align_chords(
        PositionedLine(text=" " * 40 + chord_text),
        PositionedLine(text=lyric_text),
        lyric_offset=40,
    )
    assert [c.char_index for c in plain] == [c.char_index for c in indented]


def test_a_chord_line_indented_further_than_its_lyric_still_moves_right() -> None:
    """Only the lyric's own indent comes off; the chord's extra indent is meaningful."""
    chords = align_chords(
        PositionedLine(text="        A"),
        PositionedLine(text="Goodbye yesterday"),
    )
    assert [c.char_index for c in chords] == [8]


def test_alignment_clamps_to_the_lyric() -> None:
    chords = align_chords(
        PositionedLine(text="D          E         F#m"),
        PositionedLine(text="Short"),
    )
    assert [c.char_index for c in chords] == [0, 5, 5]


def test_alignment_without_a_lyric_puts_everything_at_zero() -> None:
    chords = align_chords(PositionedLine(text="Am  F  C  G"), None)
    assert [c.char_index for c in chords] == [0, 0, 0, 0]


def test_positional_alignment_uses_real_coordinates() -> None:
    chord_line = PositionedLine(text="C   G", char_x=[0.0, 6.0, 12.0, 18.0, 24.0])
    lyric_line = PositionedLine(text="abcde", char_x=[0.0, 6.0, 12.0, 18.0, 24.0])
    chords = align_chords(chord_line, lyric_line)
    assert [(c.chord, c.char_index) for c in chords] == [("C", 0), ("G", 4)]


def test_split_inline_line() -> None:
    result = split_inline_line(PositionedLine(text="A  Bm    I have decided"))
    assert result is not None
    lyric, chords = result
    assert lyric == "I have decided"
    assert [c.chord for c in chords] == ["A", "Bm"]
    assert split_inline_line(PositionedLine(text="Goodbye yesterday")) is None


def test_classification_of_the_reference_chart(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    kinds = {item.kind for item in classify_document(document)}
    assert LineKind.HEADER in kinds
    assert LineKind.CHORD in kinds
    assert LineKind.LYRIC in kinds
    assert LineKind.ANNOTATION in kinds
    assert LineKind.AMBIGUOUS_PLACEHOLDER not in kinds, "every ambiguity must be resolved"


@given(st.text(min_size=1, max_size=60))
def test_label_parsing_never_raises(text: str) -> None:
    parse_section_label(text)


@given(st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=80))
def test_alignment_indices_stay_inside_the_lyric(lyric: str) -> None:
    chord_line = PositionedLine(text="C   G   Am   F")
    chords = align_chords(chord_line, PositionedLine(text=lyric))
    for placement in chords:
        assert 0 <= placement.char_index <= len(lyric)
