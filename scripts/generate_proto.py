#!/usr/bin/env python3
"""Regenerate the Python protobuf bindings from the vendored ProPresenter .proto files.

Run from anywhere:

    core/.venv/bin/python scripts/generate_proto.py

Generated modules are committed so that a plain checkout works without
grpcio-tools installed.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROTO_ROOT = REPO_ROOT / "core" / "pcci" / "propresenter" / "proto" / "rv"
OUT_ROOT = REPO_ROOT / "core" / "pcci" / "propresenter" / "proto" / "generated"


def main() -> int:
    if not PROTO_ROOT.is_dir():
        print(f"vendored protos not found at {PROTO_ROOT}", file=sys.stderr)
        return 1

    protos = sorted(p.name for p in PROTO_ROOT.glob("*.proto"))
    if not protos:
        print("no .proto files to compile", file=sys.stderr)
        return 1

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for stale in OUT_ROOT.glob("*_pb2.py*"):
        stale.unlink()

    command = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={PROTO_ROOT}",
        f"--python_out={OUT_ROOT}",
        f"--pyi_out={OUT_ROOT}",
        *protos,
    ]
    result = subprocess.run(command, cwd=PROTO_ROOT, check=False)
    if result.returncode != 0:
        return result.returncode

    (OUT_ROOT / "__init__.py").write_text(
        '"""Generated ProPresenter protobuf bindings. Do not edit by hand.\n\n'
        "Regenerate with ``scripts/generate_proto.py``. Provenance and licence for the\n"
        "source definitions are in ``../PROVENANCE.md``.\n"
        '"""\n',
        encoding="utf-8",
    )
    generated = sorted(OUT_ROOT.glob("*_pb2.py"))
    print(f"generated {len(generated)} modules into {OUT_ROOT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
