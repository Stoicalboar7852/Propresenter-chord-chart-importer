# Changelog

What changed in each release, and why you might care.

This file is the source of the release notes: `scripts/release_notes.py` lifts the
section matching the version being released and puts it at the top of the GitHub
release page. A version with no section here still gets notes — the commits since the
previous tag — but a written entry is better than a list of commit subjects.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet.

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
