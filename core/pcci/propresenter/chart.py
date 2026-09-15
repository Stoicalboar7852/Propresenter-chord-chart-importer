"""Rendering the chord chart to page images.

ProPresenter's own chord-chart attachment is a rasterised page (docs/FORMAT_NOTES.md
§4.4): it converts whatever you give it into one PNG per page, imports those into the
workspace, and points each slide at one of them. This module produces the same thing
from the parsed song, so the attachment pcci writes is the attachment ProPresenter
expects.

Two paths are written into each reference:

* the **absolute** path of the file pcci actually wrote, so the chart works as soon as
  the presentation is opened on this machine;
* a **show-relative** ``Media/Imported/<name>.png``, which is what resolves once the
  images are copied into the ProPresenter workspace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pcci.config import ChordPlacementStyle
from pcci.errors import OutputWriteError
from pcci.ir import Song
from pcci.notes import render_section
from pcci.propresenter.writer import ChordChartPage

#: A4 at 72 dpi, matching the pages ProPresenter produced in the reference bundle.
PAGE_WIDTH = 595.0
PAGE_HEIGHT = 842.0
MARGIN = 36.0
FONT_SIZE = 9.0
LINE_HEIGHT = 11.5
FONT_NAME = "cour"
#: Rendered at twice page size so chords stay readable on a stage display.
RENDER_SCALE = 2.0

#: Where ProPresenter keeps imported media inside a workspace.
WORKSPACE_MEDIA_PREFIX = "Media/Imported"


@dataclass
class ChartRender:
    """The rendered chart: its pages, and which page each section landed on."""

    pages: list[ChordChartPage] = field(default_factory=list)
    page_for_section: dict[int, int] = field(default_factory=dict)

    @property
    def paths(self) -> list[Path]:
        return [page.absolute_path for page in self.pages]


def _rows_for_song(song: Song, placement: ChordPlacementStyle) -> list[tuple[str, int | None]]:
    """Every printable row of the chart, tagged with the section it belongs to."""
    rows: list[tuple[str, int | None]] = [(song.title, None)]
    credits = " · ".join(
        part for part in (song.artist, f"Key of {song.key}" if song.key else "") if part
    )
    if credits:
        rows.append((credits, None))
    rows.append(("", None))
    for index, section in enumerate(song.sections):
        for row in render_section(section, placement).split("\n"):
            rows.append((row, index))
        rows.append(("", index))
    return rows


def render_chart_pages(
    song: Song,
    output_dir: Path,
    *,
    stem: str,
    placement: ChordPlacementStyle = ChordPlacementStyle.ABOVE,
) -> ChartRender:
    """Render the chart to one PNG per page under ``output_dir``."""
    try:
        import pymupdf
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise OutputWriteError(
            "Chord chart images need PyMuPDF, which is not installed.",
            str(exc),
        ) from exc

    rows = _rows_for_song(song, placement)
    rows_per_page = max(int((PAGE_HEIGHT - 2 * MARGIN) // LINE_HEIGHT), 1)
    pages = [rows[i : i + rows_per_page] for i in range(0, len(rows), rows_per_page)] or [[]]

    render = ChartRender()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OutputWriteError(
            f"pcci could not create {output_dir}.",
            str(exc),
            context={"path": str(output_dir)},
        ) from exc

    for page_number, page_rows in enumerate(pages, start=1):
        for _, section_index in page_rows:
            if section_index is not None and section_index not in render.page_for_section:
                render.page_for_section[section_index] = page_number - 1
        path = output_dir / f"{stem} chords {page_number}.png"
        _render_page(pymupdf, page_rows, path)
        render.pages.append(
            ChordChartPage(
                absolute_path=path.resolve(),
                show_relative_path=f"{WORKSPACE_MEDIA_PREFIX}/{path.name}",
            )
        )
    return render


def _render_page(pymupdf: Any, rows: list[tuple[str, int | None]], path: Path) -> None:
    document = pymupdf.open()
    page = document.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    page.draw_rect(page.rect, color=None, fill=(1, 1, 1))
    y = MARGIN + LINE_HEIGHT
    for text, _ in rows:
        if text.strip():
            page.insert_text((MARGIN, y), text, fontname=FONT_NAME, fontsize=FONT_SIZE)
        y += LINE_HEIGHT
    pixmap = page.get_pixmap(matrix=pymupdf.Matrix(RENDER_SCALE, RENDER_SCALE))
    try:
        pixmap.save(str(path))
    except (OSError, RuntimeError) as exc:
        raise OutputWriteError(
            f"pcci could not write the chord chart image {path.name}.",
            str(exc),
            context={"path": str(path)},
        ) from exc
    finally:
        document.close()
