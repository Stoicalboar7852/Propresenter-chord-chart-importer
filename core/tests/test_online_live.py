"""The same sources, against the real internet.

Everything in ``test_online.py`` runs against recorded shapes, which proves the parsing
and proves nothing at all about whether those shapes are still what the sites send.
Two of the three sources here have no public API and no promise to anybody: the day
Ultimate Guitar moves its page data or Genius renames an attribute, the offline tests
stay green and the feature stops working.

So these run for real, and they assert *shape* rather than content - that a search for
a famous public-domain hymn comes back with something, that the something has the
fields the code reads, that a chart fetched from it parses. Content assertions would
fail every time somebody edits a chart, which is not news.

A site that refuses us outright is a skip, not a failure. Genius answers 403 to a
GitHub runner - it will only talk to something that looks like a browser, and a
datacentre address does not - and Ultimate Guitar could start doing the same tomorrow.
That is the state of the world rather than a defect, it is already handled at runtime
by pointing the user at the clipboard, and a weekly job that goes red for it teaches
everyone to ignore the weekly job. A site that answers but has *changed shape* is the
thing worth a red mark, and that still fails.

They are skipped entirely unless ``PCCI_LIVE_ONLINE=1``. The development sandbox cannot
reach these hosts at all, and a test that fails because a website is having a bad
afternoon has no business blocking a merge - so CI runs them on their own schedule.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest

from pcci.errors import NetworkError
from pcci.online import Cache, Http, search
from pcci.online.retrieve import fetch, materialise
from pcci.online.sources import GENIUS, ITUNES, ULTIMATE_GUITAR
from pcci.parse.pipeline import analyze

#: Status codes that mean "not to you", as opposed to "not any more".
REFUSALS = {401, 403, 429}


@contextmanager
def refusal_is_not_a_failure(site: str) -> Iterator[None]:
    """Turn "this site will not talk to a robot" into a skip that says so."""
    try:
        yield
    except NetworkError as error:
        if error.context.get("status") in REFUSALS:
            pytest.skip(
                f"{site} refused this client ({error.technical_detail}). "
                "Expected from a datacentre address; the clipboard is the way in."
            )
        raise


pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        os.environ.get("PCCI_LIVE_ONLINE") != "1",
        reason="set PCCI_LIVE_ONLINE=1 to run the tests that use the network",
    ),
]

QUERY = "amazing grace"


@pytest.fixture
def http() -> Http:
    return Http()


@pytest.fixture
def cache(tmp_path: Path) -> Cache:
    # A fresh cache per test: the point of these is to actually make the request.
    return Cache(directory=tmp_path / "cache")


def test_apple_music_answers(http: Http, cache: Cache) -> None:
    with refusal_is_not_a_failure("Apple Music"):
        results = ITUNES.search(QUERY, limit=5, http=http, cache=cache)

    assert results, "the iTunes Search API returned nothing"
    assert all(match.title for match in results)
    assert any(match.artwork_url for match in results), "no result carried cover art"


def test_ultimate_guitar_still_keeps_its_page_data_where_we_look(http: Http, cache: Cache) -> None:
    """The canary. If this fails, the site has moved its store and search has no chords."""
    with refusal_is_not_a_failure("Ultimate Guitar"):
        results = ULTIMATE_GUITAR.search(QUERY, limit=5, http=http, cache=cache)

    assert results, "no chord listings came back - has the page store moved?"
    assert all(match.chart_url for match in results)
    assert all(match.chart_kind in ("chords", "tab") for match in results)


def test_a_real_chart_downloads_and_parses(http: Http, cache: Cache, tmp_path: Path) -> None:
    with refusal_is_not_a_failure("Ultimate Guitar"):
        results = ULTIMATE_GUITAR.search(QUERY, limit=5, http=http, cache=cache)
    if not results:
        pytest.skip("no listing to fetch; the search test above covers that")

    with refusal_is_not_a_failure("Ultimate Guitar"):
        chart = fetch(results[0].chart_url or "", http=http, cache=cache)

    assert "[ch]" not in chart.text, "markup reached the chart text"
    song = analyze(materialise(chart, tmp_path))
    assert song.sections, "the downloaded chart parsed into no sections"


def test_genius_still_labels_its_lyrics_container(http: Http, cache: Cache) -> None:
    with refusal_is_not_a_failure("Genius"):
        results = GENIUS.search(QUERY, limit=5, http=http, cache=cache)
    if not results:
        pytest.skip("Genius returned no results")

    with refusal_is_not_a_failure("Genius"):
        chart = GENIUS.fetch(results[0].chart_url or "", http=http, cache=cache)
    assert len(chart.text.splitlines()) > 4


def test_a_whole_search_comes_back_merged(http: Http, cache: Cache) -> None:
    outcome = search(QUERY, limit=8, http=http, cache=cache)

    # Every source refusing at once is worth a red mark: the feature is dead.
    assert outcome.results, f"nothing at all came back: {outcome.notes}"
    # Any one of them being unavailable is not, so this is a skip rather than a failure.
    if not any(match.importable for match in outcome.results):
        pytest.skip(f"no source supplied words today: {outcome.notes}")
