# Installing PCCI on macOS

The app is **not signed with an Apple Developer ID**, because this project does not
have one. Everything works; macOS just needs to be told once that you meant to open it.

## Build it

```bash
git clone https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer.git
cd Propresenter-chord-chart-importer

./scripts/install-deps.sh         # checks for Python and Xcode; optional
./scripts/build-macos.sh          # add --dmg for a disk image
```

`install-deps.sh` never installs anything without asking; `--yes` skips the prompt and
`--check-only` reports without installing. Xcode it can only report on — that one is an
App Store download.

The disk image is laid out by Finder: the app on the left, Applications on the right, an
arrow between them, on a black and orange background.

Finder does that layout under automation, and macOS asks permission the first time — a
prompt saying your terminal wants to control Finder. Allow it and the window looks as
intended. Refuse it, or run somewhere nothing can answer the prompt, and the build says
so and carries on: the image still works, it just opens as a plain list. If you missed
the prompt, it is in **System Settings → Privacy & Security → Automation**.

That is the whole thing. The build script sets up the engine's Python environment the
first time, so there is nothing to prepare by hand. If you would rather do that step on
its own — to run the command-line tool without building an app — it is
`./scripts/setup-engine.sh`.

The result is `build/macos/PCCI.app`. Drag it to `/Applications`.

Requirements: macOS 14 or later, **full Xcode**, and **Python 3.12 or newer**.

Xcode from the App Store, not the Command Line Tools. SwiftUI declares `@State` as a
macro on the macOS 26 SDK and later, and the plugin that expands it ships only inside
`Xcode.app` — the Command Line Tools cannot compile a SwiftUI app at all. After
installing Xcode, point the toolchain at it once:

```bash
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

`build-macos.sh` checks this before it does anything else and tells you if it is wrong,
rather than letting the compiler bury you in macro errors.

The Python that comes with macOS is older than 3.12 and cannot run the engine;
`brew install python@3.12` is the usual fix, and `setup-engine.sh` tells you so if it
cannot find a suitable one.

**The engine does not need Xcode.** If you only want the command-line converter,
`./scripts/setup-engine.sh` is the whole install and Python is the only requirement:

```bash
./scripts/setup-engine.sh
core/.venv/bin/pcci convert "My Song.docx" -o "My Song.pro" --lines-per-slide 4
```

That installs the engine alone. Add `--dev` for the test and lint tooling.

### Liquid Glass

On macOS 26 with the macOS 26 SDK installed:

```bash
./scripts/build-macos.sh --liquid-glass
```

Without that flag the app uses `.ultraThinMaterial`, which looks deliberate on every
version from macOS 14 up. The flag is opt-in because the Liquid Glass symbols do not
exist in older SDKs, so a build machine without the macOS 26 SDK cannot compile them.

## First launch

macOS will refuse to open an unsigned app on the first try. Either:

**Right-click → Open.** Control-click (or right-click) PCCI in Finder, choose **Open**,
then **Open** again in the dialog. Once only; after that it launches normally.

**Or from System Settings.** Try to open it, then go to **System Settings → Privacy &
Security**, scroll to the bottom, and click **Open Anyway** next to the message about
PCCI.

If macOS says the app "is damaged and can't be opened", that is Gatekeeper's quarantine
flag rather than actual damage. Clear it:

```bash
xattr -dr com.apple.quarantine /Applications/PCCI.app
```

## If the build fails

**`external macro implementation type 'SwiftUIMacros.StateMacro' could not be found`**,
usually followed by `cannot find '$isTargeted' in scope` and `cannot assign to property:
'self' is immutable`. Only the first error is real — the rest are what happens when
`@State` never expands. You are on the Command Line Tools. Install Xcode and run
`sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`.

**`swift not found`.** Same cause, earlier: no toolchain is selected at all.

**`setup-engine.sh` cannot find Python 3.12.** `brew install python@3.12`, then run it
again. It searches `python3.14`, `python3.13`, `python3.12`, `python3` and `python`, and
takes the first that is new enough.

## What is inside

```
PCCI.app/Contents/
  MacOS/PCCI              the app
  Resources/engine/       the frozen conversion engine (about 120 MB)
  Resources/STAGE_SETUP.md
```

The engine is an ordinary command-line program. If the app ever misbehaves, run it
directly to see what it says:

```bash
/Applications/PCCI.app/Contents/Resources/engine/pcci doctor
/Applications/PCCI.app/Contents/Resources/engine/pcci convert "My Song.docx" -o "My Song.pro"
```

Logs go to `~/Library/Logs/PCCI/pcci.log`. They record paths and structure only, never
the contents of your charts.

## If you later get a Developer ID

Signing and notarising is then two extra steps on top of the same build:

```bash
codesign --force --deep --options runtime --timestamp \
  --sign "Developer ID Application: Your Name (TEAMID)" build/macos/PCCI.app
xcrun notarytool submit build/macos/PCCI.dmg --keychain-profile "notary" --wait
xcrun stapler staple build/macos/PCCI.dmg
```

Every binary inside `Resources/engine/` has to be signed too — `build-macos.sh` already
walks them for the ad-hoc signature, so the same loop works with a real identity.
