#!/usr/bin/env python3
"""Assemble the text that goes on a GitHub release page.

    python scripts/release_notes.py --version v0.2.0 > notes.md

Two pieces. The changelog entry for the version being released, lifted out of
CHANGELOG.md, goes at the top: it is the part somebody actually wants to read, and it
is written by a person rather than derived from commit subjects. Below it goes the
standing advice - which file to download, what each operating system will say about an
unsigned app, how to get chords onto a stage screen - which is the same every time and
so lives in docs/RELEASE_NOTES_TEMPLATE.md rather than being retyped.

A version with no changelog entry still gets notes: the commits since the previous tag,
which is better than nothing and is a fairly obvious prompt to go and write the entry.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
TEMPLATE = REPO_ROOT / "docs" / "RELEASE_NOTES_TEMPLATE.md"
PLACEHOLDER = "{{CHANGELOG}}"

#: "## [0.2.0] - 2026-09-17", with either kind of dash and with or without the brackets.
_HEADING = re.compile(r"^##\s+\[?(?P<version>[^\]\s]+)\]?(?P<rest>.*)$")


def normalise(version: str) -> str:
    """``v0.2.0`` and ``0.2.0`` are the same version."""
    return version.strip().lstrip("vV")


def section_for(version: str, changelog: str) -> str | None:
    """The body of the changelog section for a version, or None if there isn't one."""
    wanted = normalise(version)
    lines = changelog.splitlines()
    collected: list[str] = []
    inside = False

    for line in lines:
        heading = _HEADING.match(line)
        if heading:
            if inside:
                break
            inside = normalise(heading.group("version")) == wanted
            continue
        if inside:
            collected.append(line)

    if not inside and not collected:
        return None
    body = "\n".join(collected).strip()
    return body or None


def commits_since_previous_tag(version: str) -> str:
    """Fallback: what went in since the last release, as the commits say it."""
    tag = version if version.startswith("v") else f"v{version}"
    try:
        previous = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0", f"{tag}^"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
    except OSError:
        previous = ""

    span = f"{previous}..{tag}" if previous else tag
    result = subprocess.run(
        ["git", "log", "--no-merges", "--pretty=format:- %s", span],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    subjects = result.stdout.strip()
    if not subjects:
        return "_No changelog entry for this version._"
    return (
        "_No changelog entry for this version, so here are the commits:_\n\n" + subjects
    )


def build(version: str) -> str:
    changelog = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
    body = section_for(version, changelog) or commits_since_previous_tag(version)
    entry = f"## What's new in {version}\n\n{body}"

    if not TEMPLATE.exists():
        return entry + "\n"
    template = strip_comments(TEMPLATE.read_text(encoding="utf-8"))
    if PLACEHOLDER not in template:
        return entry + "\n\n" + template
    return template.replace(PLACEHOLDER, entry)


def strip_comments(template: str) -> str:
    """Drop the HTML comments that tell an editor how the template works.

    They are invisible on a rendered release page either way, but they are also the
    first thing in the raw text, and somebody reading the notes through the API should
    not have to scroll past instructions meant for whoever edits the file.
    """
    return re.sub(r"<!--.*?-->\s*", "", template, flags=re.DOTALL).lstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="The version being released, e.g. v0.2.0.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Where to write the notes. Defaults to standard output.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only report whether this version has a written changelog entry.",
    )
    arguments = parser.parse_args()

    if arguments.check:
        changelog = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
        if section_for(arguments.version, changelog):
            print(f"{arguments.version} has a changelog entry.")
            return 0
        print(f"{arguments.version} has no section in CHANGELOG.md.", file=sys.stderr)
        return 1

    notes = build(arguments.version)
    if arguments.output:
        arguments.output.write_text(notes, encoding="utf-8")
        print(f"wrote {arguments.output} ({len(notes)} characters)", file=sys.stderr)
    else:
        sys.stdout.write(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
