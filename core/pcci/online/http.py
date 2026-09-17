"""Fetching things from the web, carefully.

Everything the engine pulls off the internet comes through here, for three reasons.

**One place to be careful in.** A pasted link is user input like any other, so the
scheme is checked, the host is resolved and refused if it points anywhere inside the
machine or the local network, redirects are re-checked rather than trusted, and the
body is capped. A worship volunteer pasting a URL cannot talk this into reading
``file:///etc/passwd`` or poking at a router.

**One place to swap out.** ``Transport`` is the seam the tests replace, so every
provider can be exercised against recorded responses with no network at all. That
matters more than usual here: the machines this was developed on cannot reach the
music services, and a feature that can only be tested by hand is a feature that
quietly rots.

**One place that never logs content.** Host, status and byte count go to the log.
What came back does not.
"""

from __future__ import annotations

import ipaddress
import json
import socket
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

from charset_normalizer import from_bytes

from pcci import __version__
from pcci.errors import NetworkError
from pcci.logging_setup import get_logger

#: Honest about what we are, familiar enough in shape that ordinary sites answer it.
USER_AGENT = (
    f"Mozilla/5.0 (compatible; pcci/{__version__}; "
    "+https://github.com/Stoicalboar7852/Propresenter-chord-chart-importer)"
)

#: A chord chart is a few kilobytes; a song page with every advert is a few hundred.
#: Four megabytes is far past either and well short of anything that would hurt.
MAX_BYTES = 4 * 1024 * 1024
TIMEOUT_SECONDS = 20.0
MAX_REDIRECTS = 5


@dataclass(frozen=True)
class Response:
    """What came back. ``body`` is bytes; decoding is deliberate and separate."""

    url: str
    status: int
    content_type: str
    body: bytes

    @property
    def media_type(self) -> str:
        """``text/html``, without the charset or any other parameter."""
        return self.content_type.split(";")[0].strip().lower()

    @property
    def charset(self) -> str | None:
        for parameter in self.content_type.split(";")[1:]:
            name, _, value = parameter.partition("=")
            if name.strip().lower() == "charset":
                return value.strip().strip('"') or None
        return None

    def text(self) -> str:
        """Decode the body, believing the header and guessing when it is absent."""
        return decode(self.body, self.charset)

    def json(self) -> Any:
        try:
            return json.loads(self.text())
        except ValueError as error:
            raise NetworkError(
                f"{host_of(self.url)} sent back something that was not the data pcci expected.",
                f"{type(error).__name__}: {error}",
                context={"url": self.url, "media_type": self.media_type},
            ) from error


def decode(body: bytes, charset: str | None = None) -> str:
    """Bytes to text: the declared encoding, then UTF-8, then a guess."""
    if charset:
        try:
            return body.decode(charset)
        except (LookupError, UnicodeDecodeError):
            pass
    try:
        return body.decode("utf-8")
    except UnicodeDecodeError:
        pass
    best = from_bytes(body).best()
    return str(best) if best is not None else body.decode("utf-8", errors="replace")


def host_of(url: str) -> str:
    """The hostname, for a message a human reads. Never the whole URL with its query."""
    try:
        return urllib.parse.urlsplit(url).hostname or url
    except ValueError:
        return url


def looks_like_url(text: str) -> bool:
    """True for something the user clearly pasted out of a browser."""
    candidate = text.strip()
    if " " in candidate or "\n" in candidate:
        return False
    if candidate.lower().startswith(("http://", "https://")):
        return True
    # "ultimate-guitar.com/tab/..." without the scheme is still obviously a link.
    head = candidate.split("/", 1)[0]
    return "." in head and not head.endswith(".") and "@" not in candidate


def normalise_url(text: str) -> str:
    """Add the scheme a pasted link is usually missing."""
    candidate = text.strip()
    if not candidate.lower().startswith(("http://", "https://")):
        candidate = "https://" + candidate
    return candidate


#: How a hostname becomes addresses. A parameter rather than a call so the tests can
#: exercise the guard without a working DNS server, and without being at the mercy of
#: what some real name happens to resolve to today.
Resolver = Callable[[str, int], list[str]]


def resolve_addresses(host: str, port: int) -> list[str]:
    """Every address a hostname answers to."""
    return [str(entry[4][0]) for entry in socket.getaddrinfo(host, port)]


def check_url(url: str, *, resolve: Resolver = resolve_addresses) -> None:
    """Refuse anything that is not a public http(s) address.

    The DNS answer is checked rather than the spelling, because ``localtest.me`` and a
    thousand names like it resolve to 127.0.0.1. This is not proof against a name that
    answers differently the second time it is asked - defeating that needs the socket
    itself - but it stops every pasted link that would otherwise reach inside the
    machine or the network it sits on.
    """
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError as error:
        raise NetworkError(
            "That does not look like a web address.",
            f"{type(error).__name__}: {error}",
            context={"url": url},
        ) from error

    if parts.scheme not in ("http", "https"):
        raise NetworkError(
            "pcci can only open http and https links.",
            f"scheme was {parts.scheme!r}",
            context={"url": url},
        )
    host = parts.hostname
    if not host:
        raise NetworkError(
            "That link has no website in it.",
            "no host in URL",
            context={"url": url},
        )

    try:
        resolved = resolve(host, parts.port or (443 if parts.scheme == "https" else 80))
    except OSError as error:
        raise NetworkError(
            f"pcci could not find {host}. Check the address, and that you are online.",
            f"{type(error).__name__}: {error}",
            context={"host": host},
        ) from error

    for entry in resolved:
        address = ipaddress.ip_address(entry)
        if not address.is_global or address.is_multicast:
            raise NetworkError(
                f"{host} points inside this network, so pcci will not open it.",
                f"resolved to {address}",
                context={"host": host},
            )


class Transport(Protocol):
    """The one call that actually touches a socket. Tests replace this."""

    def open(self, request: urllib.request.Request, timeout: float, max_bytes: int) -> Response: ...


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-check every hop. An open redirect is somebody else's bug, not our excuse."""

    max_redirections = MAX_REDIRECTS

    def __init__(self, resolve: Resolver = resolve_addresses) -> None:
        self._resolve = resolve

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        check_url(newurl, resolve=self._resolve)
        return super().redirect_request(req, fp, code, msg, newurl=newurl, headers=headers)


@dataclass
class UrllibTransport:
    """The real one: the standard library, with the guards wired in."""

    resolve: Resolver = resolve_addresses

    def open(self, request: urllib.request.Request, timeout: float, max_bytes: int) -> Response:
        opener = urllib.request.build_opener(_GuardedRedirectHandler(self.resolve))
        with opener.open(request, timeout=timeout) as stream:
            body = stream.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise NetworkError(
                    f"The page at {host_of(request.full_url)} is far too big to be a chord chart.",
                    f"stopped reading after {max_bytes} bytes",
                    context={"url": request.full_url},
                )
            return Response(
                url=stream.geturl(),
                status=getattr(stream, "status", 200) or 200,
                content_type=stream.headers.get("Content-Type", ""),
                body=body,
            )


@dataclass
class Http:
    """A small client with the project's manners baked in."""

    transport: Transport = field(default_factory=UrllibTransport)
    timeout: float = TIMEOUT_SECONDS
    max_bytes: int = MAX_BYTES
    user_agent: str = USER_AGENT
    resolve: Resolver = resolve_addresses

    def get(
        self,
        url: str,
        *,
        accept: str = "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        headers: dict[str, str] | None = None,
    ) -> Response:
        """GET a URL, or raise ``NetworkError`` saying what a human should do about it."""
        check_url(url, resolve=self.resolve)
        request = urllib.request.Request(url, method="GET")
        request.add_header("User-Agent", self.user_agent)
        request.add_header("Accept", accept)
        request.add_header("Accept-Language", "en")
        for name, value in (headers or {}).items():
            request.add_header(name, value)

        logger = get_logger()
        host = host_of(url)
        try:
            response = self.transport.open(request, self.timeout, self.max_bytes)
        except urllib.error.HTTPError as error:
            raise _http_error(url, error) from error
        except urllib.error.URLError as error:
            raise NetworkError(
                f"pcci could not reach {host}. Check that you are online.",
                f"{type(error).__name__}: {error.reason}",
                context={"host": host},
            ) from error
        except TimeoutError as error:
            raise NetworkError(
                f"{host} took too long to answer.",
                f"timed out after {self.timeout:g}s",
                context={"host": host},
            ) from error
        except OSError as error:
            raise NetworkError(
                f"pcci could not reach {host}.",
                f"{type(error).__name__}: {error}",
                context={"host": host},
            ) from error

        # Host, status, size. Never what came back.
        logger.debug("GET %s -> %d, %d bytes", host, response.status, len(response.body))
        return response

    def get_json(self, url: str, *, headers: dict[str, str] | None = None) -> Any:
        return self.get(url, accept="application/json", headers=headers).json()


def _http_error(url: str, error: urllib.error.HTTPError) -> NetworkError:
    """Turn a status code into something worth reading."""
    host = host_of(url)
    if error.code in (401, 403):
        message = (
            f"{host} would not let pcci read that page. Some sites only answer a real "
            "browser - open it yourself, copy the chart, and use Import from Clipboard."
        )
    elif error.code == 404:
        message = f"There is nothing at that address on {host} any more."
    elif error.code == 429:
        message = f"{host} is asking pcci to slow down. Wait a minute and try again."
    elif 500 <= error.code < 600:
        message = f"{host} is having trouble at its end. Try again shortly."
    else:
        message = f"{host} refused the request."
    return NetworkError(
        message,
        f"HTTP {error.code} {error.reason}",
        context={"host": host, "status": error.code},
    )
