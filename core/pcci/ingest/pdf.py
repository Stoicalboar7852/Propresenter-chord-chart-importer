"""PDF, with real glyph positions.

A PDF has no lines and no spaces — only glyphs at coordinates. Everything a chord chart
depends on has to be reconstructed:

1. **Columns.** Charts are routinely typeset in two columns. Clustering by y first would
   weld the left and right columns into single nonsense lines, so gutters are found and
   each column is read on its own, left to right.
2. **Lines.** Glyphs within 30% of the median glyph height of each other share a
   baseline.
3. **Spaces.** A gap wider than 40% of the font's space advance becomes one or more
   spaces, sized so that the reconstructed column of each character stays proportional
   to its real x position.

``char_x`` is populated for every line, so alignment never has to trust the
reconstructed spacing — it can binary-search real coordinates.
"""

from __future__ import annotations

import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from pcci.errors import DocumentReadError, ImageOnlyPdfError
from pcci.ingest.base import build_document, normalise_text, register
from pcci.ingest.docx import is_monospace_family
from pcci.ir import PositionedLine, RawDocument, SourceFormat

#: Fraction of the median glyph height within which glyphs share a baseline.
LINE_TOLERANCE: Final[float] = 0.30
#: Fraction of a space advance that counts as a real gap between glyphs.
SPACE_GAP_RATIO: Final[float] = 0.40
#: A gutter must be at least this fraction of the page width to split columns.
GUTTER_RATIO: Final[float] = 0.035


@dataclass(frozen=True, slots=True)
class Glyph:
    char: str
    x0: float
    x1: float
    y: float
    height: float
    font: str
    size: float


def _extract_glyphs(page: Any) -> list[Glyph]:
    glyphs: list[Glyph] = []
    raw = page.get_text("rawdict")
    for block in raw.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                font = span.get("font", "")
                size = float(span.get("size", 0.0))
                for char in span.get("chars", []):
                    text = char.get("c", "")
                    if not text or text.isspace():
                        continue
                    x0, top, x1, bottom = char["bbox"]
                    glyphs.append(
                        Glyph(
                            char=text,
                            x0=float(x0),
                            x1=float(x1),
                            y=float(char.get("origin", (0.0, bottom))[1]),
                            height=float(bottom - top),
                            font=font,
                            size=size,
                        )
                    )
    return glyphs


def _find_columns(glyphs: list[Glyph], page_width: float) -> list[tuple[float, float]]:
    """Split the page into column bands by looking for empty vertical gutters."""
    if not glyphs:
        return [(0.0, page_width)]
    occupied = [False] * (int(page_width) + 2)
    for glyph in glyphs:
        for x in range(max(int(glyph.x0), 0), min(int(glyph.x1) + 1, len(occupied))):
            occupied[x] = True

    minimum_gutter = max(int(page_width * GUTTER_RATIO), 8)
    bands: list[tuple[float, float]] = []
    start: int | None = None
    run = 0
    for x, filled in enumerate(occupied):
        if filled:
            if start is None:
                start = x
            if run and run >= minimum_gutter and bands:
                pass
            run = 0
        else:
            run += 1
            if start is not None and run >= minimum_gutter:
                bands.append((float(start), float(x - run)))
                start = None
    if start is not None:
        bands.append((float(start), float(len(occupied))))
    if not bands:
        return [(0.0, page_width)]
    # A band narrower than a fifth of the page is a stray element, not a column.
    wide = [band for band in bands if band[1] - band[0] >= page_width * 0.2]
    return wide or [(0.0, page_width)]


def _cluster_lines(glyphs: list[Glyph]) -> list[list[Glyph]]:
    """Group glyphs into baselines."""
    if not glyphs:
        return []
    heights = [glyph.height for glyph in glyphs if glyph.height > 0]
    tolerance = (statistics.median(heights) if heights else 10.0) * LINE_TOLERANCE
    rows: list[list[Glyph]] = []
    for glyph in sorted(glyphs, key=lambda g: (g.y, g.x0)):
        if rows and abs(glyph.y - rows[-1][0].y) <= tolerance:
            rows[-1].append(glyph)
        else:
            rows.append([glyph])
    return [sorted(row, key=lambda g: g.x0) for row in rows]


def _space_advance(row: list[Glyph]) -> float:
    """An estimate of one space's width for this row."""
    widths = [glyph.x1 - glyph.x0 for glyph in row if glyph.x1 > glyph.x0]
    if widths:
        return statistics.median(widths)
    sizes = [glyph.size for glyph in row if glyph.size]
    return (statistics.median(sizes) if sizes else 10.0) * 0.5


def _row_to_line(row: list[Glyph], page_number: int) -> PositionedLine:
    """Rebuild one line of text, with a real x for every character."""
    advance = _space_advance(row)
    threshold = advance * SPACE_GAP_RATIO
    characters: list[str] = []
    positions: list[float] = []
    previous_x1: float | None = None
    for glyph in row:
        if previous_x1 is not None:
            gap = glyph.x0 - previous_x1
            if gap > threshold:
                spaces = max(1, round(gap / advance))
                for index in range(spaces):
                    characters.append(" ")
                    positions.append(previous_x1 + advance * index)
        characters.append(glyph.char)
        positions.append(glyph.x0)
        previous_x1 = glyph.x1

    text = "".join(characters)
    normalised = normalise_text(text)
    if len(normalised) != len(text):
        # normalise_text may expand or drop characters; keep positions consistent by
        # falling back to the untouched text when lengths diverge.
        trimmed = text.rstrip()
        positions = positions[: len(trimmed)]
        normalised = trimmed
    else:
        positions = positions[: len(normalised)]

    fonts = Counter(glyph.font for glyph in row)
    sizes = [glyph.size for glyph in row if glyph.size]
    return PositionedLine(
        text=normalised,
        y=row[0].y,
        x0=row[0].x0,
        char_x=positions,
        page=page_number,
        font_name=fonts.most_common(1)[0][0] if fonts else None,
        font_size=statistics.median(sizes) if sizes else None,
    )


class PdfIngester:
    """Reads ``.pdf`` chord charts, positions and all."""

    extensions: tuple[str, ...] = (".pdf",)
    source_format: SourceFormat = "pdf"

    def load(self, path: Path) -> RawDocument:
        try:
            import pymupdf
        except ImportError as exc:  # pragma: no cover - dependency is declared
            raise DocumentReadError(
                "PDF support is not installed.", str(exc), context={"path": str(path)}
            ) from exc

        try:
            document: Any = pymupdf.open(str(path))
        except Exception as exc:
            raise DocumentReadError(
                f"{path.name} could not be opened as a PDF.",
                f"{type(exc).__name__}: {exc}",
                context={"path": str(path)},
            ) from exc

        warnings: list[str] = []
        lines: list[PositionedLine] = []
        fonts: Counter[str] = Counter()
        empty_pages: list[int] = []

        with document:
            for page_index, page in enumerate(iter(document), start=1):
                glyphs = _extract_glyphs(page)
                if not glyphs:
                    empty_pages.append(page_index)
                    continue
                for glyph in glyphs:
                    fonts[glyph.font] += 1
                page_width = float(page.rect.width)
                columns = _find_columns(glyphs, page_width)
                for left, right in columns:
                    column_glyphs = [g for g in glyphs if left <= g.x0 < right]
                    for row in _cluster_lines(column_glyphs):
                        lines.append(_row_to_line(row, page_index))
                    if len(columns) > 1:
                        lines.append(PositionedLine(text="", y=0.0, page=page_index))
                if len(columns) > 1:
                    warnings.append(
                        f"Page {page_index} was read as {len(columns)} columns, left to right."
                    )

        if not lines:
            raise ImageOnlyPdfError(
                f"{path.name} has no text in it — it looks like a scan or a photo. "
                "pcci cannot read chords out of an image; export or print the chart to "
                "a text PDF and try again.",
                f"no glyphs on any of {len(empty_pages)} page(s)",
                context={"path": str(path), "pages": len(empty_pages)},
            )
        if empty_pages:
            warnings.append(
                f"Page(s) {', '.join(str(p) for p in empty_pages)} contain no text and were skipped."
            )

        dominant_font = fonts.most_common(1)[0][0] if fonts else None
        monospace = is_monospace_family(dominant_font)
        if not monospace:
            warnings.append(
                f"The PDF's main font ({dominant_font or 'unknown'}) is not fixed-pitch, so "
                "chords were aligned by their position on the page rather than by column."
            )
        return build_document(path, "pdf", lines, monospace=monospace, warnings=warnings)


PDF_INGESTER = register(PdfIngester())
