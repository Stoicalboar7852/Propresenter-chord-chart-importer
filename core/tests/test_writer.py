"""The ProPresenter writer, its verifier, and the whole conversion end to end.

Every assertion about the file format here is checked against the same bindings that
read a real ProPresenter export byte-identically, so "it parses" means something.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pcci.config import RGBA, ChordDelivery, ChordPlacementStyle, ConversionConfig, FontSpec
from pcci.convert import build, convert
from pcci.errors import VerificationFailedError
from pcci.ir import SectionType
from pcci.notes import chord_row, render_lines
from pcci.parse.pipeline import analyze
from pcci.propresenter.bindings import PROTO_SOURCE_BUILD, load_bindings
from pcci.propresenter.rtf import escape
from pcci.propresenter.verify import verify_bytes
from pcci.propresenter.writer import build_presentation, presentation_bytes
from pcci.slides import plan_slides

CHART = "GOODBYE YESTERDAY A.docx"


@pytest.fixture(scope="module")
def plan(fixtures_dir: Path):
    return plan_slides(analyze(fixtures_dir / CHART), ConversionConfig())


@pytest.fixture(scope="module")
def payload(plan) -> bytes:
    return presentation_bytes(build_presentation(plan))


@pytest.fixture(scope="module")
def parsed(payload: bytes):
    presentation = load_bindings().presentation.Presentation()
    presentation.ParseFromString(payload)
    return presentation


def test_generated_file_reparses_and_round_trips(payload: bytes, parsed) -> None:
    assert parsed.SerializeToString() == payload


def test_application_info_matches_the_vendored_schema(parsed) -> None:
    version = parsed.application_info.application_version
    assert (version.major_version, version.minor_version) == (21, 4)
    assert version.build == PROTO_SOURCE_BUILD
    assert parsed.application_info.application == 1  # APPLICATION_PROPRESENTER


def test_presentation_metadata(parsed) -> None:
    assert parsed.name == "GOODBYE YESTERDAY"
    assert parsed.category == "Song"
    assert len(parsed.uuid.string) == 36


def test_one_cue_per_slide(parsed, plan) -> None:
    assert len(parsed.cues) == plan.slide_count


def test_groups_are_named_and_coloured_from_the_sections(parsed, plan) -> None:
    names = [cue_group.group.name for cue_group in parsed.cue_groups]
    assert names[:4] == ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2A"]
    verse = next(g.group for g in parsed.cue_groups if g.group.name == "Verse 1")
    expected = ConversionConfig().colour_for(SectionType.VERSE, 1)
    assert (verse.color.red, verse.color.green, verse.color.blue) == pytest.approx(
        (expected.red, expected.green, expected.blue), abs=1e-6
    )
    assert verse.hotKey.code == 1


def test_repeated_sections_reuse_one_name_and_colour(parsed) -> None:
    choruses = [g.group for g in parsed.cue_groups if g.group.name == "Chorus 1"]
    assert len(choruses) >= 1
    colours = {(g.color.red, g.color.green, g.color.blue) for g in choruses}
    assert len(colours) == 1
    assert len({g.uuid.string for g in choruses}) == len(choruses)


def test_arrangement_lists_every_group_in_order(parsed) -> None:
    assert len(parsed.arrangements) == 1
    arrangement = parsed.arrangements[0]
    group_uuids = [cue_group.group.uuid.string for cue_group in parsed.cue_groups]
    assert [identifier.string for identifier in arrangement.group_identifiers] == group_uuids
    assert parsed.selected_arrangement.string == arrangement.uuid.string


def test_every_uuid_is_unique(parsed) -> None:
    seen: list[str] = [parsed.uuid.string]
    for cue in parsed.cues:
        seen.append(cue.uuid.string)
        for action in cue.actions:
            seen.append(action.uuid.string)
            slide = action.slide.presentation.base_slide
            seen.append(slide.uuid.string)
            for element in slide.elements:
                seen.append(element.element.uuid.string)
    for cue_group in parsed.cue_groups:
        seen.append(cue_group.group.uuid.string)
    assert len(seen) == len(set(seen))


def test_slides_carry_their_lyrics_as_rtf(parsed) -> None:
    first = parsed.cues[0].actions[0].slide.presentation.base_slide.elements[0]
    rtf = first.element.text.rtf_data.decode()
    assert rtf.startswith("{\\rtf1")
    assert "Goodbye yesterday" in rtf
    assert "WorkSans-Black" in rtf
    assert "\\fs140" in rtf  # 70pt, doubled, as RTF half-points


def test_text_element_style_follows_the_config(parsed) -> None:
    element = parsed.cues[0].actions[0].slide.presentation.base_slide.elements[0].element
    attributes = element.text.attributes
    assert attributes.font.name == "WorkSans-Black"
    assert attributes.font.size == 70.0
    assert attributes.stroke_width == 4.0
    assert attributes.paragraph_style.alignment == 2  # centred
    assert element.text.vertical_alignment == 1  # middle
    assert not element.fill.enable, "a filled box would paint over the background"


def test_notes_hold_the_chord_block(parsed) -> None:
    """By default the notes carry chords only — the lyrics are already on the slide."""
    notes = parsed.cues[0].actions[0].slide.presentation.notes.rtf_data.decode()
    assert notes.startswith("{\\rtf1")
    assert "fmodern" in notes, "notes must use a fixed-pitch font or chords misalign"
    assert "Asus" in notes
    assert "Goodbye yesterday" not in notes, "repeating the lyrics shrinks the stage text"


def test_notes_can_include_the_lyrics(fixtures_dir: Path) -> None:
    config = ConversionConfig(chord_placement=ChordPlacementStyle.ABOVE)
    plan = plan_slides(analyze(fixtures_dir / CHART), config)
    presentation = build_presentation(plan)
    notes = presentation.cues[0].actions[0].slide.presentation.notes.rtf_data.decode()
    assert "Goodbye yesterday" in notes
    assert "Asus" in notes


def test_slide_size_is_configurable(fixtures_dir: Path) -> None:
    config = ConversionConfig()
    config.style.width, config.style.height = 3840, 2160
    plan = plan_slides(analyze(fixtures_dir / CHART), config)
    presentation = build_presentation(plan)
    slide = presentation.cues[0].actions[0].slide.presentation.base_slide
    assert (slide.size.width, slide.size.height) == (3840.0, 2160.0)


def test_font_is_configurable(fixtures_dir: Path) -> None:
    config = ConversionConfig()
    config.style.font = FontSpec(
        postscript_name="Helvetica-Bold", family_name="Helvetica", size=54.0, bold=True
    )
    plan = plan_slides(analyze(fixtures_dir / CHART), config)
    presentation = build_presentation(plan)
    element = presentation.cues[0].actions[0].slide.presentation.base_slide.elements[0].element
    assert element.text.attributes.font.name == "Helvetica-Bold"
    assert b"\\fs108" in element.text.rtf_data


def test_verification_passes_on_our_own_output(payload: bytes, plan) -> None:
    report = verify_bytes(payload, plan)
    assert report.ok, report.failures
    assert len(report.checks) >= 10


def test_verification_catches_a_cue_missing_from_its_group(plan) -> None:
    presentation = build_presentation(plan)
    del presentation.cue_groups[0].cue_identifiers[0]
    report = verify_bytes(presentation.SerializeToString(), plan)
    assert not report.ok
    assert any("group" in failure for failure in report.failures)


def test_verification_catches_a_dangling_arrangement_reference(plan) -> None:
    presentation = build_presentation(plan)
    presentation.arrangements[0].group_identifiers[
        0
    ].string = "11111111-2222-3333-4444-555555555555"
    report = verify_bytes(presentation.SerializeToString(), plan)
    assert not report.ok
    assert any("arrangement" in failure for failure in report.failures)


def test_verification_catches_a_missing_slide(plan) -> None:
    presentation = build_presentation(plan)
    del presentation.cues[0]
    report = verify_bytes(presentation.SerializeToString(), plan)
    assert not report.ok


def test_a_failed_verification_writes_nothing(tmp_path: Path, plan, monkeypatch) -> None:
    def broken(*args: object, **kwargs: object):
        presentation = build_presentation(plan)
        del presentation.cues[0]
        return presentation

    monkeypatch.setattr("pcci.convert.build_presentation", broken)
    output = tmp_path / "song.pro"
    with pytest.raises(VerificationFailedError):
        build(plan, output)
    assert not output.exists()
    assert not list(tmp_path.glob(".*tmp"))


def test_convert_writes_everything(tmp_path: Path, fixtures_dir: Path) -> None:
    output = tmp_path / "Goodbye Yesterday.pro"
    result = convert(fixtures_dir / CHART, output, ConversionConfig(), write_chordpro=True)
    assert output.exists()
    assert result.chordpro_path is not None and result.chordpro_path.exists()
    assert len(result.chart_pages) == 3
    assert all(page.exists() for page in result.chart_pages)
    assert all(page.suffix == ".png" for page in result.chart_pages)


def test_chart_pages_are_referenced_by_both_paths(tmp_path: Path, fixtures_dir: Path) -> None:
    output = tmp_path / "song.pro"
    convert(fixtures_dir / CHART, output, ConversionConfig())
    presentation = load_bindings().presentation.Presentation()
    presentation.ParseFromString(output.read_bytes())
    charts = [
        action.slide.presentation.chord_chart
        for cue in presentation.cues
        for action in cue.actions
        if action.slide.presentation.HasField("chord_chart")
    ]
    assert charts, "chord chart references should be written by default"
    first = charts[0]
    assert first.absolute_string.startswith("file://")
    assert first.local.root == 10  # ROOT_SHOW
    assert first.local.path.startswith("Media/Imported/")


def test_notes_only_mode_writes_no_images(tmp_path: Path, fixtures_dir: Path) -> None:
    output = tmp_path / "song.pro"
    config = ConversionConfig(chord_delivery=ChordDelivery.NOTES)
    result = convert(fixtures_dir / CHART, output, config)
    assert result.chart_pages == []
    assert not list(tmp_path.glob("*.png"))


def test_chords_can_be_switched_off(tmp_path: Path, fixtures_dir: Path) -> None:
    output = tmp_path / "song.pro"
    convert(fixtures_dir / CHART, output, ConversionConfig(chord_delivery=ChordDelivery.NONE))
    presentation = load_bindings().presentation.Presentation()
    presentation.ParseFromString(output.read_bytes())
    assert not any(
        action.slide.presentation.notes.rtf_data
        for cue in presentation.cues
        for action in cue.actions
    )


def test_output_extension_is_forced(tmp_path: Path, fixtures_dir: Path) -> None:
    result = convert(fixtures_dir / CHART, tmp_path / "song.txt", ConversionConfig())
    assert result.output_path.suffix == ".pro"


def test_chord_row_reconstructs_positions() -> None:
    from pcci.ir import ChordPlacement, Line

    line = Line(
        lyrics="Amazing grace how sweet the sound",
        chords=[
            ChordPlacement(chord="C", char_index=0),
            ChordPlacement(chord="G/B", char_index=8),
            ChordPlacement(chord="Am", char_index=18),
        ],
    )
    assert chord_row(line) == "C       G/B       Am"
    assert render_lines([line], ChordPlacementStyle.ABOVE).splitlines() == [
        "C       G/B       Am",
        "Amazing grace how sweet the sound",
    ]


def test_the_default_notes_keep_each_chord_over_its_word() -> None:
    """The default is alignment, not compactness.

    A chord's column is the whole point of a chord chart: it says which syllable the
    change lands on. The notes reproduce that and leave the lyrics out, because they
    are already on the slide and repeating them halves the size a stage screen can
    render the block at.
    """
    from pcci.ir import ChordPlacement, Line

    lines = [
        Line(
            lyrics="Again and again and again",
            chords=[
                ChordPlacement(chord="D", char_index=0),
                ChordPlacement(chord="E", char_index=11),
                ChordPlacement(chord="F#m", char_index=21),
            ],
        ),
        Line(lyrics="You rescued me", chords=[ChordPlacement(chord="Bm", char_index=0)]),
    ]
    assert render_lines(lines).splitlines() == [
        "D          E         F#m",
        "Bm",
    ]


def test_inline_row_is_horizontal() -> None:
    """The one-row style is still there for anyone who wants the largest text."""
    from pcci.ir import ChordPlacement, Line

    lines = [
        Line(lyrics="Again and again", chords=[ChordPlacement(chord="A", char_index=0)]),
        Line(lyrics="You rescued me", chords=[ChordPlacement(chord="D", char_index=0)]),
        Line(lyrics="You traded my sorrow", chords=[ChordPlacement(chord="A/C#", char_index=0)]),
    ]
    row = render_lines(lines, ChordPlacementStyle.CHORDS_INLINE)
    assert row == "A    D    A/C#"
    assert "\n" not in row


def test_inline_row_groups_a_line_s_chords_together() -> None:
    from pcci.ir import ChordPlacement, Line

    lines = [
        Line(
            lyrics="Again and again and again",
            chords=[
                ChordPlacement(chord="D", char_index=0),
                ChordPlacement(chord="E", char_index=11),
                ChordPlacement(chord="F#m", char_index=21),
            ],
        ),
        Line(lyrics="You rescued me", chords=[ChordPlacement(chord="Bm", char_index=0)]),
    ]
    assert render_lines(lines, ChordPlacementStyle.CHORDS_INLINE) == "D E F#m    Bm"


def test_inline_row_skips_lines_with_no_chords_and_keeps_annotations() -> None:
    from pcci.ir import ChordPlacement, Line

    lines = [
        Line(lyrics="Again", chords=[ChordPlacement(chord="A", char_index=0)]),
        Line(lyrics="a line with no chords"),
        Line(lyrics="last", chords=[ChordPlacement(chord="D", char_index=0)], annotation="x4"),
    ]
    assert render_lines(lines, ChordPlacementStyle.CHORDS_INLINE) == "A    D    (x4)"


def test_chords_can_be_placed_below() -> None:
    from pcci.ir import ChordPlacement, Line

    line = Line(lyrics="Amazing", chords=[ChordPlacement(chord="C", char_index=0)])
    assert render_lines([line], ChordPlacementStyle.BELOW).splitlines() == ["Amazing", "C"]


def test_chords_only_keeps_one_row_per_line() -> None:
    """Row n of the notes is chord row n of the slide, even where a line has none."""
    from pcci.ir import ChordPlacement, Line

    lines = [
        Line(lyrics="Amazing grace", chords=[ChordPlacement(chord="C", char_index=0)]),
        Line(lyrics="how sweet the sound"),
        Line(lyrics="that saved a wretch", chords=[ChordPlacement(chord="G", char_index=5)]),
    ]
    rendered = render_lines(lines, ChordPlacementStyle.CHORDS_ONLY).split("\n")
    assert rendered == ["C", "", "     G"]


def test_the_chart_always_carries_the_lyrics(fixtures_dir: Path) -> None:
    """The notes may be chords only; the chord chart is still a chord chart."""
    from pcci.notes import render_song

    text = render_song(analyze(fixtures_dir / CHART))
    assert "Goodbye yesterday" in text
    assert "Asus" in text


def test_two_chords_at_the_same_index_both_survive() -> None:
    from pcci.ir import ChordPlacement, Line

    line = Line(
        lyrics="riff",
        chords=[
            ChordPlacement(chord="A", char_index=0),
            ChordPlacement(chord="Bm", char_index=0),
        ],
    )
    assert chord_row(line) == "A Bm"


def test_rtf_escaping() -> None:
    assert escape("plain") == "plain"
    assert escape("a\\b{c}") == "a\\\\b\\{c\\}"
    assert escape("café") == "caf\\u233?"
    assert escape("’") == "\\u8217?"


def test_rtf_colour_table_matches_the_configured_colour() -> None:
    from pcci.propresenter.rtf import build_rtf

    rtf = build_rtf(["x"], font=FontSpec(), colour=RGBA(red=1.0, green=0.5, blue=0.0)).decode()
    assert "\\red255\\green128\\blue0" in rtf
    assert "\\csgenericrgb\\c100000\\c50000\\c0" in rtf
