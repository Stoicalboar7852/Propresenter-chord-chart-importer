#!/usr/bin/env python3
"""Draw the background for the macOS disk image.

    python3 scripts/make_dmg_background.py            # regenerate
    python3 scripts/make_dmg_background.py --check    # fail if the committed art is stale

Writes ``assets/dmg-background.png`` and ``assets/dmg-background@2x.png``, which
``scripts/build-macos.sh`` copies into the image as ``.background/``. The window is 660
by 420 points, and the icon positions in that script have to match the plates drawn
here.

Drawn through PyMuPDF onto a PDF page and rendered at 1x and 2x, so it needs nothing
the engine does not already depend on and the text uses a built-in font rather than
whatever happens to be installed.

**The plates are not decoration.** Finder draws icon labels in the system's text
colour: black in light appearance, white in dark. Dark text on a dark background is
unreadable, and so is white text on a light one, so the two label areas sit on
mid-toned plates that both colours can be read against.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
OUTPUTS = ((ASSETS / "dmg-background.png", 1), (ASSETS / "dmg-background@2x.png", 2))

WIDTH, HEIGHT = 660, 420

#: Where build-macos.sh puts the two icons, as Finder measures them: the centre of a
#: 128 point icon, from the top left of the window. The label sits just below, so the
#: plate has to cover both.
APP_ICON_CENTRE = (170, 200)
APPLICATIONS_ICON_CENTRE = (490, 200)
ICON_SIZE = 128
PLATE_WIDTH, PLATE_HEIGHT = 196, 182
PLATE_RADIUS = 18

BACKDROP = (0.086, 0.086, 0.094)  # #161618
BACKDROP_TOP = (0.145, 0.145, 0.157)  # #252528
PLATE = (0.337, 0.337, 0.360)  # #56565C, legible under black or white labels
PLATE_EDGE = (0.451, 0.451, 0.478)
ORANGE = (1.0, 0.478, 0.0)  # #FF7A00
ORANGE_DEEP = (1.0, 0.239, 0.0)  # #FF3D00
HEADING = (0.961, 0.957, 0.949)
SUBDUED = (0.627, 0.627, 0.651)


def draw(page: pymupdf.Page) -> None:
    # A vertical ramp, painted as strips: MuPDF will not draw an SVG gradient and a
    # PDF shading pattern is a lot of machinery for sixty rectangles.
    strips = 60
    for index in range(strips):
        fraction = index / (strips - 1)
        colour = tuple(
            top + (bottom - top) * fraction
            for top, bottom in zip(BACKDROP_TOP, BACKDROP, strict=True)
        )
        page.draw_rect(
            pymupdf.Rect(0, HEIGHT * index / strips, WIDTH, HEIGHT * (index + 1) / strips + 1),
            color=None,
            fill=colour,
        )

    for centre in (APP_ICON_CENTRE, APPLICATIONS_ICON_CENTRE):
        # Top edge a little above the icon, bottom edge below where the label lands.
        top = centre[1] - ICON_SIZE / 2 - 18
        plate = pymupdf.Rect(
            centre[0] - PLATE_WIDTH / 2,
            top,
            centre[0] + PLATE_WIDTH / 2,
            top + PLATE_HEIGHT,
        )
        page.draw_rect(plate, radius=PLATE_RADIUS / PLATE_HEIGHT, color=PLATE_EDGE, fill=PLATE)

    draw_arrow(page)

    heading = "ProPresenter Chord Chart Importer"
    page.insert_text(
        (centred(heading, 20, bold=True), 72),
        heading,
        fontsize=20,
        fontname="hebo",
        color=HEADING,
    )
    instruction = "Drag PCCI into your Applications folder"
    page.insert_text(
        (centred(instruction, 12), 100),
        instruction,
        fontsize=12,
        fontname="helv",
        color=SUBDUED,
    )
    footer = "Unsigned build - right-click PCCI and choose Open the first time"
    page.insert_text(
        (centred(footer, 10), 388),
        footer,
        fontsize=10,
        fontname="helv",
        color=SUBDUED,
    )


def centred(text: str, size: float, *, bold: bool = False) -> float:
    """Left edge that centres this text on the window."""
    width = pymupdf.get_text_length(text, fontname="hebo" if bold else "helv", fontsize=size)
    return (WIDTH - width) / 2


def draw_arrow(page: pymupdf.Page) -> None:
    """The arrow between the plates: a shaft and a head, level with the two icons."""
    left = APP_ICON_CENTRE[0] + PLATE_WIDTH / 2 + 18
    right = APPLICATIONS_ICON_CENTRE[0] - PLATE_WIDTH / 2 - 18
    middle = APP_ICON_CENTRE[1]
    head = 30.0
    half = 8.0

    page.draw_rect(
        pymupdf.Rect(left, middle - half, right - head + 2, middle + half),
        radius=0.4,
        color=None,
        fill=ORANGE,
    )

    shape = page.new_shape()
    shape.draw_polyline(
        [
            pymupdf.Point(right - head, middle - half * 2.8),
            pymupdf.Point(right, middle),
            pymupdf.Point(right - head, middle + half * 2.8),
        ]
    )
    shape.finish(color=None, fill=ORANGE_DEEP, closePath=True)
    shape.commit()


def render() -> dict[Path, bytes]:
    document = pymupdf.open()
    page = document.new_page(width=WIDTH, height=HEIGHT)
    draw(page)
    images: dict[Path, bytes] = {}
    for path, scale in OUTPUTS:
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
        expected = (WIDTH * scale, HEIGHT * scale)
        if (pixmap.width, pixmap.height) != expected:
            raise SystemExit(f"rendered {pixmap.width}x{pixmap.height}, wanted {expected}")
        images[path] = bytes(pixmap.tobytes("png"))
    document.close()
    return images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the art is out of date")
    arguments = parser.parse_args()

    images = render()
    if arguments.check:
        stale = [
            path.relative_to(REPO_ROOT)
            for path, data in images.items()
            if not path.exists() or path.read_bytes() != data
        ]
        if stale:
            print(
                "stale: " + ", ".join(str(path) for path in stale),
                "\nrun: python3 scripts/make_dmg_background.py",
                file=sys.stderr,
            )
            return 1
        print("disk image background is up to date")
        return 0

    ASSETS.mkdir(parents=True, exist_ok=True)
    for path, data in images.items():
        path.write_bytes(data)
        print(f"wrote {path.relative_to(REPO_ROOT)} ({len(data):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
