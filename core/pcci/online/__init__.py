"""Songs from the internet.

Two doors, both of which end at an ordinary file on disk that the existing pipeline
reads:

``search(query)``
    A song name in, a merged list of results out - artwork, credits, and the sites
    each part came from.

``fetch(url)`` / ``from_text(text)``
    A link or a clipboard's worth of text in, a chart out.

Nothing in here talks to ProPresenter, and nothing outside it talks to the network.
"""

from __future__ import annotations

from pcci.online.cache import Cache, cache_directory
from pcci.online.http import Http, looks_like_url, normalise_url
from pcci.online.models import FetchedChart, SearchOutcome, SongMatch, SourceRef
from pcci.online.retrieve import (
    fetch,
    from_text,
    import_text,
    import_url,
    imports_directory,
    materialise,
    title_of,
)
from pcci.online.search import describe_url, search
from pcci.online.sources import CHART_PROVIDERS, SEARCH_PROVIDERS

__all__ = [
    "CHART_PROVIDERS",
    "SEARCH_PROVIDERS",
    "Cache",
    "FetchedChart",
    "Http",
    "SearchOutcome",
    "SongMatch",
    "SourceRef",
    "cache_directory",
    "describe_url",
    "fetch",
    "from_text",
    "import_text",
    "import_url",
    "imports_directory",
    "looks_like_url",
    "materialise",
    "normalise_url",
    "search",
    "title_of",
]
