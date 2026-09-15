"""Slide planning."""

from __future__ import annotations

from pathlib import Path

import pytest

from pcci.config import ConversionConfig
from pcci.ir import ChordPlacement, Line, Section, SectionType, Song
from pcci.parse.pipeline import analyze
from pcci.slides import SlidePlan, chunk_sizes, plan_slides


def song_with(line_count: int) -> Song:
    return Song(
        title="Test",
        sections=[
            Section(
                type=SectionType.VERSE,
                number=1,
                lines=[Line(lyrics=f"line {index}") for index in range(line_count)],
            )
        ],
    )


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        (1, [1]),
        (4, [4]),
        (5, [3, 2]),  # the spec's example: never 4 + 1
        (6, [4, 2]),
        (8, [4, 4]),
        (9, [3, 3, 3]),
        (10, [4, 4, 2]),
        (13, [4, 3, 3, 3]),  # evenly redistributed, not 4 + 4 + 4 + 1
    ],
)
def test_balanced_chunking(count: int, expected: list[int]) -> None:
    assert chunk_sizes(count, 4, balance_last=True) == expected


def test_unbalanced_chunking_leaves_the_orphan() -> None:
    assert chunk_sizes(5, 4, balance_last=False) == [4, 1]
    assert chunk_sizes(9, 4, balance_last=False) == [4, 4, 1]


def test_every_chunking_preserves_the_line_count() -> None:
    for count in range(1, 40):
        for per_slide in range(1, 11):
            for balance in (True, False):
                assert sum(chunk_sizes(count, per_slide, balance_last=balance)) == count


def test_a_slide_never_spans_two_sections() -> None:
    song = Song(
        title="Test",
        sections=[
            Section(type=SectionType.VERSE, number=1, lines=[Line(lyrics="one")]),
            Section(type=SectionType.CHORUS, lines=[Line(lyrics="two")]),
        ],
    )
    plan = plan_slides(song, ConversionConfig(lines_per_slide=4))
    assert plan.slide_count == 2
    assert {slide.section_index for slide in plan.slides} == {0, 1}


def test_slide_labels_number_only_when_a_section_splits() -> None:
    plan = plan_slides(song_with(4), ConversionConfig(lines_per_slide=4))
    assert [slide.label for slide in plan.slides] == ["Verse 1"]
    plan = plan_slides(song_with(8), ConversionConfig(lines_per_slide=4))
    assert [slide.label for slide in plan.slides] == ["Verse 1 (1)", "Verse 1 (2)"]


def test_instrumental_lines_take_a_slot(fixtures_dir: Path) -> None:
    song = Song(
        title="Test",
        sections=[
            Section(
                type=SectionType.INTRO,
                lines=[Line(chords=[ChordPlacement(chord="A", char_index=0)]) for _ in range(6)],
            )
        ],
    )
    plan = plan_slides(song, ConversionConfig(lines_per_slide=4))
    assert [len(slide.lines) for slide in plan.slides] == [4, 2]
    assert all(not slide.lyrics for slide in plan.slides)


def test_annotation_only_lines_ride_along_rather_than_taking_a_slot() -> None:
    song = Song(
        title="Test",
        sections=[
            Section(
                type=SectionType.VERSE,
                lines=[
                    Line(lyrics="one"),
                    Line(annotation="Hold G X 8 BARS"),
                    Line(lyrics="two"),
                ],
            )
        ],
    )
    plan = plan_slides(song, ConversionConfig(lines_per_slide=4))
    assert plan.slide_count == 1
    assert plan.slides[0].annotations == ["Hold G X 8 BARS"]
    assert plan.slides[0].lyrics == ["one", "two"]


@pytest.mark.parametrize("per_slide", [1, 2, 3, 4, 6, 10])
def test_real_chart_plans_at_every_size(fixtures_dir: Path, per_slide: int) -> None:
    song = analyze(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    plan = plan_slides(song, ConversionConfig(lines_per_slide=per_slide))
    assert plan.slides
    for slide in plan.slides:
        assert len(slide.lines) <= per_slide
        section = song.sections[slide.section_index]
        assert slide.section_label == section.label


def test_plan_round_trips_through_json(fixtures_dir: Path) -> None:
    plan = plan_slides(analyze(fixtures_dir / "GOODBYE YESTERDAY A.docx"))
    assert SlidePlan.from_json(plan.to_json()) == plan


def test_plan_carries_the_whole_recipe(fixtures_dir: Path) -> None:
    """A plan file alone must be enough to build the same presentation."""
    config = ConversionConfig(lines_per_slide=2)
    plan = plan_slides(analyze(fixtures_dir / "GOODBYE YESTERDAY A.docx"), config)
    restored = SlidePlan.from_json(plan.to_json())
    assert restored.config.lines_per_slide == 2
    assert restored.song.title == plan.song.title
    assert restored.config.style.font.postscript_name == "WorkSans-Black"
