#!/usr/bin/env python3
"""Generate the multi-format fixture corpus from the real Word charts.

    core/.venv/bin/python scripts/make_fixtures.py

The point is that the *same song* exists in every supported format, so a parser
regression shows up as a difference between formats rather than hiding in one of them.
Everything is derived from ``core/tests/fixtures/*.docx``, which are real charts, so the
generated files keep real spacing, real chords and real section labels.
"""

from __future__ import annotations

import html as html_module
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from pcci.ingest.docx import DocxIngester  # noqa: E402

FIXTURES = REPO_ROOT / "core" / "tests" / "fixtures"
SOURCE = FIXTURES / "GOODBYE YESTERDAY A.docx"
STEM = "goodbye_yesterday"

MONOSPACE_PDF_FONT = "cour"
PDF_FONT_SIZE = 9.0
PDF_LINE_HEIGHT = 12.0
PDF_MARGIN = 40.0


def source_lines() -> list[str]:
    document = DocxIngester().load(SOURCE)
    lines = [line.text for line in document.lines]
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def write_txt(lines: list[str], directory: Path) -> Path:
    path = directory / f"{STEM}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_markdown(lines: list[str], directory: Path) -> Path:
    path = directory / f"{STEM}.md"
    out: list[str] = [f"# {lines[0]}", ""]
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            out.extend(["", f"## {stripped[1:-1]}", ""])
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path


def write_html_pre(lines: list[str], directory: Path) -> Path:
    path = directory / f"{STEM}.html"
    body = html_module.escape("\n".join(lines))
    path.write_text(
        "<!doctype html>\n<html><head><meta charset='utf-8'>"
        f"<title>{html_module.escape(lines[0])}</title></head>\n"
        f"<body>\n<pre>{body}</pre>\n</body></html>\n",
        encoding="utf-8",
    )
    return path


def write_html_blocks(lines: list[str], directory: Path) -> Path:
    """The awkward variant: no <pre>, so spacing has to survive as &nbsp;."""
    path = directory / f"{STEM}_no_pre.html"
    parts = ["<!doctype html>", "<html><head><meta charset='utf-8'></head><body>"]
    for line in lines:
        if not line.strip():
            parts.append("<p></p>")
            continue
        escaped = html_module.escape(line).replace("  ", "&nbsp;&nbsp;")
        parts.append(f"<div>{escaped}</div>")
    parts.append("</body></html>")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return path


def write_rtf(lines: list[str], directory: Path) -> Path:
    path = directory / f"{STEM}.rtf"
    body: list[str] = []
    for line in lines:
        escaped = (
            line.replace("\\", "\\\\")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace(" ", "\\~")  # non-breaking space keeps alignment through RTF readers
        )
        body.append(escaped + "\\par")
    path.write_text(
        "{\\rtf1\\ansi\\ansicpg1252\\deff0"
        "{\\fonttbl{\\f0\\fmodern\\fcharset0 Courier New;}}"
        "\\f0\\fs18\n" + "\n".join(body) + "\n}\n",
        encoding="utf-8",
    )
    return path


def write_odt(lines: list[str], directory: Path) -> Path:
    from odf.opendocument import OpenDocumentText
    from odf.style import FontFace, Style, TextProperties
    from odf.text import P, S

    path = directory / f"{STEM}.odt"
    document = OpenDocumentText()
    document.fontfacedecls.addElement(
        FontFace(name="Courier New", fontfamily="Courier New", fontpitch="fixed")
    )
    monospace = Style(name="Mono", family="paragraph")
    monospace.addElement(TextProperties(fontname="Courier New", fontsize="9pt"))
    document.styles.addElement(monospace)

    for line in lines:
        paragraph = P(stylename=monospace)
        remainder = line
        while remainder:
            if remainder.startswith(" "):
                count = len(remainder) - len(remainder.lstrip(" "))
                paragraph.addElement(S(c=count))
                remainder = remainder[count:]
            else:
                index = remainder.find(" ")
                chunk = remainder if index < 0 else remainder[:index]
                paragraph.addText(chunk)
                remainder = remainder[len(chunk) :]
        document.text.addElement(paragraph)
    document.save(str(path))
    return path


def write_pdf(lines: list[str], directory: Path, *, columns: int = 1) -> Path:
    import pymupdf

    suffix = "" if columns == 1 else f"_{columns}col"
    path = directory / f"{STEM}{suffix}.pdf"
    document = pymupdf.open()
    # Multi-column charts go on landscape paper so that the longest line still fits
    # inside its column and a real gutter survives between them — an overlapping
    # "two column" page is not two columns, it is one messy one.
    page_width, page_height = (595.0, 842.0) if columns == 1 else (842.0, 595.0)
    gutter = 0.0 if columns == 1 else 36.0
    usable_height = page_height - 2 * PDF_MARGIN
    rows_per_column = int(usable_height // PDF_LINE_HEIGHT)
    column_width = (page_width - 2 * PDF_MARGIN - gutter * (columns - 1)) / columns

    chunks = [lines[i : i + rows_per_column] for i in range(0, len(lines), rows_per_column)]
    page = None
    for index, chunk in enumerate(chunks):
        column = index % columns
        if column == 0:
            page = document.new_page(width=page_width, height=page_height)
        assert page is not None
        x = PDF_MARGIN + column * (column_width + gutter)
        y = PDF_MARGIN + PDF_LINE_HEIGHT
        for line in chunk:
            if line.strip():
                page.insert_text(
                    (x, y), line, fontname=MONOSPACE_PDF_FONT, fontsize=PDF_FONT_SIZE
                )
            y += PDF_LINE_HEIGHT
    document.save(str(path))
    document.close()
    return path


def write_scanned_pdf(lines: list[str], directory: Path) -> Path:
    """A PDF with no text layer at all, for the image-only error path."""
    import pymupdf

    path = directory / "scanned_no_text_layer.pdf"
    source = pymupdf.open()
    page = source.new_page(width=595.0, height=842.0)
    y = PDF_MARGIN + PDF_LINE_HEIGHT
    for line in lines[:60]:
        if line.strip():
            page.insert_text((PDF_MARGIN, y), line, fontname=MONOSPACE_PDF_FONT, fontsize=9)
        y += PDF_LINE_HEIGHT
    # Greyscale JPEG at screen resolution: still unmistakably a scan, but small
    # enough to live in the repository.
    pixmap = page.get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
    source.close()

    scanned = pymupdf.open()
    image_page = scanned.new_page(width=595.0, height=842.0)
    image_page.insert_image(image_page.rect, stream=pixmap.tobytes("jpg", jpg_quality=60))
    scanned.save(str(path), deflate=True, garbage=4)
    scanned.close()
    return path


def main() -> int:
    lines = source_lines()
    written: list[Path] = []
    for name in ("text", "html", "rtf", "odt", "pdf"):
        (FIXTURES / name).mkdir(parents=True, exist_ok=True)

    written.append(write_txt(lines, FIXTURES / "text"))
    written.append(write_markdown(lines, FIXTURES / "text"))
    written.append(write_html_pre(lines, FIXTURES / "html"))
    written.append(write_html_blocks(lines, FIXTURES / "html"))
    written.append(write_rtf(lines, FIXTURES / "rtf"))
    written.append(write_odt(lines, FIXTURES / "odt"))
    written.append(write_pdf(lines, FIXTURES / "pdf"))
    written.append(write_pdf(lines, FIXTURES / "pdf", columns=2))
    written.append(write_scanned_pdf(lines, FIXTURES / "pdf"))

    for path in written:
        print(f"  {path.relative_to(REPO_ROOT)}  ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
