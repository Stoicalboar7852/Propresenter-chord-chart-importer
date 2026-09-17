#!/usr/bin/env python3
"""One version number, in the five places that have to agree about it.

    python scripts/check_version.py
    python scripts/check_version.py --expect 0.2.0

The version is spelled out in the engine package, its project file, the Windows
installer authoring, the installer build script's default and the Mac app's Info.plist.
Nothing makes them agree, and a release where the Mac says 0.1.0 and Windows says 0.2.0
is the sort of thing nobody notices until somebody asks which version they are running.

Also checks that CHANGELOG.md has an entry for it, because a release with notes reading
"no changelog entry for this version" is a release somebody forgot to write up.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: file -> (what a human calls it, the pattern whose first group is the version)
SOURCES: dict[str, tuple[str, str]] = {
    "core/pcci/__init__.py": ("the engine package", r'__version__\s*=\s*"([^"]+)"'),
    "core/pyproject.toml": ("the engine project file", r'^version\s*=\s*"([^"]+)"'),
    "installer/windows/Pcci.iss": ("the Windows installer", r'#define AppVersion "([^"]+)"'),
    "scripts/build-installer.ps1": ("the installer script", r"\[string\]\$Version = '([^']+)'"),
    "macos/Resources/Info.plist": (
        "the Mac app",
        r"<key>CFBundleShortVersionString</key>\s*<string>([^<]+)</string>",
    ),
}


def found_versions() -> dict[str, tuple[str, str]]:
    """Every declared version: file -> (description, version)."""
    versions: dict[str, tuple[str, str]] = {}
    for name, (description, pattern) in SOURCES.items():
        path = REPO_ROOT / name
        if not path.exists():
            versions[name] = (description, "missing file")
            continue
        match = re.search(pattern, path.read_text(encoding="utf-8"), re.M)
        versions[name] = (description, match.group(1) if match else "not found")
    return versions


def has_changelog_entry(version: str) -> bool:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return False
    wanted = version.lstrip("vV")
    for line in changelog.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and wanted in line:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect", default=None, help="The version everything should say.")
    arguments = parser.parse_args()

    versions = found_versions()
    for name, (description, version) in sorted(versions.items()):
        print(f"  {version:<12} {description}  ({name})")

    distinct = {version for _, version in versions.values()}
    problems: list[str] = []
    if len(distinct) != 1:
        problems.append("these do not all say the same thing: " + ", ".join(sorted(distinct)))

    version = next(iter(distinct)) if len(distinct) == 1 else ""
    expected = arguments.expect.lstrip("vV") if arguments.expect else None
    if expected and version and version != expected:
        problems.append(f"expected {expected}, found {version}")
    if version and not has_changelog_entry(version):
        problems.append(f"CHANGELOG.md has no section for {version}")

    print()
    if problems:
        for problem in problems:
            print(f"FAIL  {problem}", file=sys.stderr)
        return 1
    print(f"Everything says {version}, and the changelog has an entry for it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
