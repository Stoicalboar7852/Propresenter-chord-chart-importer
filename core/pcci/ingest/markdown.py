"""Markdown.

Markdown is plain text with decoration. The decoration has to go, but the *columns*
must not move: in a monospaced chart, deleting two asterisks from a chord line slides
every chord two characters to the left. So emphasis markers are replaced by spaces
rather than removed, which keeps alignment exact and costs nothing but trailing
whitespace, which is stripped anyway.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

from pcci.ingest.base import build_document, read_text, register, split_lines, strip_common_indent
from pcci.ir import PositionedLine, RawDocument, SourceFormat

_FENCE_RE: Final[re.Pattern[str]] = re.compile(r"^\s*(```|~~~)")
_HEADING_RE: Final[re.Pattern[str]] = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
_SETEXT_RE: Final[re.Pattern[str]] = re.compile(r"^\s*(=+|-{2,})\s*$")
_EMPHASIS_RE: Final[re.Pattern[str]] = re.compile(r"\*\*|__|\*|_|`")
_LINK_RE: Final[re.Pattern[str]] = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def _strip_emphasis(text: str) -> str:
    """Blank out emphasis markers in place so column positions survive."""
    return _EMPHASIS_RE.sub(lambda match: " " * len(match.group()), text)


class MarkdownIngester:
    """Reads ``.md`` / ``.markdown`` chord charts."""

    extensions: tuple[str, ...] = (".md", ".markdown", ".mdown")
    source_format: SourceFormat = "md"

    def load(self, path: Path) -> RawDocument:
        text, warnings = read_text(path)
        source_lines = split_lines(text)

        processed: list[tuple[str, bool]] = []
        in_fence = False
        for index, line in enumerate(source_lines):
            if _FENCE_RE.match(line):
                in_fence = not in_fence
                processed.append(("", False))
                continue
            if in_fence:
                processed.append((line, False))
                continue
            if _SETEXT_RE.match(line) and index and source_lines[index - 1].strip():
                # Underline of a setext heading: mark the line above, drop this one.
                previous_text, _ = processed[index - 1]
                processed[index - 1] = (previous_text, True)
                processed.append(("", False))
                continue
            heading = _HEADING_RE.match(line)
            if heading:
                processed.append((heading.group("text"), True))
                continue
            processed.append((_strip_emphasis(_LINK_RE.sub(r"\1", line)).rstrip(), False))

        texts, indent = strip_common_indent([item[0] for item in processed])
        if indent:
            warnings.append(f"Removed an indent of {indent} spaces shared by every line.")

        lines = [
            PositionedLine(text=body, y=float(index), page=1, heading=is_heading)
            for index, (body, (_, is_heading)) in enumerate(zip(texts, processed, strict=True))
        ]
        return build_document(path, "md", lines, monospace=True, warnings=warnings)


MARKDOWN_INGESTER = register(MarkdownIngester())
