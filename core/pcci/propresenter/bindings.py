"""Access to the generated ProPresenter protobuf bindings.

The vendored ``.proto`` files import each other by bare filename
(``import "slide.proto"``), so protoc emits flat modules that expect their own
directory on ``sys.path``. Rather than rewriting 137 generated files, this module
owns that one piece of import plumbing and hands back a typed namespace.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import ModuleType

from pcci.errors import ProtoSchemaMismatchError

GENERATED_DIR = Path(__file__).resolve().parent / "proto" / "generated"

# The ProPresenter release the vendored definitions were generated from; see
# proto/PROVENANCE.md and proto/rv/version.txt.
PROTO_SOURCE_VERSION = "21.4"
PROTO_SOURCE_BUILD = "352583705"


@dataclass(frozen=True)
class Bindings:
    """The handful of generated modules the engine actually uses."""

    presentation: ModuleType
    application_info: ModuleType
    slide: ModuleType
    presentation_slide: ModuleType
    graphics_data: ModuleType
    cue: ModuleType
    action: ModuleType
    groups: ModuleType
    color: ModuleType
    uuid: ModuleType
    url: ModuleType
    hot_key: ModuleType
    font: ModuleType


@lru_cache(maxsize=1)
def load_bindings() -> Bindings:
    """Import the generated modules, or explain clearly why they are missing."""
    if not GENERATED_DIR.is_dir():
        raise ProtoSchemaMismatchError(
            "The ProPresenter file format bindings are missing from this install.",
            f"{GENERATED_DIR} does not exist; run scripts/generate_proto.py",
        )
    path_entry = str(GENERATED_DIR)
    if path_entry not in sys.path:
        sys.path.insert(0, path_entry)

    try:
        import action_pb2
        import applicationInfo_pb2
        import color_pb2
        import cue_pb2
        import font_pb2
        import graphicsData_pb2
        import groups_pb2
        import hotKey_pb2
        import presentation_pb2
        import presentationSlide_pb2
        import slide_pb2
        import url_pb2
        import uuid_pb2
    except ImportError as exc:  # pragma: no cover - only fires on a broken install
        raise ProtoSchemaMismatchError(
            "The ProPresenter file format bindings could not be loaded.",
            f"import failed: {exc}; run scripts/generate_proto.py",
        ) from exc

    return Bindings(
        presentation=presentation_pb2,
        application_info=applicationInfo_pb2,
        slide=slide_pb2,
        presentation_slide=presentationSlide_pb2,
        graphics_data=graphicsData_pb2,
        cue=cue_pb2,
        action=action_pb2,
        groups=groups_pb2,
        color=color_pb2,
        uuid=uuid_pb2,
        url=url_pb2,
        hot_key=hotKey_pb2,
        font=font_pb2,
    )
