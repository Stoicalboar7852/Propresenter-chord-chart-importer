<!--
    The standing half of a GitHub release page.

    scripts/release_notes.py substitutes the entry for the version being released into
    the placeholder on the first line below, and .github/workflows/release.yml hands
    the result to the release. Do not write the placeholder's name anywhere else in
    this file - including in a comment like this one - or the substitution lands there
    as well.

    Edit this for anything true of every release. Put what changed in CHANGELOG.md.
-->
{{CHANGELOG}}

## Which file

| You have | Download |
|---|---|
| A Mac | `PCCI.dmg` — Apple silicon |
| A Windows PC, Intel or AMD | `PCCI-win-x64-setup.exe` |
| A Windows PC on ARM (Snapdragon, Surface Pro 11) | `PCCI-win-arm64-setup.exe` |

The same app writes for **ProPresenter 7** and for **FreeShow** — one setting decides
which, and there is nothing extra to download for either.

Not sure which Windows you have? **Settings → System → About → System type**. The
`.zip` files are the same apps as a folder, for anyone who would rather not run an
installer.

The Windows installer asks whether to install for everyone or just you, lets you pick
the folder, and can put a shortcut on your desktop.

## First launch

Neither build is signed, so each system will question it once.

**macOS** — right-click PCCI in Finder and choose **Open**, then **Open** again. See
`docs/INSTALL_MACOS.md`.

**Windows** — click **More info**, then **Run anyway**. See `docs/INSTALL_WINDOWS.md`.

## How tested is this

The conversion engine is covered by 500-odd tests and is checked on Linux, macOS and
Windows on every change, including a real conversion through the frozen copy that ships
inside each app — in both formats. Both apps are compiled and packaged by the same
automation that produced these files.

What has *not* happened yet is a Sunday. If something misbehaves, the engine log (the
button in the top right) says what it saw, and issues are welcome.

## Setting up your stage screen

Chords never appear on the audience output. To see them on stage, add a **Chords** or a
**Current Slide Notes** element to your stage layout — a conversion feeds both of those
out of the box. In FreeShow they are a **Slide Text** item with Chords turned on, and a
**Slide Notes** item. `docs/STAGE_SETUP.md` has the steps for either program.

## Blocked at school or work?

The song search talks to a handful of public music and lyrics sites. `docs/NETWORK.md`
lists every domain, says what each one is for, and has the list in a block you can paste
into a ticket. Converting a file you already have needs no network at all.
