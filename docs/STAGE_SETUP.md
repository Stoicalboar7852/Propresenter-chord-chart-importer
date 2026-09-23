# Getting the chords onto your stage screen

`pcci` can put the chords into your presentation by three different routes, and out of
the box it uses two of them at once. All of them are invisible to the congregation. You
only need to set up the one you prefer.

| Route | What it is | Set-up |
|---|---|---|
| **Chords element** | The chord stored on the word it is played on | One stage-layout element. This is the default. |
| **Slide notes** | A monospaced chord-over-lyric block in each slide's notes | One stage-layout element. Nothing to copy. |
| **Chord chart** | The whole chart as page images, attached to the slides | One stage-layout element, plus copying the images into ProPresenter once. ProPresenter only. |

No route puts anything on the audience output. `pcci` never hides chords in an
off-screen or transparent text box — that leaks the moment somebody edits the slide.

**Using FreeShow instead of ProPresenter?** Set **Write files for** to FreeShow in
Settings and read [FreeShow](#freeshow) at the bottom. The Chords element and the slide
notes both work there; the chord chart does not exist.

---

## Route A — Slide notes

The route that works everywhere, with nothing to install or copy. Ask for it with
`--chords notes`, or **Slide notes only** in the apps; `--chords inline+notes` writes it
alongside Route C, for a stage layout that has both elements on it.

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

Advance through the song. Each slide's notes show that slide's chords on **one
horizontal row**, grouped by lyric line:

```
A    D    A/C#    D
```

Two deliberate choices there. The lyrics are **not** repeated, because they are already
on the slide and a stage screen shrinks its notes element to fit whatever text you give
it — half the text renders at roughly twice the size. And the chords sit on one line
rather than one per lyric line, because a column of single chords runs down the screen
and reads slowly. A wider gap separates one lyric line's chords from the next, which is
why the notes element needs a fixed-pitch font for this to read properly.

Three other layouts are available, in the app's settings or with
`--chord-placement`:

| Value | What you get |
|---|---|
| `chords_only` | One row per lyric line, each chord at the column it sits at in the chart. The default. |
| `chords_inline` | Every chord on the slide in one horizontal row. Largest on screen, but nothing lines up with anything. |
| `above` | The chart in full: chords over their own words, lyrics and all. |
| `below` | The same, lyrics first. |

```
     C        G/B      Am            <- above
Amazing grace how sweet the sound
```

---

## Route C — The Chords element (the default)

ProPresenter also has a **Chords** stage element, with a Notation menu offering Chords,
Numbers, Numerals and Do-Re-Mi. That element does not read the notes or the chart. It
reads chords stored *inside the slide's own text* — each chord attached to the word it
is played on — which is the only one of the three routes that can transpose or
renotate, because the chords are data rather than a picture or a block of text.

`pcci` writes that by default:

```bash
pcci convert "My Song.docx" -o "My Song.pro"                          # this route
pcci convert "My Song.docx" -o "My Song.pro" --chords inline+notes    # and the notes
```

Then add the **Chords** element to your stage layout. In the desktop apps the setting is
**In the slide text (Chords element)**, with **In the slide text, and slide notes** for
both at once.

### Keeping them off the audience screen

The first version of this route drew the chords on the audience output as well as the
stage — the chords are not in the slide's text (double-click the text box in the editor
and you see only the words), but ProPresenter painted them over every screen the text
element appeared on.

So the drawing is now a separate switch, and it is **off**:

```bash
pcci convert "My Song.docx" -o "My Song.pro" --chords inline                     # stage only
pcci convert "My Song.docx" -o "My Song.pro" --chords inline --chords-on-slide   # everywhere
```

In the apps it is **Draw them on the slide**, under the chord setting, and it only
appears for the two inline routes. Leave it off unless the congregation is meant to see
the chords: the Chords stage element reads the stored chords either way.

### One thing still unverified

**The chord may sit a word out.** The field that says where a chord goes is called
`end`, and on a Mac-born format that could equally mean a length. Each chord is anchored
across the whole word it belongs to, so under either reading it lands on the right word
— but that is reasoning, not observation.

`--chords notes`, `chart` or `both` writes none of this, if you would rather it did not.

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

---

## FreeShow

FreeShow has the same two stage-only routes, under different names, and `pcci` writes a
`.show` file for it with **Write files for → FreeShow** in Settings (`--target
freeshow` from the command line). Import it with **File → Import → FreeShow**, or
drop the `.show` file on the window.

What arrives: one group per section, coloured the way your own group settings colour
them, in the order the chart is written in — a chorus sung three times is one slide
played three times.

### The chords element

1. Open the **Stage** tab and pick the layout your musicians look at.
2. Add a **Slide Text** item, or select the one already there.
3. In its settings, turn **Chords** on. Size and colour are next to the switch.

The chords are stored on the words, so this is the route that can be transposed, and
there is nothing to turn on in the show itself. As in ProPresenter, the switch that
would draw them on the *audience* output is a separate one on the slide, and `pcci`
leaves it off unless you ask (**Draw them on the slide**).

FreeShow will also show the chords of an **instrumental line** — an intro, a
turnaround — which ProPresenter cannot, because there are no words there to attach
them to. Nothing appears on the audience screen for those lines.

### The slide notes

Add a **Slide Notes** item to the stage layout instead, or as well. Same block of
monospaced chords over lyrics as ProPresenter gets, and the same advice: use a
monospaced font or nothing lines up.

### What FreeShow has no answer for

There is no chord-chart element and nothing to point one at, so the **Chord chart** and
**Notes and chart** routes have nothing to write there. Settings says so when you pick
one; the notes half of "Notes and chart" still arrives.
