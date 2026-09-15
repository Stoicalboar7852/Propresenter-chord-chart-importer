# Installing PCCI on macOS

The app is **not signed with an Apple Developer ID**, because this project does not
have one. Everything works; macOS just needs to be told once that you meant to open it.

## Build it

```bash
git clone https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer.git
cd Propresenter-chord-chart-importer

# The engine's Python environment
cd core
python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
cd ..

# The app, engine included
./scripts/build-macos.sh          # add --dmg for a disk image
```

The result is `build/macos/PCCI.app`. Drag it to `/Applications`.

Requirements: macOS 14 or later, Xcode or the Swift toolchain, Python 3.12.

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
