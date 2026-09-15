"""Phase 0 guard rails.

If the vendored schema ever drifts from the ProPresenter build that produced the
reference exports, these tests fail before the writer can produce a plausible-looking
but wrong file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pcci.config import ConversionConfig
from pcci.ir import SectionType
from pcci.propresenter.bindings import PROTO_SOURCE_BUILD, load_bindings

REFERENCE_FILES = [
    "Goodbye Yesterday blank with groups.pro",
    "Goodbye Yesterday With slide notes.pro",
]


def load(path: Path):
    bindings = load_bindings()
    presentation = bindings.presentation.Presentation()
    payload = path.read_bytes()
    presentation.ParseFromString(payload)
    return presentation, payload


@pytest.mark.parametrize("name", REFERENCE_FILES)
def test_reference_files_round_trip_byte_identically(reference_dir: Path, name: str) -> None:
    presentation, payload = load(reference_dir / name)
    assert presentation.SerializeToString() == payload


@pytest.mark.parametrize("name", REFERENCE_FILES)
def test_reference_files_have_no_unknown_fields(reference_dir: Path, name: str) -> None:
    """Nothing in the file falls outside the vendored schema.

    ``UnknownFields()`` is not implemented by the upb runtime, so this asks the
    question a different way: discard anything unknown and see whether the bytes
    change. They do not, so the schema covers every field ProPresenter wrote.
    """
    presentation, payload = load(reference_dir / name)
    presentation.DiscardUnknownFields()
    assert presentation.SerializeToString() == payload


def test_slide_notes_live_where_format_notes_says(reference_dir: Path) -> None:
    presentation, _ = load(reference_dir / "Goodbye Yesterday With slide notes.pro")
    notes = [
        action.slide.presentation.notes.rtf_data
        for cue in presentation.cues
        for action in cue.actions
        if action.slide.presentation.notes.rtf_data
    ]
    assert notes, "expected the reference export to carry per-slide notes"
    assert all(rtf.startswith(b"{\\rtf1") for rtf in notes)
    assert b"This has Slide notes For Claude" in notes[0]


def test_group_colours_match_the_documented_defaults(reference_dir: Path) -> None:
    presentation, _ = load(reference_dir / "Goodbye Yesterday blank with groups.pro")
    by_name = {cue_group.group.name: cue_group.group for cue_group in presentation.cue_groups}
    config = ConversionConfig()

    verse_one = by_name["Verse 1"].color
    expected = config.colour_for(SectionType.VERSE, 1)
    assert (verse_one.red, verse_one.green, verse_one.blue) == pytest.approx(
        (expected.red, expected.green, expected.blue), abs=1e-6
    )

    # ProPresenter's own darkened repeats, reproduced exactly by the 0.75 factor
    # once the result is snapped to the 1/255 grid the application stores.
    for name, section_type in (("Verse 2", SectionType.VERSE), ("Bridge 2", SectionType.BRIDGE)):
        observed = by_name[name].color
        shaded = config.colour_for(section_type, 2)
        assert (observed.red, observed.green, observed.blue) == pytest.approx(
            (shaded.red, shaded.green, shaded.blue), abs=1e-6
        ), name


def test_repeated_sections_share_one_application_group(reference_dir: Path) -> None:
    presentation, _ = load(reference_dir / "Goodbye Yesterday blank with groups.pro")
    chorus_two = [cg.group for cg in presentation.cue_groups if cg.group.name == "Chorus 2"]
    assert len(chorus_two) > 1, "reference should contain a repeated group"
    assert len({g.uuid.string for g in chorus_two}) == len(chorus_two)
    assert len({g.application_group_identifier.string for g in chorus_two}) == 1


def test_every_cue_belongs_to_exactly_one_group(reference_dir: Path) -> None:
    presentation, _ = load(reference_dir / "Goodbye Yesterday blank with groups.pro")
    referenced = [
        uuid.string for cue_group in presentation.cue_groups for uuid in cue_group.cue_identifiers
    ]
    assert len(referenced) == len(set(referenced))
    assert set(referenced) == {cue.uuid.string for cue in presentation.cues}


def test_vendored_schema_matches_the_reference_build(reference_dir: Path) -> None:
    presentation, _ = load(reference_dir / "Goodbye Yesterday With slide notes.pro")
    assert presentation.application_info.application_version.build == PROTO_SOURCE_BUILD
