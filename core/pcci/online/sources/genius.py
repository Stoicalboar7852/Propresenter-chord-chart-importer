"""Genius: the words, when nobody has the chords.

Plenty of songs a church wants have no chart online at all, and the user was explicit
that lyrics alone are worth having. Genius is the broadest lyrics source there is, and
it writes its section headers as ``[Verse 1]`` and ``[Chorus]`` - exactly the shape
pcci's own section detector was built around - so what comes back needs no
interpretation at all.

No chords, ever. A row sourced here is marked as lyrics, and the presentation it makes
is a lyrics presentation.
"""

from __future__ import annotations

import json
import urllib.parse
from typing import Any

from bs4 import BeautifulSoup, Tag

from pcci.errors import NoChartFoundError
from pcci.online.cache import SEARCH_TTL_SECONDS, Cache
from pcci.online.http import Http
from pcci.online.models import FetchedChart, SongMatch, SourceRef, Supply, reference_for
from pcci.online.sources.base import fetch_text
from pcci.online.text import blocks_text, find_all, tidy

SEARCH_ENDPOINT = "https://genius.com/api/search/song"
LYRICS_ATTRIBUTE = "data-lyrics-container"


def _host_matches(url: str) -> bool:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host == "genius.com" or host.endswith(".genius.com")


def _looks_like_song(node: Any) -> bool:
    return (
        isinstance(node, dict)
        and isinstance(node.get("title"), str)
        and isinstance(node.get("url"), str)
        and isinstance(node.get("primary_artist"), dict)
    )


def _year(node: dict[str, Any]) -> int | None:
    components = node.get("release_date_components")
    if isinstance(components, dict) and isinstance(components.get("year"), int):
        year: int = components["year"]
        return year
    return None


def _artwork(node: dict[str, Any]) -> tuple[str | None, str | None]:
    large = node.get("song_art_image_url")
    thumb = node.get("song_art_image_thumbnail_url")
    large = large if isinstance(large, str) else None
    thumb = thumb if isinstance(thumb, str) else None
    return large or thumb, thumb or large


class GeniusSource:
    """Lyrics from Genius."""

    id = "genius"
    name = "Genius"
    site = "https://genius.com"
    supplies: tuple[Supply, ...] = ("lyrics", "artwork", "metadata")

    def search(self, query: str, *, limit: int, http: Http, cache: Cache) -> list[SongMatch]:
        parameters = urllib.parse.urlencode({"q": query, "per_page": str(max(1, min(limit, 20)))})
        url = f"{SEARCH_ENDPOINT}?{parameters}"
        raw = fetch_text(
            url, http=http, cache=cache, ttl=SEARCH_TTL_SECONDS, accept="application/json"
        )
        try:
            payload = json.loads(raw)
        except ValueError:
            return []

        matches: list[SongMatch] = []
        seen: set[str] = set()
        for node in find_all(payload, _looks_like_song):
            page = node["url"]
            if not _host_matches(page) or page in seen:
                continue
            seen.add(page)
            artist = node["primary_artist"].get("name")
            artist = artist if isinstance(artist, str) else None
            large, thumb = _artwork(node)
            matches.append(
                SongMatch(
                    ref=reference_for(self.id, page, node["title"], artist),
                    title=node["title"].strip(),
                    artist=artist,
                    year=_year(node),
                    artwork_url=large,
                    artwork_thumb_url=thumb,
                    artwork_provider=self.id if (large or thumb) else None,
                    chart_url=page,
                    chart_kind="lyrics",
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
        page = fetch_text(url, http=http, cache=cache)
        blocks = blocks_text(page, attribute=LYRICS_ATTRIBUTE)
        body = tidy("\n".join(blocks))
        if not body.strip():
            raise NoChartFoundError(
                "pcci could not find the lyrics on that Genius page.",
                f"no [{LYRICS_ATTRIBUTE}] block in the page",
                context={"url": url},
            )

        title, artist = _credits(page, url)
        header = [part for part in (title, artist) if part]
        text = "\n".join([*header, "", body]) if header else body
        return FetchedChart(
            text=text + "\n",
            suffix=".txt",
            title=title or "Lyrics",
            artist=artist,
            chart_kind="lyrics",
            source=SourceRef(provider=self.id, name=self.name, url=url, supplies=["lyrics"]),
            notes=["Genius has the words but no chords, so this import has lyrics only."],
        )


def _credits(page: str, url: str) -> tuple[str | None, str | None]:
    """Title and artist, from the page's own metadata or failing that its address."""
    soup = BeautifulSoup(page, "html.parser")
    element = soup.find("meta", attrs={"property": "og:title"})
    if isinstance(element, Tag):
        content = element.get("content")
        if isinstance(content, str) and content.strip():
            # "Artist - Title" is how Genius writes it.
            artist, separator, title = content.partition(" - ")
            if separator and title.strip():
                return _strip_lyrics_suffix(title), artist.strip() or None
            return _strip_lyrics_suffix(content), None

    # genius.com/parish-hymnal-choir-amazing-grace-lyrics
    slug = urllib.parse.urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
    words = slug.removesuffix("-lyrics").replace("-", " ").strip()
    return (words.title() or None), None


def _strip_lyrics_suffix(title: str) -> str:
    cleaned = title.strip()
    for suffix in (" Lyrics", " lyrics"):
        cleaned = cleaned.removesuffix(suffix)
    return cleaned.strip()


GENIUS = GeniusSource()
