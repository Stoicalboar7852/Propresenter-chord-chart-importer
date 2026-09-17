#!/usr/bin/env python3
"""Will these songs actually import? A dry run for a set list.

    python scripts/probe_online.py "Great Are You Lord" "Uptown Funk"
    python scripts/probe_online.py --file setlist.txt --convert

Searches for each title, reports what came back and from where, and with --convert
goes the whole way to a .pro so the answer is "yes, 14 slides" rather than "probably".

This needs the internet, so it is a script you run rather than part of the test suite.
It is also the honest way to answer "does this work for the songs *we* sing", which no
amount of testing against recorded fixtures can.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from pcci.convert import convert  # noqa: E402
from pcci.errors import PcciError  # noqa: E402
from pcci.online import Cache, Http, search  # noqa: E402
from pcci.online.retrieve import import_url  # noqa: E402


def probe(title: str, *, http: Http, cache: Cache, do_convert: bool) -> bool:
    """Look one song up and say what happened. True if it could become a presentation."""
    print(f"\n{title}")
    print("-" * len(title))
    try:
        outcome = search(title, limit=6, http=http, cache=cache)
    except PcciError as error:
        print(f"  search failed: {error.user_message}")
        return False

    for note in outcome.notes:
        print(f"  note: {note}")
    if not outcome.results:
        print("  nothing found")
        return False

    for match in outcome.results[:3]:
        mark = "importable" if match.importable else "no words  "
        credits = match.subtitle or "unknown artist"
        print(f"  [{mark}] {match.title} - {credits}")
        print(f"               {match.chart_kind}, via {', '.join(match.source_names)}")

    best = next((match for match in outcome.results if match.importable), None)
    if best is None:
        print("  -> found the song, but no source has words for it")
        return False
    if not do_convert:
        print(f"  -> would import from {best.sources[0].name}")
        return True

    try:
        with tempfile.TemporaryDirectory() as directory:
            path, chart = import_url(best.chart_url or "", Path(directory), http=http, cache=cache)
            result = convert(path, Path(directory) / "probe.pro")
    except PcciError as error:
        print(f"  -> import failed: {error.user_message}")
        return False

    sections = ", ".join(section.label for section in result.plan.song.sections[:6])
    print(
        f"  -> {result.plan.slide_count} slides, "
        f"{len(result.plan.song.sections)} sections, "
        f"{result.plan.song.chord_count} chords" + ("" if chart.has_chords else "  (lyrics only)")
    )
    print(f"     {sections}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("songs", nargs="*", help="Song titles to look up.")
    parser.add_argument("--file", type=Path, default=None, help="A file of titles, one per line.")
    parser.add_argument(
        "--convert", action="store_true", help="Go the whole way to a .pro for each."
    )
    arguments = parser.parse_args()

    titles = list(arguments.songs)
    if arguments.file:
        titles += [line.strip() for line in arguments.file.read_text().splitlines() if line.strip()]
    if not titles:
        parser.error("give it some song titles, or --file")

    http = Http()
    cache = Cache()
    worked = [
        title
        for title in titles
        if probe(title, http=http, cache=cache, do_convert=arguments.convert)
    ]

    print(f"\n{len(worked)} of {len(titles)} could become a presentation.")
    for title in titles:
        if title not in worked:
            print(f"  not this one: {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
