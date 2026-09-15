"""The intermediate representation every ingester produces and every writer consumes.

Two seams matter here:

``RawDocument``
    What an ingester saw: lines of text with whatever positional information the
    source format could give us. No song semantics at all.

``Song``
    What the parsers made of it: sections, lines, chords anchored to character
    offsets. Everything downstream (slide planning, ProPresenter writing,
    ChordPro export) consumes ``Song`` and nothing else.

``Song`` round-trips losslessly through JSON; the golden tests depend on it.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SourceFormat = Literal["txt", "md", "pdf", "docx", "rtf", "odt", "html", "chordpro"]


class PositionedLine(BaseModel):
    """One visual line of source text, with per-character x positions when known.

    ``char_x`` is either empty (no positional information — the source was plain
    text and column indices are the only alignment signal) or exactly as long as
    ``text``. Ingesters that cannot supply positions leave it empty rather than
    faking values.
    """

    model_config = ConfigDict(extra="forbid")

    text: str
    y: float = 0.0
    x0: float = 0.0
    char_x: list[float] = Field(default_factory=list)
    page: int = 1
    bold: bool = False
    italic: bool = False
    font_size: float | None = None
    font_name: str | None = None
    heading: bool = False

    @model_validator(mode="after")
    def _char_x_matches_text(self) -> PositionedLine:
        if self.char_x and len(self.char_x) != len(self.text):
            msg = f"char_x has {len(self.char_x)} entries for {len(self.text)} characters"
            raise ValueError(msg)
        return self

    @property
    def positioned(self) -> bool:
        """True when this line carries real per-character geometry."""
        return bool(self.char_x)


class RawDocument(BaseModel):
    """The output of ingestion: positioned text plus what we know about the source."""

    model_config = ConfigDict(extra="forbid")

    source_path: Path
    source_format: SourceFormat
    lines: list[PositionedLine] = Field(default_factory=list)
    monospace: bool = False
    warnings: list[str] = Field(default_factory=list)

    def non_empty_lines(self) -> list[PositionedLine]:
        return [line for line in self.lines if line.text.strip()]


class ChordPlacement(BaseModel):
    """A chord anchored to a character offset in the lyric it sits above."""

    model_config = ConfigDict(extra="forbid")

    chord: str
    char_index: int = Field(ge=0)
    raw: str = ""

    @model_validator(mode="after")
    def _default_raw(self) -> ChordPlacement:
        if not self.raw:
            object.__setattr__(self, "raw", self.chord)
        return self


class Line(BaseModel):
    """A lyric line and the chords placed over it.

    Three shapes occur in real charts:

    * lyrics with chords — the ordinary case;
    * ``lyrics == ""`` with chords — an instrumental line (intros, turnarounds);
    * ``annotation`` set — a performance instruction such as ``Hold G X 8 BARS``.
      Annotations are never projected as lyrics; they travel in slide notes.
    """

    model_config = ConfigDict(extra="forbid")

    lyrics: str = ""
    chords: list[ChordPlacement] = Field(default_factory=list)
    annotation: str | None = None

    @model_validator(mode="after")
    def _chords_within_lyrics(self) -> Line:
        limit = len(self.lyrics)
        for placement in self.chords:
            if placement.char_index > limit:
                msg = f"chord {placement.chord!r} at {placement.char_index} exceeds lyric length {limit}"
                raise ValueError(msg)
        return self

    @property
    def is_instrumental(self) -> bool:
        return not self.lyrics and bool(self.chords)

    @property
    def is_empty(self) -> bool:
        return not self.lyrics and not self.chords and not self.annotation


class SectionType(StrEnum):
    INTRO = "Intro"
    VERSE = "Verse"
    PRE_CHORUS = "Pre-Chorus"
    CHORUS = "Chorus"
    POST_CHORUS = "Post-Chorus"
    BRIDGE = "Bridge"
    TAG = "Tag"
    OUTRO = "Outro"
    INSTRUMENTAL = "Instrumental"
    INTERLUDE = "Interlude"
    VAMP = "Vamp"
    BREAKDOWN = "Breakdown"
    REFRAIN = "Refrain"
    ENDING = "Ending"
    MISC = "Misc"


class Section(BaseModel):
    """A detected song section and the lines beneath its header."""

    model_config = ConfigDict(extra="forbid")

    type: SectionType
    number: int | None = None
    raw_label: str = ""
    lines: list[Line] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    @property
    def label(self) -> str:
        """``Verse 2``, ``Chorus``, or the user's own label for a MISC section."""
        if self.type is SectionType.MISC and self.raw_label:
            return self.raw_label
        if self.number is None:
            return str(self.type)
        return f"{self.type} {self.number}"

    @property
    def lyric_lines(self) -> list[Line]:
        return [line for line in self.lines if line.lyrics]


class Song(BaseModel):
    """The parsed song. Everything downstream consumes this and nothing else."""

    model_config = ConfigDict(extra="forbid")

    title: str
    artist: str | None = None
    ccli_number: str | None = None
    copyright: str | None = None
    key: str | None = None
    tempo: int | None = None
    sections: list[Section] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    source_path: Path | None = None
    source_format: SourceFormat | None = None

    @field_validator("title")
    @classmethod
    def _title_not_blank(cls, value: str) -> str:
        if not value.strip():
            msg = "song title must not be blank"
            raise ValueError(msg)
        return value.strip()

    @property
    def line_count(self) -> int:
        return sum(len(section.lines) for section in self.sections)

    @property
    def chord_count(self) -> int:
        return sum(len(line.chords) for section in self.sections for line in section.lines)

    def to_json(self, *, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls, payload: str) -> Song:
        return cls.model_validate_json(payload)
