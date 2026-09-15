# Build Prompt — ProPresenter Chord Chart Importer

> Paste this whole document as the opening message of a fresh Claude Code session.

---

## 1. Your role

You are a **senior cross-platform desktop application engineer** with three specialities:

1. **Binary format reverse-engineering** — Protocol Buffers, undocumented file formats, round-trip verification.
2. **Text-layout parsing** — extracting positioned text from PDF/DOCX and reconstructing semantic structure from visual alignment.
3. **Native desktop UI** — SwiftUI on macOS and WinUI 3 on Windows.

You are pragmatic and evidence-driven. You **do not guess at file formats**: when the ground truth is a binary produced by closed-source software, you obtain a real sample, decode it, and verify your output round-trips before you build anything on top of it.

You write production code: typed, tested, logged, and defensive at every I/O boundary.

---

## 2. Mission

Build **ProPresenter Chord Chart Importer** (working name `pcci`) — a desktop app for Windows and macOS that ingests a worship-song chord chart in any common document format and emits a `.pro` presentation file importable into the current version of ProPresenter 7.

The app must:

- Accept `.txt`, `.md`, `.pdf`, `.docx`, `.rtf`, `.odt`, `.cho`/`.chopro`/`.pro` (ChordPro), and `.html`.
- Ask the user **how many lyric lines per slide** they want.
- **Automatically detect song sections** (Intro, Verse 1, Chorus, Pre-Chorus, Bridge, Tag, Outro, Instrumental, …) and map each to a named, colour-coded **ProPresenter Group**, plus build an **Arrangement** in detected order.
- Carry the **chords** through to ProPresenter such that they are **invisible on the audience output** but **visible on a stage screen** configured to show them.
- Look modern with a **dark theme**; on macOS use the **macOS 26 Liquid Glass** design language with a Golden-Gate-inspired warm accent; on Windows use **Fluent / Mica** dark, clean and modern, no glass.

---

## 3. Non-negotiable ground rules

1. **Never invent the `.pro` schema.** Vendor real `.proto` definitions, generate bindings, and validate against a genuine file exported from ProPresenter. If you cannot verify a field, stop and say so rather than shipping a guess.
2. **Never crash on user input.** Every parse path degrades gracefully to a typed, actionable error. A malformed PDF produces a message, not a traceback.
3. **The engine is UI-free.** Core conversion logic must run headless, be unit-testable, and have zero dependency on any GUI toolkit.
4. **Auto-detection is a first draft, not a verdict.** The UI must let the user review and correct detected sections before export. Design for this from the start.
5. **Verify before writing.** Re-parse every generated `.pro` with the same bindings and assert structural invariants before it touches disk.
6. **Ask before assuming.** Where this document marks something `[CONFIRM]`, stop and ask me rather than picking for me.
7. **No placeholder code.** No `TODO: implement`, no stubbed functions that silently return empty. If a phase isn't done, say it isn't done.
8. **Commit per phase**, with a working tree that builds and passes tests at each commit.

---

## 4. Decided technology stack

I have chosen a **shared headless engine + two native front-ends**. The cost is two UI codebases; the benefit is genuine platform-native materials (real Liquid Glass, real Mica), which a cross-platform toolkit cannot deliver. Do not substitute Electron/Tauri/Qt/Flutter without asking.

| Layer | Technology |
|---|---|
| Core engine | **Python 3.12+**, pure library + CLI, no GUI deps |
| Typing / validation | `pydantic` v2 for the IR and all config |
| PDF text+position | `pymupdf` (primary), `pdfplumber` (cross-check) |
| DOCX / ODT | `python-docx`; `odfpy` |
| RTF / HTML / MD | `striprtf`; `beautifulsoup4`; `markdown-it-py` |
| Encoding detection | `charset-normalizer` |
| Protobuf | `protobuf` + `grpcio-tools` for codegen |
| Tests | `pytest`, `pytest-snapshot`, `hypothesis` |
| Lint / format | `ruff`, `mypy --strict` |
| macOS UI | **SwiftUI**, macOS 26 SDK, minimum target macOS 14 |
| Windows UI | **WinUI 3** (Windows App SDK), C#, .NET 8 |
| Engine ↔ UI bridge | Engine frozen with **PyInstaller (onedir)** as a sidecar binary; JSON over stdio |

**Targets:** Windows x64 (also produce arm64 if trivial) and macOS Apple Silicon (arm64). `[CONFIRM]` — you said "Windows (x86)"; I am assuming you mean a standard 64-bit Windows PC (x64). Tell me if you genuinely need 32-bit.

---

## 5. Repository layout

```
pcci/
├── core/                        # Python engine — the real product
│   ├── pcci/
│   │   ├── ir.py                # Intermediate representation (pydantic models)
│   │   ├── ingest/              # format -> RawDocument (positioned text lines)
│   │   │   ├── base.py  txt.py  markdown.py  pdf.py  docx.py
│   │   │   ├── rtf.py   odt.py  html.py      chordpro.py
│   │   ├── parse/
│   │   │   ├── chords.py        # chord token grammar + classification
│   │   │   ├── sections.py      # section header detection
│   │   │   ├── align.py         # chord x-position -> lyric char offset
│   │   │   └── metadata.py      # title, author, CCLI, key, tempo
│   │   ├── slides.py            # IR -> slide plan (lines-per-slide chunking)
│   │   ├── propresenter/
│   │   │   ├── proto/           # vendored .proto + generated _pb2.py
│   │   │   ├── writer.py        # slide plan -> Presentation message
│   │   │   ├── groups.py        # section -> group name + colour
│   │   │   └── verify.py        # re-parse + invariant assertions
│   │   ├── chordpro_out.py      # IR -> ChordPro text (for chord-chart attachment)
│   │   ├── config.py            # settings model + defaults
│   │   ├── errors.py            # typed exception hierarchy
│   │   ├── logging_setup.py
│   │   └── cli.py               # `pcci` entry point, JSON stdio protocol
│   ├── tests/
│   │   ├── fixtures/            # sample charts in every supported format
│   │   ├── golden/              # expected IR JSON per fixture
│   │   └── reference/           # REAL .pro files exported from ProPresenter
│   └── pyproject.toml
├── macos/  PCCI.xcodeproj  Sources/  Resources/
├── windows/  Pcci.sln  Pcci/
├── scripts/  build-engine.sh  build-macos.sh  build-windows.ps1
└── docs/  FORMAT_NOTES.md  STAGE_SETUP.md  BUILD_PROMPT.md
```

---

## 6. The intermediate representation (build this first)

Every ingester produces `RawDocument`; every parser refines it into `Song`. Everything downstream consumes `Song` only. This seam is what makes the project testable without ProPresenter or a UI.

```python
class PositionedLine(BaseModel):
    text: str            # tabs already expanded, NBSP normalised
    y: float             # baseline, document coordinates
    x0: float            # left edge of first glyph
    char_x: list[float]  # x position of each character in `text`
    page: int
    bold: bool = False
    italic: bool = False
    font_size: float | None = None

class RawDocument(BaseModel):
    source_path: Path
    source_format: Literal["txt","md","pdf","docx","rtf","odt","html","chordpro"]
    lines: list[PositionedLine]
    monospace: bool          # True => column index is reliable for alignment
    warnings: list[str]

class ChordPlacement(BaseModel):
    chord: str               # normalised, e.g. "C#m7/G#"
    char_index: int          # offset into Line.lyrics; may equal len(lyrics)

class Line(BaseModel):
    lyrics: str              # "" for instrumental / chords-only lines
    chords: list[ChordPlacement]

class SectionType(StrEnum):
    INTRO = "Intro"; VERSE = "Verse"; PRE_CHORUS = "Pre-Chorus"
    CHORUS = "Chorus"; POST_CHORUS = "Post-Chorus"; BRIDGE = "Bridge"
    TAG = "Tag"; OUTRO = "Outro"; INSTRUMENTAL = "Instrumental"
    INTERLUDE = "Interlude"; VAMP = "Vamp"; BREAKDOWN = "Breakdown"
    REFRAIN = "Refrain"; ENDING = "Ending"; MISC = "Misc"

class Section(BaseModel):
    type: SectionType
    number: int | None       # Verse 2 -> 2
    raw_label: str           # exactly as it appeared in the source
    lines: list[Line]
    confidence: float        # 0..1, drives UI highlighting of guesses

class Song(BaseModel):
    title: str
    artist: str | None = None
    ccli_number: str | None = None
    copyright: str | None = None
    key: str | None = None
    tempo: int | None = None
    sections: list[Section]
    warnings: list[str]
```

`Song` must serialise to JSON and round-trip losslessly. Golden tests compare against that JSON.

---

## 7. Phase 0 — Format reconnaissance (BLOCKING)

Do not write the writer until this is finished and written up in `docs/FORMAT_NOTES.md`.

1. Vendor community ProPresenter 7 `.proto` definitions (start from `greyshirtguy/ProPresenter7-Proto`) into `core/pcci/propresenter/proto/`. Record the source commit and licence.
2. **Ask me to export three reference files from my ProPresenter** and commit them to `tests/reference/`:
   - a song with several groups and an arrangement,
   - the same song with **per-slide notes** filled in,
   - the same song with a **chord chart attached** via ProPresenter's own chord-chart import.
3. Decode all three. Produce a text dump of each message tree.
4. Answer these in `FORMAT_NOTES.md`, citing the decoded bytes for each:
   - Exact path to per-slide **notes** text.
   - Is the **chord chart embedded** in the `.pro`, or stored as an external path reference? If external, where does ProPresenter keep the file, and does the `.pro` store an absolute path, a relative path, or a UUID?
   - Which format does the chord chart attachment hold — ChordPro text, plain text, or PDF?
   - Exact structure of groups (name, colour encoding, hot-key) and arrangements.
   - What `application_info` version values the current ProPresenter accepts, and how it behaves on a mismatch.
   - Default group colours as RGBA, read from a real file rather than from memory.
5. **Round-trip proof:** decode a reference `.pro`, re-encode it with your bindings, and demonstrate the result is byte-identical or — if not — that ProPresenter still opens it unchanged. Report which.

Report findings and **wait for my go-ahead** before Phase 4.

---

## 8. Phase 1 — Ingestion

One ingester per format, all returning `RawDocument`.

- **Plain text / Markdown**: detect encoding with `charset-normalizer`, strip BOM, normalise line endings, **expand tabs to spaces using a tab stop of 4** (chord alignment depends on this), normalise NBSP/thin-space to U+0020, normalise Unicode `♭`/`♯` to `b`/`#`. Set `monospace = True`. Strip Markdown emphasis and code fences but **preserve intra-line spacing**.
- **PDF**: extract per-character positions with PyMuPDF. Cluster characters into lines by y within a tolerance of ~30% of median glyph height. Sort by x; synthesise spaces from inter-glyph gaps wider than ~0.4× the space-glyph advance. Populate `char_x`. Set `monospace` true only if the dominant font is fixed-pitch. **If a page yields no text layer, raise `ImageOnlyPdfError`** with a message telling the user the PDF is scanned and OCR is not supported in v1.
- **DOCX**: iterate paragraphs and runs; preserve run-level bold/italic (used as a section-header signal); convert tabs to spaces; treat each table cell as its own line. Capture `font_size` and whether the paragraph style is a heading.
- **RTF / ODT / HTML**: convert to text while preserving line structure and leading whitespace; set `monospace = False` unless the source declares a monospace font.
- **ChordPro**: parse directives directly (`{title}`, `{artist}`, `{key}`, `{ccli}`, `{comment}`, `{start_of_verse}`/`{sov}`, `{soc}`, `{sob}`) and inline `[C]` brackets. This path skips heuristics entirely — build it early, it is your cleanest test bed.

---

## 9. Phase 2 — Detection and alignment

### 9.1 Chord grammar

```
root      := [A-G]
accidental:= (#|b|##|bb)?
quality   := (maj|Maj|M|min|m|dim|aug|o|ø|\+|-)?
extension := (2|4|5|6|7|9|11|13)*
alteration:= (sus2|sus4|sus|add9|add11|add13|b5|#5|b9|#9|#11|b13)*
bass      := (/ root accidental)?
chord     := root accidental quality extension alteration bass
token     := chord | "N.C." | "NC" | "%" | "|" | "||" | ":||" | "||:" | "x2".."x8" | "-"
```

Normalise on output: `Cmaj7`, `C#m7/G#`, `Bb`. Keep the original spelling in a `raw` field for debugging.

### 9.2 Chord-line classification

A line is a **chord line** when all of:
- it has ≥ 1 token,
- ≥ 75% of whitespace-separated tokens match `token`,
- median token length ≤ 6,
- it is not a section header.

Guard against false positives explicitly: a line consisting only of `A`, `a`, `I`, `Be`, `Am`, `Do`, `Dad` is ambiguous English. Resolve with context — a chord line is nearly always immediately followed by a non-chord line, and nearly always sits inside a section whose other lines already classified as chord lines. Add a unit test for the lyric line `A man of sorrows`.

### 9.3 Chord ↔ lyric alignment

For a chord line at index *i* followed by a lyric line at *i+1*:

- **Monospace sources**: `char_index` = the chord token's starting column index, clamped to `len(lyrics)`.
- **Positional sources (PDF/DOCX)**: for each chord token take its `x0`, then binary-search the lyric line's `char_x` for the nearest character whose x is ≤ the chord's x; that character's index is `char_index`. When the chord's x precedes the lyric's first glyph, use 0.
- A chord line with no following lyric line becomes a `Line` with `lyrics=""` and all chords at index 0 — an instrumental line. Preserve these; they matter for Intros and Instrumentals.
- Two chords resolving to the same `char_index` must not be merged; keep both in source order.

### 9.4 Section detection

In priority order:

1. **ChordPro directives** — authoritative when present.
2. **Bracketed / labelled headers** — a standalone short line matching:
   `^\s*[\[\(]?\s*(Intro|Verse|Chorus|Pre[\s-]?Chorus|Post[\s-]?Chorus|Bridge|Tag|Outro|Ending|Interlude|Instrumental|Refrain|Vamp|Turnaround|Coda|Breakdown|Hook|Solo|Reprise|Channel|Link)\s*([0-9]+|[A-Z])?\s*[\]\)]?\s*:?\s*$`
   Case-insensitive. Confidence 0.95.
3. **Formatting signals** — a short standalone line that is bold, all-caps, or a heading style, and is not a chord line. Confidence 0.7.
4. **Fallback** — split on blank-line-separated stanzas; first stanza becomes `Intro` only if it is chords-only, otherwise `Verse 1`, then `Verse 2`, …. Confidence 0.3.

Auto-number repeated types: two unnumbered `Verse` headers become Verse 1 and Verse 2. A repeated identical `Chorus` stays one group and repeats in the arrangement rather than becoming Chorus 2. Unrecognised labels map to `MISC` with `raw_label` preserved — never discard the user's label.

### 9.5 Metadata

Title: `{title}` directive → a `Title:` line → the first non-chord, non-section line on page 1 → the filename stem. Also scrape `CCLI Song #`, `CCLI #`, `© …`, `Key of X`, `BPM`/`Tempo`.

---

## 10. Phase 3 — Slide planning

Input: `Song` + `lines_per_slide: int` (default **4**, range 1–10) + options.

Rules:
- **A slide never spans two sections.** Ever.
- Chunk each section's lines into runs of at most `lines_per_slide`.
- `balance_last_slide` (default **on**): when the final chunk of a section would hold a single line and the section has > `lines_per_slide` lines, redistribute evenly — 5 lines at N=4 becomes 3+2, not 4+1.
- Instrumental lines (`lyrics == ""`) count toward the limit but render as chords only.
- Each slide records: section reference, ordinal within section, its `Line` objects, and a label like `Verse 1` / `Verse 1 (2)`.

Emit a `SlidePlan` model. The UI renders this for review; the writer consumes it.

---

## 11. Phase 4 — ProPresenter writer

### 11.1 Presentation structure

- One **Cue** per slide; one **CueGroup** per detected section, named from `SectionType` + number, coloured from the group colour map.
- **Arrangement** listing groups in detected order, so an operator can hit Play and follow the chart.
- Slide size configurable, default **1920×1080**.
- Lyric text element: centred, configurable font (default a bold sans at ~60pt), white on transparent, with a subtle shadow. Safe-area inset ~5%.
- Populate `application_info`, presentation `uuid`, `name` (= song title), `category` ("Song"), and CCLI/copyright fields wherever Phase 0 shows ProPresenter stores them.
- Every UUID must be a fresh UUIDv4, and every UUID reference must resolve within the document.

### 11.2 Getting chords onto the stage screen only

There is no per-text-element "stage only" flag in ProPresenter. Implement **both** supported routes and let the user pick (default: both).

**Route A — Slide Notes (reliable, works everywhere).** Write each slide's chords into that slide's **notes** field as a monospaced chord-over-lyric block, reconstructed from `char_index`:

```
     C        G/B      Am
Amazing grace how sweet the sound
```

Notes are never rendered to audience output. The user adds a *Current Slide Notes* element to their stage layout.

**Route B — Native chord chart (the proper feature).** Generate ChordPro from the IR via `chordpro_out.py` and attach it as ProPresenter's own chord chart, exactly as Phase 0 determined it is stored. If Phase 0 proves the attachment is an external path reference, write the `.cho` sidecar next to the `.pro` **and** offer to copy it into ProPresenter's chord-chart directory, and say plainly in the UI that the reference is path-based.

Ship `docs/STAGE_SETUP.md`: step-by-step instructions for adding a Slide Notes element and a Chord Chart element to a stage layout, and surface it from the app's success screen.

**Explicitly forbidden:** do not place chords in an off-canvas or zero-opacity text element. It leaks to audience output the moment someone edits the slide, and it is not what the user asked for.

### 11.3 Group colour map

Ship defaults from Phase 0's decoded reference file; expose the whole map as user-editable config. Suggested starting point if the reference proves inconclusive: Intro `#7F8C8D`, Verse `#2E6DB4`, Pre-Chorus `#E67E22`, Chorus `#C0392B`, Post-Chorus `#8E44AD`, Bridge `#27AE60`, Instrumental `#16A085`, Tag `#F1C40F`, Outro/Ending `#566573`, Misc `#95A5A6`.

### 11.4 Verification before write

`verify.py` re-parses the serialised bytes and asserts: parses cleanly; slide count matches the plan; every cue belongs to exactly one group; the arrangement references only existing groups; no duplicate or dangling UUIDs; every slide with chords has non-empty notes when Route A is enabled. Any failure aborts the write with a diagnostic — **never** ship a half-valid file.

---

## 12. Phase 5 — CLI and the UI bridge

```
pcci convert IN.pdf -o OUT.pro --lines-per-slide 4 [--balance/--no-balance]
                    [--chords notes|chart|both|none] [--json]
pcci analyze IN.docx --json          # -> Song JSON, no file written
pcci plan    IN.docx --lines-per-slide 4 --json   # -> SlidePlan JSON
pcci build   --plan plan.json -o OUT.pro          # accepts a user-edited plan
pcci doctor                          # environment + proto binding self-check
```

The four-step `analyze → (user edits) → plan → build` flow is what makes the review UI possible. Design the CLI around it, not around a single monolithic `convert`.

**Bridge contract:** with `--json`, stdout carries exactly one JSON object and nothing else; all logs and progress go to stderr as JSON Lines (`{"level","msg","ts"}`). Exit codes: `0` success, `2` user-input error, `3` unsupported format, `4` internal error. The UIs must not scrape human-readable text.

---

## 13. Phase 6 — macOS app

**SwiftUI, macOS 26 SDK, deployment target macOS 14.**

*Design language.* Use the macOS 26 Liquid Glass APIs — `glassEffect(_:in:)`, `GlassEffectContainer`, `.buttonStyle(.glass)`, `ToolbarSpacer`, `backgroundExtensionEffect()`. **Verify exact signatures against the installed SDK before use; do not code from memory.** Gate them behind `if #available(macOS 26, *)` with `.ultraThinMaterial` as the fallback path, and confirm the app still looks deliberate on macOS 14.

*"Golden Gate" palette.* Deep charcoal base (`#1C1C1E`-ish, use semantic colours so light mode is free), accent International Orange `#C0362C` warming to `#E8603C` for interactive states. Define these in an asset catalogue with light/dark variants. Respect the user's system accent colour when they have set one; otherwise use the Golden Gate accent.

*Layout.* `NavigationSplitView`: sidebar = queued files; detail = the three-pane flow.

1. **Drop** — full-window drop target, multi-file, with file-type validation on hover.
2. **Review** — the critical screen. Left: detected sections as a reorderable list, each row showing type, number and a confidence dot; the type is an editable menu, sections can be merged, split, renamed or deleted. Right: a live slide-plan preview showing exactly what each slide will contain, chords rendered above lyrics in a monospaced face. A prominent **Lines per slide** stepper at the top re-plans live on change.
3. **Export** — destination picker, chord-delivery mode, then a success state with *Reveal in Finder* and a link to the stage-setup guide.

*Engine integration.* Bundle the PyInstaller onedir engine in `Contents/Resources/engine/`; invoke via `Process`, decode the JSON, surface `stderr` log lines in a collapsible console. Never block the main actor on the subprocess.

---

## 14. Phase 7 — Windows app

**WinUI 3 (Windows App SDK), C#, .NET 8, Windows 10 1809+.**

Same three-pane flow, same view-model semantics, same JSON bridge — re-implemented, not ported literally. Use **Mica Alt** as the window backdrop, Fluent controls, rounded corners, and the same Golden Gate accent over a Fluent dark neutral ramp. Follow the system theme by default with a manual Light/Dark/System override in settings. No acrylic-as-fake-glass — clean and flat reads better on Windows than an imitation of macOS.

Engine ships alongside the app as `engine\pcci.exe`, invoked identically.

---

## 15. Phase 8 — Packaging

- `scripts/build-engine.sh` / `.ps1`: PyInstaller **onedir** (not onefile — onefile breaks macOS notarization and is slow to start).
- **macOS**: arm64 `.app`, hardened runtime, sign every embedded binary in the engine directory, notarize and staple, ship a DMG. `[CONFIRM]` — this needs a paid Apple Developer ID. Tell me whether you have one; if not I will produce an unsigned build plus instructions for the Gatekeeper bypass.
- **Windows**: x64 MSIX (preferred) or WiX MSI. `[CONFIRM]` — code-signing certificate available?
- CI: GitHub Actions matrix running lint, `mypy --strict`, and the full test suite on both platforms for every push.

---

## 16. Error handling and logging contract

Exception hierarchy rooted at `PcciError`, each carrying `user_message` (plain language + remediation) and `technical_detail`:

`UnsupportedFormatError`, `EncodingDetectionError`, `ImageOnlyPdfError`, `EmptyDocumentError`, `NoSectionsDetectedError`, `ChordAlignmentWarning` (non-fatal), `ProtoSchemaMismatchError`, `VerificationFailedError`, `OutputWriteError`.

- The CLI catches everything at `main()`, maps to the exit codes above, and emits `{"error": {...}}` under `--json`.
- The UIs render `user_message` in an inline banner; `technical_detail` sits behind a disclosure triangle with a copy button.
- Logs: rotating file, 5×2 MB, in `~/Library/Logs/PCCI/` and `%LOCALAPPDATA%\PCCI\Logs\`. `--verbose` raises the level. **Never log file contents** — paths and structural metadata only.
- Warnings accumulate on `Song.warnings` / `RawDocument.warnings` and surface in the Review screen so the user sees what the parser was unsure about.

---

## 17. Testing requirements

- **Fixture corpus**: the same three real songs in every supported format, plus adversarial cases — no section headers at all, unconventional labels (`V1`, `CH`, `PC`), chord-only intro, a lyric line reading `A man of sorrows`, Nashville numbers, multi-column PDF, a two-page PDF with a section split across the page break, mixed tabs and spaces, UTF-16 with BOM, a scanned image-only PDF.
- **Golden tests**: fixture → `Song` JSON, snapshot-compared.
- **Property tests** (`hypothesis`): generated chord strings round-trip through parse→normalise→parse; alignment `char_index` is always within `[0, len(lyrics)]`.
- **Writer tests**: generated `.pro` re-parses; invariants from §11.4 hold; a snapshot of the decoded structure catches regressions.
- **Acceptance checklist** in `docs/` for manual verification in real ProPresenter: file imports without error; groups appear with correct names and colours; arrangement plays in order; audience output shows **no chords**; a stage layout with Slide Notes shows the chords; the native chord chart element follows the slides.
- Coverage ≥ 85% on `core/pcci/parse/`, `slides.py`, and `propresenter/`.

---

## 18. Definition of done

A ProPresenter operator with no technical knowledge drags a PDF chord chart onto the app, sets lines per slide to 4, glances at the detected sections, clicks Export, double-clicks the `.pro`, and runs the song in ProPresenter with correct groups and arrangement, clean audience output, and chords on their stage monitor — on both a MacBook and a Windows machine.

---

## 19. Sequencing and check-ins

Work in this order, committing at each step and **pausing for my review** where marked 🛑:

1. Repo scaffold, `pyproject.toml`, CI, IR models, error hierarchy, logging.
2. ChordPro ingester + chord grammar + full test harness (the clean-room path).
3. txt/md/docx/rtf/odt/html ingesters.
4. PDF ingester with positional extraction.
5. Section detection + alignment, golden tests across the whole corpus. 🛑 **Show me detection accuracy on the corpus before continuing.**
6. Phase 0 format reconnaissance. 🛑 **`FORMAT_NOTES.md` + round-trip proof, reviewed before any writer code.**
7. Slide planner + ProPresenter writer + verifier.
8. CLI and JSON bridge. 🛑 **I test the CLI against real charts and import into ProPresenter.**
9. macOS app.
10. Windows app.
11. Packaging, signing, release workflow.

---

## 20. Questions to resolve before you start

Ask me all of these in one message, then wait:

1. Which exact ProPresenter version am I running? (Menu → About)
2. Windows x64, or genuinely 32-bit x86?
3. Do I have an Apple Developer ID and a Windows code-signing certificate?
4. Can I export the three reference `.pro` files for Phase 0, and provide 5–10 real chord charts in the formats I actually use?
5. Preferred chord delivery: slide notes, native chord chart, or both?
6. Should v1 handle multi-song documents, or one song per file?
7. Any preference on slide font, size, and the default lines-per-slide?

Do not write implementation code until I have answered 1, 4, and 5.
