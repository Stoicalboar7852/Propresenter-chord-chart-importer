#!/usr/bin/env bash
# Check this machine can build PCCI, and install what it is missing.
#
#   scripts/install-deps.sh [--yes] [--check-only]
#
# The engine needs Python 3.12 or newer. The Mac app additionally needs full Xcode,
# which is an App Store download and cannot be installed from here — that one is
# reported, not fixed.
#
# Nothing is installed without being asked first, unless --yes is passed. Installing
# software on somebody's machine is not a thing to do quietly.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASSUME_YES=0
CHECK_ONLY=0

for argument in "$@"; do
    case "$argument" in
        --yes|-y) ASSUME_YES=1 ;;
        --check-only) CHECK_ONLY=1 ;;
        *) echo "unknown option: $argument" >&2; exit 2 ;;
    esac
done

missing=()

echo "==> Checking what this machine has"

find_python() {
    local candidate
    for candidate in python3.14 python3.13 python3.12 python3 python; do
        command -v "$candidate" >/dev/null 2>&1 || continue
        if "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' \
            2>/dev/null; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

if PYTHON="$(find_python)"; then
    VERSION="$("$PYTHON" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
    echo "  ok       Python $VERSION ($(command -v "$PYTHON"))"
else
    echo "  MISSING  Python 3.12 or newer - the conversion engine"
    missing+=("python")
fi

if [[ "$(uname -s)" == "Darwin" ]]; then
    DEVELOPER_DIR_PATH="${DEVELOPER_DIR:-$(xcode-select -p 2>/dev/null || true)}"
    case "$DEVELOPER_DIR_PATH" in
        ""|*/CommandLineTools|*/CommandLineTools/*)
            echo "  MISSING  full Xcode - the Mac app (the engine alone does not need it)"
            missing+=("xcode")
            ;;
        *)
            echo "  ok       Xcode at $DEVELOPER_DIR_PATH"
            ;;
    esac
fi

if [[ ${#missing[@]} -eq 0 ]]; then
    cat <<'MESSAGE'

Everything needed is here. Next:

    ./scripts/build-macos.sh
MESSAGE
    exit 0
fi

if [[ "$CHECK_ONLY" == "1" ]]; then
    exit 1
fi

# Xcode first, because nothing here can install it and the answer is the same either
# way: it is a several-gigabyte App Store download.
if [[ " ${missing[*]} " == *" xcode "* ]]; then
    cat <<'MESSAGE'

Xcode has to come from the App Store; no command line can fetch it. Install it, then:

    sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

The engine and the command line tool do not need it, and work now.
MESSAGE
fi

if [[ " ${missing[*]} " != *" python "* ]]; then
    exit 1
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
    cat <<'MESSAGE'

Install Python 3.12 or newer with this system's package manager, then run this again.
MESSAGE
    exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
    cat <<'MESSAGE'

Homebrew is not installed, so Python cannot be installed automatically. Either install
Homebrew from https://brew.sh and run this again, or download Python 3.12 or newer from
https://www.python.org/downloads/
MESSAGE
    exit 1
fi

if [[ "$ASSUME_YES" != "1" ]]; then
    if [[ ! -t 0 ]]; then
        echo
        echo "Run with --yes to install Python 3.12 without asking."
        exit 1
    fi
    echo
    read -r -p "Install Python 3.12 with Homebrew now? [y/N] " answer
    case "$answer" in
        y|Y|yes|YES) ;;
        *) echo "Nothing installed."; exit 1 ;;
    esac
fi

echo
echo "==> brew install python@3.12"
brew install python@3.12

cat <<'MESSAGE'

Installed. Confirm with:

    ./scripts/install-deps.sh --check-only
MESSAGE
