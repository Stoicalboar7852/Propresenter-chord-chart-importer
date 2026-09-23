# Changelog

What changed in each release, and why you might care.

This file is the source of the release notes: `scripts/release_notes.py` lifts the
section matching the version being released and puts it at the top of the GitHub
release page. A version with no section here still gets notes — the commits since the
previous tag — but a written entry is better than a list of commit subjects.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **FreeShow as well as ProPresenter.** One setting, **Write files for**, and the same
  chart comes out as a `.show` instead of a `.pro` — written natively, not exported
  through some common subset: the same named groups in your own FreeShow colours, a
  long section as a parent slide with children, a repeated chorus as one slide played
  three times, and the chords stored on the words for FreeShow's own Chords stage
  element. Its slide notes work too. It has no chord-chart element, and the settings
  screen says so rather than writing nothing and leaving you to find out. FreeShow will
  even show the chords of an intro, which ProPresenter cannot: there are no words there
  to attach them to. Every claim about the format is read out of FreeShow's own source
  and written down in `docs/FORMAT_NOTES.md` §6.
- **A list of every domain the program contacts**, in
  [docs/NETWORK.md](docs/NETWORK.md), for anyone whose school or office blocks the
  search. It says what each one is for, which are optional, what is sent (the words you
  typed, and nothing else), and has the list in a block you can paste into a ticket. A
  test keeps it honest: a source added to the engine without its domain in that file
  fails the build.
- **A Settings window on macOS** (⌘,). The Mac app had none — chord delivery was fixed
  in code — so the routes below could only be chosen from the command line.
- **Search filters**: artist, album and year, in both apps. The artist is not only a
  filter, it is added to what the sources are asked, which finds songs a bare title
  never reaches.
- **Show more results.** Search stopped at one batch with no way to go further, so a
  song further down the list was simply unreachable.
- **`--chords inline`**, a third route that writes chords into the slide's own text so
  the built-in **Chords** stage element can read them — the only route that can
  transpose or switch to Nashville numbers. Now part of the default; see Changed below
  and `docs/STAGE_SETUP.md`.
- **A plus button at the top of the song list.** The search box and the drop target
  only show with nothing selected, so adding a second song used to mean clearing the
  first. On Windows the file picker moved to Ctrl+O, where it was going to be looked
  for anyway.
- **LRCLIB** as a source: a free, keyless, open lyrics API, which fills the gap for
  songs no chord site carries.
- **Musixmatch** as an optional source. It needs your own API key in
  `PCCI_MUSIXMATCH_KEY`, and its free plan returns only part of each song — the import
  tells you when that has happened rather than handing over a third of the words.

### Changed

- **The Chords stage element is now the default**, together with the slide notes
  (`--chords inline+notes`). It was `notes` and a rendered chord chart, which meant
  choosing the good route by hand every time and a folder of PNGs nobody asked for.
  Both defaults are stage-only; nothing reaches the audience screen either way.

### Fixed

- **A line of the song was read as a note to the band and never reached a slide.**
  Any short line containing one word off the performance-instruction list - "break",
  "hold", "stop", "times" - was treated as an instruction, so "We break the power of
  death" went into the notes instead of onto the screen. A line that reads as a
  sentence is now a lyric whatever words it contains: a pronoun, an article or a
  determiner says somebody is doing something, which "Drum break" and "HOLD G X 8
  BARS" never do. Capitals no longer outvote that, because some charts are typed
  entirely in capitals.
- **A mistyped chord was projected as a lyric.** One real chart writes `Dmd/E` on a
  line where every sibling line carries a plain `Dm`, `F` or `B/E`. It is not a chord,
  so the line was read as words and the typo went on the audience screen. A line whose
  every token is *built* like a chord - starting on a root, short, carrying a slash
  bass or an accidental or an extension number - is a chart with a typo in it, and is
  kept exactly as written with a warning naming what pcci did not recognise. `God/Man`
  and `Bed` are still words.
- **A long chord was projected as a lyric.** `Bbsus4/D` and `Cmaj7/G` are longer than
  the guard that stops long English words being read as chords, so a line of nothing
  but those went to the audience screen. Length cannot make a chord into a word.
- A line reading only `(x3)` was projected. It is furniture, not something to sing.
- An imported song could come back **missing its first section**. Lyrics sites run
  their own page furniture — a contributor count and the song's name — straight into
  the first heading with no line break, so the heading was really the tail of a long
  line and everything under it belonged to no section at all.
- A backing vocal on its own line, such as one written entirely in brackets, could be
  mistaken for a section heading. That left the real section with no lines in it, and
  a section with no lines is discarded — so two more sections went missing.
- A heading that names who sings it, like `[Build: Someone]`, kept the name in the
  group label. The name is dropped now, while a genuine aside such as
  `[Talking: to the band]` is still kept whole.
- A search that finds the song but nothing carrying its words now says so, and says
  what to do instead, rather than showing rows whose Import button is simply greyed.
- When two sources both had the words, the one asked first won rather than the better
  one. A source that records where the chorus is now beats one that only has the lines,
  so an import comes back with named sections instead of a run of numbered verses.
- Searching found the right song but importing could fetch a **different** one: two
  bands with the same song title were being folded into a single row, so a correct
  result could have someone else's chart behind it.
- A song imported from a lyrics site was named after the **band** rather than the song.
  Those sites write "Artist - Song" and pcci read it the other way round; credits now
  travel as labelled `Title:` and `Artist:` lines that cannot be misread.
- The sidebar said "Charts" and counted "charts". Not everything imported is a chord
  chart, so it says **Songs** now.
- Clearing the list could lay the start screen out taller than the window and clip it
  top and bottom. It fills the space when there is room and scrolls when there is not.
- **Inline chords reached the audience screen.** On a real rig the Chords stage element
  showed them correctly — and so did the audience output, which is the one thing this
  program exists to prevent. The chords were never in the slide's text; the switch that
  stores them is also what makes ProPresenter draw them. Drawing is now its own setting,
  **Draw them on the slide**, and it is off: the stage element reads the stored chords
  either way. Turn it on (`--chords-on-slide`) only if the congregation is meant to see
  them.

## [0.2.0] — 2026-09-17

### Added

- **Find a song online.** A search box in both apps that takes a song name *or* a link
  pasted out of a browser. Results come back as one row per song with its cover art,
  album and year, and each row names the sites it was assembled from. Three sources are
  asked at once and merged, because none of them knows everything: Ultimate Guitar has
  the chords, Genius has the words, Apple Music has the artwork and the credits. Genius
  refuses automated requests from some networks; when a source says no, the search says
  which one and carries on with the others.
- **Import from the clipboard**, the way ProPresenter does it — Cmd+Shift+V on a Mac,
  Ctrl+Shift+V on Windows. Copy a chart from a web page, an email or a PDF and paste it
  straight in. This is also the answer when a site refuses to let a program read it.
- **Import from a link.** Paste any address: a church website, a Google Doc published
  to the web, a ChordPro file in a repository. When the page lays its chart out as
  preformatted text — which is where a chart's column alignment lives — that is taken
  exactly as it is.
- **Lyrics with no chords** are now a first-class import rather than something that
  happened to work. A hymn text or a lyrics sheet converts like anything else, in every
  format the app reads.
- New commands for anyone using the engine directly: `pcci search`, `pcci fetch`,
  `pcci paste` and `pcci cache`.

### Changed

- A song with no chords no longer writes an empty chord-chart page beside the `.pro`,
  and the app now says plainly that the presentation will be lyrics only — "no chords
  in this file" and "pcci misread the chords" looked identical before.
- Downloaded pages are cached briefly, so searching for a song and then importing it is
  one request rather than two seconds apart. `pcci cache --clear` empties it.

### Fixed

- A chord fingering printed above a chart — `F - X33210`, the kind of thing chord sites
  put at the top — was being read as a section, so an imported song could open with a
  group called "F - X33210". Found by importing Shivers for real.
- A song that several sites knew about listed each of them once per listing, so a
  popular one read "via Ultimate Guitar, Ultimate Guitar, Ultimate Guitar, Apple Music,
  Apple Music". One entry per site now.
- `[Verse 1: A Singer]` — how lyrics sites label a section when they also say who sings
  it — became a group named after the singer, which never matched the song's other
  verses or took a verse's colour. It is a verse now, and the original wording is kept.

### Security

- Every pasted link is checked before it is opened: http and https only, and the
  address it resolves to must be a public one, so a link cannot be used to make the app
  read something inside your own machine or network. Redirects are re-checked rather
  than trusted, and the download is capped.

## [0.1.0] — 2026-09-16

First release.

### Added

- Convert chord charts to ProPresenter 7 `.pro` presentations from Word, PDF, plain
  text, Markdown, RTF, OpenDocument, HTML and ChordPro.
- Chords reach the stage screen as slide notes and as a rendered chord chart, and never
  appear on the audience output.
- Section detection with a review screen for correcting what the parser guessed.
- A configurable number of lyric lines per slide.
- Convert a whole folder of charts in one go, with one set of settings.
- Native apps for macOS and Windows, and a command-line engine for either.
- A Windows installer that asks where to install and offers a desktop shortcut, plus a
  portable zip.

[Unreleased]: https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer/releases/tag/v0.1.0
