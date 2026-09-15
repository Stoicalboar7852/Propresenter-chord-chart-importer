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

## Working on the engine

```bash
cd core
uv venv --python 3.12 .venv          # or: python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
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

See `docs/BUILD_PROMPT.md` for the full plan, `docs/ACCEPTANCE.md` for the manual
checklist, and `docs/STAGE_SETUP.md` for getting the chords onto a stage screen.
