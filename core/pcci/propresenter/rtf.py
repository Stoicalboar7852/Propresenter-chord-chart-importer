"""Generating the RTF that ProPresenter stores for slide text and slide notes.

ProPresenter writes Cocoa-flavoured RTF. The shape here is copied from a real export
(see docs/FORMAT_NOTES.md), including the details that look redundant but appear in
every slide the application writes: the ``expandedcolortbl`` block, ``partightenfactor``
and the ``\\`` + newline line break.
"""

from __future__ import annotations

from pcci.config import RGBA, FontSpec

#: Cocoa's RTF line break: a backslash followed by a real newline.
LINE_BREAK = "\\\n"


def escape(text: str) -> str:
    """Escape one run of text for RTF."""
    out: list[str] = []
    for character in text:
        code = ord(character)
        if character in ("\\", "{", "}"):
            out.append("\\" + character)
        elif character == "\t":
            out.append("\\tab ")
        elif code < 0x80:
            out.append(character)
        elif code <= 0xFFFF:
            # RTF signed 16-bit unicode escape, with a '?' fallback character.
            out.append(f"\\u{code if code < 0x8000 else code - 0x10000}?")
        else:
            high = 0xD800 + ((code - 0x10000) >> 10)
            low = 0xDC00 + ((code - 0x10000) & 0x3FF)
            out.append(f"\\u{high - 0x10000}?\\u{low - 0x10000}?")
    return "".join(out)


def _colour_table(colour: RGBA) -> str:
    red, green, blue = (round(channel * 255) for channel in (colour.red, colour.green, colour.blue))
    percent = tuple(round(channel * 100000) for channel in (colour.red, colour.green, colour.blue))
    return (
        f"{{\\colortbl;\\red255\\green255\\blue255;\\red{red}\\green{green}\\blue{blue};}}\n"
        f"{{\\*\\expandedcolortbl;;\\csgenericrgb\\c{percent[0]}\\c{percent[1]}\\c{percent[2]};}}\n"
    )


def build_rtf(
    lines: list[str],
    *,
    font: FontSpec,
    colour: RGBA,
    centred: bool = True,
    font_class: str = "fswiss",
) -> bytes:
    """Build an RTF document holding ``lines``, one per visual line."""
    half_points = round(font.size * 2)
    tab_width = max(round(font.size * 22.4), 1)
    alignment = "\\qc" if centred else "\\ql"
    bold = "\\b" if font.bold else ""
    italic = "\\i" if font.italic else ""
    body = LINE_BREAK.join(escape(line) for line in lines)
    document = (
        "{\\rtf1\\ansi\\ansicpg1252\\cocoartf2907\n"
        "\\cocoatextscaling0\\cocoaplatform0"
        f"{{\\fonttbl\\f0\\{font_class}\\fcharset0 {escape(font.postscript_name)};}}\n"
        f"{_colour_table(colour)}"
        f"\\deftab{tab_width}\n"
        f"\\pard\\pardeftab{tab_width}{alignment}\\partightenfactor0\n\n"
        f"\\f0{bold}{italic}\\fs{half_points} \\cf2 \\CocoaLigature0 {body}}}"
    )
    return document.encode("utf-8")


def build_notes_rtf(
    text: str, *, font: FontSpec | None = None, colour: RGBA | None = None
) -> bytes:
    """Build the RTF for a slide's notes.

    The font must be fixed-pitch or the chord positions stop lining up with the words
    underneath them, which is the entire point of the block.
    """
    font = font or FontSpec(postscript_name="Courier", family_name="Courier", size=24.0, bold=False)
    colour = colour or RGBA(red=1.0, green=1.0, blue=1.0)
    return build_rtf(
        text.split("\n"),
        font=font,
        colour=colour,
        centred=False,
        font_class="fmodern",
    )
