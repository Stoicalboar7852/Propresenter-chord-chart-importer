#!/usr/bin/env python3
"""Draw the background for the macOS disk image.

    python3 scripts/make_dmg_background.py            # regenerate
    python3 scripts/make_dmg_background.py --check    # fail if the committed art is stale

Writes ``assets/dmg-background.png`` and ``assets/dmg-background@2x.png``, which
``scripts/build-macos.sh`` puts inside the image as ``.background/``. The window is 660
by 420 points, and the icon positions in that script have to match the plates drawn
here.

Black, with orange mist: soft radial glows painted pixel by pixel, which is a blur
without needing a blur - a radial falloff is already smooth, so nothing has to be
convolved afterwards. The mist goes down as a raster, and the arrow, plates and text go
on top as vectors through PyMuPDF, which is already a dependency and carries its own
fonts.

**The plates are not decoration.** Finder draws icon labels in the system's text
colour: black in light appearance, white in dark. Black text on a black background is
unreadable, so the two label areas sit on mid-toned plates that either colour can be
read against.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
OUTPUTS = ((ASSETS / "dmg-background.png", 1), (ASSETS / "dmg-background@2x.png", 2))

WIDTH, HEIGHT = 660, 420
#: The mist is painted once at this scale and scaled down for each output.
MIST_SCALE = 2

#: Where build-macos.sh puts the two icons, as Finder measures them: the centre of a
#: 128 point icon, from the top left of the window. The label sits just below, so the
#: plate has to cover both. The app goes on the left, Applications on the right, and
#: the arrow points from one to the other.
APP_ICON_CENTRE = (170, 210)
APPLICATIONS_ICON_CENTRE = (490, 210)
ICON_SIZE = 128
PLATE_WIDTH, PLATE_HEIGHT = 196, 182
PLATE_RADIUS = 18

PLATE = (0.29, 0.29, 0.31)  # legible under a black label or a white one
PLATE_EDGE = (1.0, 0.478, 0.0, 0.5)
ORANGE = (1.0, 0.478, 0.0)  # #FF7A00
ORANGE_DEEP = (1.0, 0.239, 0.0)  # #FF3D00
HEADING = (0.98, 0.97, 0.96)
SUBDUED = (0.72, 0.70, 0.68)

#: Each glow: centre as a fraction of the canvas, radius in the same units, peak
#: strength, and colour. Overlapping warm and deep orange keeps it from looking like
#: one flat circle.
GLOWS: tuple[tuple[float, float, float, float, tuple[int, int, int]], ...] = (
    (0.22, 0.42, 0.60, 1.15, (0xFF, 0x6A, 0x00)),
    (0.78, 0.56, 0.56, 1.05, (0xFF, 0x33, 0x00)),
    (0.50, 0.10, 0.44, 0.62, (0xFF, 0x7A, 0x0A)),
    (0.50, 0.97, 0.48, 0.58, (0xFF, 0x3D, 0x00)),
    (0.04, 0.94, 0.34, 0.48, (0xFF, 0x5A, 0x00)),
    (0.97, 0.06, 0.32, 0.45, (0xFF, 0x70, 0x08)),
)


def paint_mist(width: int, height: int) -> bytes:
    """Black, with soft orange glows. Returns PNG bytes.

    Each glow falls off as a smoothstep cubed, which is what makes it read as haze
    rather than as a circle with a gradient in it. Values add and clamp, so where two
    glows overlap the mist brightens rather than one covering the other.
    """
    diagonal = math.hypot(width, height)
    glows = [
        (
            centre_x * width,
            centre_y * height,
            radius * diagonal * 0.5,
            strength,
            colour,
        )
        for centre_x, centre_y, radius, strength, colour in GLOWS
    ]

    out = bytearray(width * height * 3)
    for y in range(height):
        row = y * width * 3
        for x in range(width):
            red = green = blue = 0.0
            for centre_x, centre_y, radius, strength, colour in glows:
                distance = math.hypot(x - centre_x, y - centre_y)
                if distance >= radius:
                    continue
                falloff = 1.0 - distance / radius
                weight = strength * falloff * falloff
                red += colour[0] * weight
                green += colour[1] * weight
                blue += colour[2] * weight
            index = row + x * 3
            out[index] = 255 if red > 255 else int(red)
            out[index + 1] = 255 if green > 255 else int(green)
            out[index + 2] = 255 if blue > 255 else int(blue)

    pixmap = pymupdf.Pixmap(pymupdf.csRGB, width, height, bytes(out), False)
    return bytes(pixmap.tobytes("png"))


def draw(page: pymupdf.Page, mist: bytes) -> None:
    page.insert_image(pymupdf.Rect(0, 0, WIDTH, HEIGHT), stream=mist)

    for centre in (APP_ICON_CENTRE, APPLICATIONS_ICON_CENTRE):
        top = centre[1] - ICON_SIZE / 2 - 18
        plate = pymupdf.Rect(
            centre[0] - PLATE_WIDTH / 2,
            top,
            centre[0] + PLATE_WIDTH / 2,
            top + PLATE_HEIGHT,
        )
        page.draw_rect(
            plate,
            radius=PLATE_RADIUS / PLATE_HEIGHT,
            color=PLATE_EDGE[:3],
            fill=PLATE,
            fill_opacity=0.74,
            stroke_opacity=PLATE_EDGE[3],
            width=1.2,
        )

    draw_arrow(page)

    heading = "ProPresenter Chord Chart Importer"
    page.insert_text(
        (centred(heading, 20, bold=True), 62),
        heading,
        fontsize=20,
        fontname="hebo",
        color=HEADING,
    )
    instruction = "Drag PCCI onto the Applications folder"
    page.insert_text(
        (centred(instruction, 12), 88),
        instruction,
        fontsize=12,
        fontname="helv",
        color=SUBDUED,
    )
    footer = "Unsigned build - right-click PCCI and choose Open the first time"
    page.insert_text(
        (centred(footer, 10), 392),
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
    """From the app on the left to the Applications folder on the right."""
    left = APP_ICON_CENTRE[0] + PLATE_WIDTH / 2 + 16
    right = APPLICATIONS_ICON_CENTRE[0] - PLATE_WIDTH / 2 - 16
    middle = APP_ICON_CENTRE[1] - 8
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
    mist = paint_mist(WIDTH * MIST_SCALE, HEIGHT * MIST_SCALE)
    document = pymupdf.open()
    page = document.new_page(width=WIDTH, height=HEIGHT)
    draw(page, mist)
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
