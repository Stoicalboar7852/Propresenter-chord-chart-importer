"""Songs fetched from the web.

Every test here runs against ``tests/online_fakes``, never the internet: the shapes
are recorded, the transport is injected, and the DNS guard is handed a resolver that
answers. What is being checked is the part that can actually be wrong - reading
somebody else's undocumented payload, keeping a chart's column alignment intact
through three transformations, and degrading sensibly when a site says no.
"""

from __future__ import annotations

import urllib.error
from pathlib import Path

import pytest

from pcci.errors import NetworkError, NoChartFoundError
from pcci.online import retrieve
from pcci.online.cache import Cache
from pcci.online.http import check_url, looks_like_url, normalise_url
from pcci.online.models import fold
from pcci.online.search import merge, search
from pcci.online.sources import GENIUS, ITUNES, PAGE, ULTIMATE_GUITAR
from pcci.online.text import safe_filename, strip_ultimate_guitar_markup
from pcci.parse.pipeline import analyze
from tests.online_fakes import (
    FakeTransport,
    everything_answers,
    fixture,
    http_with,
    js_store_page,
    public_resolver,
)

GRACE_TAB = "https://tabs.ultimate-guitar.com/tab/parish-hymnal-choir/amazing-grace-chords-1234567"


@pytest.fixture
def cache(tmp_path: Path) -> Cache:
    return Cache(directory=tmp_path / "cache")


# --- The guard on a pasted link ---------------------------------------------------


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://example.com/song.txt",
        "javascript:alert(1)",
        "https://",
    ],
)
def test_only_http_links_are_opened(url: str) -> None:
    with pytest.raises(NetworkError):
        check_url(url, resolve=public_resolver)


@pytest.mark.parametrize(
    "address",
    ["127.0.0.1", "10.0.0.5", "192.168.1.1", "169.254.169.254", "::1"],
)
def test_links_pointing_inside_the_network_are_refused(address: str) -> None:
    """A name that resolves inward is refused whatever it is spelled like."""
    with pytest.raises(NetworkError, match="inside this network"):
        check_url("https://songs.example.com/chart", resolve=lambda host, port: [address])


def test_a_public_address_is_allowed() -> None:
    check_url("https://tabs.ultimate-guitar.com/tab/x", resolve=public_resolver)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("https://genius.com/x-lyrics", True),
        ("tabs.ultimate-guitar.com/tab/x", True),
        ("amazing grace hymn", False),
        ("Amazing Grace", False),
        ("worship@example.com", False),
    ],
)
def test_a_search_box_can_tell_a_link_from_a_song_name(text: str, expected: bool) -> None:
    assert looks_like_url(text) is expected


def test_a_pasted_link_gets_the_scheme_it_is_missing() -> None:
    assert (
        normalise_url("tabs.ultimate-guitar.com/tab/x") == "https://tabs.ultimate-guitar.com/tab/x"
    )
    assert normalise_url(" https://genius.com/x ") == "https://genius.com/x"


# --- Apple Music: the artwork and the credits -------------------------------------


def test_itunes_search_reads_artwork_and_credits(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route("itunes.apple.com/search", fixture("itunes-search.json"), "application/json")

    results = ITUNES.search("amazing grace", limit=5, http=http_with(transport), cache=cache)

    first = results[0]
    assert first.title == "Amazing Grace"
    assert first.artist == "Parish Hymnal Choir"
    assert first.album == "Hymns, Volume One"
    assert first.year == 2019
    # Apple serves any size by rewriting the filename, so a results list is not stuck
    # with the 100px thumbnail the API hands back.
    assert first.artwork_thumb_url is not None and "200x200bb" in first.artwork_thumb_url
    assert first.artwork_url is not None and "600x600bb" in first.artwork_url
    # It has no words, and says so rather than looking importable.
    assert first.chart_kind == "none"
    assert first.importable is False
    assert first.source_names == ["Apple Music"]


# --- Ultimate Guitar: the chords --------------------------------------------------


def test_ultimate_guitar_search_keeps_only_listings_with_words(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route(
        "ultimate-guitar.com/search.php", js_store_page(fixture("ug-search-store.json"))
    )

    results = ULTIMATE_GUITAR.search(
        "amazing grace", limit=10, http=http_with(transport), cache=cache
    )

    urls = [match.chart_url for match in results]
    # Official needs an account and Tab is notation with no lyrics under it.
    assert not any(url and "official" in url for url in urls)
    assert not any(url and "tabs-555" in url for url in urls)
    assert all(match.chart_kind == "chords" for match in results)


def test_the_best_rated_version_wins_rather_than_one_row_per_version(cache: Cache) -> None:
    """Twelve user submissions of one song is one row, not twelve."""
    transport = FakeTransport()
    transport.route(
        "ultimate-guitar.com/search.php", js_store_page(fixture("ug-search-store.json"))
    )

    results = ULTIMATE_GUITAR.search(
        "amazing grace", limit=10, http=http_with(transport), cache=cache
    )

    grace = [match for match in results if "Amazing Grace" in match.title]
    assert len(grace) == 1
    # 4.82 with 912 votes beats a bare 5.0 with four.
    assert grace[0].chart_url == GRACE_TAB
    assert grace[0].key == "D"


def test_ultimate_guitar_markup_comes_off_without_moving_a_column() -> None:
    """The spacing in a UG chart is the chart. Stripping tags must not disturb it."""
    stripped = strip_ultimate_guitar_markup("[tab][ch]D[/ch]           [ch]A[/ch]\r\nAmazing grace")
    assert stripped == "D           A\nAmazing grace"
    assert stripped.index("A") == 12


def test_fetching_a_tab_page_returns_the_chart_and_its_credits(cache: Cache) -> None:
    transport = everything_answers()
    chart = ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http_with(transport), cache=cache)

    assert chart.title == "Amazing Grace"
    assert chart.artist == "Parish Hymnal Choir"
    assert chart.has_chords
    assert chart.suffix == ".txt"
    assert "Key: D" in chart.text
    assert "Capo: 2" in chart.text
    assert "[ch]" not in chart.text
    assert "[Verse 1]" in chart.text


def test_a_page_with_no_readable_chart_says_so(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route("amazing-grace-chords-1234567", "<html><body>Buy Pro!</body></html>")

    with pytest.raises(NoChartFoundError, match="Chords"):
        ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http_with(transport), cache=cache)


# --- Genius: the words, when there are no chords ----------------------------------


def test_genius_search_finds_songs_with_their_artwork(cache: Cache) -> None:
    transport = everything_answers()
    results = GENIUS.search("amazing grace", limit=5, http=http_with(transport), cache=cache)

    assert results[0].title == "Amazing Grace"
    assert results[0].artist == "Parish Hymnal Choir"
    assert results[0].year == 2019
    assert results[0].artwork_thumb_url == "https://images.genius.com/small.jpg"
    assert results[0].chart_kind == "lyrics"
    assert results[0].importable is True


def test_genius_lyrics_arrive_with_their_section_headers(cache: Cache) -> None:
    transport = everything_answers()
    chart = GENIUS.fetch(
        "https://genius.com/Parish-hymnal-choir-blessed-assurance-lyrics",
        http=http_with(transport),
        cache=cache,
    )

    assert chart.chart_kind == "lyrics"
    assert chart.has_chords is False
    assert "[Verse 1]" in chart.text
    assert "[Chorus]" in chart.text
    assert "Blessed assurance, Jesus is mine" in chart.text
    # <br> is a line break, not a space.
    assert "mine\nOh what a foretaste" in chart.text
    assert chart.notes and "lyrics only" in chart.notes[0]


# --- Any other link ---------------------------------------------------------------


def test_a_preformatted_block_is_taken_exactly_as_it_is(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route("example.church", fixture("church-page.html"))

    chart = PAGE.fetch(
        "https://example.church/charts/holy-holy-holy", http=http_with(transport), cache=cache
    )

    assert chart.suffix == ".txt"
    assert chart.has_chords
    assert "Holy, holy, holy! Lord God Almighty!" in chart.text
    # The chord sits over the syllable it did in the page.
    lines = chart.text.splitlines()
    chord_row = next(line for line in lines if line.strip().startswith("G") and "C" in line)
    assert chord_row.index("C") == 13
    # Nothing outside the <pre> comes with it.
    assert "Printed with permission" not in chart.text


def test_a_page_without_preformatted_text_is_handed_to_the_html_reader(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route("setlist.example", fixture("blog-page.html"))

    chart = PAGE.fetch("https://setlist.example/notes", http=http_with(transport), cache=cache)

    assert chart.suffix == ".html"
    assert chart.title == "Come Thou Fount of Every Blessing"
    assert chart.notes and "chord positions" in chart.notes[0]


def test_a_file_the_engine_cannot_read_from_a_link_is_refused(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route("dropbox.example", "%PDF-1.4 binary", "application/pdf")

    with pytest.raises(NoChartFoundError, match="Download it"):
        PAGE.fetch("https://dropbox.example/chart", http=http_with(transport), cache=cache)


def test_a_chordpro_file_at_a_link_keeps_its_extension(cache: Cache) -> None:
    transport = FakeTransport()
    transport.route(
        "raw.example/song.cho",
        "{title: Be Thou My Vision}\n{start_of_verse}\n[G]Be Thou my [C]vision\n{end_of_verse}\n",
        "text/plain",
    )

    chart = PAGE.fetch("https://raw.example/song.cho", http=http_with(transport), cache=cache)
    assert chart.suffix == ".cho"


# --- Everything at once -----------------------------------------------------------


def test_one_row_per_song_carrying_chords_from_one_site_and_artwork_from_another(
    cache: Cache,
) -> None:
    outcome = search("amazing grace", http=http_with(everything_answers()), cache=cache)

    assert outcome.is_url is False
    grace = next(match for match in outcome.results if "Amazing Grace" in match.title)
    # The chords came from Ultimate Guitar...
    assert grace.chart_url == GRACE_TAB
    assert grace.has_chords
    # ...the cover and the album from Apple, and the row says so.
    assert grace.album == "Hymns, Volume One"
    assert grace.artwork_url is not None and "600x600bb" in grace.artwork_url
    assert {"Ultimate Guitar", "Apple Music"} <= set(grace.source_names)


def test_importable_rows_come_before_ones_with_nothing_to_import(cache: Cache) -> None:
    outcome = search("amazing grace", http=http_with(everything_answers()), cache=cache)
    importable = [match.importable for match in outcome.results]
    assert importable == sorted(importable, reverse=True)


def test_a_site_being_down_is_a_note_not_a_failed_search(cache: Cache) -> None:
    transport = everything_answers()
    transport.fail(
        "ultimate-guitar.com",
        urllib.error.HTTPError(GRACE_TAB, 403, "Forbidden", hdrs=None, fp=None),  # type: ignore[arg-type]
    )

    outcome = search("amazing grace", http=http_with(transport), cache=cache)

    assert outcome.results, "the other sources still answered"
    assert any("Ultimate Guitar" in note for note in outcome.notes)
    assert any("Import from Clipboard" in note for note in outcome.notes)


def test_a_source_changing_shape_does_not_break_the_search(cache: Cache) -> None:
    transport = everything_answers()
    transport.route("ultimate-guitar.com/search.php", "<html><body>redesigned</body></html>")

    outcome = search("amazing grace", http=http_with(transport), cache=cache)

    assert outcome.results, "the other sources still answered"


def test_the_same_song_under_two_spellings_is_one_row() -> None:
    from pcci.online.models import SongMatch, SourceRef

    chords = SongMatch(
        ref="a",
        title="Come Thou Fount of Every Blessing chords",
        artist="Parish Hymnal Choir",
        chart_url="https://tabs.example/come-thou-fount",
        chart_kind="chords",
        sources=[SourceRef(provider="ug", name="Ultimate Guitar")],
    )
    metadata = SongMatch(
        ref="b",
        title="Come Thou Fount of Every Blessing",
        artist="PARISH HYMNAL CHOIR",
        album="Hymns, Volume One",
        sources=[SourceRef(provider="itunes", name="Apple Music")],
    )

    merged = merge([[chords], [metadata]])

    assert len(merged) == 1
    assert merged[0].album == "Hymns, Volume One"
    assert merged[0].chart_url == "https://tabs.example/come-thou-fount"


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("Come Thou Fount (of Every Blessing)", "Come Thou Fount of Every Blessing chords"),
        ("Blessed Assurance", "blessed assurance"),
        ("Holy, Holy, Holy [Live]", "Holy Holy Holy"),
    ],
)
def test_titles_that_mean_the_same_song_fold_together(left: str, right: str) -> None:
    assert fold(left) == fold(right)


def test_a_search_and_the_import_after_it_are_one_request(cache: Cache) -> None:
    """The page is fetched once. Asking a site for the same page twice is just rude."""
    transport = everything_answers()
    http = http_with(transport)

    ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http, cache=cache)
    before = len(transport.calls)
    ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http, cache=cache)

    assert len(transport.calls) == before


def test_turning_the_cache_off_really_turns_it_off() -> None:
    transport = everything_answers()
    http = http_with(transport)
    off = Cache(enabled=False)

    ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http, cache=off)
    before = len(transport.calls)
    ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http, cache=off)

    assert len(transport.calls) == before + 1


# --- From the web to a parsed song ------------------------------------------------


def test_a_fetched_chart_parses_with_its_chords_over_the_right_words(
    cache: Cache, tmp_path: Path
) -> None:
    """The whole point, end to end: a link in, a correctly aligned song out."""
    chart = ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http_with(everything_answers()), cache=cache)
    path = retrieve.materialise(chart, tmp_path)
    song = analyze(path)

    assert song.title == "Amazing Grace"
    assert song.key == "D"
    verse = next(section for section in song.sections if section.label == "Verse 1")
    first = verse.lines[0]
    assert first.lyrics == "Amazing grace how sweet the sound"
    assert [(placement.chord, placement.char_index) for placement in first.chords] == [
        ("D", 0),
        ("A", 14),
    ]
    # Column 14 is the "h" of "how" - exactly where the chart put it.
    assert first.lyrics[14] == "h"


def test_the_saved_file_is_named_after_the_song(cache: Cache, tmp_path: Path) -> None:
    chart = ULTIMATE_GUITAR.fetch(GRACE_TAB, http=http_with(everything_answers()), cache=cache)
    path = retrieve.materialise(chart, tmp_path)
    assert path.name == "Amazing Grace.txt"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Holy, Holy, Holy", "Holy, Holy, Holy"),
        ("AC/DC: Thunder", "AC DC Thunder"),
        ("con", "chart"),
        ("   ", "chart"),
        ("Be Thou My Vision?", "Be Thou My Vision"),
    ],
)
def test_a_song_title_becomes_a_file_name_every_platform_accepts(name: str, expected: str) -> None:
    assert safe_filename(name) == expected


# --- The clipboard ----------------------------------------------------------------


def test_pasted_text_becomes_a_chart(tmp_path: Path) -> None:
    pasted = """HOLY, HOLY, HOLY

Verse 1
G            C
Holy, holy, holy! Lord God Almighty!
G              C
Early in the morning our song shall rise to Thee
"""
    path, chart = retrieve.import_text(pasted, tmp_path)

    assert chart.title == "HOLY, HOLY, HOLY"
    assert chart.has_chords
    assert path.suffix == ".txt"
    song = analyze(path)
    assert song.title == "HOLY, HOLY, HOLY"
    assert song.chord_count == 4


def test_pasted_chordpro_is_recognised_as_chordpro(tmp_path: Path) -> None:
    pasted = (
        "{title: Be Thou My Vision}\n{start_of_verse}\n"
        "[G]Be Thou my [C]vision, O [D]Lord of my heart\n{end_of_verse}\n"
    )
    path, chart = retrieve.import_text(pasted, tmp_path)

    assert path.suffix == ".cho"
    assert chart.title == "Be Thou My Vision"
    assert analyze(path).title == "Be Thou My Vision"


def test_pasted_lyrics_with_no_chords_are_still_a_song(tmp_path: Path) -> None:
    """Words on their own are a presentation too - the user asked for exactly this."""
    pasted = """Blessed Assurance

Verse 1
Blessed assurance, Jesus is mine
Oh what a foretaste of glory divine

Chorus
This is my story, this is my song
Praising my Saviour all the day long
"""
    path, chart = retrieve.import_text(pasted, tmp_path)

    assert chart.chart_kind == "lyrics"
    song = analyze(path)
    assert song.chord_count == 0
    assert [section.label for section in song.sections] == ["Verse 1", "Chorus"]


def test_pasting_something_that_is_not_a_song_says_so() -> None:
    with pytest.raises(NoChartFoundError, match="Copy the whole chart"):
        retrieve.from_text("Amazing Grace")


def test_a_title_is_taken_from_the_first_line_that_is_one() -> None:
    assert retrieve.title_of("[Verse 1]\nG C D\nAmazing grace") == "Amazing grace"
    assert retrieve.title_of("{title: Be Thou My Vision}\n[G]words") == "Be Thou My Vision"
    assert retrieve.title_of("") == "Pasted chart"


def test_a_subtitle_on_one_site_and_not_the_other_is_still_one_row() -> None:
    from pcci.online.models import SongMatch, SourceRef

    short = SongMatch(
        ref="a",
        title="Come Thou Fount",
        artist="Parish Hymnal Choir",
        chart_url="https://tabs.example/come-thou-fount",
        chart_kind="chords",
        sources=[SourceRef(provider="ug", name="Ultimate Guitar")],
    )
    full = SongMatch(
        ref="b",
        title="Come Thou Fount of Every Blessing",
        artist="PARISH HYMNAL CHOIR",
        album="Hymns, Volume One",
        sources=[SourceRef(provider="itunes", name="Apple Music")],
    )

    merged = merge([[short], [full]])

    assert len(merged) == 1
    assert merged[0].album == "Hymns, Volume One"


def test_two_different_songs_that_share_a_word_stay_apart() -> None:
    """One choir's Amazing Grace is not another band's Grace, alike as the titles read."""
    from pcci.online.models import SongMatch, SourceRef

    hymn = SongMatch(
        ref="a",
        title="Amazing Grace",
        artist="Parish Hymnal Choir",
        sources=[SourceRef(provider="itunes", name="Apple Music")],
    )
    other = SongMatch(
        ref="b",
        title="Amazing",
        artist="Riverside Band",
        sources=[SourceRef(provider="itunes", name="Apple Music")],
    )

    assert len(merge([[hymn], [other]])) == 2
