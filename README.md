# ProPresenter Chord Chart Importer (`pcci`)

Turn a worship chord chart — Word, PDF, plain text, ChordPro, RTF, ODT, HTML — into a
ProPresenter 7 `.pro` presentation with named, colour-coded groups, an arrangement, and
the chords carried through to the stage screen without ever reaching audience output.

The project is a headless Python engine plus two native front-ends:

| Part | What it is |
|---|---|
| `core/` | The engine. Pure Python 3.12, no GUI dependencies, importable as a library and runnable as the `pcci` CLI. |
| `macos/` | SwiftUI app, macOS 26 Liquid Glass where available, macOS 14 deployment target. |
| `windows/` | WinUI 3 / .NET 8 app, Mica Alt, Fluent dark. |
| `scripts/` | Build and code-generation scripts. |
| `docs/` | Format reconnaissance, stage setup guide, build prompt. |

## Install it

Pick your machine. Each page covers what to install first, how to build, and what to do
about the unsigned-app warning on first launch.

| | |
|---|---|
| **macOS** | **[docs/INSTALL_MACOS.md](docs/INSTALL_MACOS.md)** — needs full Xcode for the app, Python 3.12+ for the engine. Right-click → Open the first time. |
| **Windows** | **[docs/INSTALL_WINDOWS.md](docs/INSTALL_WINDOWS.md)** — needs the .NET 8 SDK for the app, Python 3.12+ for the engine. x64 and ARM64. |
| **Stage screen** | **[docs/STAGE_SETUP.md](docs/STAGE_SETUP.md)** — the ProPresenter side: getting the chords onto a stage display and nowhere near the audience. |
| **Checking a build** | **[docs/ACCEPTANCE.md](docs/ACCEPTANCE.md)** — the manual pass before you trust it on a Sunday. |
| **The file format** | **[docs/FORMAT_NOTES.md](docs/FORMAT_NOTES.md)** — what is actually inside a `.pro`, every claim read out of a real export. |
| **The original brief** | **[docs/BUILD_PROMPT.md](docs/BUILD_PROMPT.md)** — the plan this was built from. |

Not sure what a machine is missing? `./scripts/install-deps.sh` (or
`.\scripts\install-deps.ps1`) checks for Python, the .NET SDK and Xcode, and offers to
install what it can.

## Getting set up

```bash
./scripts/setup-engine.sh          # or .\scripts\setup-engine.ps1 on Windows
```

It finds a Python 3.12 or newer, builds `core/.venv`, installs the engine and checks the
result runs. Add `--dev` (`-Dev` on Windows) for the test and lint tooling. The platform
build scripts call it themselves when the environment is missing, so
`./scripts/build-macos.sh` alone is enough to get an app.

## Downloading a build instead of making one

Every push to the default branch builds all three targets on GitHub's runners and
attaches them to the run:

**[Actions -> Build all](https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/actions/workflows/build-all.yml)**
-> the newest run -> **Artifacts**

| Artifact | What is in it |
|---|---|
| `PCCI-windows-x64` | The app as a zip, and a setup program. Intel and AMD machines. |
| `PCCI-windows-arm64` | The same, for ARM machines (Snapdragon, and Windows on Apple silicon). |
| `PCCI-macos-arm64` | `PCCI.dmg`, Apple silicon. |

Artifacts keep for 90 days and need a GitHub account to download, which is fine for
you and awkward for anyone you hand this to. **Releases** have neither limit: push a
`v*` tag and `release.yml` builds the same three and attaches them to a release page
that anybody can download from, permanently.

```bash
git tag v0.1.0 && git push origin v0.1.0
```

Or, without a tag to hand: **Actions -> Release -> Run workflow**, give it a version,
and it creates the tag on whatever it built.

Nothing has to be installed locally for either: GitHub's macOS runners come with Xcode
and its Windows runners with the .NET SDK, which is exactly why this works.

## Building for a machine you are not sitting at

The engine cannot be cross-compiled. PyInstaller freezes using the interpreter it runs
on, so a Windows engine has to be built on Windows and an ARM64 one on ARM64, and the
Mac app needs Xcode, which needs a Mac. Rather than pretend otherwise, one command
starts each build on a machine that can do it:

```bash
./scripts/build-all.sh --wait          # or .\scripts\build-all.ps1 -Wait
```

That runs the **Build all** workflow — Windows x64, Windows ARM64, macOS — and downloads
the zips, installers and disk image into `build/remote/`. Without the GitHub CLI
installed, start it from **Actions → Build all → Run workflow** instead.

On one machine you can still cross-build within Windows: `-Architecture win-x64` on an
ARM64 machine rebuilds the engine environment around an x64 interpreter if you have one
installed, and says so if you do not.

## Converting charts

```bash
core/.venv/bin/pcci convert "My Song.docx" -o "My Song.pro" --lines-per-slide 4
core/.venv/bin/pcci convert-all "Sunday 12th" -d "out" --lines-per-slide 4
```

`convert-all` takes files, folders, or both, and writes every presentation into one
folder. Both apps have the same thing behind a Convert All button.

```bash
cd core
.venv/bin/python -m pytest
.venv/bin/ruff check . && .venv/bin/mypy pcci
```

## Inspecting a real ProPresenter file

```bash
core/.venv/bin/python scripts/dump_pro.py "core/tests/reference/Goodbye Yesterday With slide notes.pro"
core/.venv/bin/python scripts/dump_pro.py <file> --cue 12     # one slide, full message tree
```

## Where the format knowledge comes from

`docs/FORMAT_NOTES.md`. Every claim in it is read out of a real export from
ProPresenter 21.4 and is reproducible with the command above. The protobuf definitions
are vendored from a schema generated from the same build — see
`core/pcci/propresenter/proto/PROVENANCE.md`.

## Status

| Part | State |
|---|---|
| Format reconnaissance | Done. All three reference exports round-trip byte-identically; findings in `docs/FORMAT_NOTES.md`. |
| Engine | Done. Every format, detection, slide planning, writer, verifier, CLI. |
| macOS app | Written and compiling; not yet run on a Mac. |
| Windows app | Written; building in CI. |
| Packaging | Engine freezes and self-checks; both apps build unsigned. |

Verified in real ProPresenter 21.4 so far: the exported `.pro` imports, groups and
slides come through, and the chord chart appears in the editor.

## The icon

`assets/icon.png` is the master. To change it, replace that file and run:

```bash
core/.venv/bin/python scripts/make_icons.py
```

That regenerates `macos/Resources/AppIcon.icns` and `windows/Pcci/Assets/AppIcon.ico`
from it. CI fails if they drift apart.
