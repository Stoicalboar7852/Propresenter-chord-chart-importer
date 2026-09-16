#!/usr/bin/env python3
"""Check that the engine installs on Windows without a compiler.

A Windows machine has no C++ or Rust toolchain unless somebody installed one. A
dependency that publishes wheels for other platforms but none for this one sends pip to
the source distribution, and the install dies several minutes later asking for Microsoft
Visual C++ Build Tools. That is how ``pdfplumber`` broke the Windows build: it pulls in
pdfminer.six, which pulls in ``cryptography``, which is written in Rust and ships no
ARM64 wheel.

ARM64 is where this bites, but x64 is checked too: it is the machine most people will
run this on, and "it works on x64" should be something CI knows rather than something
anybody assumes.

The rule this enforces:

* a package with a pure-Python wheel (``py3-none-any``) installs anywhere;
* a package with a wheel for the platform being checked installs there;
* a package with **no** wheels at all is pure Python distributed as a source archive
  (odfpy is one) and builds with nothing more than setuptools;
* a package with platform wheels but none for this platform is a compiler waiting to
  happen, and fails this check.

    python3 scripts/check_windows_arm64.py                      # both, runtime deps
    python3 scripts/check_windows_arm64.py --platform win_arm64
    python3 scripts/check_windows_arm64.py --dev                # and the test tooling

The dev extra is expected to fail: grpcio-tools has no ARM64 wheel. It is only needed
to regenerate the protobuf bindings, which are committed, so nobody has to install it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "core" / "pyproject.toml"
#: Frozen with PyInstaller, so the build needs it on the same machine.
EXTRA_REQUIREMENTS = ("pyinstaller",)
PYPI = "https://pypi.org/pypi/{name}/{version}/json"

#: The two shapes of Windows this project ships for.
PLATFORMS = ("win_amd64", "win_arm64")


def requirements(include_dev: bool) -> list[str]:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    declared: list[str] = list(project["dependencies"])
    if include_dev:
        declared += project["optional-dependencies"]["dev"]
    return declared + list(EXTRA_REQUIREMENTS)


def resolve(declared: list[str]) -> list[tuple[str, str]]:
    """Every package pip would install, transitively, as (name, version)."""
    report = REPO_ROOT / "build" / "arm64-report.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--dry-run",
        "--ignore-installed",
        "--quiet",
        "--report",
        str(report),
        *declared,
    ]
    finished = subprocess.run(command, capture_output=True, text=True, check=False)
    if finished.returncode != 0:
        print(finished.stdout, file=sys.stderr)
        print(finished.stderr, file=sys.stderr)
        raise SystemExit("pip could not resolve the dependencies")
    resolved = json.loads(report.read_text(encoding="utf-8"))["install"]
    report.unlink()
    return sorted((item["metadata"]["name"], item["metadata"]["version"]) for item in resolved)


def release_files(name: str, version: str) -> list[str]:
    url = PYPI.format(name=name, version=version)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f"PyPI has no {name} {version}: {error}") from error
    return [entry["filename"] for entry in payload["urls"]]


def verdict(filenames: list[str], platform: str) -> tuple[bool, str]:
    wheels = [name for name in filenames if name.endswith(".whl")]
    if not wheels:
        return True, "source only, so pure Python"
    if any(name.endswith("-none-any.whl") for name in wheels):
        return True, "pure Python wheel"
    if any(platform in name for name in wheels):
        return True, f"{platform} wheel"
    return False, f"{len(wheels)} wheels, none for {platform}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dev", action="store_true", help="include the dev extra")
    parser.add_argument(
        "--platform",
        choices=PLATFORMS,
        action="append",
        help="check one platform (repeatable). Both by default.",
    )
    arguments = parser.parse_args()
    platforms = tuple(arguments.platform) if arguments.platform else PLATFORMS

    packages = resolve(requirements(arguments.dev))
    # One request per package, not one per package per platform: the answer for every
    # platform is in the same list of filenames.
    releases = {(name, version): release_files(name, version) for name, version in packages}
    print(f"{len(packages)} packages to install\n")

    failed = False
    for platform in platforms:
        print(f"{platform}")
        failures: list[str] = []
        for name, version in packages:
            ok, reason = verdict(releases[(name, version)], platform)
            print(f"  {'ok  ' if ok else 'FAIL'}  {name} {version}: {reason}")
            if not ok:
                failures.append(f"{name} {version}")
        if failures:
            failed = True
            print(f"\n  compiled from source on {platform}: {', '.join(failures)}")
            print("  That machine has no C++ or Rust toolchain, so the install fails.")
        print()

    if failed:
        return 1
    print("Every package installs without a compiler, on both.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
