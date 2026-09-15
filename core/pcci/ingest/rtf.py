"""Rich Text Format.

RTF from a word processor keeps its line structure but not always its leading
whitespace, so alignment here is treated as approximate unless the document declares a
fixed-pitch font.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

from pcci.errors import DocumentReadError
from pcci.ingest.base import (
    build_document,
    normalise_text,
    read_text,
    register,
    strip_common_indent,
)
from pcci.ingest.docx import MONOSPACE_FAMILIES
from pcci.ir import PositionedLine, RawDocument, SourceFormat

_FONT_TABLE_RE: Final[re.Pattern[str]] = re.compile(r"\\f\d+[^;{}]*?\s([A-Za-z][A-Za-z0-9 \-]*);")


def _declares_monospace(rtf_source: str) -> bool:
    if "\\fmodern" in rtf_source:
        return True
    for name in _FONT_TABLE_RE.findall(rtf_source):
        if any(family in name.casefold() for family in MONOSPACE_FAMILIES):
            return True
    return False


class RtfIngester:
    """Reads ``.rtf`` documents."""

    extensions: tuple[str, ...] = (".rtf",)
    source_format: SourceFormat = "rtf"

    def load(self, path: Path) -> RawDocument:
        source, warnings = read_text(path)
        try:
            from striprtf.striprtf import rtf_to_text
        except ImportError as exc:  # pragma: no cover - dependency is declared
            raise DocumentReadError(
                "RTF support is not installed.", str(exc), context={"path": str(path)}
            ) from exc

        if not source.lstrip().startswith("{\\rtf"):
            raise DocumentReadError(
                f"{path.name} does not look like an RTF document.",
                "missing {\\rtf header",
                context={"path": str(path)},
            )
        try:
            text = rtf_to_text(source, errors="ignore")
        except Exception as exc:
            raise DocumentReadError(
                f"{path.name} could not be read as RTF.",
                f"{type(exc).__name__}: {exc}",
                context={"path": str(path)},
            ) from exc

        monospace = _declares_monospace(source)
        if not monospace:
            warnings.append(
                "The RTF does not declare a fixed-pitch font, so chord positions were "
                "read from spacing rather than exact columns."
            )
        texts, indent = strip_common_indent(
            [normalise_text(line) for line in text.replace("\r\n", "\n").split("\n")]
        )
        if indent:
            warnings.append(f"Removed an indent of {indent} spaces shared by every line.")
        lines = [
            PositionedLine(text=line, y=float(index), page=1) for index, line in enumerate(texts)
        ]
        return build_document(path, "rtf", lines, monospace=monospace, warnings=warnings)


RTF_INGESTER = register(RtfIngester())
