"""Asking every source at once, and turning the answers into one list.

Three sources answer a search and none of them knows everything. Ultimate Guitar has
the chords and a bare song title; Genius has the words and the artwork; Apple has the
album, the year and the artist's name spelled the way the artist spells it. Shown as
three separate lists that would be a puzzle. Merged on the song they are all about, it
is one row per song that says what is known and where each part came from - which is
what the search box is for.

Nothing here lets one source's bad day become an error. A site that is down, slow or
refusing us contributes a note to the outcome and the search returns whatever the
others found.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from pcci.errors import PcciError
from pcci.logging_setup import get_logger
from pcci.online.cache import Cache
from pcci.online.http import Http, looks_like_url, normalise_url
from pcci.online.models import SearchOutcome, SongMatch, SourceRef, fold
from pcci.online.sources import SEARCH_PROVIDERS, SearchProvider

DEFAULT_LIMIT = 12


def search(
    query: str,
    *,
    limit: int = DEFAULT_LIMIT,
    http: Http | None = None,
    cache: Cache | None = None,
    providers: tuple[SearchProvider, ...] = SEARCH_PROVIDERS,
) -> SearchOutcome:
    """Search every source and return one merged, ranked list."""
    text = query.strip()
    if not text:
        return SearchOutcome(query=query, notes=["Type a song name, or paste a link to one."])

    http = http or Http()
    cache = cache or Cache()

    # A link is not a search, but it arrives through the same box, so it is answered
    # here rather than making every caller check first and leaving the one that forgets
    # with an empty list and no idea why.
    if looks_like_url(text):
        return describe_url(text, http=http, cache=cache)

    notes: list[str] = []
    gathered: list[tuple[SearchProvider, list[SongMatch]]] = []

    # Three independent round trips to three unrelated sites. Run together, a search
    # takes as long as the slowest one rather than all three added up.
    with ThreadPoolExecutor(max_workers=len(providers) or 1) as pool:
        futures = {
            pool.submit(_ask, provider, text, limit, http, cache): provider
            for provider in providers
        }
        for future, provider in futures.items():
            found, note = future.result()
            gathered.append((provider, found))
            if note:
                notes.append(note)

    # Back into the configured order, whichever thread happened to finish first.
    order = {provider.id: index for index, provider in enumerate(providers)}
    gathered.sort(key=lambda pair: order.get(pair[0].id, len(order)))

    results = merge([found for _, found in gathered])
    if not results and not notes:
        notes.append(f"Nothing came back for {text!r}.")
    return SearchOutcome(query=text, is_url=False, results=results[:limit], notes=notes)


def _ask(
    provider: SearchProvider, query: str, limit: int, http: Http, cache: Cache
) -> tuple[list[SongMatch], str | None]:
    """One provider's answer, or a note explaining why there isn't one."""
    try:
        return provider.search(query, limit=limit, http=http, cache=cache), None
    except PcciError as error:
        get_logger().info("%s search unavailable: %s", provider.id, error.technical_detail)
        return [], f"{provider.name}: {error.user_message}"
    except Exception as error:  # a source changing its shape must not break the search
        get_logger().warning("%s search failed: %s: %s", provider.id, type(error).__name__, error)
        return [], f"{provider.name} did not answer in a way pcci understood."


def merge(groups: list[list[SongMatch]]) -> list[SongMatch]:
    """Fold every source's results into one row per song.

    Three rules, loosening as they go, because no two sites file a song the same way:

    1. Same folded title *and* artist - the easy case.
    2. Same folded title. Ultimate Guitar files a song under whoever posted it and
       Apple under the label's spelling of the band, and those disagree constantly.
    3. Same artist, and one title is the other with a subtitle on the end. "Come Thou
       Fount" and "Come Thou Fount of Every Blessing" are one song; another band's
       "Come Thou Fount" is not, which is why this rule insists the artists match.
    """
    merged: list[SongMatch] = []
    by_pair: dict[str, int] = {}
    by_title: dict[str, int] = {}

    for group in groups:
        for match in group:
            pair = match.merge_key()
            title = fold(match.title)
            index = by_pair.get(pair)
            if index is None and title:
                index = by_title.get(title)
            if index is None:
                index = _same_song_shortened(merged, match)
            if index is None:
                merged.append(match.model_copy(deep=True))
                position = len(merged) - 1
                by_pair[pair] = position
                if title:
                    by_title.setdefault(title, position)
                continue
            merged[index] = _combine(merged[index], match)
            by_pair.setdefault(pair, index)

    merged.sort(key=_rank, reverse=True)
    return merged


#: Who to believe about the cover art. Apple serves the album's own artwork at any
#: size we ask for; everyone else serves whatever they happened to store.
ARTWORK_RANK = {"itunes": 2, "genius": 1}


def _combine(existing: SongMatch, extra: SongMatch) -> SongMatch:
    """Fill the gaps in a row from another source's version of the same song.

    The first source to know something keeps it, with two exceptions worth the extra
    lines: a chart with chords beats one with only lyrics, and a better cover beats an
    earlier one - whichever order the answers happened to come back in.
    """
    combined = existing.model_copy(deep=True)
    for field in (
        "artist",
        "album",
        "year",
        "key",
        "ccli_number",
        "copyright",
        "rating",
        "votes",
    ):
        if getattr(combined, field) is None:
            setattr(combined, field, getattr(extra, field))

    if _chart_rank(extra.chart_kind) > _chart_rank(combined.chart_kind):
        combined.chart_url = extra.chart_url
        combined.chart_kind = extra.chart_kind

    if extra.artwork_url or extra.artwork_thumb_url:
        mine = (
            ARTWORK_RANK.get(combined.artwork_provider or "", 0)
            if combined.artwork_provider
            else -1
        )
        theirs = ARTWORK_RANK.get(extra.artwork_provider or "", 0)
        if theirs > mine:
            combined.artwork_url = extra.artwork_url
            combined.artwork_thumb_url = extra.artwork_thumb_url
            combined.artwork_provider = extra.artwork_provider

    # One entry per site, not one per listing. A popular song has half a dozen
    # user-submitted charts and as many Apple releases, and all of them fold into this
    # row - which read as "via Ultimate Guitar, Ultimate Guitar, Ultimate Guitar,
    # Apple Music, Apple Music" in the app until this deduplicated them.
    known = {source.provider for source in combined.sources}
    for source in extra.sources:
        if source.provider not in known:
            combined.sources.append(SourceRef(**source.model_dump()))
            known.add(source.provider)
    return combined


def _same_song_shortened(merged: list[SongMatch], match: SongMatch) -> int | None:
    """A row for the same song under a shorter or longer form of its title.

    Only ever within one artist. Across artists this would happily merge two unrelated
    songs that share an opening word, which is exactly the failure worth avoiding.
    """
    artist = fold(match.artist or "")
    title = fold(match.title)
    if not artist or not title:
        return None
    for index, existing in enumerate(merged):
        if fold(existing.artist or "") != artist:
            continue
        other = fold(existing.title)
        if not other:
            continue
        if title.startswith(other + " ") or other.startswith(title + " "):
            return index
    return None


def _chart_rank(kind: str) -> int:
    return {"chords": 3, "tab": 2, "lyrics": 1}.get(kind, 0)


def _rank(match: SongMatch) -> tuple[int, int, float]:
    """Importable first, then better words, then whatever its own site thinks of it."""
    return (
        1 if match.importable else 0,
        _chart_rank(match.chart_kind),
        (match.rating or 0.0) + (1.0 if match.artwork_thumb_url else 0.0),
    )


def describe_url(
    url: str,
    *,
    http: Http | None = None,
    cache: Cache | None = None,
) -> SearchOutcome:
    """Turn a pasted link into a single result row, with artwork if it can be found.

    The page is fetched once, here, and left in the cache, so importing the row the
    user then clicks costs nothing more.
    """
    from pcci.online.retrieve import fetch

    address = normalise_url(url)
    http = http or Http()
    cache = cache or Cache()
    chart = fetch(address, http=http, cache=cache)

    match = SongMatch(
        ref=chart.source.url or address,
        title=chart.title,
        artist=chart.artist,
        chart_url=address,
        chart_kind=chart.chart_kind,
        sources=[chart.source],
    )
    notes = list(chart.notes)

    # The page has the words; Apple has the cover. Ask for it, and shrug if it is not
    # there - the import works perfectly well without a picture.
    enriched = _enrich(match, http=http, cache=cache)
    return SearchOutcome(query=address, is_url=True, results=[enriched], notes=notes)


def _enrich(match: SongMatch, *, http: Http, cache: Cache) -> SongMatch:
    from pcci.online.sources import ITUNES

    query = " ".join(part for part in (match.title, match.artist) if part)
    if not query.strip():
        return match
    try:
        candidates = ITUNES.search(query, limit=5, http=http, cache=cache)
    except Exception as error:
        get_logger().debug("artwork lookup skipped: %s: %s", type(error).__name__, error)
        return match

    wanted = fold(match.title)
    for candidate in candidates:
        if fold(candidate.title) == wanted:
            return _combine(match, candidate)
    return match
