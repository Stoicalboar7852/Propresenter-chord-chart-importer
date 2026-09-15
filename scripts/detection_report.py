#!/usr/bin/env python3
"""Report what detection made of every fixture.

    core/.venv/bin/python scripts/detection_report.py [--verbose]

Prints one block per chart: the title, the sections with their confidence, and any
line that looks like a detection mistake. The point is to be able to see accuracy
across the whole corpus at a glance rather than trusting a single example.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from pcci.errors import PcciError  # noqa: E402
from pcci.ir import Song  # noqa: E402
from pcci.parse.chords import LineClass, classify_line  # noqa: E402
from pcci.parse.pipeline import analyze  # noqa: E402

FIXTURES = REPO_ROOT / "core" / "tests" / "fixtures"


def suspicious_lines(song: Song) -> list[str]:
    """Lines that suggest detection went wrong."""
    problems: list[str] = []
    for section in song.sections:
        for line in section.lines:
            if not line.lyrics:
                continue
            if classify_line(line.lyrics) is LineClass.CHORD:
                problems.append(f"chords projected as a lyric in {section.label}: {line.lyrics!r}")
            if any(marker in line.lyrics.lower() for marker in ("hold ", " bars", "repeat ")):
                problems.append(f"instruction inside a lyric in {section.label}: {line.lyrics!r}")
    return problems


def report(path: Path, *, verbose: bool) -> tuple[int, int]:
    """Print one chart's result. Returns (sections, problems)."""
    try:
        song = analyze(path)
    except PcciError as error:
        print(f"\n=== {path.name}\n    ERROR {type(error).__name__}: {error.user_message}")
        return 0, 1

    labelled = sum(1 for section in song.sections if section.confidence >= 0.95)
    guessed = len(song.sections) - labelled
    lyrics = sum(1 for s in song.sections for line in s.lines if line.lyrics)
    chords = song.chord_count
    print(f"\n=== {path.name}")
    print(f"    title      {song.title!r}" + (f"  artist {song.artist!r}" if song.artist else ""))
    print(
        f"    sections   {len(song.sections)}  "
        f"({labelled} from labels, {guessed} guessed)   "
        f"lyric lines {lyrics}   chords {chords}"
    )
    print(
        "    detected   "
        + ", ".join(
            f"{section.label}{'' if section.confidence >= 0.95 else f'?{section.confidence:g}'}"
            for section in song.sections
        )
    )
    problems = suspicious_lines(song)
    for problem in problems:
        print(f"    !! {problem}")
    if verbose:
        for section in song.sections:
            print(f"    -- {section.label}")
            for line in section.lines:
                chord_text = " ".join(f"{c.chord}@{c.char_index}" for c in line.chords)
                print(f"       [{chord_text}] {line.lyrics!r}" + (f"  ({line.annotation})" if line.annotation else ""))
    return len(song.sections), len(problems)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()

    paths = args.paths or [
        *sorted(FIXTURES.glob("*.docx")),
        *sorted(FIXTURES.glob("text/*")),
        *sorted(FIXTURES.glob("html/*")),
        *sorted(FIXTURES.glob("rtf/*")),
        *sorted(FIXTURES.glob("odt/*")),
        *sorted(p for p in FIXTURES.glob("pdf/*") if "scanned" not in p.name),
        *sorted(FIXTURES.glob("chordpro/*")),
        *sorted(FIXTURES.glob("adversarial/*")),
    ]

    total_sections = total_problems = 0
    for path in paths:
        sections, problems = report(path, verbose=args.verbose)
        total_sections += sections
        total_problems += problems
    print(f"\n{len(paths)} charts, {total_sections} sections, {total_problems} suspicious lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
