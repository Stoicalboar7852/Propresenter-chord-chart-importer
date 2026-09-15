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

GOLDEN_CASES: dict[str, str] = {
    "GOODBYE YESTERDAY A.docx": "goodbye_yesterday_docx.json",
    "AMAZING.docx": "amazing_docx.json",
    "PRODIGAL.docx": "prodigal_docx.json",
    "WASHED D.docx": "washed_docx.json",
    "IN THE RIVER.docx": "in_the_river_docx.json",
    "text/goodbye_yesterday.txt": "goodbye_yesterday_txt.json",
    "pdf/goodbye_yesterday.pdf": "goodbye_yesterday_pdf.json",
    "chordpro/goodbye_yesterday.cho": "goodbye_yesterday_cho.json",
    "adversarial/no_headers.txt": "no_headers_txt.json",
    "adversarial/abbreviations.txt": "abbreviations_txt.json",
    "adversarial/nashville.txt": "nashville_txt.json",
    "adversarial/chord_only_intro.txt": "chord_only_intro_txt.json",
}


@pytest.mark.parametrize(("fixture", "golden_name"), sorted(GOLDEN_CASES.items()))
def test_song_matches_its_golden_snapshot(
    fixtures_dir: Path, golden_dir: Path, fixture: str, golden_name: str
) -> None:
    song = analyze(fixtures_dir / fixture)
    produced = json.loads(song.to_json().replace(str(fixtures_dir), "<fixtures>"))
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
