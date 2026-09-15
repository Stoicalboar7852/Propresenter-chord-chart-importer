"""What the golden snapshots cover, and how a Song is normalised before comparison.

Shared by ``tests/test_golden.py`` and ``scripts/update_golden.py`` so the two can
never disagree about either the case list or the normalisation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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


def normalise(song_json: str, fixtures_dir: Path) -> dict[str, Any]:
    """Make a snapshot independent of where — and on which platform — it was made.

    ``source_path`` becomes a fixtures-relative POSIX path. Without this, a snapshot
    written on one machine can never match another, and a Linux snapshot can never
    match Windows, which writes ``\\`` separators.
    """
    payload: dict[str, Any] = json.loads(song_json)
    source = payload.get("source_path")
    if source:
        path = Path(source)
        try:
            relative = path.resolve().relative_to(fixtures_dir.resolve())
        except ValueError:
            relative = Path(path.name)
        payload["source_path"] = relative.as_posix()
    return payload
