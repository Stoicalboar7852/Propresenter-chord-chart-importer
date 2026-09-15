"""Plain text.

The simplest and most trustworthy source: what you see is what the columns are.
"""

from __future__ import annotations

from pathlib import Path

from pcci.ingest.base import build_document, read_text, register, split_lines, strip_common_indent
from pcci.ir import PositionedLine, RawDocument, SourceFormat


class TextIngester:
    """Reads ``.txt`` and other plain-text chord charts."""

    extensions: tuple[str, ...] = (".txt", ".text", ".chord", ".chart", "")
    source_format: SourceFormat = "txt"

    def load(self, path: Path) -> RawDocument:
        text, warnings = read_text(path)
        texts, indent = strip_common_indent(split_lines(text))
        if indent:
            warnings.append(f"Removed an indent of {indent} spaces shared by every line.")
        lines = [
            PositionedLine(text=line, y=float(index), page=1) for index, line in enumerate(texts)
        ]
        return build_document(path, "txt", lines, monospace=True, warnings=warnings)


TEXT_INGESTER = register(TextIngester())
