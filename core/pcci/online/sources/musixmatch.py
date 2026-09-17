"""Musixmatch, for anyone who has a key for it.

Musixmatch is the obvious place to ask for words, and its API is a real documented
one. Two things stop it being the default:

* it needs an API key, which is per-person and cannot be shipped in a public
  repository;
* the free plan returns **30% of each song** and marks the rest excluded. Thirty per
  cent of a song is not a presentation.

So this source is present and dormant. Set ``PCCI_MUSIXMATCH_KEY`` and it joins the
search; leave it unset and it contributes nothing and costs nothing. When a truncated
body comes back it says so on the import rather than quietly handing over a third of
the words.
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
from typing import Any

from pcci.errors import NoChartFoundError
from pcci.online.cache import SEARCH_TTL_SECONDS, Cache
from pcci.online.http import Http
from pcci.online.models import FetchedChart, SongMatch, SourceRef, Supply, reference_for
from pcci.online.sources.base import fetch_text, with_credits
from pcci.online.text import tidy

API_ROOT = "https://api.musixmatch.com/ws/1.1"
KEY_VARIABLE = "PCCI_MUSIXMATCH_KEY"
HOST = "api.musixmatch.com"

#: What the free plan appends to every body it truncates.
_COMMERCIAL_NOTICE = re.compile(
    r"\*+\s*This Lyrics is NOT for Commercial use\s*\*+|\(\d{10,}\)", re.IGNORECASE
)
_TRUNCATION = re.compile(r"\.{3}\s*$|\(\d+% of lyrics excluded\)", re.IGNORECASE)


def api_key() -> str | None:
    key = os.environ.get(KEY_VARIABLE, "").strip()
    return key or None


def _host_matches(url: str) -> bool:
    return (urllib.parse.urlsplit(url).hostname or "").lower() == HOST


def _dig(payload: Any, *path: str) -> Any:
    current = payload
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


class MusixmatchSource:
    """Words from Musixmatch, when a key is configured."""

    id = "musixmatch"
    name = "Musixmatch"
    site = "https://www.musixmatch.com"
    supplies: tuple[Supply, ...] = ("lyrics", "metadata")

    def search(self, query: str, *, limit: int, http: Http, cache: Cache) -> list[SongMatch]:
        key = api_key()
        if key is None:
            return []
        parameters = urllib.parse.urlencode(
            {
                "q": query,
                "page_size": str(max(1, min(limit, 20))),
                "s_track_rating": "desc",
                "f_has_lyrics": "1",
                "apikey": key,
            }
        )
        raw = fetch_text(
            f"{API_ROOT}/track.search?{parameters}",
            http=http,
            cache=cache,
            ttl=SEARCH_TTL_SECONDS,
            accept="application/json",
        )
        try:
            payload = json.loads(raw)
        except ValueError:
            return []

        tracks = _dig(payload, "message", "body", "track_list")
        if not isinstance(tracks, list):
            return []

        matches: list[SongMatch] = []
        for entry in tracks[:limit]:
            track = entry.get("track") if isinstance(entry, dict) else None
            if not isinstance(track, dict):
                continue
            title = track.get("track_name")
            identifier = track.get("track_id")
            if not isinstance(title, str) or not title.strip() or identifier is None:
                continue
            artist = track.get("artist_name")
            # The key is never put in a stored URL: it would end up in the cache, in
            # the result list and in whatever the front-end logs.
            page = f"{API_ROOT}/track.lyrics.get?track_id={identifier}"
            matches.append(
                SongMatch(
                    ref=reference_for(
                        self.id, page, title, artist if isinstance(artist, str) else None
                    ),
                    title=title.strip(),
                    artist=artist.strip() if isinstance(artist, str) and artist.strip() else None,
                    album=track.get("album_name")
                    if isinstance(track.get("album_name"), str)
                    else None,
                    chart_url=page,
                    chart_kind="lyrics",
                    chart_provider=self.id,
                    sources=[
                        SourceRef(
                            provider=self.id,
                            name=self.name,
                            url=page,
                            supplies=list(self.supplies),
                        )
                    ],
                )
            )
        return matches

    def owns(self, url: str) -> bool:
        return _host_matches(url) and api_key() is not None

    def fetch(self, url: str, *, http: Http, cache: Cache) -> FetchedChart:
        key = api_key()
        if key is None:
            raise NoChartFoundError(
                f"Musixmatch needs an API key. Set {KEY_VARIABLE} and try again.",
                "no API key configured",
                context={"url": url},
            )
        separator = "&" if "?" in url else "?"
        raw = fetch_text(
            f"{url}{separator}apikey={urllib.parse.quote(key)}",
            http=http,
            cache=cache,
            accept="application/json",
        )
        try:
            payload = json.loads(raw)
        except ValueError as error:
            raise NoChartFoundError(
                "Musixmatch sent back something pcci could not read.",
                f"{type(error).__name__}: {error}",
                context={"url": url},
            ) from error

        raw_body = _dig(payload, "message", "body", "lyrics", "lyrics_body")
        if not isinstance(raw_body, str) or not raw_body.strip():
            raise NoChartFoundError(
                "Musixmatch has no words for that track.",
                f"status {_dig(payload, 'message', 'header', 'status_code')}",
                context={"url": url},
            )

        title, artist = self._name_of(url, key, http=http, cache=cache)
        truncated = bool(_TRUNCATION.search(raw_body))
        body = tidy(_COMMERCIAL_NOTICE.sub("", raw_body))
        notes = [
            "Musixmatch stores words without section headings, so the sections here "
            "were guessed from the blank lines."
        ]
        if truncated:
            notes.insert(
                0,
                "Musixmatch returned only part of this song, which is what the free "
                "plan does. Use another source, or paste the rest in yourself.",
            )
        return FetchedChart(
            text=with_credits(body, title=title, artist=artist),
            suffix=".txt",
            title=title,
            artist=artist,
            chart_kind="lyrics",
            source=SourceRef(provider=self.id, name=self.name, url=url, supplies=["lyrics"]),
            notes=notes,
        )

    def _name_of(self, url: str, key: str, *, http: Http, cache: Cache) -> tuple[str, str | None]:
        """The track's name, which the lyrics endpoint does not return.

        Worth a second request: without it every import from here would be a file
        called "Lyrics.pro". A failure is not fatal - the words are the point - so it
        falls back rather than throwing away a good fetch.
        """
        identifier = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query).get("track_id")
        if not identifier:
            return "Lyrics", None
        try:
            raw = fetch_text(
                f"{API_ROOT}/track.get?track_id={identifier[0]}&apikey={urllib.parse.quote(key)}",
                http=http,
                cache=cache,
                accept="application/json",
            )
            track = _dig(json.loads(raw), "message", "body", "track")
        except Exception:
            return "Lyrics", None
        if not isinstance(track, dict):
            return "Lyrics", None
        name = track.get("track_name")
        artist = track.get("artist_name")
        return (
            name.strip() if isinstance(name, str) and name.strip() else "Lyrics",
            artist.strip() if isinstance(artist, str) and artist.strip() else None,
        )


MUSIXMATCH = MusixmatchSource()
