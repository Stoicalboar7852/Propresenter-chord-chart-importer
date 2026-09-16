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
    MOUNT_POINT="/Volumes/$VOLUME"
    rm -f "$DMG" "$WRITABLE"
    rm -rf "$STAGING"
    mkdir -p "$STAGING/.background"
    cp -R "$APP" "$STAGING/"
    ln -s /Applications "$STAGING/Applications"
    cp "$REPO_ROOT/assets/dmg-background.png" "$STAGING/.background/background.png"
    cp "$REPO_ROOT/assets/dmg-background@2x.png" "$STAGING/.background/background@2x.png"
    cp "$MACOS_DIR/Resources/AppIcon.icns" "$STAGING/.VolumeIcon.icns"

    # One file for both resolutions. Finder reads a single background image, so the
    # retina version has to travel inside a multi-representation TIFF rather than
    # beside it as @2x.
    BACKGROUND=".background:background.png"
    if command -v tiffutil >/dev/null 2>&1; then
        if tiffutil -cathidpicheck \
            "$STAGING/.background/background.png" \
            "$STAGING/.background/background@2x.png" \
            -out "$STAGING/.background/background.tiff" >/dev/null 2>&1; then
            BACKGROUND=".background:background.tiff"
        fi
    fi

    # Room to write a .DS_Store into. An image sized exactly to its contents has none,
    # and the layout then fails with no space left on device - which looks exactly like
    # Finder ignoring the script.
    STAGING_MB="$(du -sm "$STAGING" | cut -f1)"
    hdiutil create -volname "$VOLUME" -srcfolder "$STAGING" -ov -format UDRW \
        -fs HFS+ -size "$(( STAGING_MB + 80 ))m" "$WRITABLE" >/dev/null

    # Mounted where Finder can see it, and browsable. Finder addresses a disk by name
    # under /Volumes: mounted anywhere else, or with -nobrowse, `tell disk "PCCI"`
    # finds nothing and the whole layout silently does not happen. That is what made
    # earlier images come out plain.
    if [[ -d "$MOUNT_POINT" ]]; then
        hdiutil detach "$MOUNT_POINT" -force -quiet || true
    fi
    hdiutil attach "$WRITABLE" -quiet
    for _ in 1 2 3 4 5 6 7 8 9 10; do
        [[ -d "$MOUNT_POINT" ]] && break
        sleep 1
    done
    if [[ ! -d "$MOUNT_POINT" ]]; then
        echo "    could not mount the image at $MOUNT_POINT" >&2
        exit 1
    fi

    LAYOUT_LOG="$BUILD/dmg-layout.log"
    if osascript >"$LAYOUT_LOG" 2>&1 <<APPLESCRIPT
tell application "Finder"
    tell disk "$VOLUME"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {200, 140, 860, 588}
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 128
        set text size of viewOptions to 13
        set background picture of viewOptions to file "$BACKGROUND"
        set position of item "PCCI.app" of container window to {170, 210}
        set position of item "Applications" of container window to {490, 210}
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
APPLESCRIPT
    then
        echo "    window laid out"
    else
        echo "    Finder would not lay the window out:" >&2
        sed 's/^/      /' "$LAYOUT_LOG" >&2
        echo "      (the image is still usable, just unstyled)" >&2
        echo "      If this says \"Not authorized to send Apple events\", allow your" >&2
        echo "      terminal to control Finder in System Settings > Privacy & Security" >&2
        echo "      > Automation, then build again." >&2
    fi

    sync
    if [[ -f "$MOUNT_POINT/.DS_Store" ]]; then
        echo "    layout saved ($(stat -f%z "$MOUNT_POINT/.DS_Store") bytes of .DS_Store)"
    else
        echo "    no .DS_Store was written, so the window will open with defaults" >&2
    fi

    # Makes the mounted volume show the app's icon rather than a blank disk.
    if [[ -x /usr/bin/SetFile ]]; then
        /usr/bin/SetFile -a C "$MOUNT_POINT" || true
    fi

    hdiutil detach "$MOUNT_POINT" -quiet || hdiutil detach "$MOUNT_POINT" -force -quiet
    hdiutil convert "$WRITABLE" -format UDZO -imagekey zlib-level=9 -o "$DMG" >/dev/null
    rm -f "$WRITABLE"
    echo "==> Built $DMG"
fi
