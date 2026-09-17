"""Apple's iTunes Search API: the cover art and the credits.

This is the one source here that is a real, documented, public API - no key, no
account, no scraping - so it is what the result list leans on for everything that is
not the words themselves: the artwork, the album, the year, the exact spelling of the
artist's name.

It has no lyrics and no chords, and never will. A row that only Apple knows about is
shown anyway, marked as having no words available, because "this song exists but pcci
cannot find its chart" is a useful answer and an empty list is not.
"""

from __future__ import annotations

import json
import urllib.parse
from typing import Any

from pcci.online.cache import SEARCH_TTL_SECONDS, Cache
from pcci.online.http import Http
from pcci.online.models import SongMatch, SourceRef, Supply, reference_for
from pcci.online.sources.base import fetch_text

SEARCH_ENDPOINT = "https://itunes.apple.com/search"

#: Apple serves artwork at whatever size you ask for by rewriting the filename.
#: 100x100 is what the API hands back; a results list wants a little more than that,
#: and a detail view wants rather more again.
THUMB_SIZE = "200x200bb"
LARGE_SIZE = "600x600bb"


def _artwork(url: str | None, size: str) -> str | None:
    if not url:
        return None
    for known in ("100x100bb", "60x60bb", "30x30bb"):
        if known in url:
            return url.replace(known, size)
    return url


def _year(entry: dict[str, Any]) -> int | None:
    release = entry.get("releaseDate")
    if not isinstance(release, str) or len(release) < 4:
        return None
    try:
        return int(release[:4])
    except ValueError:
        return None


class ITunesSource:
    """Metadata and artwork from the iTunes Search API."""

    id = "itunes"
    name = "Apple Music"
    site = "https://music.apple.com"
    supplies: tuple[Supply, ...] = ("metadata", "artwork")

    def search(self, query: str, *, limit: int, http: Http, cache: Cache) -> list[SongMatch]:
        parameters = urllib.parse.urlencode(
            {
                "term": query,
                "entity": "song",
                "media": "music",
                "limit": str(max(1, min(limit * 2, 25))),
            }
        )
        url = f"{SEARCH_ENDPOINT}?{parameters}"
        payload = _parse(
            fetch_text(
                url, http=http, cache=cache, ttl=SEARCH_TTL_SECONDS, accept="application/json"
            )
        )
        entries = payload.get("results") if isinstance(payload, dict) else None
        if not isinstance(entries, list):
            return []

        matches: list[SongMatch] = []
        for entry in entries[:limit]:
            if not isinstance(entry, dict):
                continue
            title = entry.get("trackName") or entry.get("collectionName")
            if not isinstance(title, str) or not title.strip():
                continue
            artist = entry.get("artistName") if isinstance(entry.get("artistName"), str) else None
            page = entry.get("trackViewUrl") or entry.get("collectionViewUrl")
            matches.append(
                SongMatch(
                    ref=reference_for(self.id, None, title, artist),
                    title=title.strip(),
                    artist=artist,
                    album=entry.get("collectionName")
                    if isinstance(entry.get("collectionName"), str)
                    else None,
                    year=_year(entry),
                    artwork_url=_artwork(entry.get("artworkUrl100"), LARGE_SIZE),
                    artwork_thumb_url=_artwork(entry.get("artworkUrl100"), THUMB_SIZE),
                    artwork_provider=self.id,
                    chart_kind="none",
                    sources=[
                        SourceRef(
                            provider=self.id,
                            name=self.name,
                            url=page if isinstance(page, str) else None,
                            supplies=list(self.supplies),
                        )
                    ],
                )
            )
        return matches


def _parse(text: str) -> Any:
    try:
        return json.loads(text)
    except ValueError:
        return {}


ITUNES = ITunesSource()
