"""LRCLIB: an open lyrics database with a real, free, keyless API.

This is the gap-filler. Ultimate Guitar has the chords for anything with a guitar
part; the sites that hold words for everything else mostly refuse a program outright.
LRCLIB is built to be read by software - no key, no account, no scraping, documented
endpoints - and it hands back the words in one field.

What it does not have is section headings. The lyrics arrive as stanzas separated by
blank lines, which the parser's last-resort route reads as verses and marks as
guessed, so the review screen flags them for a human to name. That is the honest
outcome for a source that simply does not record where the chorus is.
"""

from __future__ import annotations

import json
import urllib.parse
from typing import Any

from pcci.errors import NoChartFoundError
from pcci.online.cache import SEARCH_TTL_SECONDS, Cache
from pcci.online.http import Http
from pcci.online.models import FetchedChart, SongMatch, SourceRef, Supply, reference_for
from pcci.online.sources.base import fetch_text, with_credits
from pcci.online.text import tidy

SEARCH_ENDPOINT = "https://lrclib.net/api/search"
RECORD_ENDPOINT = "https://lrclib.net/api/get"
HOST = "lrclib.net"


def _host_matches(url: str) -> bool:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host == HOST or host.endswith("." + HOST)


def _text_of(record: dict[str, Any], key: str) -> str | None:
    value = record.get(key)
    return value.strip() if isinstance(value, str) and value.strip() else None


def _year_of(record: dict[str, Any]) -> int | None:
    released = record.get("releaseDate")
    if isinstance(released, str) and len(released) >= 4 and released[:4].isdigit():
        return int(released[:4])
    return None


class LrclibSource:
    """Words from LRCLIB."""

    id = "lrclib"
    name = "LRCLIB"
    site = "https://lrclib.net"
    supplies: tuple[Supply, ...] = ("lyrics", "metadata")

    def search(self, query: str, *, limit: int, http: Http, cache: Cache) -> list[SongMatch]:
        url = f"{SEARCH_ENDPOINT}?{urllib.parse.urlencode({'q': query})}"
        raw = fetch_text(
            url, http=http, cache=cache, ttl=SEARCH_TTL_SECONDS, accept="application/json"
        )
        try:
            records = json.loads(raw)
        except ValueError:
            return []
        if not isinstance(records, list):
            return []

        matches: list[SongMatch] = []
        for record in records:
            if not isinstance(record, dict):
                continue
            title = _text_of(record, "trackName") or _text_of(record, "name")
            identifier = record.get("id")
            if not title or not isinstance(identifier, int):
                continue
            # An instrumental has no words by definition. Saying so is more use than
            # offering an import that would produce an empty presentation.
            instrumental = bool(record.get("instrumental")) or not _text_of(record, "plainLyrics")
            page = f"{RECORD_ENDPOINT}/{identifier}"
            matches.append(
                SongMatch(
                    ref=reference_for(self.id, page, title, _text_of(record, "artistName")),
                    title=title,
                    artist=_text_of(record, "artistName"),
                    album=_text_of(record, "albumName"),
                    year=_year_of(record),
                    chart_url=None if instrumental else page,
                    chart_kind="none" if instrumental else "lyrics",
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
            if len(matches) >= limit:
                break
        return matches

    def owns(self, url: str) -> bool:
        return _host_matches(url)

    def fetch(self, url: str, *, http: Http, cache: Cache) -> FetchedChart:
        raw = fetch_text(url, http=http, cache=cache, accept="application/json")
        try:
            record = json.loads(raw)
        except ValueError as error:
            raise NoChartFoundError(
                "LRCLIB sent back something pcci could not read.",
                f"{type(error).__name__}: {error}",
                context={"url": url},
            ) from error
        if not isinstance(record, dict):
            raise NoChartFoundError(
                "LRCLIB has no song at that address.",
                "the response was not a record",
                context={"url": url},
            )

        body = tidy(_text_of(record, "plainLyrics") or "")
        if not body:
            raise NoChartFoundError(
                "LRCLIB has that song but no words for it - it is marked instrumental.",
                "plainLyrics was empty",
                context={"url": url},
            )

        title = _text_of(record, "trackName") or _text_of(record, "name") or "Lyrics"
        artist = _text_of(record, "artistName")
        return FetchedChart(
            text=with_credits(body, title=title, artist=artist),
            suffix=".txt",
            title=title,
            artist=artist,
            chart_kind="lyrics",
            source=SourceRef(provider=self.id, name=self.name, url=url, supplies=["lyrics"]),
            notes=[
                "LRCLIB stores words without section headings, so the verses and "
                "choruses here were guessed from the blank lines. Check them on the "
                "review screen before exporting."
            ],
        )


LRCLIB = LrclibSource()
