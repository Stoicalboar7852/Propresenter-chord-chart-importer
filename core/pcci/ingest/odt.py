"""OpenDocument text.

ODT encodes runs of spaces as ``<text:s c="n"/>`` and tabs as ``<text:tab/>``, so the
raw element text loses exactly the whitespace chord alignment needs. This ingester
reconstructs it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pcci.errors import DocumentReadError
from pcci.ingest.base import build_document, normalise_text, register, strip_common_indent
from pcci.ingest.docx import is_monospace_family
from pcci.ir import PositionedLine, RawDocument, SourceFormat

_TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"


def _node_text(node: Any) -> str:
    """Recover a paragraph's text with its whitespace intact."""
    from odf.element import Text

    pieces: list[str] = []
    for child in node.childNodes:
        if isinstance(child, Text):
            pieces.append(child.data)
            continue
        qname = getattr(child, "qname", None)
        if qname and qname[0] == _TEXT_NS:
            local = qname[1]
            if local == "s":
                count = child.getAttribute("c")
                pieces.append(" " * (int(count) if count else 1))
                continue
            if local == "tab":
                pieces.append("\t")
                continue
            if local == "line-break":
                pieces.append("\n")
                continue
        pieces.append(_node_text(child))
    return "".join(pieces)


class OdtIngester:
    """Reads ``.odt`` OpenDocument text documents."""

    extensions: tuple[str, ...] = (".odt", ".fodt")
    source_format: SourceFormat = "odt"

    def load(self, path: Path) -> RawDocument:
        try:
            from odf.opendocument import load as load_odf
            from odf.text import H, P
        except ImportError as exc:  # pragma: no cover - dependency is declared
            raise DocumentReadError(
                "OpenDocument support is not installed.",
                str(exc),
                context={"path": str(path)},
            ) from exc

        try:
            document = load_odf(str(path))
        except Exception as exc:
            raise DocumentReadError(
                f"{path.name} could not be opened as an OpenDocument file.",
                f"{type(exc).__name__}: {exc}",
                context={"path": str(path)},
            ) from exc

        entries: list[tuple[str, bool]] = []
        for node in document.getElementsByType(P) + document.getElementsByType(H):
            is_heading = node.qname[1] == "h"
            for piece in _node_text(node).split("\n"):
                entries.append((normalise_text(piece), is_heading))

        fonts = [
            face.getAttribute("name") or ""
            for face in document.fontfacedecls.childNodes
            if hasattr(face, "getAttribute")
        ]
        monospace = any(is_monospace_family(name) for name in fonts)

        warnings: list[str] = []
        if not monospace:
            warnings.append(
                "The document does not use a fixed-pitch font, so chord positions were "
                "read from spacing rather than exact columns."
            )
        texts, indent = strip_common_indent([entry[0] for entry in entries])
        if indent:
            warnings.append(f"Removed an indent of {indent} spaces shared by every line.")

        lines = [
            PositionedLine(text=text, y=float(index), page=1, heading=entries[index][1])
            for index, text in enumerate(texts)
        ]
        return build_document(path, "odt", lines, monospace=monospace, warnings=warnings)


ODT_INGESTER = register(OdtIngester())
