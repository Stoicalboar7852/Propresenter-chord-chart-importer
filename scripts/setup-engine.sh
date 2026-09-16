#!/usr/bin/env bash
# Create the engine's Python environment.
#
#   scripts/setup-engine.sh [--dev]
#
# Finds a Python new enough to run the engine, makes core/.venv, installs it, and checks
# the result actually works. The build scripts call this for you when the environment is
# missing, so you should rarely need to run it by hand.
#
# --dev also installs the test and lint tooling. Contributors want it; people who just
# want to convert charts do not.
set -euo pipefail

WITH_DEV=0
for argument in "$@"; do
    case "$argument" in
        --dev) WITH_DEV=1 ;;
        *) echo "unknown option: $argument" >&2; exit 2 ;;
    esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE="$REPO_ROOT/core"
VENV="$CORE/.venv"
REQUIRED="3.12"

if [[ ! -f "$CORE/pyproject.toml" ]]; then
    cat >&2 <<'MESSAGE'
core/pyproject.toml is missing, so this checkout does not contain the engine.

This usually means the checkout predates the engine landing on the default branch.
Bring it up to date:

    git fetch origin
    git checkout claude/blissful-planck-pbslml
    git pull

MESSAGE
    exit 1
fi

# Newest first: a 3.13 that is present is preferable to a 3.12 that is also present.
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

if ! PYTHON="$(find_python)"; then
    found="none found"
    if command -v python3 >/dev/null 2>&1; then
        found="python3 is $(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
    fi
    cat >&2 <<MESSAGE
The engine needs Python $REQUIRED or newer, and this machine does not have one
($found).

macOS ships an older Python for its own use. Install a current one:

    brew install python@3.12

or download an installer from https://www.python.org/downloads/

Then run this script again.
MESSAGE
    exit 1
fi

VERSION="$("$PYTHON" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
echo "==> Using $PYTHON ($VERSION)"

if [[ -d "$VENV" ]]; then
    echo "==> Removing the previous environment at core/.venv"
    rm -rf "$VENV"
fi

echo "==> Creating core/.venv"
"$PYTHON" -m venv "$VENV"

# The engine itself, not the test tooling: the dev extra pulls in grpcio-tools, which
# is only needed to regenerate the protobuf bindings and has to be compiled on any
# machine without a wheel for it.
PACKAGE="$CORE"
if [[ "$WITH_DEV" == "1" ]]; then
    PACKAGE="$CORE[dev]"
fi

echo "==> Installing the engine (this takes a minute)"
"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet -e "$PACKAGE"

echo "==> Checking it works"
"$VENV/bin/pcci" doctor

cat <<'MESSAGE'

Ready. Useful commands:

    core/.venv/bin/pcci convert "My Song.docx" -o "My Song.pro"
    ./scripts/build-macos.sh               builds the app, engine included
MESSAGE
if [[ "$WITH_DEV" == "1" ]]; then
    echo '    core/.venv/bin/python -m pytest        (from inside core/)'
else
    echo '    ./scripts/setup-engine.sh --dev         adds pytest, mypy and ruff'
fi
