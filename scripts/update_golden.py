#!/usr/bin/env python3
"""Regenerate the golden Song JSON snapshots.

    core/.venv/bin/python scripts/update_golden.py

Run this after a deliberate parser change, then read the diff before committing: it is
the clearest view there is of what a change did to every chart at once.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from pcci.parse.pipeline import analyze  # noqa: E402

FIXTURES = REPO_ROOT / "core" / "tests" / "fixtures"
GOLDEN = REPO_ROOT / "core" / "tests" / "golden"

#: Fixture path (relative to tests/fixtures) -> golden file name.
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


def normalise(song_json: str, fixture: str) -> str:
    """Make the snapshot independent of where the repository lives."""
    return song_json.replace(str(FIXTURES), "<fixtures>")


def main() -> int:
    GOLDEN.mkdir(parents=True, exist_ok=True)
    for fixture, golden_name in GOLDEN_CASES.items():
        song = analyze(FIXTURES / fixture)
        (GOLDEN / golden_name).write_text(normalise(song.to_json(), fixture) + "\n", encoding="utf-8")
        print(f"  {golden_name}: {len(song.sections)} sections, {song.chord_count} chords")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
