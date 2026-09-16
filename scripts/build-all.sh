#!/usr/bin/env bash
# Build every target, on machines that can actually build them.
#
#   scripts/build-all.sh [all|windows-x64|windows-arm64|macos] [--wait]
#
# The engine cannot be cross-compiled: PyInstaller freezes with the interpreter it runs
# on, and the Mac app needs Xcode, which needs a Mac. So rather than pretend a Linux box
# can produce a Windows build, this starts the Build all workflow on GitHub's runners
# and, with --wait, brings the finished artifacts back here.
#
# Needs the GitHub CLI (https://cli.github.com) and a push to have happened: the
# workflow builds what is on the branch, not what is in your working tree.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGETS="all"
WAIT=0

for argument in "$@"; do
    case "$argument" in
        all|windows-x64|windows-arm64|macos) TARGETS="$argument" ;;
        --wait) WAIT=1 ;;
        *) echo "unknown option: $argument" >&2; exit 2 ;;
    esac
done

BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"

if ! command -v gh >/dev/null 2>&1; then
    cat >&2 <<MESSAGE
The GitHub CLI is not installed, so this cannot start the build for you.

Either install it (https://cli.github.com), or start the build in a browser:

    Actions -> Build all -> Run workflow -> $BRANCH

MESSAGE
    exit 1
fi

if [[ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]]; then
    echo "note: you have uncommitted changes; the runners build $BRANCH as pushed." >&2
fi

echo "==> Starting Build all ($TARGETS) on $BRANCH"
gh workflow run build-all.yml --ref "$BRANCH" -f "targets=$TARGETS"

# The run takes a moment to appear, and asking for it too early finds the previous one.
sleep 5
RUN_ID="$(gh run list --workflow build-all.yml --branch "$BRANCH" --limit 1 \
    --json databaseId --jq '.[0].databaseId')"
echo "==> Run $RUN_ID: $(gh run view "$RUN_ID" --json url --jq .url)"

if [[ "$WAIT" != "1" ]]; then
    echo "    (pass --wait to follow it and download what it builds)"
    exit 0
fi

gh run watch "$RUN_ID" --exit-status
DESTINATION="$REPO_ROOT/build/remote"
mkdir -p "$DESTINATION"
gh run download "$RUN_ID" --dir "$DESTINATION"
echo "==> Downloaded into $DESTINATION"
find "$DESTINATION" -type f -maxdepth 2 -print
