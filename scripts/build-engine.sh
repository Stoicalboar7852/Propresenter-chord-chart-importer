#!/usr/bin/env bash
# Freeze the pcci engine into a self-contained directory the desktop apps can ship.
#
#   scripts/build-engine.sh [output-directory]
#
# onedir, not onefile: onefile breaks macOS notarisation (the embedded binaries cannot
# be signed individually) and adds a second or two to every launch while it unpacks.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE="$REPO_ROOT/core"
OUTPUT="${1:-$REPO_ROOT/build/engine}"
VENV="$CORE/.venv"
PYTHON="$VENV/bin/python"

if [[ ! -x "$PYTHON" ]]; then
    echo "No virtualenv at $VENV. Create one first:" >&2
    echo "  cd core && python3.12 -m venv .venv && .venv/bin/pip install -e '.[dev]'" >&2
    exit 1
fi

echo "==> Installing PyInstaller"
# uv-created virtualenvs have no pip; use uv when it is the one that made the venv.
if "$PYTHON" -m pip --version >/dev/null 2>&1; then
    "$PYTHON" -m pip install --quiet --upgrade pyinstaller
elif command -v uv >/dev/null; then
    uv pip install --quiet --python "$PYTHON" pyinstaller
else
    echo "Neither pip nor uv is available to install PyInstaller." >&2
    exit 1
fi

WORK="$REPO_ROOT/build/pyinstaller"
rm -rf "$OUTPUT" "$WORK"
mkdir -p "$OUTPUT" "$WORK"

# The generated protobuf modules are imported by bare name after their directory is
# added to sys.path at runtime, so PyInstaller cannot find them by static analysis.
# They ship as data and the runtime path lookup finds them exactly as it does in a
# source checkout. Their dependency on google.protobuf is invisible to the analyser for
# the same reason, so it is collected explicitly — without it the engine builds,
# launches, and then fails the moment somebody tries to export.
# --add-data resolves relative source paths against --specpath, not the working
# directory, so the source side is absolute and only the destination is relative.
GENERATED="pcci/propresenter/proto/generated"
GENERATED_SOURCE="$CORE/$GENERATED"

echo "==> Freezing the engine"
cd "$CORE"
"$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    --onedir \
    --console \
    --name pcci \
    --distpath "$OUTPUT" \
    --workpath "$WORK" \
    --specpath "$WORK" \
    --add-data "$GENERATED_SOURCE:$GENERATED" \
    --hidden-import "pcci.ingest.chordpro" \
    --hidden-import "pcci.ingest.docx" \
    --hidden-import "pcci.ingest.html" \
    --hidden-import "pcci.ingest.markdown" \
    --hidden-import "pcci.ingest.odt" \
    --hidden-import "pcci.ingest.pdf" \
    --hidden-import "pcci.ingest.rtf" \
    --hidden-import "pcci.ingest.txt" \
    --collect-submodules pymupdf \
    --collect-submodules charset_normalizer \
    --collect-submodules google.protobuf \
    --copy-metadata protobuf \
    entrypoint.py

BINARY="$OUTPUT/pcci/pcci"
if [[ ! -x "$BINARY" ]]; then
    echo "Build produced no executable at $BINARY" >&2
    exit 1
fi

echo "==> Smoke testing the frozen engine"
# A frozen build that cannot load its protobuf bindings looks fine until someone tries
# to export, so the build fails here rather than in front of a congregation.
if ! "$BINARY" doctor --json > "$WORK/doctor.json" 2>"$WORK/doctor.log"; then
    echo "The frozen engine failed its own doctor check:" >&2
    cat "$WORK/doctor.log" >&2
    exit 1
fi
"$PYTHON" - "$WORK/doctor.json" <<'PYEOF'
import json
import sys

report = json.load(open(sys.argv[1]))
failed = [check for check in report["checks"] if not check["ok"]]
if failed:
    for check in failed:
        print(f"  FAIL {check['check']}: {check['detail']}", file=sys.stderr)
    sys.exit(1)
print(f"  {len(report['checks'])} checks passed")
PYEOF

SAMPLE="$CORE/tests/fixtures/chordpro/goodbye_yesterday.cho"
if [[ -f "$SAMPLE" ]]; then
    "$BINARY" convert "$SAMPLE" -o "$WORK/smoke.pro" --json > /dev/null
    [[ -s "$WORK/smoke.pro" ]] || { echo "conversion smoke test wrote nothing" >&2; exit 1; }
    echo "  conversion smoke test passed"
fi

echo "==> Engine built: $OUTPUT/pcci"
du -sh "$OUTPUT/pcci"
