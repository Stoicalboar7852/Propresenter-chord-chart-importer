#!/usr/bin/env python3
"""Build the app icons for both platforms from one piece of source art.

    python3 scripts/make_icons.py            # regenerate the icons
    python3 scripts/make_icons.py --check    # fail if the committed icons are stale

The master is ``assets/icon.png`` at 1024x1024. Replacing that file and running this
script again is the whole way to change the icon: everything below is derived from it.
If it is missing, the four-arrow cycle in ``draw_source_art`` is drawn instead and
saved as the master, so a fresh checkout still builds an app with an icon on it.

Outputs, both committed so no build has to run this:

* ``macos/Resources/AppIcon.icns`` - the sizes macOS asks for, PNG inside an icns
  container written here rather than by ``iconutil``, which only exists on a Mac.
* ``windows/Pcci/Assets/AppIcon.ico`` - the same, in an ICO with PNG payloads, which
  Windows has read since Vista.

Rendering goes through PyMuPDF, already a dependency, so this needs nothing installed
that the engine does not need anyway. Each size is rendered from the master rather than
resampled from the size above it.

MuPDF draws SVG but not SVG gradients - a ``url(#...)`` fill comes out black - so the
art is drawn as a flat silhouette, and the orange ramp and the drop shadow are painted
onto it here, through the shape's own antialiased alpha.
"""

from __future__ import annotations

import argparse
import math
import struct
import sys
from pathlib import Path

import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
SOURCE_SVG = ASSETS / "icon.svg"
MASTER_PNG = ASSETS / "icon.png"
ICNS_PATH = REPO_ROOT / "macos" / "Resources" / "AppIcon.icns"
ICO_PATH = REPO_ROOT / "windows" / "Pcci" / "Assets" / "AppIcon.ico"

MASTER_SIZE = 1024

#: (four-character type, pixel size). macOS picks whichever fits the place it is drawn.
ICNS_ENTRIES: tuple[tuple[bytes, int], ...] = (
    (b"icp4", 16),
    (b"icp5", 32),
    (b"ic11", 32),
    (b"ic12", 64),
    (b"ic07", 128),
    (b"ic13", 256),
    (b"ic08", 256),
    (b"ic14", 512),
    (b"ic09", 512),
    (b"ic10", 1024),
)

#: Explorer, the taskbar and Alt-Tab all want different ones.
ICO_SIZES: tuple[int, ...] = (16, 24, 32, 48, 64, 128, 256)


# --------------------------------------------------------------------------- source art


def draw_source_art() -> str:
    """The four-arrow cycle, as an SVG silhouette. Colour is painted on afterwards.

    Four arrows chase each other clockwise round a circle, each covering a quadrant:
    a thick arc, then a triangular head pointing the way round. Angles are measured in
    SVG's coordinate system, where y grows downwards, so increasing the angle moves
    clockwise on screen.
    """
    centre = MASTER_SIZE / 2
    outer_radius = 430.0
    inner_radius = 306.0
    middle_radius = (outer_radius + inner_radius) / 2
    head_half_width = 104.0
    head_sweep = 27.0
    tail_gap = 5.0
    head_gap = 5.0

    def point(angle: float, radius: float) -> tuple[float, float]:
        radians = math.radians(angle)
        return centre + radius * math.cos(radians), centre + radius * math.sin(radians)

    def coordinate(angle: float, radius: float) -> str:
        x, y = point(angle, radius)
        return f"{x:.2f},{y:.2f}"

    arrows: list[str] = []
    for quadrant in range(4):
        # Quadrant 0 runs from the top-left diagonal over the top to the top-right,
        # which puts its head at one o'clock, like the art it is copied from.
        start = 225.0 + 90.0 * quadrant + tail_gap
        end = 225.0 + 90.0 * (quadrant + 1) - head_sweep - head_gap
        arrows.append(
            " ".join(
                [
                    f"M{coordinate(start, outer_radius)}",
                    f"A{outer_radius:.2f},{outer_radius:.2f} 0 0 1"
                    f" {coordinate(end, outer_radius)}",
                    f"L{coordinate(end, middle_radius + head_half_width)}",
                    f"L{coordinate(end + head_sweep, middle_radius)}",
                    f"L{coordinate(end, middle_radius - head_half_width)}",
                    f"L{coordinate(end, inner_radius)}",
                    f"A{inner_radius:.2f},{inner_radius:.2f} 0 0 0"
                    f" {coordinate(start, inner_radius)}",
                    "Z",
                ]
            )
        )

    paths = "\n".join(f'  <path d="{arrow}"/>' for arrow in arrows)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{MASTER_SIZE}"'
        f' height="{MASTER_SIZE}" viewBox="0 0 {MASTER_SIZE} {MASTER_SIZE}">\n'
        f'<g fill="#000000">\n{paths}\n</g>\n</svg>\n'
    )


# ------------------------------------------------------------------------------ paint

#: The ramp the art runs along, corner to corner: lighter orange at the top left,
#: deeper at the bottom right.
RAMP: tuple[tuple[float, tuple[int, int, int]], ...] = (
    (0.00, (0xFF, 0xA3, 0x18)),
    (0.45, (0xFF, 0x7A, 0x00)),
    (1.00, (0xFF, 0x3D, 0x00)),
)

#: Offset and strength of each pass standing in for a blurred drop shadow.
SHADOW_PASSES: tuple[tuple[int, int, float], ...] = ((5, 7, 0.07), (10, 14, 0.05))


def ramp_colour(position: float) -> tuple[int, int, int]:
    """The ramp sampled at 0..1, linearly between the stops."""
    for (low, left), (high, right) in zip(RAMP, RAMP[1:], strict=False):
        if position <= high:
            span = high - low
            fraction = 0.0 if span == 0 else (position - low) / span
            return tuple(  # type: ignore[return-value]
                round(a + (b - a) * fraction) for a, b in zip(left, right, strict=True)
            )
    return RAMP[-1][1]


def paint(silhouette: pymupdf.Pixmap) -> bytes:
    """Colour the silhouette and drop a shadow behind it, as one RGBA PNG.

    The shape's alpha is the only thing taken from the render, so every edge keeps the
    antialiasing MuPDF produced. The shadow is that same alpha, offset and faded, which
    costs nothing and cannot depend on how a renderer reads an opacity attribute.
    """
    size = silhouette.width
    mask = silhouette.samples[3::4]

    shadow = bytearray(size * size)
    for offset_x, offset_y, strength in SHADOW_PASSES:
        for y in range(offset_y, size):
            source_row = (y - offset_y) * size
            target_row = y * size
            for x in range(offset_x, size):
                value = mask[source_row + x - offset_x]
                if not value:
                    continue
                index = target_row + x
                total = shadow[index] + int(value * strength)
                shadow[index] = 255 if total > 255 else total

    ramp = [ramp_colour(index / (2 * size - 2)) for index in range(2 * size - 1)]
    out = bytearray(size * size * 4)
    for y in range(size):
        row = y * size
        for x in range(size):
            index = row + x
            shape_alpha = mask[index]
            target = index * 4
            if shape_alpha == 255:
                red, green, blue = ramp[x + y]
                out[target] = red
                out[target + 1] = green
                out[target + 2] = blue
                out[target + 3] = 255
                continue
            shadow_alpha = shadow[index]
            if not shape_alpha and not shadow_alpha:
                continue
            # Source-over: the coloured shape above a black shadow.
            top = shape_alpha / 255.0
            below = shadow_alpha / 255.0 * (1.0 - top)
            alpha = top + below
            red, green, blue = ramp[x + y]
            out[target] = round(red * top / alpha)
            out[target + 1] = round(green * top / alpha)
            out[target + 2] = round(blue * top / alpha)
            out[target + 3] = round(alpha * 255)

    painted = pymupdf.Pixmap(pymupdf.csRGB, size, size, bytes(out), True)
    return bytes(painted.tobytes("png"))


# ----------------------------------------------------------------------------- raster


def render_pixmap(source: Path, size: int) -> pymupdf.Pixmap:
    """One square RGBA raster of the given size, rendered from the art itself."""
    with pymupdf.open(source) as document:
        page = document[0]
        matrix = pymupdf.Matrix(size / page.rect.width, size / page.rect.height)
        pixmap = page.get_pixmap(matrix=matrix, alpha=True)
    if (pixmap.width, pixmap.height) != (size, size):
        raise SystemExit(f"rendered {pixmap.width}x{pixmap.height}, wanted {size}x{size}")
    return pixmap


def render(source: Path, size: int) -> bytes:
    """One square PNG of the given size, rendered from the source art itself."""
    return bytes(render_pixmap(source, size).tobytes("png"))


def build_icns(images: dict[int, bytes]) -> bytes:
    """An icns container: magic, total length, then a typed chunk per size."""
    chunks = b"".join(
        icon_type + struct.pack(">I", len(images[size]) + 8) + images[size]
        for icon_type, size in ICNS_ENTRIES
    )
    return b"icns" + struct.pack(">I", len(chunks) + 8) + chunks


def build_ico(images: dict[int, bytes]) -> bytes:
    """An ICO holding PNGs. 256 is written as 0, which is how ICO spells it."""
    header = struct.pack("<HHH", 0, 1, len(ICO_SIZES))
    offset = len(header) + 16 * len(ICO_SIZES)
    directory = b""
    payload = b""
    for size in ICO_SIZES:
        data = images[size]
        directory += struct.pack(
            "<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), offset
        )
        payload += data
        offset += len(data)
    return header + directory + payload


# ---------------------------------------------------------------------------- verify


def png_size(data: bytes) -> tuple[int, int]:
    """Pixel dimensions, read from the PNG header.

    Not from the rendered page rect: PNG carries a resolution, so a 16 pixel icon at
    96 DPI measures 12 points and comparing those to pixels fails for no reason.
    """
    if data[12:16] != b"IHDR":
        raise SystemExit("png: no IHDR where one should be")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_icns(data: bytes, expected: dict[int, bytes]) -> None:
    if data[:4] != b"icns":
        raise SystemExit("icns: wrong magic")
    if struct.unpack(">I", data[4:8])[0] != len(data):
        raise SystemExit("icns: length field disagrees with the file")
    position = 8
    seen: list[bytes] = []
    while position < len(data):
        icon_type = data[position : position + 4]
        length = struct.unpack(">I", data[position + 4 : position + 8])[0]
        body = data[position + 8 : position + length]
        if body[:8] != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"icns: {icon_type!r} is not a PNG")
        promised = dict(ICNS_ENTRIES).get(icon_type)
        if promised is not None and png_size(body) != (promised, promised):
            raise SystemExit(f"icns: {icon_type!r} holds {png_size(body)}, wanted {promised}")
        seen.append(icon_type)
        position += length
    if seen != [icon_type for icon_type, _ in ICNS_ENTRIES]:
        raise SystemExit("icns: chunks are not the ones that were asked for")
    if position != len(data):
        raise SystemExit("icns: trailing bytes")
    sizes = {size for _, size in ICNS_ENTRIES}
    missing = sizes - set(expected)
    if missing:
        raise SystemExit(f"icns: nothing rendered at {sorted(missing)}")


def check_ico(data: bytes) -> None:
    reserved, kind, count = struct.unpack("<HHH", data[:6])
    if (reserved, kind) != (0, 1):
        raise SystemExit("ico: wrong header")
    if count != len(ICO_SIZES):
        raise SystemExit(f"ico: {count} entries, expected {len(ICO_SIZES)}")
    for index, size in enumerate(ICO_SIZES):
        entry = data[6 + 16 * index : 22 + 16 * index]
        width, height, _, _, _, _, length, offset = struct.unpack("<BBBBHHII", entry)
        if (width, height) != (size % 256, size % 256):
            raise SystemExit(f"ico: entry {index} claims {width}x{height}, wanted {size}")
        payload = data[offset : offset + length]
        if payload[:8] != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"ico: entry {index} is not a PNG")
        pixels = png_size(payload)
        if pixels != (size, size):
            raise SystemExit(f"ico: entry {index} holds {pixels[0]}x{pixels[1]}, wanted {size}")


# ------------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write anything; fail if the committed icons are out of date",
    )
    arguments = parser.parse_args()

    ASSETS.mkdir(parents=True, exist_ok=True)
    if not MASTER_PNG.exists():
        if arguments.check:
            return complain(f"{MASTER_PNG.relative_to(REPO_ROOT)} is missing")
        SOURCE_SVG.write_text(draw_source_art(), encoding="utf-8")
        MASTER_PNG.write_bytes(paint(render_pixmap(SOURCE_SVG, MASTER_SIZE)))
        print(f"drew {SOURCE_SVG.relative_to(REPO_ROOT)} -> {MASTER_PNG.relative_to(REPO_ROOT)}")

    wanted = sorted({size for _, size in ICNS_ENTRIES} | set(ICO_SIZES))
    images = {size: render(MASTER_PNG, size) for size in wanted}

    icns = build_icns(images)
    ico = build_ico(images)
    check_icns(icns, images)
    check_ico(ico)

    if arguments.check:
        stale = [
            path.relative_to(REPO_ROOT)
            for path, data in ((ICNS_PATH, icns), (ICO_PATH, ico))
            if not path.exists() or path.read_bytes() != data
        ]
        if stale:
            return complain(
                "these do not match the source art: "
                + ", ".join(str(path) for path in stale)
                + "\nrun: python3 scripts/make_icons.py"
            )
        print(f"icons are in step with {MASTER_PNG.relative_to(REPO_ROOT)}")
        return 0

    for path, data in ((ICNS_PATH, icns), (ICO_PATH, ico)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"wrote {path.relative_to(REPO_ROOT)} ({len(data):,} bytes)")
    return 0


def complain(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
