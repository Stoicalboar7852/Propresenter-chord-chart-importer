"""The FreeShow writer and its verifier.

Every claim about the format here traces back to FreeShow's own source, not to a guess
about what it might accept: the types in ``src/types/Show.ts``, the ChordPro importer
that shows what FreeShow itself writes, and the renderer that decides what a chord's
``pos`` means. See docs/FORMAT_NOTES.md section 6.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from pcci.config import ChordDelivery, ConversionConfig, ExportTarget
from pcci.convert import convert
from pcci.errors import VerificationFailedError
from pcci.freeshow.verify import verify_bytes, verify_or_raise
from pcci.freeshow.writer import build_show, item_style, show_bytes
from pcci.ir import ChordPlacement, Line, Section, SectionType, Song
from pcci.parse.pipeline import analyze
from pcci.slides import plan_slides

CHART = "GOODBYE YESTERDAY A.docx"


def freeshow_config(**overrides: Any) -> ConversionConfig:
    return ConversionConfig(export_target=ExportTarget.FREESHOW, **overrides)


@pytest.fixture(scope="module")
def plan(fixtures_dir: Path):
    return plan_slides(analyze(fixtures_dir / CHART), freeshow_config())


@pytest.fixture(scope="module")
def written(plan) -> tuple[str, dict[str, Any]]:
    return build_show(plan)


@pytest.fixture(scope="module")
def show(written) -> dict[str, Any]:
    return written[1]


def ordered(show: dict[str, Any]) -> list[dict[str, Any]]:
    """Slides in playing order: each layout entry, then its children."""
    layout = show["layouts"][show["settings"]["activeLayout"]]
    result: list[dict[str, Any]] = []
    for entry in layout["slides"]:
        parent = show["slides"][entry["id"]]
        result.append(parent)
        result.extend(show["slides"][child] for child in parent.get("children", []))
    return result


def words(slide: dict[str, Any]) -> list[str]:
    return [
        "".join(chunk["value"] for chunk in line["text"])
        for item in slide["items"]
        for line in item["lines"]
    ]


def test_the_file_is_the_pair_freeshow_saves(written) -> None:
    payload = show_bytes(*written)
    parsed = json.loads(payload)
    assert isinstance(parsed, list)
    assert len(parsed) == 2
    assert isinstance(parsed[0], str) and parsed[0]
    assert isinstance(parsed[1], dict)


def test_the_show_carries_the_song_and_its_credits(show) -> None:
    assert show["name"] == "GOODBYE YESTERDAY"
    assert show["category"] == "song"
    assert show["meta"]["title"] == "GOODBYE YESTERDAY"
    assert set(show).issuperset({"slides", "layouts", "settings", "timestamps", "media"})


def test_one_layout_plays_every_planned_slide(show, plan) -> None:
    assert len(ordered(show)) == plan.slide_count
    played = [words(slide) for slide in ordered(show)]
    planned = [[line.lyrics for line in slide.lines] for slide in plan.slides]
    assert played == planned


def test_a_section_is_one_group_with_the_rest_as_children(show, plan) -> None:
    layout = show["layouts"][show["settings"]["activeLayout"]]
    for entry in layout["slides"]:
        parent = show["slides"][entry["id"]]
        assert parent["group"], "the slide a section starts on names the group"
        for child in parent.get("children", []):
            assert show["slides"][child]["group"] is None, "a child slide has no group"


def test_known_sections_use_freeshow_s_own_groups(show) -> None:
    groups = {
        slide["group"]: slide.get("globalGroup")
        for slide in show["slides"].values()
        if slide["group"]
    }
    assert groups.get("verse") == "verse"
    assert groups.get("chorus") == "chorus"
    # And the colour is the one a default FreeShow install gives that group.
    verse = next(slide for slide in show["slides"].values() if slide["group"] == "verse")
    assert verse["color"] == "#5825f5"


def test_a_section_type_freeshow_does_not_know_keeps_pcci_s_label() -> None:
    song = Song(
        title="Hymn",
        sections=[
            Section(
                type=SectionType.INSTRUMENTAL,
                lines=[Line(lyrics="", chords=[ChordPlacement(chord="G", char_index=0)])],
            )
        ],
    )
    _, show = build_show(plan_slides(song, freeshow_config()))
    slide = next(iter(show["slides"].values()))
    assert slide["group"] == "Instrumental"
    assert "globalGroup" not in slide
    assert slide["color"].startswith("#")


def test_chords_ride_on_the_words_by_character_index(show) -> None:
    lines = [
        line
        for slide in show["slides"].values()
        for item in slide["items"]
        for line in item["lines"]
        if line.get("chords")
    ]
    assert lines, "the default route stores chords on the words"
    for line in lines:
        text = "".join(chunk["value"] for chunk in line["text"])
        for chord in line["chords"]:
            assert chord["key"].strip()
            assert len(chord["id"]) == 5
            if text:
                assert 0 <= chord["pos"] <= len(text)


def test_a_chord_only_line_reaches_the_stage_in_order() -> None:
    """An intro has chords and no words. FreeShow can show those; a ``.pro`` cannot.

    Every chord on such a line is at index zero - the IR anchors a chord inside the
    lyric it sits on, and there is no lyric - so what has to survive is the order, which
    FreeShow spaces out rather than stacking.
    """
    song = Song(
        title="Turnaround",
        sections=[
            Section(
                type=SectionType.INTRO,
                lines=[
                    Line(
                        lyrics="",
                        chords=[
                            ChordPlacement(chord="G", char_index=0),
                            ChordPlacement(chord="D", char_index=0),
                        ],
                    )
                ],
            )
        ],
    )
    _, show = build_show(plan_slides(song, freeshow_config()))
    line = next(iter(show["slides"].values()))["items"][0]["lines"][0]
    assert line["text"] == [{"value": "", "style": ""}], "the line is there to hold them"
    assert [chord["key"] for chord in line["chords"]] == ["G", "D"]


def test_the_chords_are_stored_without_being_drawn(plan) -> None:
    _, show = build_show(plan)
    drawn = [item.get("chords") for slide in show["slides"].values() for item in slide["items"]]
    assert all(entry is None for entry in drawn), "nothing asks FreeShow to paint them"


def test_asking_for_chords_on_the_audience_screen_is_deliberate(fixtures_dir: Path) -> None:
    config = freeshow_config(chords_on_slide=True)
    _, show = build_show(plan_slides(analyze(fixtures_dir / CHART), config))
    drawn = [
        item.get("chords", {}).get("enabled")
        for slide in show["slides"].values()
        for item in slide["items"]
    ]
    assert any(drawn), "the switch has to reach the file or it does nothing"


def test_a_repeated_section_is_played_twice_not_written_twice() -> None:
    chorus = Section(
        type=SectionType.CHORUS,
        lines=[Line(lyrics="Praise the Lord", chords=[ChordPlacement(chord="G", char_index=0)])],
    )
    song = Song(title="Doxology", sections=[chorus, chorus.model_copy(deep=True)])
    _, show = build_show(plan_slides(song, freeshow_config()))
    layout = show["layouts"][show["settings"]["activeLayout"]]
    assert len(layout["slides"]) == 2, "both are played"
    assert len(show["slides"]) == 1, "one slide, played twice"
    assert layout["slides"][0]["id"] == layout["slides"][1]["id"]


def test_notes_carry_the_chord_block(fixtures_dir: Path) -> None:
    config = freeshow_config(chord_delivery=ChordDelivery.INLINE_NOTES)
    _, show = build_show(plan_slides(analyze(fixtures_dir / CHART), config))
    with_notes = [slide for slide in show["slides"].values() if slide["notes"].strip()]
    assert with_notes, "the notes a stage layout can show are written too"


def test_the_notes_are_left_out_by_default(plan) -> None:
    """The default route feeds the Chords element and nothing else."""
    _, show = build_show(plan)
    assert all(not slide["notes"].strip() for slide in show["slides"].values())


def test_the_item_style_follows_the_conversion_settings() -> None:
    config = freeshow_config()
    config.style.width, config.style.height = 1920, 1080
    style = item_style(config.style)
    assert "top:54px" in style and "left:96px" in style
    assert "width:1728px" in style and "height:972px" in style
    assert "font-family:Work Sans" in style
    assert "color:#FFFFFF" in style


def test_verification_passes_on_our_own_output(written, plan) -> None:
    report = verify_bytes(show_bytes(*written), plan)
    assert report.ok, report.failures
    assert len(report.checks) > 10


def test_verification_catches_a_slide_the_layout_cannot_reach(written, plan) -> None:
    show_id, show = written
    broken = json.loads(json.dumps(show))
    layout = broken["layouts"][broken["settings"]["activeLayout"]]
    layout["slides"] = layout["slides"][:-1]
    report = verify_bytes(show_bytes(show_id, broken), plan)
    assert not report.ok
    assert any("unreachable" in failure for failure in report.failures)


def test_verification_catches_a_dangling_layout_reference(written, plan) -> None:
    show_id, show = written
    broken = json.loads(json.dumps(show))
    broken["layouts"][broken["settings"]["activeLayout"]]["slides"].append({"id": "nope"})
    report = verify_bytes(show_bytes(show_id, broken), plan)
    assert not report.ok
    assert any("dangling" in failure for failure in report.failures)


def test_verification_catches_chords_drawn_without_asking(written, plan) -> None:
    show_id, show = written
    broken = json.loads(json.dumps(show))
    next(iter(broken["slides"].values()))["items"][0]["chords"] = {"enabled": True}
    report = verify_bytes(show_bytes(show_id, broken), plan)
    assert not report.ok
    assert any("audience" in failure for failure in report.failures)


def test_verification_refuses_anything_that_is_not_a_show(plan) -> None:
    with pytest.raises(VerificationFailedError):
        verify_or_raise(b"{}", plan)


def test_converting_writes_a_show_file(tmp_path: Path, fixtures_dir: Path) -> None:
    result = convert(fixtures_dir / CHART, tmp_path / "song.show", freeshow_config())
    assert result.output_path.suffix == ".show"
    assert result.output_path.exists()
    assert result.chart_pages == []
    show = json.loads(result.output_path.read_text(encoding="utf-8"))[1]
    assert show["name"] == "GOODBYE YESTERDAY"


def test_the_extension_follows_the_target(tmp_path: Path, fixtures_dir: Path) -> None:
    """A ``.pro`` name with the FreeShow target still gets a ``.show`` file."""
    result = convert(fixtures_dir / CHART, tmp_path / "song.pro", freeshow_config())
    assert result.output_path == tmp_path / "song.show"


def test_the_chart_route_says_so_rather_than_rendering_pages(
    tmp_path: Path, fixtures_dir: Path
) -> None:
    config = freeshow_config(chord_delivery=ChordDelivery.BOTH)
    result = convert(fixtures_dir / CHART, tmp_path / "song.show", config)
    assert result.chart_pages == []
    assert any("no chord-chart element" in warning for warning in result.warnings)
    assert not list(tmp_path.glob("*.png"))
