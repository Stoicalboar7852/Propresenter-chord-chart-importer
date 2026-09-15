"""Turning a parsed song into a plan of slides.

The plan is the thing the review screen shows and the user edits, and it is what the
writer consumes. Keeping it as a separate, serialisable step is what makes
``analyze -> edit -> plan -> build`` possible.

One rule matters more than the rest: **a slide never spans two sections.**
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from pcci.config import ConversionConfig
from pcci.ir import Line, Section, SectionType, Song


class Slide(BaseModel):
    """One slide: some lines of one section, and where it sits in that section."""

    model_config = ConfigDict(extra="forbid")

    section_index: int = Field(ge=0)
    section_label: str
    section_type: SectionType
    ordinal: int = Field(ge=1)
    total_in_section: int = Field(ge=1)
    lines: list[Line] = Field(default_factory=list)

    @property
    def label(self) -> str:
        """``Verse 1`` for a single-slide section, ``Verse 1 (2)`` for the second of several."""
        if self.total_in_section == 1:
            return self.section_label
        return f"{self.section_label} ({self.ordinal})"

    @property
    def lyrics(self) -> list[str]:
        return [line.lyrics for line in self.lines if line.lyrics]

    @property
    def has_chords(self) -> bool:
        return any(line.chords for line in self.lines)

    @property
    def annotations(self) -> list[str]:
        return [line.annotation for line in self.lines if line.annotation]


class SlidePlan(BaseModel):
    """Everything needed to build a presentation, and nothing else.

    A plan is a complete build recipe: hand ``pcci build`` a plan file and it produces
    the same ``.pro`` on any machine, whatever the original document was.
    """

    model_config = ConfigDict(extra="forbid")

    song: Song
    slides: list[Slide] = Field(default_factory=list)
    config: ConversionConfig = Field(default_factory=ConversionConfig)
    warnings: list[str] = Field(default_factory=list)

    @property
    def slide_count(self) -> int:
        return len(self.slides)

    def slides_for_section(self, section_index: int) -> list[Slide]:
        return [slide for slide in self.slides if slide.section_index == section_index]

    def to_json(self, *, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls, payload: str) -> SlidePlan:
        return cls.model_validate_json(payload)


def chunk_sizes(count: int, per_slide: int, *, balance_last: bool) -> list[int]:
    """How many lines go on each slide of a section.

    ``balance_last`` only kicks in when the last slide would be left with a single
    line and the section is longer than one slide: five lines at four per slide become
    3 + 2 rather than 4 + 1.
    """
    if count <= 0:
        return []
    if count <= per_slide:
        return [count]

    remainder = count % per_slide
    slides = -(-count // per_slide)  # ceil
    if balance_last and remainder == 1:
        base, extra = divmod(count, slides)
        return [base + (1 if index < extra else 0) for index in range(slides)]

    sizes = [per_slide] * (count // per_slide)
    if remainder:
        sizes.append(remainder)
    return sizes


def _plannable_lines(section: Section) -> list[Line]:
    """Lines that occupy space on a slide.

    A line that carries only an annotation is a note about the section, not something
    to project, so it rides along with the line before it instead of taking a slot.
    """
    lines: list[Line] = []
    for line in section.lines:
        if line.is_empty:
            continue
        if not line.lyrics and not line.chords and line.annotation:
            if lines:
                previous = lines[-1]
                lines[-1] = Line(
                    lyrics=previous.lyrics,
                    chords=previous.chords,
                    annotation=" / ".join(filter(None, [previous.annotation, line.annotation])),
                )
            else:
                lines.append(line)
            continue
        lines.append(line)
    return lines


def plan_slides(song: Song, config: ConversionConfig | None = None) -> SlidePlan:
    """Chunk every section into slides."""
    config = config or ConversionConfig()
    slides: list[Slide] = []
    warnings: list[str] = list(song.warnings)

    for section_index, section in enumerate(song.sections):
        lines = _plannable_lines(section)
        if not lines:
            continue
        sizes = chunk_sizes(
            len(lines), config.lines_per_slide, balance_last=config.balance_last_slide
        )
        position = 0
        for ordinal, size in enumerate(sizes, start=1):
            slides.append(
                Slide(
                    section_index=section_index,
                    section_label=section.label,
                    section_type=section.type,
                    ordinal=ordinal,
                    total_in_section=len(sizes),
                    lines=lines[position : position + size],
                )
            )
            position += size

    if not slides:
        warnings.append("The song produced no slides; every section was empty.")
    return SlidePlan(song=song, slides=slides, config=config, warnings=warnings)
