"""Golden snapshots: fixture in, exact Song JSON out.

These catch the changes no unit test thinks to look for — a chord that moved one
character, a section that quietly merged with its neighbour. Regenerate deliberately
with ``scripts/update_golden.py`` and read the diff.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pcci.ir import Song
from pcci.parse.pipeline import analyze
from tests.golden_cases import GOLDEN_CASES, normalise


@pytest.mark.parametrize(("fixture", "golden_name"), sorted(GOLDEN_CASES.items()))
def test_song_matches_its_golden_snapshot(
    fixtures_dir: Path, golden_dir: Path, fixture: str, golden_name: str
) -> None:
    song = analyze(fixtures_dir / fixture)
    produced = normalise(song.to_json(), fixtures_dir)
    expected = json.loads((golden_dir / golden_name).read_text(encoding="utf-8"))
    assert produced == expected, (
        f"{fixture} no longer matches {golden_name}. "
        "If the change is intended, run scripts/update_golden.py and review the diff."
    )


@pytest.mark.parametrize("golden_name", sorted(set(GOLDEN_CASES.values())))
def test_golden_files_are_valid_songs(golden_dir: Path, golden_name: str) -> None:
    song = Song.from_json((golden_dir / golden_name).read_text(encoding="utf-8"))
    assert song.title
    assert song.sections


@pytest.mark.parametrize("golden_name", sorted(set(GOLDEN_CASES.values())))
def test_golden_paths_are_portable(golden_dir: Path, golden_name: str) -> None:
    """A snapshot must not carry the machine that made it."""
    payload = json.loads((golden_dir / golden_name).read_text(encoding="utf-8"))
    source = payload["source_path"]
    assert "\\" not in source, "Windows separators would never match a Linux snapshot"
    assert not Path(source).is_absolute()
