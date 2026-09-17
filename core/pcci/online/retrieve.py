"""Getting a chart onto disk, from a link or from the clipboard.

Everything downstream of this point is the pipeline that already exists. A fetched
chart is written out as an ordinary file with an honest extension, and then read by
the same ingester that would have read it if the user had saved the page themselves
and dropped it on the window. There is no second conversion path to keep in step with
the first one, and no format the web route supports that the file route does not.

That is also why the clipboard lands here. Text pasted out of a browser and text
pulled from a URL are the same problem - some words, possibly some chords, no file -
and they deserve the same answer.
"""

from __future__ import annotations

import re
from pathlib import Path

from pcci.errors import NoChartFoundError, OutputWriteError
from pcci.logging_setup import get_logger
from pcci.online.cache import Cache, cache_directory
from pcci.online.http import Http, host_of, normalise_url
from pcci.online.models import FetchedChart, SourceRef
from pcci.online.sources import CHART_PROVIDERS, ChartProvider
from pcci.online.text import looks_like_chart, safe_filename, tidy
from pcci.parse.chords import looks_like_chord_line
from pcci.parse.sections import parse_section_label


def imports_directory() -> Path:
    """Where fetched charts are kept.

    Beside the cache, because that is what they are: a copy of something that came from
    somewhere else, safe to delete, and rebuilt by asking again. The presentation the
    user actually wants is written wherever the user says.
    """
    return cache_directory().parent / "imports"


def fetch(
    url: str,
    *,
    http: Http | None = None,
    cache: Cache | None = None,
    providers: tuple[ChartProvider, ...] = CHART_PROVIDERS,
) -> FetchedChart:
    """Read the chart at a URL, using whichever source knows that site."""
    address = normalise_url(url)
    http = http or Http()
    cache = cache or Cache()
    for provider in providers:
        if not provider.owns(address):
            continue
        get_logger().info("fetching a chart from %s via %s", host_of(address), provider.id)
        return provider.fetch(address, http=http, cache=cache)
    raise NoChartFoundError(
        f"pcci does not know how to read anything at {host_of(address)}.",
        "no chart provider claimed the URL",
        context={"url": address},
    )


#: ChordPro announces itself: a directive in braces, or chords in square brackets
#: inside the lyric line rather than on a line of their own.
_CHORDPRO_DIRECTIVE = re.compile(r"^\s*\{\s*[a-z_]+\s*[:}]", re.I | re.M)
_CHORDPRO_INLINE = re.compile(r"\S\[[A-G][#b]?[^\]]{0,10}\]|\[[A-G][#b]?[^\]]{0,10}\]\S")


def looks_like_chordpro(text: str) -> bool:
    return bool(_CHORDPRO_DIRECTIVE.search(text) or _CHORDPRO_INLINE.search(text))


def title_of(text: str, *, fallback: str = "Pasted chart") -> str:
    """The song's name, from the top of a chart somebody pasted.

    The first line of a chart is nearly always its title. It is occasionally a section
    header or a row of chords instead, and neither of those is a name worth putting on
    a presentation, so both are stepped over.
    """
    directive = re.search(r"^\s*\{\s*(?:title|t)\s*:\s*(.+?)\s*\}", text, re.I | re.M)
    if directive:
        return directive.group(1).strip() or fallback

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if parse_section_label(stripped) is not None:
            continue
        if looks_like_chord_line(stripped):
            continue
        return stripped[:80]
    return fallback


def from_text(
    text: str,
    *,
    title: str | None = None,
    source_name: str = "Clipboard",
) -> FetchedChart:
    """Turn pasted text into a chart, working out for itself what kind it is."""
    body = tidy(text)
    if not looks_like_chart(body):
        raise NoChartFoundError(
            "There is not enough text there to be a song. Copy the whole chart - "
            "the title, the section headings and the words - and paste it again.",
            f"{len([line for line in body.splitlines() if line.strip()])} non-blank lines",
        )
    chordpro = looks_like_chordpro(body)
    return FetchedChart(
        text=body + "\n",
        suffix=".cho" if chordpro else ".txt",
        title=title or title_of(body),
        chart_kind="chords"
        if chordpro or any(looks_like_chord_line(line) for line in body.splitlines())
        else "lyrics",
        source=SourceRef(provider="clipboard", name=source_name, supplies=["chords", "lyrics"]),
    )


def materialise(chart: FetchedChart, directory: Path | None = None) -> Path:
    """Write a fetched chart out, and return the path the pipeline should read.

    The name is the song's, not a hash: it becomes the suggested name of the
    presentation, and "Great Are You Lord.pro" is what the user is expecting to save.
    An existing file of the same name is replaced rather than numbered - re-importing
    the same song twice should not leave a trail of copies in a cache folder.
    """
    target = directory or imports_directory()
    name = safe_filename(chart.title) + chart.suffix
    path = target / name
    try:
        target.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(chart.text, encoding="utf-8")
        temporary.replace(path)
    except OSError as error:
        raise OutputWriteError(
            f"pcci could not save the chart it downloaded into {target}.",
            f"{type(error).__name__}: {error}",
            context={"path": str(path)},
        ) from error
    get_logger().info("wrote an imported chart to %s", path.name)
    return path


def import_url(
    url: str,
    directory: Path | None = None,
    *,
    http: Http | None = None,
    cache: Cache | None = None,
) -> tuple[Path, FetchedChart]:
    """Fetch a URL and write it out, ready for ``analyze``."""
    chart = fetch(url, http=http, cache=cache)
    return materialise(chart, directory), chart


def import_text(
    text: str,
    directory: Path | None = None,
    *,
    title: str | None = None,
) -> tuple[Path, FetchedChart]:
    """Take pasted text and write it out, ready for ``analyze``."""
    chart = from_text(text, title=title)
    return materialise(chart, directory), chart
