"""Any link at all: the fallback that makes "paste the address" mean something.

The sites pcci knows by name will never be all of them. Church websites, Google Docs
published to the web, a PDF on a worship leader's Dropbox, somebody's plain .cho file
in a repository - a link is a link, and the engine already knows how to read every one
of those formats once the bytes are on disk.

So this source does as little interpreting as it can get away with. It works out what
kind of document came back, writes it out with the extension that says so, and hands
it to the same reader a dropped file would have gone through. The one piece of real
work is preferring a ``<pre>`` block when the page has one: that is where a chart's
column alignment lives, and a page's ordinary markup throws it away.
"""

from __future__ import annotations

import urllib.parse
from typing import Final

from bs4 import BeautifulSoup, Tag

from pcci.errors import NoChartFoundError
from pcci.online.cache import Cache
from pcci.online.http import Http
from pcci.online.models import ChartKind, FetchedChart, SourceRef, Supply
from pcci.online.text import element_text, looks_like_chart, tidy

#: Extensions the engine reads directly, mapped to what the bytes actually are.
_DIRECT_SUFFIXES: Final[dict[str, str]] = {
    ".txt": ".txt",
    ".text": ".txt",
    ".md": ".md",
    ".markdown": ".md",
    ".cho": ".cho",
    ".chopro": ".cho",
    ".chordpro": ".cho",
    ".crd": ".cho",
    ".pro": ".txt",
}

_TEXT_MEDIA: Final[frozenset[str]] = frozenset(
    {"text/plain", "text/markdown", "text/x-chordpro", "application/octet-stream"}
)


class PageSource:
    """Whatever is at a pasted address."""

    id = "page"
    name = "Web page"
    site = ""
    supplies: tuple[Supply, ...] = ("chords", "lyrics")

    def owns(self, url: str) -> bool:  # noqa: ARG002 - every URL, by design
        """Anything. This runs last, after every source that knows its own site."""
        return True

    def fetch(self, url: str, *, http: Http, cache: Cache) -> FetchedChart:
        cached = cache.get(url, ttl=86400)
        if cached is not None:
            page = cached.decode("utf-8")
            media = "text/html" if page.lstrip()[:1] == "<" else "text/plain"
        else:
            response = http.get(url)
            page = response.text()
            media = response.media_type
            cache.put(url, page.encode("utf-8"))

        path = urllib.parse.urlsplit(url).path.lower()
        suffix = next(
            (mapped for ending, mapped in _DIRECT_SUFFIXES.items() if path.endswith(ending)),
            None,
        )

        if suffix is not None or media in _TEXT_MEDIA:
            body = tidy(page)
            if not looks_like_chart(body):
                raise NoChartFoundError(
                    f"There is not enough text at {_host(url)} to be a song.",
                    f"{len(body.splitlines())} lines of {media or 'unknown'} content",
                    context={"url": url},
                )
            return self._chart(url, body, suffix or ".txt", _title_from(page) or _slug(url))

        if media and not media.startswith(("text/html", "application/xhtml")):
            raise NoChartFoundError(
                f"{_host(url)} sent back a {media} file, which pcci cannot read from a link. "
                "Download it and drop it on the window instead.",
                f"media type {media}",
                context={"url": url, "media_type": media},
            )

        return self._from_html(url, page)

    def _from_html(self, url: str, page: str) -> FetchedChart:
        soup = BeautifulSoup(page, "html.parser")
        for unwanted in soup.find_all(["script", "style", "noscript"]):
            unwanted.decompose()

        title = _title_from(page) or _slug(url)
        notes: list[str] = []

        # A <pre> block is a chart that has kept its spacing. Nothing else on a web
        # page has, so when one is there it is the whole answer.
        blocks = [
            element_text(element) for element in soup.find_all("pre") if isinstance(element, Tag)
        ]
        usable = [tidy(block) for block in blocks if looks_like_chart(tidy(block))]
        if usable:
            body = "\n\n".join(usable)
            return self._chart(url, body, ".txt", title, notes=notes)

        notes.append(
            "That page does not lay its chart out as preformatted text, so pcci rebuilt "
            "the lines from the page structure. Check the chord positions before exporting."
        )
        if not looks_like_chart(soup.get_text()):
            raise NoChartFoundError(
                f"pcci could not find a song on {_host(url)}.",
                "page had no preformatted block and too little text",
                context={"url": url},
            )
        # Hand the markup itself to the HTML reader rather than flattening it here:
        # it already knows about headings, <br>, tables and monospaced styling.
        return self._chart(url, page, ".html", title, notes=notes, kind="lyrics")

    def _chart(
        self,
        url: str,
        body: str,
        suffix: str,
        title: str,
        *,
        notes: list[str] | None = None,
        kind: ChartKind | None = None,
    ) -> FetchedChart:
        return FetchedChart(
            text=body if body.endswith("\n") else body + "\n",
            suffix=suffix,
            title=title,
            chart_kind=kind or ("chords" if _has_chord_shape(body) else "lyrics"),
            source=SourceRef(
                provider=self.id, name=_host(url), url=url, supplies=list(self.supplies)
            ),
            notes=notes or [],
        )


def _host(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or url).removeprefix("www.")


def _slug(url: str) -> str:
    """A title from the address, for a page that does not name itself."""
    path = urllib.parse.urlsplit(url).path.rstrip("/")
    tail = path.rsplit("/", 1)[-1] if path else ""
    for ending in _DIRECT_SUFFIXES:
        tail = tail.removesuffix(ending)
    words = urllib.parse.unquote(tail).replace("-", " ").replace("_", " ").strip()
    return words.title() if words else _host(url)


def _title_from(page: str) -> str | None:
    soup = BeautifulSoup(page, "html.parser")
    element = soup.find("meta", attrs={"property": "og:title"})
    if isinstance(element, Tag):
        content = element.get("content")
        if isinstance(content, str) and content.strip():
            return content.strip()
    if soup.title and soup.title.string:
        return str(soup.title.string).strip() or None
    return None


def _has_chord_shape(body: str) -> bool:
    """Whether the text has lines that are chords and nothing else.

    Deliberately crude - it only decides how the result is labelled in the UI. The
    parser does the real work, and it does it on the text either way.
    """
    from pcci.parse.chords import looks_like_chord_line

    return any(looks_like_chord_line(line) for line in body.splitlines() if line.strip())


PAGE = PageSource()
