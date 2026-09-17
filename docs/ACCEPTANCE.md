# Acceptance checklist

Things only a human with ProPresenter open can confirm. The automated suite covers
everything below the line "the file is structurally valid"; this list covers "the file
does what a worship team needs".

Run through it with a real chart from your own set list, not a fixture.

## Export

- [ ] `pcci convert "My Song.docx" -o "My Song.pro"` exits 0 and prints a slide count
      that matches what you expected.
- [ ] The chord chart PNGs are written next to the `.pro`.
- [ ] `pcci analyze "My Song.docx"` lists the sections you would have listed yourself.
      Anything marked *(guessed)* deserves a look.

## Getting a song in from somewhere other than a file

The engine's side of this is tested against recorded responses, because the sites
themselves cannot be reached from the machines it is developed on. What no test can
tell you is whether a real search finds the songs your team actually sings.

- [ ] A search for a song you know lists it, with its cover art, near the top.
- [ ] A row that says **Chords** imports something with chords over the words; a row
      that says **Lyrics** imports the words alone and says so.
- [ ] A row marked **No words** cannot be imported and does not pretend it can.
- [ ] A site being down or refusing us leaves a note under the results and the other
      sources still answer, rather than the whole search failing.
- [ ] Pasting a chord-site link into the search box describes that one page.
- [ ] Copying a chart out of a browser and pressing the paste shortcut imports it, with
      the chords still over the right words.
- [ ] Pasting something that is not a song says so in plain words.
- [ ] A lyrics-only import makes a presentation with no chord chart beside it, and the
      app says it is lyrics only rather than leaving you to wonder.
- [ ] The imported song is named after the song, not after a URL or a hash.

## Import

- [ ] Double-clicking the `.pro`, or dragging it into a ProPresenter playlist, imports
      without an error dialog.
- [ ] The presentation is named after the song, not after the file.
- [ ] The slide count matches the export.
- [ ] No slide is blank, and no slide holds a chord line as if it were a lyric.

## Groups and arrangement

- [ ] Groups appear with the names from the chart — Verse 1, Chorus, Bridge 2 — and not
      as a wall of ungrouped slides.
- [ ] Group colours look like ProPresenter's own: blue verses, red choruses, purple
      bridges, and darker shades for the numbered repeats.
- [ ] The arrangement plays the song in the order the chart is written in.
- [ ] A section that repeats (a chorus sung three times) appears once in the group
      list and three times in the arrangement.

## Output — the part that matters on a Sunday

- [ ] Audience output shows **lyrics only**. No chords. No section labels. No
      performance notes such as "Hold G X 8 BARS".
- [ ] A stage layout with a **Current Slide Notes** element shows the chords, lined up
      over the right syllables (see `STAGE_SETUP.md`).
- [ ] A stage layout with a **Chord Chart** element shows the chart pages, and the page
      follows the section being sung.
- [ ] With `--chords inline`, a stage layout with a **Chords** element shows the chords
      over the words — and the audience output still shows none. Turning **Draw them on
      the slide** on is the one case where they are meant to appear on both.
- [ ] Text is legible from the back of the room: font, size and outline came through as
      configured.

## Editing

- [ ] Opening a slide in ProPresenter's editor shows one text box with the lyrics and
      nothing hidden behind or beside it.
- [ ] Deleting a slide, re-ordering the arrangement and re-saving all work normally.
- [ ] Re-exporting the same chart over the top of an existing file replaces it cleanly.

## Awkward cases worth trying once

- [ ] A chart with no section headers at all — everything should land in numbered
      verses at low confidence rather than failing.
- [ ] A scanned PDF — should refuse with a message about OCR, not a traceback.
- [ ] A chart in a language with accented characters — the accents should survive to
      the slide.
- [ ] A very long line — should not be truncated in the notes block.

## Reporting a problem

Include the chart that caused it, the exact command, and the log file
(`~/Library/Logs/PCCI/pcci.log` or `%LOCALAPPDATA%\PCCI\Logs\pcci.log`). The log
records paths and structure only — never the contents of your files.
