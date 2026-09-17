"""Documents with no chords in them at all.

A lyrics sheet is a perfectly ordinary thing for a church to have - a hymn text, a
page printed off for the singers, something pasted out of an email - and it should
become a presentation exactly the way a chord chart does. That was never in doubt for
plain text, but each reader reaches the parser by a different route, and "no chords"
is precisely the input that makes a chord/lyric pairing heuristic interesting.

So every format is built here at run time from one public-domain hymn and put through
the whole pipeline. The song is Amazing Grace, which is out of copyright, real, and
has the section structure a worship chart has.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pcci.config import ChordDelivery, ConversionConfig
from pcci.convert import convert
from pcci.parse.pipeline import analyze
from pcci.slides import plan_slides

LINES = [
    "Amazing Grace",
    "",
    "Verse 1",
    "Amazing grace how sweet the sound",
    "That saved a wretch like me",
    "I once was lost but now am found",
    "Was blind but now I see",
    "",
    "Verse 2",
    "Twas grace that taught my heart to fear",
    "And grace my fears relieved",
    "",
    "Chorus",
    "Praise God praise God",
    "Praise God who set me free",
]

EXPECTED_SECTIONS = ["Verse 1", "Verse 2", "Chorus"]
EXPECTED_LYRICS = 8


def write_txt(directory: Path) -> Path:
    path = directory / "grace.txt"
    path.write_text("\n".join(LINES) + "\n", encoding="utf-8")
    return path


def write_markdown(directory: Path) -> Path:
    path = directory / "grace.md"
    out = [f"# {LINES[0]}", ""]
    for line in LINES[1:]:
        out.append(f"## {line}" if line in EXPECTED_SECTIONS else line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path


def write_html(directory: Path) -> Path:
    path = directory / "grace.html"
    body = "\n".join(LINES)
    path.write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><title>{LINES[0]}</title></head>"
        f"<body><pre>{body}</pre></body></html>\n",
        encoding="utf-8",
    )
    return path


def write_rtf(directory: Path) -> Path:
    path = directory / "grace.rtf"
    body = "\n".join(f"{line}\\par" for line in LINES)
    path.write_text(
        "{\\rtf1\\ansi\\ansicpg1252\\deff0"
        "{\\fonttbl{\\f0\\fmodern\\fcharset0 Courier New;}}"
        "\\f0\\fs18\n" + body + "\n}\n",
        encoding="utf-8",
    )
    return path


def write_docx(directory: Path) -> Path:
    from docx import Document

    path = directory / "grace.docx"
    document = Document()
    for line in LINES:
        paragraph = document.add_paragraph()
        run = paragraph.add_run(line)
        run.font.name = "Courier New"
    document.save(str(path))
    return path


def write_odt(directory: Path) -> Path:
    from odf.opendocument import OpenDocumentText
    from odf.style import FontFace, Style, TextProperties
    from odf.text import P

    path = directory / "grace.odt"
    document = OpenDocumentText()
    document.fontfacedecls.addElement(
        FontFace(name="Courier New", fontfamily="Courier New", fontpitch="fixed")
    )
    monospace = Style(name="Mono", family="paragraph")
    monospace.addElement(TextProperties(fontname="Courier New", fontsize="9pt"))
    document.styles.addElement(monospace)
    for line in LINES:
        paragraph = P(stylename=monospace)
        paragraph.addText(line)
        document.text.addElement(paragraph)
    document.save(str(path))
    return path


def write_pdf(directory: Path) -> Path:
    import pymupdf

    path = directory / "grace.pdf"
    document = pymupdf.open()
    page = document.new_page(width=595.0, height=842.0)
    y = 60.0
    for line in LINES:
        if line.strip():
            page.insert_text((40.0, y), line, fontname="cour", fontsize=10.0)
        y += 14.0
    document.save(str(path))
    document.close()
    return path


WRITERS = {
    "txt": write_txt,
    "md": write_markdown,
    "html": write_html,
    "rtf": write_rtf,
    "docx": write_docx,
    "odt": write_odt,
    "pdf": write_pdf,
}


@pytest.mark.parametrize("fmt", sorted(WRITERS))
def test_a_document_with_no_chords_parses_into_a_song(fmt: str, tmp_path: Path) -> None:
    song = analyze(WRITERS[fmt](tmp_path))

    assert song.title == "Amazing Grace"
    assert [section.label for section in song.sections] == EXPECTED_SECTIONS
    assert song.chord_count == 0
    lyrics = [line.lyrics for section in song.sections for line in section.lines if line.lyrics]
    assert len(lyrics) == EXPECTED_LYRICS
    assert lyrics[0] == "Amazing grace how sweet the sound"


@pytest.mark.parametrize("fmt", sorted(WRITERS))
def test_a_document_with_no_chords_converts(fmt: str, tmp_path: Path) -> None:
    output = tmp_path / "out" / "grace.pro"
    result = convert(WRITERS[fmt](tmp_path), output)

    assert output.exists()
    assert result.plan.slide_count >= 3
    # A lyrics sheet has no chord chart, so none is written beside the presentation.
    assert result.chart_pages == []
    assert not list(output.parent.glob("*.png"))


def test_the_plan_says_out_loud_that_there_were_no_chords(tmp_path: Path) -> None:
    """Because "no chords in this file" and "pcci misread the chords" look identical."""
    plan = plan_slides(analyze(write_txt(tmp_path)))
    assert any("lyrics only" in warning for warning in plan.warnings)


def test_asking_for_no_chords_does_not_produce_that_warning(tmp_path: Path) -> None:
    config = ConversionConfig(chord_delivery=ChordDelivery.NONE)
    plan = plan_slides(analyze(write_txt(tmp_path)), config)
    assert not any("lyrics only" in warning for warning in plan.warnings)


def test_lyrics_with_no_section_headers_at_all_still_convert(tmp_path: Path) -> None:
    """The last-resort route: blank-line stanzas, and not a chord or a label in sight."""
    path = tmp_path / "bare.txt"
    path.write_text(
        "Amazing grace how sweet the sound\n"
        "That saved a wretch like me\n"
        "\n"
        "I once was lost but now am found\n"
        "Was blind but now I see\n",
        encoding="utf-8",
    )

    song = analyze(path)

    assert len(song.sections) == 2
    assert all(section.type.value == "Verse" for section in song.sections)
    # Guessed, and flagged as guessed, so the review screen puts a marker on it.
    assert all(section.confidence < 0.9 for section in song.sections)
    assert any("guessed" in warning for warning in song.warnings)


def test_a_chart_with_chords_still_gets_its_chart_page(tmp_path: Path) -> None:
    """The counterpart: skipping the page must depend on the chords, not on luck."""
    path = tmp_path / "chords.txt"
    path.write_text(
        "Amazing Grace\n\nVerse 1\nG            C\nAmazing grace how sweet the sound\n",
        encoding="utf-8",
    )

    result = convert(path, tmp_path / "out" / "chords.pro")

    assert result.plan.song.chord_count == 2
    assert result.chart_pages, "a song with chords still gets a chord chart"


# --- What a chord site puts above the chart ---------------------------------------


CHORD_DIAGRAMS = """Some Song

F - X33210
Am - X02210
x33210

[Verse 1]
F            Am
Amazing grace how sweet the sound
"""

BRACKETED_DIAGRAMS = """Some Song

[F - x33210]
[Am - x02210]

[Verse 1]
F            Am
Amazing grace how sweet the sound
"""


def test_a_chord_fingering_is_not_a_section(tmp_path: Path) -> None:
    """Chord sites print fingerings in brackets above the chart, and they are short and
    bracketed, which is exactly what an unrecognised section label looks like. A real
    import of Shivers came out with a group called "F - X33210"."""
    path = tmp_path / "diagrams.txt"
    path.write_text(CHORD_DIAGRAMS, encoding="utf-8")

    song = analyze(path)

    labels = [section.label for section in song.sections]
    assert labels == ["Verse 1"], labels


def test_a_bracketed_fingering_is_not_a_section_either(tmp_path: Path) -> None:
    """The same thing by the other route: some charts bracket their fingerings."""
    path = tmp_path / "bracketed.txt"
    path.write_text(BRACKETED_DIAGRAMS, encoding="utf-8")

    labels = [section.label for section in analyze(path).sections]
    assert labels == ["Verse 1"], labels


@pytest.mark.parametrize(
    "inner",
    ["F - x33210", "Am - x02210", "x33210", "F#m7 - 242222", "C - X32010"],
)
def test_fingerings_are_recognised_as_fingerings(inner: str) -> None:
    from pcci.parse.sections import looks_like_chord_diagram

    assert looks_like_chord_diagram(inner)


@pytest.mark.parametrize(
    "inner",
    ["Verse 1", "Chorus", "Bridge 2", "Instrumental", "Tag", "Interlude 1", "Drop"],
)
def test_real_section_names_are_not_mistaken_for_fingerings(inner: str) -> None:
    from pcci.parse.sections import looks_like_chord_diagram

    assert not looks_like_chord_diagram(inner)


# --- What a lyrics site puts in its section labels --------------------------------


GENIUS_STYLE = """Some Song

[Verse 1: A Singer]
The first line of the verse here
The second line of the verse here

[Pre-Chorus: A Singer & Another]
Building up to something now
Building up a little more

[Chorus]
The hook goes around again
The hook goes around again

[Verse 2: Another]
Something different happens
Something different happens
"""


def test_a_label_that_names_the_singer_is_still_that_section(tmp_path: Path) -> None:
    """Lyrics sites write "[Verse 1: A Singer]", and that is a verse.

    It matters more than it looks. The sites that label sections this way are also the
    ones that refuse an automated request, so the way their words arrive is somebody
    copying and pasting them - and a presentation whose groups are called
    "Verse 1: A Singer" never matches its other verses or gets a verse's colour.
    """
    path = tmp_path / "genius.txt"
    path.write_text(GENIUS_STYLE, encoding="utf-8")

    song = analyze(path)

    assert [section.label for section in song.sections] == [
        "Verse 1",
        "Pre-Chorus",
        "Chorus",
        "Verse 2",
    ]
    # The original wording is still there for anyone who wants it.
    assert song.sections[0].raw_label == "[Verse 1: A Singer]"


def test_a_bracketed_aside_is_not_forced_into_a_section_type(tmp_path: Path) -> None:
    """Only a real section name survives the colon; the rest is kept whole."""
    path = tmp_path / "aside.txt"
    path.write_text(
        "Some Song\n\n[Talking: to the band]\nTake it away\nTake it away now\n",
        encoding="utf-8",
    )

    song = analyze(path)

    assert song.sections[0].label == "Talking: to the band"


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("Verse 1: A Singer", "Verse 1"),
        ("Chorus: A Singer & Another", "Chorus"),
        ("Bridge: Someone, Someone Else", "Bridge"),
        ("Chorus: x2", None),
        ("Chorus", None),
    ],
)
def test_the_performer_is_told_apart_from_a_repeat_count(label: str, expected: str | None) -> None:
    from pcci.parse.sections import without_performer

    assert without_performer(label) == expected
