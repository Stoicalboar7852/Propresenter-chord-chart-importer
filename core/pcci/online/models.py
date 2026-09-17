"""What an online search found, and what an online fetch brought back.

These are the shapes the desktop apps render, so they carry everything a result row
needs - the artwork, the credits, and the name of whichever site the row came from -
and nothing the engine would have to invent.

A match is not necessarily importable. A song can be findable on Apple Music and
nowhere that has its words, and saying so plainly is better than hiding the song or
pretending there is a chart behind it.
"""

from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

#: What a source contributed to a match.
Supply = Literal["metadata", "artwork", "chords", "lyrics"]

#: What the words behind a match actually are.
ChartKind = Literal["chords", "tab", "lyrics", "none"]


class SourceRef(BaseModel):
    """A site that contributed to a result, and what it contributed."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    name: str
    url: str | None = None
    supplies: list[Supply] = Field(default_factory=list)


class SongMatch(BaseModel):
    """One row in the search results."""

    model_config = ConfigDict(extra="forbid")

    ref: str
    title: str
    artist: str | None = None
    album: str | None = None
    year: int | None = None
    artwork_url: str | None = None
    artwork_thumb_url: str | None = None
    #: Which source the cover came from. Two sites can both have one and they are not
    #: equally good: Apple serves the album's own artwork at whatever size is asked
    #: for, so it wins a tie. See ``search.ARTWORK_RANK``.
    artwork_provider: str | None = None
    chart_url: str | None = None
    chart_kind: ChartKind = "none"
    rating: float | None = None
    votes: int | None = None
    key: str | None = None
    ccli_number: str | None = None
    copyright: str | None = None
    sources: list[SourceRef] = Field(default_factory=list)

    @property
    def importable(self) -> bool:
        """Whether there is anything here to turn into a presentation."""
        return self.chart_url is not None and self.chart_kind != "none"

    @property
    def has_chords(self) -> bool:
        return self.chart_kind in ("chords", "tab")

    @property
    def source_names(self) -> list[str]:
        return [source.name for source in self.sources]

    @property
    def subtitle(self) -> str:
        """``Parish Choir - Hymns, Volume One (2019)``, as much of it as is known."""
        parts = [part for part in (self.artist, self.album) if part]
        line = " - ".join(parts)
        if self.year:
            line = f"{line} ({self.year})" if line else str(self.year)
        return line

    def merge_key(self) -> str:
        """Two rows for the same song collapse into one. Punctuation is not identity."""
        return f"{fold(self.title)}|{fold(self.artist or '')}"


class SearchOutcome(BaseModel):
    """Everything one search produced, including what went wrong on the way."""

    model_config = ConfigDict(extra="forbid")

    query: str
    is_url: bool = False
    results: list[SongMatch] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class FetchedChart(BaseModel):
    """A chart pulled off the web, before it is written anywhere."""

    model_config = ConfigDict(extra="forbid")

    text: str
    suffix: str = ".txt"
    title: str
    artist: str | None = None
    chart_kind: ChartKind = "lyrics"
    source: SourceRef
    match: SongMatch | None = None
    notes: list[str] = Field(default_factory=list)

    @property
    def has_chords(self) -> bool:
        return self.chart_kind in ("chords", "tab")


_FOLD_RE = re.compile(r"[^a-z0-9]+")

#: Words a search result routinely carries that are not part of the song's identity.
_NOISE = (
    "chords",
    "chord",
    "lyrics",
    "tab",
    "tabs",
    "official",
    "live",
    "acoustic",
    "remastered",
    "version",
    "feat",
    "featuring",
)


def fold(text: str) -> str:
    """Reduce a title to the part that identifies the song.

    ``"Come Thou Fount (of Every Blessing) [Live]"`` and ``"Come Thou Fount of Every
    Blessing chords"`` are the same song, and a result list that shows both twice is a
    worse list. Punctuation goes, and so do the handful of words that only ever
    describe the *listing* rather than the song. What is inside the brackets stays:
    "(of Every Blessing)" is half the title, and throwing it away would merge two
    different songs that both begin "Come Thou Fount".
    """
    words = [word for word in _FOLD_RE.split(text.casefold()) if word and word not in _NOISE]
    return " ".join(words)


def reference_for(provider: str, url: str | None, title: str, artist: str | None) -> str:
    """A stable id for a result row, short enough to pass around as an argument."""
    seed = url or f"{provider}:{fold(title)}:{fold(artist or '')}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
