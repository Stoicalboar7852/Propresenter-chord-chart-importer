"""What a source of songs looks like, and the two things they all do the same way.

Sources come in two kinds and some are both:

``SearchProvider``
    Answers "what songs match these words?" - the rows in the result list.

``ChartProvider``
    Answers "what are the words and chords at this address?" - the import itself.

Apple Music can only do the first (it has the artwork and the credits, and no lyrics);
a pasted link can only do the second; Ultimate Guitar does both. Keeping them apart
means no source has to carry a method it cannot honour.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pcci.online.cache import CHART_TTL_SECONDS, Cache
from pcci.online.http import Http
from pcci.online.models import FetchedChart, SongMatch, Supply


@runtime_checkable
class SearchProvider(Protocol):
    """A site that can be asked for songs by name."""

    id: str
    name: str
    site: str
    supplies: tuple[Supply, ...]

    def search(self, query: str, *, limit: int, http: Http, cache: Cache) -> list[SongMatch]: ...


@runtime_checkable
class ChartProvider(Protocol):
    """A site whose pages can be turned into a chart."""

    id: str
    name: str
    site: str
    supplies: tuple[Supply, ...]

    def owns(self, url: str) -> bool: ...

    def fetch(self, url: str, *, http: Http, cache: Cache) -> FetchedChart: ...


def fetch_text(
    url: str,
    *,
    http: Http,
    cache: Cache,
    ttl: int = CHART_TTL_SECONDS,
    accept: str | None = None,
) -> str:
    """A page's text, from the cache when it is there and fresh.

    A search followed by an import is two requests for the same page seconds apart,
    which is rude to the site and slow for the user. One line of cache removes both.
    """
    hit = cache.get(url, ttl=ttl)
    if hit is not None:
        return hit.decode("utf-8")
    response = http.get(url) if accept is None else http.get(url, accept=accept)
    text = response.text()
    cache.put(url, text.encode("utf-8"))
    return text
