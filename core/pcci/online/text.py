"""Turning what a website sends back into the plain text the parsers already read.

The engine's whole pipeline is built around columns: a chord sits above the syllable
it is played on, and the number of spaces in front of it is the only thing saying so.
So the job here is never "extract the words" - it is "recover the monospaced chart the
page is displaying", spaces and all, and hand it to the same ingesters a dropped file
goes through.
"""

from __future__ import annotations

import html as html_module
import json
import re
from typing import Any

from bs4 import BeautifulSoup, Tag

#: Ultimate Guitar wraps chords in [ch]...[/ch] and chart blocks in [tab]...[/tab].
#: Both are markers around text that is already correctly spaced, so removing them
#: leaves every column exactly where the chart had it.
_UG_CHORD_RE = re.compile(r"\[/?ch\]")
_UG_TAB_RE = re.compile(r"\[/?tab\]")
_UG_SYNTAX_RE = re.compile(r"\[/?(?:syntaxerror|chord)\]", re.I)


def strip_ultimate_guitar_markup(content: str) -> str:
    """UG's stored chart text, as the site itself renders it.

    Only the markers go. Nothing is re-indented, re-wrapped or tidied: the spacing in
    ``[ch]C[/ch]      [ch]G[/ch]`` is the chart's own, and it has to survive.
    """
    text = content.replace("\r\n", "\n").replace("\r", "\n")
    text = _UG_TAB_RE.sub("", text)
    text = _UG_CHORD_RE.sub("", text)
    text = _UG_SYNTAX_RE.sub("", text)
    return html_module.unescape(text)


def _classes(element: Tag) -> list[str]:
    """An element's class list, however BeautifulSoup happens to be handing it over."""
    value: Any = element.get("class")
    if isinstance(value, str):
        return value.split()
    if isinstance(value, list):
        return [str(entry) for entry in value]
    return []


def js_store(page: str) -> dict[str, Any] | None:
    """The JSON blob Ultimate Guitar hides its page data in.

    The site renders from ``<div class="js-store" data-content="{...}">``. Reading that
    is far steadier than scraping the rendered markup, which is generated and changes
    with every deploy - but it is still somebody else's private shape, so every caller
    treats a miss as "no results", never as an error.
    """
    soup = BeautifulSoup(page, "html.parser")
    for element in soup.find_all(True, attrs={"data-content": True}):
        if "js-store" not in _classes(element):
            continue
        raw = element.get("data-content")
        if not isinstance(raw, str):
            continue
        try:
            parsed = json.loads(raw)
        except ValueError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def dig(payload: Any, *path: str) -> Any:
    """``payload["store"]["page"]["data"]`` without four separate guards."""
    current = payload
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def find_first(payload: Any, predicate: Any, *, limit: int = 2000) -> Any:
    """Walk a JSON structure for the first node a predicate likes.

    Undocumented APIs move their payload around between deploys. Looking for the shape
    rather than the path survives that, and costs a few microseconds on a document that
    is already in memory.
    """
    stack: list[Any] = [payload]
    seen = 0
    while stack and seen < limit:
        node = stack.pop()
        seen += 1
        if predicate(node):
            return node
        if isinstance(node, dict):
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return None


def find_all(payload: Any, predicate: Any, *, limit: int = 5000) -> list[Any]:
    """Every node a predicate likes, in the order they were reached."""
    found: list[Any] = []
    stack: list[Any] = [payload]
    seen = 0
    while stack and seen < limit:
        node = stack.pop(0)
        seen += 1
        if predicate(node):
            found.append(node)
            continue
        if isinstance(node, dict):
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return found


def element_text(element: Tag) -> str:
    """An element's text with ``<br>`` honoured as a line break."""
    for br in element.find_all("br"):
        br.replace_with("\n")
    return element.get_text()


def blocks_text(page: str, *, attribute: str, value: str = "true") -> list[str]:
    """Text of every element carrying an attribute, one string per element."""
    soup = BeautifulSoup(page, "html.parser")
    found: list[str] = []
    for element in soup.find_all(True, attrs={attribute: value}):
        found.append(element_text(element))
    return found


def tidy(text: str) -> str:
    """Normalise line endings, drop trailing spaces, collapse runs of blank lines.

    Leading spaces are never touched: on a chord chart they are the alignment.
    """
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    out: list[str] = []
    blanks = 0
    for line in lines:
        if line.strip():
            blanks = 0
            out.append(line)
            continue
        blanks += 1
        if blanks <= 1:
            out.append("")
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def looks_like_chart(text: str) -> bool:
    """Whether some text plausibly holds a song rather than a cookie banner."""
    lines = [line for line in text.splitlines() if line.strip()]
    return len(lines) >= 4


_SAFE_NAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def safe_filename(name: str, *, fallback: str = "chart") -> str:
    """A file name every platform will accept, from a song title off the web."""
    cleaned = _SAFE_NAME_RE.sub(" ", name).replace("\n", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    # Windows refuses these whatever the extension.
    reserved = {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{digit}" for digit in range(1, 10)),
        *(f"lpt{digit}" for digit in range(1, 10)),
    }
    if not cleaned or cleaned.casefold() in reserved:
        return fallback
    return cleaned[:80].strip(" .") or fallback
