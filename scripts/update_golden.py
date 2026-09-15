#!/usr/bin/env python3
"""Regenerate the golden Song JSON snapshots.

    core/.venv/bin/python scripts/update_golden.py

Run this after a deliberate parser change, then read the diff before committing: it is
the clearest view there is of what a change did to every chart at once.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from pcci.parse.pipeline import analyze  # noqa: E402
from tests.golden_cases import GOLDEN_CASES, normalise  # noqa: E402

FIXTURES = REPO_ROOT / "core" / "tests" / "fixtures"
GOLDEN = REPO_ROOT / "core" / "tests" / "golden"


def main() -> int:
    GOLDEN.mkdir(parents=True, exist_ok=True)
    for fixture, golden_name in GOLDEN_CASES.items():
        song = analyze(FIXTURES / fixture)
        payload = normalise(song.to_json(), FIXTURES)
        (GOLDEN / golden_name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"  {golden_name}: {len(song.sections)} sections, {song.chord_count} chords")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
