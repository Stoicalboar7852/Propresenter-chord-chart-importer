#!/usr/bin/env bash
# Build PCCI.app, engine included.
#
#   scripts/build-macos.sh [--liquid-glass] [--dmg]
#
# --liquid-glass   compile the macOS 26 Liquid Glass path (needs the macOS 26 SDK)
# --dmg            also produce a disk image
# --install-missing  install anything the machine is missing, without asking
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
INSTALL_MISSING=0

for argument in "$@"; do
    case "$argument" in
        --liquid-glass) LIQUID_GLASS=1 ;;
        --dmg) MAKE_DMG=1 ;;
        --install-missing) INSTALL_MISSING=1 ;;
        *) echo "unknown option: $argument" >&2; exit 2 ;;
    esac
done

if [[ "$INSTALL_MISSING" == "1" ]]; then
    "$REPO_ROOT/scripts/install-deps.sh" --yes
fi

if ! command -v swift >/dev/null; then
    cat >&2 <<'MESSAGE'
swift is not on this machine, so the app cannot be built.

    ./scripts/install-deps.sh     checks what is missing and what to do about it

Xcode comes from the App Store. The engine does not need it:

    ./scripts/setup-engine.sh
    core/.venv/bin/pcci convert "My Song.docx" -o "My Song.pro"
MESSAGE
    exit 1
fi

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
cp "$MACOS_DIR/Resources/AppIcon.icns" "$APP/Contents/Resources/AppIcon.icns"
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
    WRITABLE="$BUILD/PCCI-rw.dmg"
    STAGING="$BUILD/dmg"
    VOLUME="PCCI"
    rm -f "$DMG" "$WRITABLE"
    rm -rf "$STAGING"
    mkdir -p "$STAGING/.background"
    cp -R "$APP" "$STAGING/"
    ln -s /Applications "$STAGING/Applications"
    cp "$REPO_ROOT/assets/dmg-background.png" "$STAGING/.background/background.png"
    cp "$REPO_ROOT/assets/dmg-background@2x.png" "$STAGING/.background/background@2x.png"

    # Read/write first, so Finder can be told where things go, then compressed. The
    # positions below have to match the plates drawn in make_dmg_background.py.
    hdiutil create -volname "$VOLUME" -srcfolder "$STAGING" -ov -format UDRW "$WRITABLE" \
        >/dev/null
    MOUNT_POINT="$BUILD/mount"
    # If a previous run died between attach and detach, this is still a mount point,
    # and rm -rf would be reaching inside a mounted image rather than cleaning up.
    if mount | grep -q " on $MOUNT_POINT "; then
        hdiutil detach "$MOUNT_POINT" -force -quiet || true
    fi
    rm -rf "$MOUNT_POINT"
    mkdir -p "$MOUNT_POINT"
    hdiutil attach "$WRITABLE" -mountpoint "$MOUNT_POINT" -nobrowse -quiet

    # Dressing the window means driving Finder, which a machine may refuse: automation
    # permission is a prompt, and there is nobody to answer it on a build server. A
    # plain disk image is a perfectly good disk image, so this is allowed to fail.
    if osascript <<APPLESCRIPT >/dev/null 2>&1
tell application "Finder"
    tell disk "$VOLUME"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {200, 140, 860, 588}
        set options to the icon view options of container window
        set arrangement of options to not arranged
        set icon size of options to 128
        set text size of options to 13
        set background picture of options to file ".background:background.png"
        set position of item "PCCI.app" of container window to {170, 200}
        set position of item "Applications" of container window to {490, 200}
        close
        open
        update without registering applications
        delay 1
    end tell
end tell
APPLESCRIPT
    then
        echo "    window laid out"
    else
        echo "    (Finder would not lay the window out; the image is plain but fine)"
    fi

    sync
    hdiutil detach "$MOUNT_POINT" -quiet || hdiutil detach "$MOUNT_POINT" -force -quiet
    rmdir "$MOUNT_POINT" 2>/dev/null || true
    hdiutil convert "$WRITABLE" -format UDZO -imagekey zlib-level=9 -o "$DMG" >/dev/null
    rm -f "$WRITABLE"
    echo "==> Built $DMG"
fi
