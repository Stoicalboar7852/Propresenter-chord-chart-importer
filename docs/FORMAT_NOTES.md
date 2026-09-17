# ProPresenter `.pro` format notes

Everything here was read out of real files exported from ProPresenter **21.4 (build
352583705)** on macOS 27, plus one older export from **20.0.1 (build 335544583)** on
macOS 26.3.1. Nothing in this document is inferred from documentation or memory: each
claim names the reference file it came from, and every dump is reproducible with

```
core/.venv/bin/python scripts/dump_pro.py <file> [--full|--cue N]
```

## 1. Reference material

| File | Exported by | Purpose |
|---|---|---|
| `core/tests/reference/Goodbye Yesterday blank with groups.pro` | 20.0.1 | groups + colours + hot keys |
| `core/tests/reference/Goodbye Yesterday With slide notes.pro` | 21.4 | per-slide notes |
| `core/tests/reference/Goodbye Yesterday with chord charts.probundle` | 21.4 | chord chart attachment |

The `.probundle` is a **zip64** archive. Python's `zipfile` refuses it ("Corrupt zip64
end of central directory record"), so `scripts/dump_pro.py` walks the central directory
by hand. It contains one `.pro` plus the chord-chart images, each stored under its
**absolute source path on the exporting machine**:

```
/Users/<user>/Library/Application Support/RenewedVision/ProPresenter/UserWorkspaces/
    ProPresenter/Media/Imported/GOODBYE YESTERDAY A.png     (87291 bytes, 595x842)
    ProPresenter/Media/Imported/GOODBYE YESTERDAY A 2.png
    ProPresenter/Media/Imported/GOODBYE YESTERDAY A 3.png
Goodbye Yesterday.pro                                       (54618 bytes)
```

## 2. Vendored schema

`core/pcci/propresenter/proto/rv/` holds the `.proto` definitions from
[greyshirtguy/ProPresenter7-Proto](https://github.com/greyshirtguy/ProPresenter7-Proto)
`autogen-proto/`, commit `bf6325d243897a6c64dde46eec803ec29f5f8569`, MIT licensed.

The repository's own `rv/version.txt` reads:

```
21.4,352583705
```

which is **exactly** the `application_info` in the two current reference exports. The
schema and the sample files therefore come from the same ProPresenter build; field
numbers used by the writer are validated, not guessed.

## 3. Round-trip proof

Decode with the generated bindings, re-encode, compare bytes:

| File | Bytes | Round-trip |
|---|---|---|
| `Goodbye Yesterday blank with groups.pro` | 44 378 | **byte-identical** |
| `Goodbye Yesterday With slide notes.pro` | 54 000 | **byte-identical** |
| `Goodbye Yesterday.pro` (from the bundle) | 54 618 | **byte-identical** |

No unknown fields survive parsing, and serialisation reproduces the original byte
stream exactly. `tests/test_reference_roundtrip.py` asserts this on every test run, so a
schema drift that would silently drop data fails CI rather than a Sunday morning.

## 4. Where things live

### 4.1 Presentation

```
Presentation
  application_info  = 1   ApplicationInfo
  uuid              = 2
  name              = 3   "Goodbye Yesterday"  (the song title)
  category          = 6   ""  in all three references — ProPresenter does not
                          require it, but the UI shows it, so we write "Song"
  notes             = 7   presentation-level notes (empty in all references)
  background        = 8
  chord_chart       = 9   URL — EMPTY in all three references (see 4.4)
  selected_arrangement = 10  (absent)
  arrangements      = 11  (absent — none of the exports has an arrangement)
  cue_groups        = 12  repeated CueGroup
  cues              = 13  repeated Cue
  ccli              = 14  Presentation.CCLI (empty in all references)
  timeline          = 17  duration 300 in the 20.0.1 export
```

### 4.2 Cue and slide

One cue per slide. The chain from cue to lyric text is:

```
Cue
  uuid = 1, name = 2, isEnabled = 12
  actions = 10  Action
    uuid = 1, isEnabled = 3, type = ACTION_TYPE_PRESENTATION_SLIDE
    slide = 23  Action.SlideType
      presentation = 2  PresentationSlide
        base_slide  = 1  Slide
          elements = 1  Slide.Element
            element = 1  Graphics.Element
              uuid=1 name=2 ("Text") bounds=3 opacity=5 path=8
              fill=9 stroke=10 shadow=11 feather=12
              text = 13  Graphics.Text
                attributes = 3   font, colour, paragraph style, stroke_width/colour
                shadow     = 4
                rtf_data   = 5   <- the visible lyric text, as RTF
                vertical_alignment = 6
                chord_pro  = 12  Graphics.Text.ChordPro
            info = 4  (uint32; the reference writes 3 for the lyric element)
          background_color = 5, size = 6 (1920x1080), uuid = 7
        notes       = 2  PresentationSlide.Notes
        chord_chart = 4  URL
```

Reference values for the lyric element (`--cue 12` of the slide-notes export): bounds
`origin.y = -239.86`, `size 1920x810`, opacity 1, `fill` and `stroke` present but with
`enable` unset (so neither is drawn), shadow `angle 315 / offset 5 / radius 5 /
opacity 0.75`, `feather.radius 0.05`, font `CenturyGothic-Bold 75pt` (family
`Century Gothic`), paragraph alignment `ALIGNMENT_CENTER`, vertical alignment
`VERTICAL_ALIGNMENT_MIDDLE`.

### 4.3 Per-slide notes — **answer: RTF at `PresentationSlide.notes.rtf_data`**

```
Cue.actions[].slide.presentation.notes = PresentationSlide.Notes {
    bytes rtf_data = 1;
    Graphics.Text.Attributes attributes = 2;   // empty in the reference
}
```

Verbatim from `Goodbye Yesterday With slide notes.pro`, cue 12:

```
{\rtf1\ansi\ansicpg1252\cocoartf2907
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;\red255\green255\blue255;}
{\*\expandedcolortbl;;\csgray\c100000;}
\deftab1300
\pard\pardeftab1300\pardirnatural\partightenfactor0

\f0\fs48 \cf2 This has Slide notes For Claude}
```

So notes are **RTF, not plain text**, `\fs48` = 24 pt, white. 31 of 33 cues carry the
same note. This is Route A: a monospaced chord-over-lyric block goes here, and notes
never reach audience output.

### 4.4b Chords as text attributes — **in the schema, in no export**

Separately from the page images below, the schema carries a second, richer mechanism:

```
Graphics.Text.chord_pro = 12   ChordPro { enabled, notation, color }
    Notation: NOTATION_CHORDS | NUMBERS | NUMERALS | DO_RE_MI
Graphics.Text.attributes.custom_attributes = 13   repeated CustomAttribute
    CustomAttribute { IntRange range = 1; oneof { ... string chord = 7; ... } }
Slide.Element.DataLink.chord_pro_chart = 29       ChordProChart {}   (an empty marker)
```

So a chord can be a string attached to a range of the lyric text, and the stage
element that displays them is a distinct DataLink from the page-image one at field 5.
That is what makes ProPresenter's Notation menu possible: these are data, not pixels.

**No export this project has seen uses it.** The bundle named "with chord charts" is
page images (below); across all three references there are zero `CustomAttribute`
entries of any kind, and `chord_pro` appears on every text element with only a colour
set and `enabled` false. Two things are therefore unresolved, and `pcci` writes this
only when asked (`--chords inline`):

1. **`IntRange.end`** — index or length? Nothing observed says which. `pcci` anchors a
   chord across the whole word, which lands correctly under either reading.
2. **Does enabling it reach the audience output?** The flag is on the audience lyric
   element. Unknown, and the reason the route is opt-in.

### 4.4 Chord chart — **answer: a rendered page image, referenced per slide**

This is the finding that changes the design. ProPresenter does **not** store the chord
chart as ChordPro text or as an embedded document. It rasterises the chart to one PNG
per page, imports those PNGs into the workspace media folder, and points each slide at
one of them:

```
Cue.actions[].slide.presentation.chord_chart = URL {
  absolute_string = 1: "file:///Users/<user>/Library/Application%20Support/RenewedVision/
                        ProPresenter/UserWorkspaces/ProPresenter/Media/Imported/
                        GOODBYE%20YESTERDAY%20A%202.png"
  platform        = 3: PLATFORM_MACOS
  local           = 4: LocalRelativePath {
      root = ROOT_SHOW (10)
      path = "Media/Imported/GOODBYE YESTERDAY A 2.png"
  }
}
```

Facts, not guesses:

* **External, not embedded.** The `.pro` holds only the path. The PNG bytes live in the
  workspace; the `.probundle` is what carries them between machines.
* **Both an absolute path and a show-relative path** are stored. The relative form
  (`root = ROOT_SHOW`, `path = "Media/Imported/…"`) is the portable one.
* **Per slide, not per presentation.** `Presentation.chord_chart` (field 9) is empty in
  all three references; three individual cues carry a chart (cue 0, 12 and 14).
* **The format is PNG**, 595x842 px — A4 at 72 dpi, so the source document was rendered
  a page at a time.

### 4.5 A native chord representation also exists in the schema

The 21.4 schema carries a genuine chord model that the reference files do not exercise:

```
Graphics.Text.Attributes.CustomAttribute { IntRange range = 1; ... string chord = 7; }
Graphics.Text.chord_pro = 12  ChordPro { bool enabled = 1; Notation notation = 2; Color color = 3; }
      Notation: NOTATION_CHORDS | NOTATION_NUMBERS | NOTATION_NUMERALS | NOTATION_DO_RE_MI
Slide.Element.DataLink.ChordChart {}      // stage-layout element: the chart image
Slide.Element.DataLink.ChordProChart {}   // stage-layout element: the parsed chart
```

`chord_pro { color { alpha: 1 } }` is present on the lyric element of every reference
slide with `enabled` unset — the feature is wired up but switched off.

That is enough to say the fields exist and what they mean. It is **not** enough to
promise how ProPresenter renders them, in particular whether chords anchored with
`CustomAttribute.chord` stay off the audience output. Ground rule 1 applies: the writer
ships this path as an opt-in flagged experimental until it has been tested in the real
application, and slide notes remain the default route.

### 4.6 Groups, colours and hot keys

```
Presentation.cue_groups = 12  CueGroup {
    Group group = 1 {
        UUID uuid = 1;                            // unique per occurrence
        string name = 2;                          // "Verse 1", "Chorus 2", …
        Color color = 3;                          // float RGBA, 0..1
        HotKey hotKey = 4;                        // { uint32 code = 1 }
        UUID application_group_identifier = 5;    // the workspace group preset
        string application_group_name = 6;        // empty in the reference
    }
    repeated UUID cue_identifiers = 2;
}
```

From `Goodbye Yesterday blank with groups.pro` — ProPresenter's own colours:

| Group | Hex | RGBA (as stored) | Hot key |
|---|---|---|---|
| Intro | `#B3A724` | 0.701961, 0.654902, 0.141176, 1 | 9 |
| Verse 1 | `#0077CC` | 0.000000, 0.466667, 0.800000, 1 | 1 |
| Verse 2 | `#005999` | 0.000000, 0.349020, 0.600000, 1 | 19 |
| Chorus 1 | `#C20049` | 0.760784, 0.000000, 0.286275, 1 | 3 |
| Chorus 2 | `#AF0043` | 0.686275, 0.000000, 0.262745, 1 | 24 |
| Bridge 1 | `#7600CC` | 0.462745, 0.000000, 0.800000, 1 | 2 |
| Bridge 2 | `#590099` | 0.349020, 0.000000, 0.600000, 1 | 14 |
| Interlude | `#24B34C` | 0.141176, 0.701961, 0.298039, 1 | 0 |
| Vamp | `#24B34C` | 0.141176, 0.701961, 0.298039, 1 | 0 |
| Post Chorus | `#A52A2A` | 0.647059, 0.164706, 0.164706, 1 | 0 |
| *(unnamed)* "Group" | `#000000` | 0, 0, 0, **alpha 0** | 0 |

Two behaviours worth copying:

* **Repeats share a preset, not a name.** "Chorus 2" appears as three separate
  `CueGroup`s with three different `group.uuid`s but the *same*
  `application_group_identifier` (`6478AED4-…`). A section that recurs is repeated
  membership of one preset, not "Chorus 3", "Chorus 4".
* **Numbered variants are darker.** Verse 2 is exactly 0.75x Verse 1 and Bridge 2
  exactly 0.75x Bridge 1; Chorus 2 is about 0.9x Chorus 1. `pcci` uses a single 0.75
  factor per step (`NUMBERED_SHADE_FACTOR`), which reproduces Verse 2 and Bridge 2
  exactly and Chorus 2 approximately. The whole map is user-editable.
* Post Chorus has **no** `application_group_identifier` — a user-created group rather
  than a built-in preset. Writing an empty one is legal.

Cue membership is complete and disjoint: all 33 cues appear exactly once across the 13
groups. Group order is *not* the cue array order, so `cues` order carries no meaning;
`cue_groups` order does.

### 4.7 Arrangements

```
Presentation.arrangements = 11  Arrangement {
    UUID uuid = 1; string name = 2; repeated UUID group_identifiers = 3;
}
Presentation.selected_arrangement = 10  UUID
```

**None of the three references contains an arrangement**, so the structure below is
taken from the schema rather than from bytes. `group_identifiers` holds `Group.uuid`
values (the per-occurrence UUID from 4.6), which is why repeats need their own
`CueGroup`. The writer builds one arrangement in detected order and sets
`selected_arrangement`; the acceptance checklist has the user confirm it in the app.

### 4.8 `application_info` and version behaviour

```
ApplicationInfo {
  platform = 1            PLATFORM_MACOS | PLATFORM_WINDOWS
  platform_version = 2    Version
  application = 3         APPLICATION_PROPRESENTER
  application_version = 4 Version { major_version, minor_version, patch_version, build }
}
```

Observed:

| File | application_version | build | platform_version |
|---|---|---|---|
| blank with groups | 20.0.1 | `335544583` | macOS 26.3.1 |
| with slide notes | 21.4.0 | `352583705` | macOS 27.0.0 |
| with chord charts | 21.4.0 | `352583705` | macOS 27.0.0 |

ProPresenter 21.4 opens the 20.0.1 file without complaint, which is direct evidence that
it tolerates an older `application_info` — the field records provenance, it is not a
compatibility gate. `pcci` writes `APPLICATION_PROPRESENTER 21.4.0` with build
`352583705`, matching the vendored schema, and `platform` set to the machine doing the
conversion.

**What is not proven:** how a *newer* ProPresenter than 21.4 reacts, and whether any
future build rejects an unknown-but-larger version. Neither can be tested without that
build.

## 5. Consequences for the writer

1. Slide notes (Route A) are fully specified and safe: RTF at
   `presentation.notes.rtf_data`, never shown to the audience.
2. The native chord chart (Route B) is an **image reference**, so "attach the chord
   chart" means rendering chart pages to PNG and writing a `ROOT_SHOW`-relative URL.
   `pcci` writes the PNG next to the `.pro` and offers to copy it into
   `…/UserWorkspaces/<workspace>/Media/Imported/`; the reference is path-based and the
   UI says so plainly.
3. Chords anchored in text (`CustomAttribute.chord`) stay behind an experimental flag
   until tested against the real application.
4. Repeated sections reuse one group preset via `application_group_identifier`.
5. Every reference file round-trips byte-identically, so `verify.py` re-parsing our
   output is a meaningful check rather than a formality.
