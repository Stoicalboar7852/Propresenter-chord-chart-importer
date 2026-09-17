# ProPresenter Chord Chart Importer (`pcci`)

Turn a worship chord chart — Word, PDF, plain text, ChordPro, RTF, ODT, HTML — into a
ProPresenter 7 `.pro` presentation with named, colour-coded groups, an arrangement, and
the chords carried through to the stage screen without ever reaching audience output.

Four ways to get a song in:

- **Drop a file on the window**, in any of the formats above.
- **Search for it by name.** Every source is asked at once and the answers merged into
  one row per song, with its cover art and the names of the sites each part came from.
- **Paste a link.** A chord site, a church's own page, a Google Doc published to the
  web, a ChordPro file in a repository.
- **Paste the chart itself**, the way ProPresenter's own clipboard import works.
  Cmd+Shift+V on a Mac, Ctrl+Shift+V on Windows.

A chart with no chords in it — a hymn text, a lyrics sheet — converts just the same.

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
| **What changed** | **[CHANGELOG.md](CHANGELOG.md)** — every release, and what went into it. |
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

### Songs from the web

```bash
pcci search "be thou my vision"            # every source, merged, one row per song
pcci search https://example.com/chart      # a pasted link, described
pcci fetch  https://example.com/chart -o "Be Thou My Vision.pro"
pbpaste | pcci paste -o "Be Thou My Vision.pro"     # Get-Clipboard on Windows
```

`search` asks Apple Music for the artwork and the credits, and the chord and lyric
sites for the words, then merges them into one row per song. A site that is down, slow
or refusing us adds a note and the search returns whatever the others found.

`fetch` and `paste` write a chart file and print where it went, so `analyze`, `plan`
and `build` then work on it exactly as they would on a file you dropped in yourself —
there is no separate conversion path for songs that came off the web. Add `-o` to go
straight to a presentation.

Downloaded pages are cached for a day so that searching and then importing is one
request rather than two. `pcci cache` says where that is; `pcci cache --clear` empties
it, which is what to do if a site has corrected a chart and you keep getting the old one.

**On the sources.** Only Apple Music's is a documented public API. The others are read
the way a browser reads them, which means they can change shape or refuse a program
outright without notice — so no result is ever the only way in.

| Source | Supplies | Key needed | Last checked against the live site |
|---|---|---|---|
| Ultimate Guitar | Chords and words | no | Answers |
| LRCLIB | Words, for anything with no chord chart | no | Open API, built to be read by software |
| Apple Music | Cover art, album, year, the artist's own spelling | no | Answers |
| Musixmatch | Words | **yes** | Dormant unless `PCCI_MUSIXMATCH_KEY` is set. Its free plan returns about 30% of a song, which is not a presentation — the import says so when that happens. |
| Genius | Words | no | **Refuses an automated request** (403). May work from a home connection; it would not talk to a GitHub runner. |

LRCLIB and Musixmatch store words with no section headings, so verses and choruses are
guessed from the blank lines and flagged on the review screen for you to name.

Coverage is not worship-only: a run across Great Are You Lord, Washed, Uptown Funk,
Bohemian Rhapsody, Shivers and Amazing Grace turned all six into presentations with
their sections intact. To check your own set list before you rely on it:

```bash
python scripts/probe_online.py --convert "Washed" "Great Are You Lord" "Build My Life"
```

When a site says no, the message says which one and points at the clipboard, which
always works: open the page yourself, select the chart, copy, paste. A weekly
[Online sources](https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/actions/workflows/online.yml)
workflow re-checks that table — a site that answers but has *changed shape* fails it,
while one that simply refuses is recorded as a skip, because that is the state of the
world rather than something to fix.

Lyrics are somebody's copyright. What this does is fetch a page you asked for and
reformat it for your own screens, which is what a worship team's CCLI licence is
generally for — the licence is yours to hold, not the tool's.

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
| Songs from the web | Search, a pasted link and the clipboard, in the engine and both apps. Offline tests against recorded shapes; a weekly job checks the live sites. |
| macOS app | Written and compiling; not yet run on a Mac. |
| Windows app | Written and compiling; not yet run on a PC. |
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
