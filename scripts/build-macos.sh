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

command -v swift >/dev/null || { echo "swift not found — install Xcode or the Swift toolchain" >&2; exit 1; }

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
