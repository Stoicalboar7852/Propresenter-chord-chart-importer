"""Ultimate Guitar: where the chords actually are.

For modern worship songs this is the source that has a chart at all, so it is what the
search leans on for words. It has no public API, but it does not need scraping either:
the site renders itself from a JSON document it leaves in the page
(``<div class="js-store" data-content="...">``), and reading that is both kinder and
far steadier than picking through generated markup.

It is still somebody else's private shape, so nothing here insists on it. Every lookup
that does not find what it expects returns no results and says so, and the search goes
on with whatever the other sources found. When the site refuses us outright - it
sometimes does - the message tells the user to open the page themselves and paste the
chart in, which works every time.
"""

from __future__ import annotations

import math
import urllib.parse
from typing import Any

from pcci.errors import NoChartFoundError
from pcci.online.cache import SEARCH_TTL_SECONDS, Cache
from pcci.online.http import Http
from pcci.online.models import (
    ChartKind,
    FetchedChart,
    SongMatch,
    SourceRef,
    Supply,
    reference_for,
)
from pcci.online.sources.base import fetch_text, with_credits
from pcci.online.text import (
    dig,
    find_first,
    js_store,
    strip_ultimate_guitar_markup,
    tidy,
)

SEARCH_ENDPOINT = "https://www.ultimate-guitar.com/search.php"
HOSTS = ("ultimate-guitar.com", "tabs.ultimate-guitar.com", "www.ultimate-guitar.com")

#: Listing types that carry words. Tab, Bass Tab and Drums are notation with no lyrics
#: under it; Pro and Power are binary files for other programs; Official needs an
#: account. None of those can become a presentation, so they never reach the list.
USABLE_TYPES = {"chords", "ukulele chords"}


def _host_matches(url: str) -> bool:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return any(host == known or host.endswith("." + known) for known in ("ultimate-guitar.com",))


def _results_from(store: Any) -> list[dict[str, Any]]:
    """The search results list, however deep this week's page buries it."""
    direct = dig(store, "store", "page", "data", "results")
    if isinstance(direct, list):
        return [entry for entry in direct if isinstance(entry, dict)]
    found = find_first(
        store,
        lambda node: (
            isinstance(node, list) and node and isinstance(node[0], dict) and "tab_url" in node[0]
        ),
    )
    if isinstance(found, list):
        return [entry for entry in found if isinstance(entry, dict)]
    return []


def _content_from(store: Any) -> str | None:
    """The chart text on a tab page."""
    direct = dig(store, "store", "page", "data", "tab_view", "wiki_tab", "content")
    if isinstance(direct, str) and direct.strip():
        return direct
    found = find_first(
        store,
        lambda node: (
            isinstance(node, dict)
            and isinstance(node.get("content"), str)
            and "[ch]" in node["content"]
        ),
    )
    if isinstance(found, dict):
        content = found.get("content")
        if isinstance(content, str):
            return content
    return None


def _number(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) and not isinstance(value, bool) else None


def _kind_of(listing_type: str) -> ChartKind:
    return "chords" if "chord" in listing_type.lower() else "tab"


class UltimateGuitarSource:
    """Chord charts from Ultimate Guitar."""

    id = "ultimate-guitar"
    name = "Ultimate Guitar"
    site = "https://www.ultimate-guitar.com"
    supplies: tuple[Supply, ...] = ("chords", "lyrics")

    def search(self, query: str, *, limit: int, http: Http, cache: Cache) -> list[SongMatch]:
        parameters = urllib.parse.urlencode({"search_type": "title", "value": query})
        url = f"{SEARCH_ENDPOINT}?{parameters}"
        store = js_store(fetch_text(url, http=http, cache=cache, ttl=SEARCH_TTL_SECONDS))
        if store is None:
            return []

        best: dict[str, SongMatch] = {}
        for entry in _results_from(store):
            listing_type = str(entry.get("type") or "")
            if listing_type.strip().lower() not in USABLE_TYPES:
                continue
            access = entry.get("tab_access_type")
            if isinstance(access, str) and access.lower() not in ("public", ""):
                continue
            tab_url = entry.get("tab_url")
            title = entry.get("song_name")
            if not isinstance(tab_url, str) or not isinstance(title, str) or not title.strip():
                continue
            artist = entry.get("artist_name") if isinstance(entry.get("artist_name"), str) else None
            rating = _number(entry.get("rating"))
            votes = entry.get("votes") if isinstance(entry.get("votes"), int) else None
            tonality = entry.get("tonality_name")

            match = SongMatch(
                ref=reference_for(self.id, tab_url, title, artist),
                title=title.strip(),
                artist=artist,
                chart_url=tab_url,
                chart_kind=_kind_of(listing_type),
                rating=rating,
                votes=votes,
                key=tonality if isinstance(tonality, str) and tonality else None,
                sources=[
                    SourceRef(
                        provider=self.id,
                        name=self.name,
                        url=tab_url,
                        supplies=list(self.supplies),
                    )
                ],
            )
            # The same song has a dozen user-submitted versions. Show the one the site's
            # own readers rate highest, not twelve rows of the same words.
            key = match.merge_key()
            incumbent = best.get(key)
            if incumbent is None or _score(match) > _score(incumbent):
                best[key] = match

        ranked = sorted(best.values(), key=_score, reverse=True)
        return ranked[:limit]

    def owns(self, url: str) -> bool:
        return _host_matches(url)

    def fetch(self, url: str, *, http: Http, cache: Cache) -> FetchedChart:
        store = js_store(fetch_text(url, http=http, cache=cache))
        content = _content_from(store) if store is not None else None
        if content is None:
            raise NoChartFoundError(
                "That Ultimate Guitar page does not have a chord chart pcci can read. "
                "Official and Pro tabs are pictures and files, not text - look for a "
                "listing marked Chords.",
                "no wiki_tab content in the page store",
                context={"url": url},
            )

        metadata = dig(store, "store", "page", "data", "tab")
        metadata = metadata if isinstance(metadata, dict) else {}
        title = metadata.get("song_name")
        artist = metadata.get("artist_name")
        tonality = metadata.get("tonality_name")
        capo = metadata.get("capo")

        chart_text = tidy(strip_ultimate_guitar_markup(content))
        extra: dict[str, str] = {}
        if isinstance(tonality, str) and tonality.strip():
            extra["Key"] = tonality.strip()
        if isinstance(capo, int) and capo:
            extra["Capo"] = str(capo)
        body = with_credits(
            chart_text,
            title=title if isinstance(title, str) else None,
            artist=artist if isinstance(artist, str) else None,
            extra=extra,
        )

        return FetchedChart(
            text=body,
            suffix=".txt",
            title=title.strip() if isinstance(title, str) and title.strip() else "Chord chart",
            artist=artist if isinstance(artist, str) and artist.strip() else None,
            chart_kind="chords" if "[ch]" in content else "lyrics",
            source=SourceRef(
                provider=self.id, name=self.name, url=url, supplies=list(self.supplies)
            ),
        )


def _score(match: SongMatch) -> float:
    """Rank a listing the way the site's own readers already have.

    Rating alone puts a five-star chart with one vote above a 4.8 with nine hundred, so
    votes carry weight too - gently, on a log scale, because the difference between one
    vote and fifty matters far more than between five hundred and a thousand.
    """
    rating = match.rating or 0.0
    votes = match.votes or 0
    return rating + math.log10(votes + 1)


ULTIMATE_GUITAR = UltimateGuitarSource()
