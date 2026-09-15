# Getting the chords onto your stage screen

`pcci` puts the chords into your presentation twice, by two different routes. Both are
invisible to the congregation. You only need to set up the one you prefer, and you can
set up both.

| Route | What it is | Set-up |
|---|---|---|
| **Slide notes** | A monospaced chord-over-lyric block in each slide's notes | One stage-layout element. Nothing to copy. |
| **Chord chart** | The whole chart as page images, attached to the slides | One stage-layout element, plus copying the images into ProPresenter once. |

Neither route puts anything on the audience output. `pcci` never hides chords in an
off-screen or transparent text box — that leaks the moment somebody edits the slide.

---

## Route A — Slide notes (start here)

This is the route that works everywhere, with nothing to install or copy.

1. In ProPresenter, open **Screens → Stage Layouts** (or the Stage tab of the
   Screens window).
2. Pick the layout your musicians look at, or press **+** to add one.
3. Press **+** inside the layout editor and choose **Current Slide Notes**.
4. Drag it to fill most of the screen. Notes are where the chords are, so give them
   room — the block is as wide as the longest lyric line plus its chords.
5. Set the font to a **monospaced** one — Courier, Menlo, Consolas, Roboto Mono. This
   matters: in any other font the chords stop sitting above the right syllables.
6. Turn text scaling **off** or set it to shrink-to-fit, so long lines are not wrapped.
7. Assign the layout to the stage screen your band sees.

Advance through the song. Each slide's notes show that slide's chords, one row per
lyric line:

```
C       G/B       Am
              G          D
```

The lyrics are **not** repeated in the notes, because they are already on the slide and
a stage screen shrinks its notes element to fit whatever text you give it. Half the text
means the chords render at roughly twice the size. Row one is the chord row for line
one, row two for line two, and a line with no chords leaves its row blank, so the rows
still read against the words beside them.

If you would rather have the lyrics in the notes as well, convert with
`--chord-placement above` (or `below`), or change it in the app's settings:

```
     C        G/B      Am
Amazing grace how sweet the sound
```

---

## Route B — The chord chart

ProPresenter's own chord-chart feature holds **page images**, not text (this is
documented, with the decoded bytes, in `FORMAT_NOTES.md` §4.4). `pcci` renders your
chart the same way and attaches the right page to each slide.

### Add the element

1. **Screens → Stage Layouts**, pick your layout.
2. Press **+** and choose **Chord Chart**.
3. Size it to fill the screen. The pages are A4-shaped, so a tall element suits them.

### Make the images findable

When `pcci` exports `My Song.pro`, it writes the pages beside it:

```
My Song.pro
My Song chords 1.png
My Song chords 2.png
```

Each slide points at those files **twice**: by their absolute path, and by the
show-relative path `Media/Imported/My Song chords 1.png`.

* **If you keep the `.pro` and its PNGs together and import from that folder**, the
  absolute path resolves and the chart appears immediately.
* **If you move the presentation to another machine**, copy the PNGs into that
  machine's ProPresenter media folder so the relative path resolves:

  | Platform | Folder |
  |---|---|
  | macOS | `~/Library/Application Support/RenewedVision/ProPresenter/UserWorkspaces/<workspace>/Media/Imported/` |
  | Windows | `%APPDATA%\RenewedVision\ProPresenter\UserWorkspaces\<workspace>\Media\Imported\` |

  Keep the file names exactly as they are.

This is a path-based reference, not an embedded copy. If the images are missing, the
slides still work — the chord chart element is simply empty. The slide notes are
unaffected, which is why Route A is the default and the one to rely on.

---

## Checking it worked

1. Put the presentation into a playlist and go live.
2. Look at the audience output: **lyrics only**, no chords, no section labels.
3. Look at the stage screen: chords over (or under) the words, following the slides.
4. Advance a slide. Both screens should change together.

If the chords look misaligned on the stage screen, the notes element is not using a
monospaced font. That is the cause almost every time.
