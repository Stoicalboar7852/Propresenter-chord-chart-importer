"""Word documents.

The real charts this project was built for are Word files: Roboto Mono, chords bold on
their own line above the lyric, and — because they were pasted out of a web chart —
sixteen leading tabs on every single line. So this ingester cares about three things:

* **Column fidelity.** Tabs expand to spaces before anything measures a column, and the
  indent every line shares is removed afterwards.
* **Run formatting.** Bold is a strong chord-line signal in these charts, and heading
  styles are a strong section-header signal. Both are carried on the ``PositionedLine``.
* **Monospace detection.** If the dominant font is fixed-pitch, column indices are
  trustworthy and alignment can use them directly.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from pcci.errors import DocumentReadError
from pcci.ingest.base import build_document, normalise_text, register, strip_common_indent
from pcci.ir import PositionedLine, RawDocument, SourceFormat

# Font families that are fixed-pitch. Word does not record pitch reliably, so the
# family name is the signal available.
MONOSPACE_FAMILIES = (
    "courier",
    "consolas",
    "menlo",
    "monaco",
    "roboto mono",
    "source code",
    "sf mono",
    "dejavu sans mono",
    "liberation mono",
    "andale mono",
    "lucida console",
    "ibm plex mono",
    "jetbrains mono",
    "fira mono",
    "fira code",
    "ubuntu mono",
    "space mono",
    "inconsolata",
    "nimbus mono",
    "pt mono",
    "cousine",
    "monospac",
)


def is_monospace_family(name: str | None) -> bool:
    if not name:
        return False
    lowered = name.casefold()
    return any(family in lowered for family in MONOSPACE_FAMILIES)


def _paragraph_text(paragraph: Any) -> str:
    """Paragraph text with tabs and line breaks preserved.

    ``python-docx``'s ``paragraph.text`` silently drops ``<w:tab/>`` and ``<w:br/>``,
    which is exactly the information chord alignment depends on.
    """
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    pieces: list[str] = []
    for node in paragraph._element.iter():
        tag = node.tag
        if tag == f"{namespace}t":
            pieces.append(node.text or "")
        elif tag == f"{namespace}tab":
            pieces.append("\t")
        elif tag in (f"{namespace}br", f"{namespace}cr"):
            pieces.append("\n")
    return "".join(pieces)


def _run_properties(paragraph: Any) -> tuple[bool, bool, float | None, str | None]:
    """Bold, italic, size and font name, as they apply to the paragraph as a whole."""
    bolds: list[bool] = []
    italics: list[bool] = []
    sizes: list[float] = []
    fonts: Counter[str] = Counter()
    for run in paragraph.runs:
        if not run.text.strip():
            continue
        bolds.append(bool(run.bold))
        italics.append(bool(run.italic))
        if run.font.size is not None:
            sizes.append(run.font.size.pt)
        name = run.font.name
        if name:
            fonts[name] += len(run.text)
    bold = bool(bolds) and all(bolds)
    italic = bool(italics) and all(italics)
    size = max(sizes) if sizes else None
    font = fonts.most_common(1)[0][0] if fonts else None
    return bold, italic, size, font


def _is_heading(paragraph: Any) -> bool:
    style = getattr(paragraph.style, "name", "") or ""
    return style.lower().startswith(("heading", "title", "subtitle"))


class DocxIngester:
    """Reads ``.docx`` Word documents."""

    extensions: tuple[str, ...] = (".docx",)
    source_format: SourceFormat = "docx"

    def load(self, path: Path) -> RawDocument:
        try:
            import docx
        except ImportError as exc:  # pragma: no cover - dependency is declared
            raise DocumentReadError(
                "Word support is not installed.", str(exc), context={"path": str(path)}
            ) from exc

        try:
            document = docx.Document(str(path))
        except Exception as exc:  # python-docx raises a variety of types
            raise DocumentReadError(
                f"{path.name} could not be opened as a Word document. "
                "If it is an older .doc file, re-save it as .docx.",
                f"{type(exc).__name__}: {exc}",
                context={"path": str(path)},
            ) from exc

        raw_lines: list[tuple[str, bool, bool, float | None, str | None, bool]] = []
        font_usage: Counter[str] = Counter()

        def add_paragraph(paragraph: Any) -> None:
            bold, italic, size, font = _run_properties(paragraph)
            if font:
                font_usage[font] += len(paragraph.text)
            heading = _is_heading(paragraph)
            for piece in _paragraph_text(paragraph).split("\n"):
                raw_lines.append((normalise_text(piece), bold, italic, size, font, heading))

        for block in _iter_block_items(document):
            if block.__class__.__name__ == "Table":
                for row in block.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            add_paragraph(paragraph)
            else:
                add_paragraph(block)

        texts, indent = strip_common_indent([line[0] for line in raw_lines])
        dominant_font = font_usage.most_common(1)[0][0] if font_usage else None
        monospace = is_monospace_family(dominant_font)

        warnings: list[str] = []
        if indent:
            warnings.append(f"Removed an indent of {indent} spaces shared by every line.")
        if not monospace:
            warnings.append(
                f"The document's main font ({dominant_font or 'unknown'}) is not fixed-pitch, "
                "so chord positions were read from spacing rather than exact columns."
            )

        lines = [
            PositionedLine(
                text=text,
                y=float(index),
                x0=0.0,
                page=1,
                bold=bold,
                italic=italic,
                font_size=size,
                font_name=font,
                heading=heading,
            )
            for index, (text, (_, bold, italic, size, font, heading)) in enumerate(
                zip(texts, raw_lines, strict=True)
            )
        ]
        return build_document(path, "docx", lines, monospace=monospace, warnings=warnings)


def _iter_block_items(document: Any) -> Any:
    """Paragraphs and tables in document order."""
    from docx.document import Document as DocumentClass
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    parent = document.element.body if isinstance(document, DocumentClass) else document
    for child in parent.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


DOCX_INGESTER = register(DocxIngester())
