"""Settings for conversion, with defaults chosen from the reference material.

Everything a user might reasonably want to change lives here so the desktop
front-ends can expose it without reaching into engine internals. The model
serialises to JSON, so a UI can round-trip a settings file unchanged.
"""

from __future__ import annotations

import math
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from pcci.ir import SectionType

DEFAULT_LINES_PER_SLIDE = 4
MIN_LINES_PER_SLIDE = 1
MAX_LINES_PER_SLIDE = 10


class ChordDelivery(StrEnum):
    """How chords reach the stage screen."""

    NONE = "none"
    NOTES = "notes"
    CHART = "chart"
    BOTH = "both"

    @property
    def writes_notes(self) -> bool:
        return self in (ChordDelivery.NOTES, ChordDelivery.BOTH)

    @property
    def writes_chart(self) -> bool:
        return self in (ChordDelivery.CHART, ChordDelivery.BOTH)


class ChordPlacementStyle(StrEnum):
    """Where chords sit relative to the lyric in the notes block."""

    ABOVE = "above"
    BELOW = "below"


class RGBA(BaseModel):
    """A colour in ProPresenter's own normalised 0..1 float form."""

    model_config = ConfigDict(extra="forbid")

    red: float = Field(ge=0.0, le=1.0)
    green: float = Field(ge=0.0, le=1.0)
    blue: float = Field(ge=0.0, le=1.0)
    alpha: float = Field(default=1.0, ge=0.0, le=1.0)

    @classmethod
    def from_hex(cls, value: str) -> RGBA:
        text = value.lstrip("#")
        if len(text) not in (6, 8):
            msg = f"expected #RRGGBB or #RRGGBBAA, got {value!r}"
            raise ValueError(msg)
        channels = [int(text[i : i + 2], 16) / 255.0 for i in range(0, len(text), 2)]
        if len(channels) == 3:
            channels.append(1.0)
        return cls(red=channels[0], green=channels[1], blue=channels[2], alpha=channels[3])

    def to_hex(self) -> str:
        r, g, b = (round(c * 255) for c in (self.red, self.green, self.blue))
        return f"#{r:02X}{g:02X}{b:02X}"


# Group colours ProPresenter itself wrote into
# core/tests/reference/Goodbye Yesterday blank with groups.pro. Values marked
# "observed" are read out of that file; the rest are our own choices for section
# types the reference does not contain. See docs/FORMAT_NOTES.md.
DEFAULT_GROUP_COLOURS: dict[SectionType, RGBA] = {
    # observed in the reference export
    SectionType.INTRO: RGBA.from_hex("#B3A724"),
    SectionType.VERSE: RGBA.from_hex("#0077CC"),
    SectionType.CHORUS: RGBA.from_hex("#C20049"),
    SectionType.BRIDGE: RGBA.from_hex("#7600CC"),
    SectionType.INTERLUDE: RGBA.from_hex("#24B34C"),
    SectionType.VAMP: RGBA.from_hex("#24B34C"),
    SectionType.POST_CHORUS: RGBA.from_hex("#A52A2A"),
    # our own choices: the reference contains no section of these types
    SectionType.PRE_CHORUS: RGBA.from_hex("#E67E22"),
    SectionType.TAG: RGBA.from_hex("#F1C40F"),
    SectionType.OUTRO: RGBA.from_hex("#566573"),
    SectionType.ENDING: RGBA.from_hex("#566573"),
    SectionType.INSTRUMENTAL: RGBA.from_hex("#16A085"),
    SectionType.BREAKDOWN: RGBA.from_hex("#658196"),
    SectionType.REFRAIN: RGBA.from_hex("#C20049"),
    SectionType.MISC: RGBA.from_hex("#95A5A6"),
}

# ProPresenter darkens a repeated section type for its second occurrence: in the
# reference, Verse 2 and Bridge 2 are exactly 0.75x Verse 1 and Bridge 1. Chorus 2 is
# darkened less (about 0.9x); we use one factor for all of them rather than hard-code
# per-type exceptions, and the whole map stays user-editable.
NUMBERED_SHADE_FACTOR = 0.75


def quantise_8bit(value: float) -> float:
    """Snap a channel to the 1/255 grid ProPresenter stores.

    Every colour in the reference file is an exact ``n/255``. Shading without this
    lands a thousandth away from what the application itself would write; with it,
    Verse 2 and Bridge 2 come out bit-for-bit identical to the reference.
    """
    return min(1.0, max(0.0, math.floor(value * 255.0 + 0.5) / 255.0))


class FontSpec(BaseModel):
    """A font as ProPresenter stores it: PostScript name plus display family."""

    model_config = ConfigDict(extra="forbid")

    postscript_name: str = "WorkSans-Black"
    family_name: str = "Work Sans"
    size: float = Field(default=70.0, gt=0.0)
    bold: bool = False
    italic: bool = False


class SlideStyle(BaseModel):
    """How the lyric text element is drawn."""

    model_config = ConfigDict(extra="forbid")

    width: int = Field(default=1920, gt=0)
    height: int = Field(default=1080, gt=0)
    font: FontSpec = Field(default_factory=FontSpec)
    text_colour: RGBA = Field(default_factory=lambda: RGBA(red=1.0, green=1.0, blue=1.0))
    outline_width: float = Field(default=4.0, ge=0.0)
    outline_colour: RGBA = Field(default_factory=lambda: RGBA(red=0.0, green=0.0, blue=0.0))
    shadow_enabled: bool = True
    shadow_radius: float = Field(default=5.0, ge=0.0)
    shadow_offset: float = Field(default=5.0, ge=0.0)
    shadow_angle: float = 315.0
    shadow_opacity: float = Field(default=0.75, ge=0.0, le=1.0)
    all_caps: bool = False
    safe_area_inset: float = Field(default=0.05, ge=0.0, le=0.25)


class ConversionConfig(BaseModel):
    """Everything the conversion pipeline reads."""

    model_config = ConfigDict(extra="forbid")

    lines_per_slide: int = Field(
        default=DEFAULT_LINES_PER_SLIDE, ge=MIN_LINES_PER_SLIDE, le=MAX_LINES_PER_SLIDE
    )
    balance_last_slide: bool = True
    chord_delivery: ChordDelivery = ChordDelivery.BOTH
    chord_placement: ChordPlacementStyle = ChordPlacementStyle.ABOVE
    include_annotations_in_notes: bool = True
    category: str = "Song"
    style: SlideStyle = Field(default_factory=SlideStyle)
    group_colours: dict[SectionType, RGBA] = Field(
        default_factory=lambda: dict(DEFAULT_GROUP_COLOURS)
    )
    shade_numbered_groups: bool = True
    build_arrangement: bool = True
    arrangement_name: str = "Detected"

    @model_validator(mode="after")
    def _every_section_has_a_colour(self) -> Self:
        missing = [t for t in SectionType if t not in self.group_colours]
        for section_type in missing:
            self.group_colours[section_type] = DEFAULT_GROUP_COLOURS[section_type]
        return self

    def colour_for(self, section_type: SectionType, number: int | None = None) -> RGBA:
        """Group colour for a section, darkened for repeats the way ProPresenter does."""
        base = self.group_colours.get(section_type, DEFAULT_GROUP_COLOURS[SectionType.MISC])
        if not self.shade_numbered_groups or number is None or number < 2:
            return base
        factor = NUMBERED_SHADE_FACTOR ** (number - 1)
        return RGBA(
            red=quantise_8bit(base.red * factor),
            green=quantise_8bit(base.green * factor),
            blue=quantise_8bit(base.blue * factor),
            alpha=base.alpha,
        )
