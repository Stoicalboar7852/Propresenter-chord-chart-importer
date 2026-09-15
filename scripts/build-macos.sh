#!/usr/bin/env bash
# Build PCCI.app, engine included.
#
#   scripts/build-macos.sh [--liquid-glass] [--dmg]
#
# --liquid-glass  compile the macOS 26 Liquid Glass path (needs the macOS 26 SDK)
# --dmg           also produce a disk image
#
# There is no Apple Developer ID for this project, so the app is signed ad-hoc. That is
# enough for it to run locally; see docs/INSTALL_MACOS.md for the Gatekeeper step a
# first launch needs.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MACOS_DIR="$REPO_ROOT/macos"
BUILD="$REPO_ROOT/build/macos"
APP="$BUILD/PCCI.app"
LIQUID_GLASS=0
MAKE_DMG=0

for argument in "$@"; do
    case "$argument" in
        --liquid-glass) LIQUID_GLASS=1 ;;
        --dmg) MAKE_DMG=1 ;;
        *) echo "unknown option: $argument" >&2; exit 2 ;;
    esac
done

command -v swift >/dev/null || { echo "swift not found — install Xcode" >&2; exit 1; }

# Building SwiftUI needs *full Xcode*, not the Command Line Tools.
#
# On the macOS 26 SDK and later, SwiftUI declares @State (and its siblings) as macros
# rather than property wrappers. The plugin that expands them, SwiftUIMacros, lives
# inside Xcode.app; the Command Line Tools ship ObservationMacros and SwiftMacros but
# not that one. Compiling without it fails with "external macro implementation type
# 'SwiftUIMacros.StateMacro' could not be found", followed by a long tail of errors
# that are all just consequences of @State never expanding. Catch it here instead.
DEVELOPER_DIR_PATH="${DEVELOPER_DIR:-$(xcode-select -p 2>/dev/null || true)}"
case "$DEVELOPER_DIR_PATH" in
    ""|*/CommandLineTools|*/CommandLineTools/*)
        cat >&2 <<MESSAGE
The app needs full Xcode to build, and this machine is pointed at the Command Line Tools.

    xcode-select -p
    ${DEVELOPER_DIR_PATH:-(nothing selected)}

SwiftUI's @State is a macro on recent SDKs, and the plugin that expands it ships inside
Xcode.app. The Command Line Tools cannot build a SwiftUI app at all.

  1. Install Xcode from the App Store (it is a large download).
  2. Point the tools at it:

         sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

  3. Run this script again.

The engine does not need Xcode. To convert charts from the command line meanwhile:

    ./scripts/setup-engine.sh
    core/.venv/bin/pcci convert "My Song.docx" -o "My Song.pro" --lines-per-slide 4

MESSAGE
        exit 1
        ;;
esac

echo "==> Building the engine"
"$REPO_ROOT/scripts/build-engine.sh" "$BUILD/engine"

echo "==> Compiling PCCI"
cd "$MACOS_DIR"
SWIFT_FLAGS=(-c release --arch arm64)
if [[ "$LIQUID_GLASS" == "1" ]]; then
    SWIFT_FLAGS+=(-Xswiftc -DPCCI_LIQUID_GLASS)
    echo "    (Liquid Glass enabled — needs the macOS 26 SDK)"
fi
swift build "${SWIFT_FLAGS[@]}"
BINARY="$(swift build "${SWIFT_FLAGS[@]}" --show-bin-path)/PCCI"

echo "==> Assembling the bundle"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$BINARY" "$APP/Contents/MacOS/PCCI"
cp "$MACOS_DIR/Resources/Info.plist" "$APP/Contents/Info.plist"
cp "$REPO_ROOT/docs/STAGE_SETUP.md" "$APP/Contents/Resources/STAGE_SETUP.md"
cp -R "$BUILD/engine/pcci" "$APP/Contents/Resources/engine"
printf 'APPL????' > "$APP/Contents/PkgInfo"

echo "==> Signing (ad-hoc)"
# Every embedded binary is signed, innermost first, which is what notarisation would
# require and what keeps macOS from refusing to launch the sidecar.
find "$APP/Contents/Resources/engine" -type f \( -perm -u+x -o -name '*.dylib' -o -name '*.so' \) \
    -exec codesign --force --sign - --timestamp=none {} \; 2>/dev/null || true
codesign --force --deep --sign - "$APP"
codesign --verify --verbose=2 "$APP" || echo "    (ad-hoc signature; Gatekeeper will still prompt on first launch)"

echo "==> Built $APP"
du -sh "$APP"

if [[ "$MAKE_DMG" == "1" ]]; then
    echo "==> Making a disk image"
    DMG="$BUILD/PCCI.dmg"
    rm -f "$DMG"
    STAGING="$BUILD/dmg"
    rm -rf "$STAGING"
    mkdir -p "$STAGING"
    cp -R "$APP" "$STAGING/"
    ln -s /Applications "$STAGING/Applications"
    hdiutil create -volname "PCCI" -srcfolder "$STAGING" -ov -format UDZO "$DMG" >/dev/null
    echo "==> Built $DMG"
fi
