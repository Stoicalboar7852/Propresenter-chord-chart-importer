"""Every source pcci knows, in the order it asks them.

Search order is answer quality first: the site with the chords leads, the site with
the words follows, and the site with the artwork fills in what the other two could not
say about the song.

Fetch order is specific-before-general. ``PAGE`` accepts every address there is, so it
has to come last or it would swallow the links the other two know how to read properly.
"""

from __future__ import annotations

from pcci.online.sources.base import ChartProvider, SearchProvider, fetch_text
from pcci.online.sources.genius import GENIUS
from pcci.online.sources.itunes import ITUNES
from pcci.online.sources.page import PAGE
from pcci.online.sources.ultimate_guitar import ULTIMATE_GUITAR

SEARCH_PROVIDERS: tuple[SearchProvider, ...] = (ULTIMATE_GUITAR, GENIUS, ITUNES)
CHART_PROVIDERS: tuple[ChartProvider, ...] = (ULTIMATE_GUITAR, GENIUS, PAGE)

__all__ = [
    "CHART_PROVIDERS",
    "GENIUS",
    "ITUNES",
    "PAGE",
    "SEARCH_PROVIDERS",
    "ULTIMATE_GUITAR",
    "ChartProvider",
    "SearchProvider",
    "fetch_text",
]
