# Installing PCCI on macOS

The app is **not signed with an Apple Developer ID**, because this project does not
have one. Everything works; macOS just needs to be told once that you meant to open it.

## Build it

```bash
git clone https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer.git
cd Propresenter-chord-chart-importer

# The engine and the apps live on this branch, which is not the repository's default
git checkout claude/affectionate-hamilton-ad8a08

./scripts/build-macos.sh          # add --dmg for a disk image
```

That is the whole thing. The build script sets up the engine's Python environment the
first time, so there is nothing to prepare by hand. If you would rather do that step on
its own — to run the command-line tool without building an app — it is
`./scripts/setup-engine.sh`.

The result is `build/macos/PCCI.app`. Drag it to `/Applications`.

Requirements: macOS 14 or later, Xcode or the Swift toolchain, and **Python 3.12 or
newer**. The Python that comes with macOS is older than that and cannot run the engine;
`brew install python@3.12` is the usual fix, and `setup-engine.sh` tells you so if it
cannot find a suitable one.

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
