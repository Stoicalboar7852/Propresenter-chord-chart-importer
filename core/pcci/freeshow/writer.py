"""Building a FreeShow show from a slide plan.

Every structure here was read out of FreeShow's own source rather than guessed at, the
same way the ProPresenter writer was read out of a real export. The three files that
settle it, and what each one settles:

``src/types/Show.ts``
    The shape: ``Show``, ``Slide``, ``Item``, ``Line`` and ``Chords {id, pos, key}``.
``src/frontend/converters/chordpro.ts``
    What FreeShow itself writes when it imports a chart: ``pos`` is a character index
    into the line's plain text, and the chords live on the line, not in the text.
``src/frontend/components/slide/TextboxLines.svelte``
    How they are drawn: a chord past the end of the line renders as a trailing chord,
    and a line with chords but no text renders as a chord-only line, spaced by ``pos``.

A show is saved as ``JSON.stringify([id, show])`` (``src/electron/data/save.ts``), and
the importer accepts either that pair or a bare show object
(``src/frontend/converters/importHelpers.ts``). pcci writes the pair.
"""

from __future__ import annotations

import json
import math
import secrets
import time
from typing import Any

from pcci.config import RGBA, ChordDelivery, ConversionConfig, SlideStyle
from pcci.ir import Line, SectionType
from pcci.notes import render_lines
from pcci.slides import Slide, SlidePlan

#: FreeShow's ``uid`` package: lower-case base 36, eleven characters by default and
#: five for a chord. Any unique string would do - these are object keys - but matching
#: the shape keeps a pcci file indistinguishable from one FreeShow wrote itself.
ID_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
ID_LENGTH = 11
CHORD_ID_LENGTH = 5

#: The song category FreeShow ships with (``src/electron/data/defaults.ts``).
SONG_CATEGORY = "song"

#: FreeShow's default groups, and the section types that are the same thing. A section
#: type with no entry here keeps pcci's own label and colour instead: FreeShow replaces
#: both from its own settings when it recognises the group, and a Post-Chorus filed as
#: a chorus would be a lie about the song.
GLOBAL_GROUPS: dict[SectionType, str] = {
    SectionType.INTRO: "intro",
    SectionType.VERSE: "verse",
    SectionType.PRE_CHORUS: "pre_chorus",
    SectionType.CHORUS: "chorus",
    SectionType.BRIDGE: "bridge",
    SectionType.TAG: "tag",
    SectionType.OUTRO: "outro",
}

#: The colours those groups have in a default install, so the file already looks right
#: before FreeShow normalises it against the user's own group settings.
GLOBAL_GROUP_COLOURS: dict[str, str] = {
    "break": "#f5255e",
    "bridge": "#f52598",
    "chorus": "#f525d2",
    "intro": "#d525f5",
    "outro": "#a525f5",
    "pre_chorus": "#8825f5",
    "tag": "#7525f5",
    "verse": "#5825f5",
}


def new_id(length: int = ID_LENGTH) -> str:
    """An id shaped like the ones FreeShow's ``uid`` package produces."""
    return "".join(secrets.choice(ID_ALPHABET) for _ in range(length))


def _css_colour(colour: RGBA) -> str:
    return colour.to_hex()


def _shadow_offsets(style: SlideStyle) -> tuple[float, float]:
    """pcci stores a shadow as angle plus offset; CSS wants x and y.

    Screen coordinates grow downwards, so the y component is negated: the default
    315 degrees comes out as the down-and-right drop shadow it looks like in
    ProPresenter.
    """
    radians = math.radians(style.shadow_angle)
    return (
        round(style.shadow_offset * math.cos(radians), 2),
        round(-style.shadow_offset * math.sin(radians), 2),
    )


def item_style(style: SlideStyle) -> str:
    """The CSS FreeShow keeps on a text item: position first, then type.

    Position is pcci's safe area rather than FreeShow's own default box, so a slide
    lands in the same place as the ProPresenter one written from the same settings.
    """
    inset = style.safe_area_inset
    left = round(style.width * inset)
    top = round(style.height * inset)
    width = round(style.width * (1 - 2 * inset))
    height = round(style.height * (1 - 2 * inset))
    parts = [
        f"top:{top}px",
        f"left:{left}px",
        f"height:{height}px",
        f"width:{width}px",
        f"font-family:{style.font.family_name}",
        f"font-size:{round(style.font.size)}px",
        f"color:{_css_colour(style.text_colour)}",
        "align-items:center",
        "text-align:center",
    ]
    if style.font.bold:
        parts.append("font-weight:bold")
    if style.font.italic:
        parts.append("font-style:italic")
    if style.outline_width > 0:
        parts.append(f"-webkit-text-stroke-width:{round(style.outline_width)}px")
        parts.append(f"-webkit-text-stroke-color:{_css_colour(style.outline_colour)}")
    if style.shadow_enabled:
        x, y = _shadow_offsets(style)
        opacity = round(style.shadow_opacity, 2)
        parts.append(
            f"text-shadow:{x}px {y}px {round(style.shadow_radius)}px rgb(0 0 0 / {opacity})"
        )
    return ";".join(parts) + ";"


def _line_payload(line: Line, config: ConversionConfig) -> dict[str, Any]:
    """One ``Line``: the words, and the chords anchored to them by character index.

    A chord-only line is kept rather than dropped. FreeShow draws one as a row of
    chords spaced by ``pos`` when a chords element asks for it, and as nothing at all
    when it does not - so an intro's chords reach the stage without the congregation
    seeing anything the words did not already say.
    """
    lyrics = line.lyrics.upper() if config.style.all_caps else line.lyrics
    payload: dict[str, Any] = {
        "align": "",
        "text": [{"value": lyrics, "style": ""}],
    }
    if config.chord_delivery.writes_inline and line.chords:
        # ``pos`` is an index into the words, and the IR guarantees a chord sits inside
        # the lyric it belongs to - so the clamp only ever catches upper-casing that
        # lengthened the string (a German sharp s becomes two letters).
        #
        # A chord-only line therefore arrives with every chord at zero, because there
        # is no lyric to index into. FreeShow spaces those evenly rather than stacking
        # them, which is the right reading of a bar line: the chart said four bars of
        # G, not that they all happen at once.
        payload["chords"] = [
            {
                "id": new_id(CHORD_ID_LENGTH),
                "pos": min(placement.char_index, len(lyrics)),
                "key": placement.chord,
            }
            for placement in line.chords
        ]
    return payload


def _item_payload(slide: Slide, config: ConversionConfig) -> dict[str, Any]:
    item: dict[str, Any] = {
        "style": item_style(config.style),
        "lines": [_line_payload(line, config) for line in slide.lines],
    }
    if config.chord_delivery.writes_inline and config.chords_on_slide and slide.has_chords:
        # The show's own item, which is what the output layer reads
        # (components/output/layers/SlideContent.svelte passes item.chords?.enabled
        # straight through). The stage has its own switch and does not need this one,
        # so it stays off unless somebody asks for chords on the audience screen.
        item["chords"] = {"enabled": True}
    return item


def _slide_payload(slide: Slide, config: ConversionConfig) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "group": None,
        "color": None,
        "settings": {},
        "notes": "",
        "items": [_item_payload(slide, config)],
    }
    if config.chord_delivery.writes_notes:
        block = render_lines(slide.lines, config.chord_placement)
        if block.strip():
            # FreeShow's slide notes are plain text, read by a "slide_notes" stage item.
            payload["notes"] = block
    return payload


def _group_for(slide: Slide, config: ConversionConfig) -> tuple[str, str | None, str]:
    """The group name, global group id and colour for a section's first slide."""
    global_group = GLOBAL_GROUPS.get(slide.section_type)
    if global_group:
        # FreeShow overwrites both name and colour from its own group settings when it
        # recognises the id, so write what it will settle on rather than something it
        # is about to replace.
        return global_group, global_group, GLOBAL_GROUP_COLOURS[global_group]
    colour = config.colour_for(slide.section_type, None)
    return slide.section_label, None, colour.to_hex()


def _slide_text(payload: dict[str, Any]) -> str:
    """Every word on a slide, for telling two sections apart."""
    return "\n".join(
        "".join(chunk.get("value", "") for chunk in line.get("text", []))
        for item in payload.get("items", [])
        for line in item.get("lines", [])
    )


def build_show(plan: SlidePlan, *, created: int | None = None) -> tuple[str, dict[str, Any]]:
    """Build the ``[id, show]`` pair FreeShow saves and imports.

    Each section becomes one parent slide carrying the group, with the section's later
    slides as its children - FreeShow's own arrangement for a verse too long for one
    screen. A section whose words and group match one already written reuses it rather
    than adding a second copy, so a chorus sung three times is one slide played three
    times, which is what the layout counter in FreeShow is for.
    """
    config = plan.config
    song = plan.song
    layout_id = new_id()

    slides: dict[str, dict[str, Any]] = {}
    layout: list[dict[str, Any]] = []
    seen: dict[str, str] = {}

    for section_index, _section in enumerate(song.sections):
        section_slides = plan.slides_for_section(section_index)
        if not section_slides:
            continue

        parent_id = new_id()
        parent = _slide_payload(section_slides[0], config)
        name, global_group, colour = _group_for(section_slides[0], config)
        parent["group"] = name
        parent["color"] = colour
        if global_group:
            parent["globalGroup"] = global_group

        children: list[tuple[str, dict[str, Any]]] = []
        for slide in section_slides[1:]:
            child_id = new_id()
            children.append((child_id, _slide_payload(slide, config)))
        if children:
            parent["children"] = [child_id for child_id, _ in children]

        signature = "\n".join(
            [name, _slide_text(parent), *[_slide_text(child) for _, child in children]]
        )
        existing = seen.get(signature)
        if existing is not None:
            layout.append({"id": existing})
            continue

        seen[signature] = parent_id
        slides[parent_id] = parent
        for child_id, child in children:
            slides[child_id] = child
        layout.append({"id": parent_id})

    stamp = created if created is not None else int(time.time() * 1000)
    show: dict[str, Any] = {
        "name": song.title,
        "category": SONG_CATEGORY,
        "settings": {"activeLayout": layout_id, "template": None},
        "timestamps": {"created": stamp, "modified": None, "used": None},
        "quickAccess": {},
        "meta": _meta(plan),
        "slides": slides,
        "layouts": {layout_id: {"name": config.arrangement_name, "notes": "", "slides": layout}},
        "media": {},
    }
    return new_id(), show


def _meta(plan: SlidePlan) -> dict[str, str]:
    """FreeShow's metadata keys, and only the ones we actually know."""
    song = plan.song
    meta: dict[str, str] = {"title": song.title}
    if song.artist:
        meta["artist"] = song.artist
    if song.ccli_number:
        meta["CCLI"] = song.ccli_number
    if song.copyright:
        meta["copyright"] = song.copyright
    if song.key:
        meta["key"] = song.key
    return meta


def show_bytes(show_id: str, show: dict[str, Any]) -> bytes:
    """The file itself: the pair, as compact JSON, the way FreeShow writes it."""
    return json.dumps([show_id, show], ensure_ascii=False).encode("utf-8")


def uses_unsupported_chart(config: ConversionConfig) -> bool:
    """True when the chosen chord route cannot be honoured in this format."""
    return config.chord_delivery in (ChordDelivery.CHART, ChordDelivery.BOTH)
