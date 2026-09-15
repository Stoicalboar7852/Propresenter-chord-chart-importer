"""HTML.

Chord charts on the web are almost always inside a ``<pre>`` block, because that is the
only way HTML preserves the spacing the chart depends on. When one is present this
ingester trusts it completely and treats the document as monospaced; otherwise it
reconstructs lines from block elements and ``<br>`` and says that alignment is
approximate.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Final

from pcci.errors import DocumentReadError
from pcci.ingest.base import (
    build_document,
    normalise_text,
    read_text,
    register,
    strip_common_indent,
)
from pcci.ingest.docx import is_monospace_family
from pcci.ir import PositionedLine, RawDocument, SourceFormat

_BLOCK_TAGS: Final[tuple[str, ...]] = (
    "p",
    "div",
    "li",
    "tr",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "section",
    "article",
    "blockquote",
    "td",
    "th",
)
_HEADING_TAGS: Final[frozenset[str]] = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_DROP_TAGS: Final[tuple[str, ...]] = ("script", "style", "head", "noscript", "svg")
_MONOSPACE_STYLE_RE: Final[re.Pattern[str]] = re.compile(r"font-family\s*:\s*([^;\"']+)", re.I)


def _looks_monospace(soup: Any) -> bool:
    if soup.find("pre") is not None:
        return True
    for element in soup.find_all(style=True):
        match = _MONOSPACE_STYLE_RE.search(element["style"])
        if match and (is_monospace_family(match.group(1)) or "monospace" in match.group(1).lower()):
            return True
    for style in soup.find_all("style"):
        text = style.get_text()
        if "monospace" in text.lower() or is_monospace_family(text):
            return True
    return False


class HtmlIngester:
    """Reads ``.html`` / ``.htm`` chord charts."""

    extensions: tuple[str, ...] = (".html", ".htm", ".xhtml")
    source_format: SourceFormat = "html"

    def load(self, path: Path) -> RawDocument:
        source, warnings = read_text(path)
        try:
            from bs4 import BeautifulSoup
        except ImportError as exc:  # pragma: no cover - dependency is declared
            raise DocumentReadError(
                "HTML support is not installed.", str(exc), context={"path": str(path)}
            ) from exc

        soup = BeautifulSoup(source, "html.parser")
        for tag_name in _DROP_TAGS:
            for element in soup.find_all(tag_name):
                element.decompose()

        monospace = _looks_monospace(soup)
        entries: list[tuple[str, bool]] = []

        preformatted = soup.find_all("pre")
        if preformatted:
            for block in preformatted:
                for piece in block.get_text().replace("\r\n", "\n").split("\n"):
                    entries.append((normalise_text(piece), False))
                entries.append(("", False))
        else:
            for element in soup.find_all(_BLOCK_TAGS):
                if element.find(_BLOCK_TAGS):
                    continue  # only take the innermost block, or text repeats
                for br in element.find_all("br"):
                    br.replace_with("\n")
                is_heading = element.name in _HEADING_TAGS
                for piece in element.get_text().replace("\r\n", "\n").split("\n"):
                    entries.append((normalise_text(piece), is_heading))
            if not entries:
                for piece in soup.get_text().replace("\r\n", "\n").split("\n"):
                    entries.append((normalise_text(piece), False))
            warnings.append(
                "This page has no <pre> block, so the chart's spacing was rebuilt from "
                "the HTML structure and chord positions may be approximate."
            )

        texts, indent = strip_common_indent([entry[0] for entry in entries])
        if indent:
            warnings.append(f"Removed an indent of {indent} spaces shared by every line.")

        lines = [
            PositionedLine(text=text, y=float(index), page=1, heading=entries[index][1])
            for index, text in enumerate(texts)
        ]
        return build_document(path, "html", lines, monospace=monospace, warnings=warnings)


HTML_INGESTER = register(HtmlIngester())
