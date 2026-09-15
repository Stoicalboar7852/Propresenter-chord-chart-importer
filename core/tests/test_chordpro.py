"""The ChordPro path: explicit structure in, exact Song out."""

from __future__ import annotations

from pathlib import Path

import pytest

from pcci.errors import UnsupportedFormatError
from pcci.ingest.base import ingester_for
from pcci.ingest.chordpro import ChordProIngester, parse_chordpro
from pcci.ir import SectionType, Song


def load(path: Path) -> Song:
    return parse_chordpro(ChordProIngester().load(path))


@pytest.fixture(scope="module")
def goodbye(fixtures_dir: Path) -> Song:
    return load(fixtures_dir / "chordpro" / "goodbye_yesterday.cho")


def test_metadata_comes_from_directives(goodbye: Song) -> None:
    assert goodbye.title == "Goodbye Yesterday"
    assert goodbye.artist == "Test Worship"
    assert goodbye.key == "A"
    assert goodbye.tempo == 140
    assert goodbye.ccli_number == "7654321"
    assert goodbye.copyright == "2024 Test Music"


def test_sections_and_labels(goodbye: Song) -> None:
    assert [section.label for section in goodbye.sections] == [
        "Verse 1",
        "Chorus 1",
        "Verse 2",
        "Interlude",
        "Bridge 1",
        "Chorus 1",
    ]
    assert all(section.confidence >= 0.95 for section in goodbye.sections)


def test_chords_are_anchored_to_the_right_characters(goodbye: Song) -> None:
    bridge = next(s for s in goodbye.sections if s.type is SectionType.BRIDGE)
    line = bridge.lines[0]
    assert line.lyrics == "I have decided"
    assert [(c.chord, c.char_index) for c in line.chords] == [("A", 0), ("Bm", 7)]
    assert line.lyrics[7:] == "decided"


def test_chord_only_line_becomes_an_instrumental_line(goodbye: Song) -> None:
    interlude = next(s for s in goodbye.sections if s.type is SectionType.INTERLUDE)
    assert len(interlude.lines) == 1
    assert interlude.lines[0].is_instrumental
    assert interlude.lines[0].chords[0].chord == "A"


def test_comment_becomes_an_annotation_on_the_previous_section(goodbye: Song) -> None:
    verse_one = goodbye.sections[0]
    assert [line.annotation for line in verse_one.lines if line.annotation] == ["Hold G X 8 BARS"]


def test_repeated_chorus_keeps_one_identity(goodbye: Song) -> None:
    choruses = [s for s in goodbye.sections if s.type is SectionType.CHORUS]
    assert len(choruses) == 2
    assert choruses[0].number == choruses[1].number
    assert choruses[0].label == choruses[1].label


def test_song_round_trips(goodbye: Song) -> None:
    assert Song.from_json(goodbye.to_json()) == goodbye


def test_file_without_directives_still_parses(fixtures_dir: Path) -> None:
    song = load(fixtures_dir / "chordpro" / "minimal.cho")
    assert song.title == "minimal"  # falls back to the file name
    assert any("file name" in warning for warning in song.warnings)
    assert song.sections[0].lines[0].lyrics == "Amazing grace how sweet the sound"
    assert [c.chord for c in song.sections[0].lines[0].chords] == ["G", "G7", "C", "G"]


def test_comments_starting_with_hash_are_ignored(fixtures_dir: Path) -> None:
    song = load(fixtures_dir / "chordpro" / "minimal.cho")
    assert all(
        "nothing but lyrics" not in (line.annotation or "")
        for s in song.sections
        for line in s.lines
    )


def test_bare_headers_inside_chordpro(fixtures_dir: Path) -> None:
    song = load(fixtures_dir / "chordpro" / "bare_headers.cho")
    assert [section.label for section in song.sections] == ["Verse 1", "Chorus"]
    # "A man of sorrows" must survive as a lyric, chords and all.
    assert song.sections[0].lines[0].lyrics == "A man of sorrows came"


def test_extension_dispatch() -> None:
    assert isinstance(ingester_for(Path("song.cho")), ChordProIngester)
    assert isinstance(ingester_for(Path("song.chopro")), ChordProIngester)


def test_a_propresenter_file_is_not_mistaken_for_chordpro(
    reference_dir: Path, tmp_path: Path
) -> None:
    disguised = tmp_path / "presentation.pro"
    disguised.write_bytes((reference_dir / "Goodbye Yesterday With slide notes.pro").read_bytes())
    with pytest.raises(UnsupportedFormatError) as excinfo:
        ChordProIngester().load(disguised)
    assert "ProPresenter presentation" in excinfo.value.user_message
