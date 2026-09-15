"""The IR is the contract between ingestion, parsing and writing. Pin it down."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from pcci.ir import (
    ChordPlacement,
    Line,
    PositionedLine,
    RawDocument,
    Section,
    SectionType,
    Song,
)


def make_song() -> Song:
    return Song(
        title="Goodbye Yesterday",
        artist="Test Artist",
        ccli_number="1234567",
        key="A",
        tempo=140,
        sections=[
            Section(
                type=SectionType.INTRO,
                raw_label="[Intro]",
                confidence=0.95,
                lines=[Line(chords=[ChordPlacement(chord="A", char_index=0)])],
            ),
            Section(
                type=SectionType.VERSE,
                number=1,
                raw_label="[Verse 1]",
                lines=[
                    Line(
                        lyrics="Goodbye yesterday",
                        chords=[
                            ChordPlacement(chord="A", char_index=0),
                            ChordPlacement(chord="Asus4", char_index=8, raw="Asus"),
                        ],
                    )
                ],
            ),
        ],
    )


def test_song_round_trips_through_json() -> None:
    song = make_song()
    assert Song.from_json(song.to_json()) == song


def test_song_json_is_stable() -> None:
    song = make_song()
    assert Song.from_json(song.to_json()).to_json() == song.to_json()


def test_title_may_not_be_blank() -> None:
    with pytest.raises(ValidationError):
        Song(title="   ")


def test_chord_may_sit_at_end_of_lyric_but_not_past_it() -> None:
    Line(lyrics="abc", chords=[ChordPlacement(chord="G", char_index=3)])
    with pytest.raises(ValidationError):
        Line(lyrics="abc", chords=[ChordPlacement(chord="G", char_index=4)])


def test_two_chords_may_share_a_char_index() -> None:
    line = Line(
        lyrics="riff",
        chords=[
            ChordPlacement(chord="A", char_index=0),
            ChordPlacement(chord="Bm", char_index=0),
        ],
    )
    assert [c.chord for c in line.chords] == ["A", "Bm"]


def test_instrumental_line_has_chords_and_no_lyrics() -> None:
    line = Line(chords=[ChordPlacement(chord="A", char_index=0)])
    assert line.is_instrumental
    assert not line.is_empty


def test_raw_defaults_to_the_normalised_chord() -> None:
    assert ChordPlacement(chord="Cmaj7", char_index=0).raw == "Cmaj7"
    assert ChordPlacement(chord="Cmaj7", char_index=0, raw="CM7").raw == "CM7"


def test_char_x_must_match_the_text_length() -> None:
    PositionedLine(text="abc", char_x=[1.0, 2.0, 3.0])
    with pytest.raises(ValidationError):
        PositionedLine(text="abc", char_x=[1.0, 2.0])


def test_positioned_is_false_without_geometry() -> None:
    assert not PositionedLine(text="abc").positioned
    assert PositionedLine(text="a", char_x=[0.0]).positioned


def test_section_label_uses_number_and_falls_back_to_raw_label() -> None:
    assert Section(type=SectionType.VERSE, number=2).label == "Verse 2"
    assert Section(type=SectionType.CHORUS).label == "Chorus"
    assert Section(type=SectionType.MISC, raw_label="Channel").label == "Channel"


def test_raw_document_filters_blank_lines() -> None:
    document = RawDocument(
        source_path=Path("song.txt"),
        source_format="txt",
        lines=[PositionedLine(text="A"), PositionedLine(text="   "), PositionedLine(text="B")],
    )
    assert [line.text for line in document.non_empty_lines()] == ["A", "B"]


def test_counts() -> None:
    song = make_song()
    assert song.line_count == 2
    assert song.chord_count == 3
