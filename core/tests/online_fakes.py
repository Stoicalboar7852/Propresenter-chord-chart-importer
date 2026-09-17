"""A web that does not exist, so the online sources can be tested like anything else.

The machines this was developed on cannot reach Apple, Ultimate Guitar or Genius: the
network policy refuses them outright. Rather than leave the whole feature only
testable by hand on somebody's laptop, every request goes through ``Transport`` and
these fakes stand in for the real thing - which also means the tests keep passing on a
train, and a site having a bad day never turns into a red build.

What the fakes serve is recorded shape, not invented shape: the JSON under
``tests/fixtures/online`` is laid out the way each service really lays it out, down to
Ultimate Guitar hiding its page data in an HTML attribute.
"""

from __future__ import annotations

import html
import json
import urllib.error
import urllib.request
from pathlib import Path

from pcci.online.http import Http, Response

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "online"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def js_store_page(store_fixture: str, *, title: str = "Ultimate Guitar") -> str:
    """Wrap a page-store JSON fixture the way the site itself does.

    The escaping is the point: the JSON lives in an HTML attribute, so every quote in
    it arrives as ``&quot;``. A parser that forgets to unescape works perfectly against
    a hand-written fixture and not at all against the real page.
    """
    escaped = html.escape(store_fixture, quote=True)
    return (
        "<!doctype html><html><head><title>"
        + title
        + '</title></head><body><div class="js-store" data-content="'
        + escaped
        + '"></div></body></html>'
    )


def public_resolver(host: str, port: int) -> list[str]:
    """Every host is a public one. Keeps the tests off the DNS server."""
    del host, port
    return ["93.184.216.34"]


class FakeTransport:
    """Answers from a table of URL fragments. Anything unlisted is a 404."""

    def __init__(self, routes: dict[str, tuple[str, str]] | None = None) -> None:
        #: fragment -> (media type, body)
        self.routes: dict[str, tuple[str, str]] = dict(routes or {})
        self.errors: dict[str, Exception] = {}
        self.calls: list[str] = []

    def route(self, fragment: str, body: str, media: str = "text/html; charset=utf-8") -> None:
        self.routes[fragment] = (media, body)

    def fail(self, fragment: str, error: Exception) -> None:
        self.errors[fragment] = error

    def open(self, request: urllib.request.Request, timeout: float, max_bytes: int) -> Response:
        del timeout, max_bytes
        url = request.full_url
        self.calls.append(url)
        for fragment, error in self.errors.items():
            if fragment in url:
                raise error
        for fragment, (media, body) in self.routes.items():
            if fragment in url:
                return Response(url=url, status=200, content_type=media, body=body.encode("utf-8"))
        raise urllib.error.HTTPError(url, 404, "Not Found", hdrs=None, fp=None)  # type: ignore[arg-type]


def everything_answers() -> FakeTransport:
    """A transport where all three sources are up and have the song."""
    transport = FakeTransport()
    transport.route("itunes.apple.com/search", fixture("itunes-search.json"), "application/json")
    transport.route(
        "ultimate-guitar.com/search.php", js_store_page(fixture("ug-search-store.json"))
    )
    transport.route("amazing-grace-chords-1234567", js_store_page(fixture("ug-tab-store.json")))
    transport.route("genius.com/api/search/song", fixture("genius-search.json"), "application/json")
    transport.route("genius.com/Parish-hymnal-choir", fixture("genius-song.html"))
    return transport


def http_with(transport: FakeTransport) -> Http:
    return Http(transport=transport, resolve=public_resolver)


def store_of(payload: dict[str, object]) -> str:
    return js_store_page(json.dumps(payload))
