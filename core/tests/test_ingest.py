"""Ingestion: every format, the same song, the same lines.

The corpus is generated from the real Word charts by ``scripts/make_fixtures.py``, so
"the txt and the pdf disagree" is a real signal rather than a fixture artefact.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pcci.errors import (
    DocumentReadError,
    EmptyDocumentError,
    ImageOnlyPdfError,
    UnsupportedFormatError,
)
from pcci.ingest import ingest, supported_extensions
from pcci.ingest.base import decode_bytes, normalise_text, strip_common_indent

SAME_SONG = [
    "GOODBYE YESTERDAY A.docx",
    "text/goodbye_yesterday.txt",
    "text/goodbye_yesterday.md",
    "html/goodbye_yesterday.html",
    "html/goodbye_yesterday_no_pre.html",
    "rtf/goodbye_yesterday.rtf",
    "odt/goodbye_yesterday.odt",
    "pdf/goodbye_yesterday.pdf",
    "pdf/goodbye_yesterday_2col.pdf",
]


@pytest.mark.parametrize("name", SAME_SONG)
def test_every_format_yields_the_same_lines(fixtures_dir: Path, name: str) -> None:
    document = ingest(fixtures_dir / name)
    texts = [line.text.strip() for line in document.non_empty_lines()]
    assert len(texts) == 128, f"{name} produced {len(texts)} non-blank lines"
    assert texts[0] == "GOODBYE YESTERDAY"
    # Markdown turns [Verse 1] into a heading, which drops the brackets.
    assert texts[1].strip("[]") == "Verse 1"
    assert "Goodbye yesterday" in texts


@pytest.mark.parametrize("name", SAME_SONG)
def test_chord_spacing_survives_every_format(fixtures_dir: Path, name: str) -> None:
    """The three-chord line must keep its chords in the right columns."""
    document = ingest(fixtures_dir / name)
    line = next(
        line for line in document.lines if line.text.strip().startswith("D") and "F#m" in line.text
    )
    text = line.text.strip()
    assert text.split() == ["D", "E", "F#m"]
    assert text.index("E") > 5, f"{name} collapsed the gap before E: {text!r}"


def test_word_document_is_recognised_as_monospace(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    assert document.monospace
    assert document.lines[0].font_name == "Roboto Mono"


def test_word_bold_runs_are_preserved(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    chord_line = next(line for line in document.lines if line.text.strip() == "Asus")
    lyric_line = next(line for line in document.lines if line.text.strip().startswith("I'm living"))
    assert chord_line.bold
    assert not lyric_line.bold


def test_shared_indent_is_reported_and_removed(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "GOODBYE YESTERDAY A.docx")
    assert any("indent" in warning for warning in document.warnings)
    assert not document.lines[0].text.startswith(" ")


def test_pdf_carries_real_character_positions(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "pdf" / "goodbye_yesterday.pdf")
    line = next(line for line in document.lines if line.text.strip() == "Goodbye yesterday")
    assert line.positioned
    assert len(line.char_x) == len(line.text)
    assert line.char_x == sorted(line.char_x)


def test_two_column_pdf_is_read_column_by_column(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "pdf" / "goodbye_yesterday_2col.pdf")
    assert any("2 columns" in warning for warning in document.warnings)
    texts = [line.text.strip() for line in document.non_empty_lines()]
    # Reading order must follow the song, not the page rows.
    assert texts.index("[Verse 1]") < texts.index("[Chorus 1]") < texts.index("[Bridge 1]")


def test_pdf_spanning_pages_keeps_page_numbers_and_reading_order(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "pdf" / "goodbye_yesterday.pdf")
    lines = document.non_empty_lines()
    pages = [line.page for line in lines]
    assert len(set(pages)) > 1, "the fixture is meant to span several pages"
    assert pages == sorted(pages), "lines must stay in page order"
    # A section split by a page break must still read as one run of lines.
    texts = [line.text.strip() for line in lines]
    assert texts.index("[Verse 1]") < texts.index("[Bridge 1]")


def test_scanned_pdf_raises_a_useful_error(fixtures_dir: Path) -> None:
    with pytest.raises(ImageOnlyPdfError) as excinfo:
        ingest(fixtures_dir / "pdf" / "scanned_no_text_layer.pdf")
    assert "scan" in excinfo.value.user_message
    assert excinfo.value.exit_code == 2


def test_utf16_with_bom(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "adversarial" / "utf16_bom.txt")
    assert document.lines[0].text == "Man Of Sorrows"


def test_mixed_tabs_and_spaces_expand_to_a_stop_of_four(fixtures_dir: Path) -> None:
    document = ingest(fixtures_dir / "adversarial" / "mixed_tabs.txt")
    tabbed = next(
        line
        for line in document.lines
        if line.text.strip().startswith("C	")
        or (line.text.strip().startswith("C") and "G" in line.text and "Am" in line.text)
    )
    assert "\t" not in tabbed.text


def test_unsupported_extension(tmp_path: Path) -> None:
    path = tmp_path / "chart.pages"
    path.write_text("not supported")
    with pytest.raises(UnsupportedFormatError) as excinfo:
        ingest(path)
    assert excinfo.value.exit_code == 3


def test_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.txt"
    path.write_bytes(b"")
    with pytest.raises(EmptyDocumentError):
        ingest(path)


def test_corrupt_docx(tmp_path: Path) -> None:
    path = tmp_path / "broken.docx"
    path.write_bytes(b"PK\x03\x04 this is not really a docx")
    with pytest.raises(DocumentReadError) as excinfo:
        ingest(path)
    assert ".doc" in excinfo.value.user_message


def test_rtf_that_is_not_rtf(tmp_path: Path) -> None:
    path = tmp_path / "fake.rtf"
    path.write_text("just some words")
    with pytest.raises(DocumentReadError):
        ingest(path)


def test_supported_extensions_cover_the_spec() -> None:
    for extension in (".txt", ".md", ".pdf", ".docx", ".rtf", ".odt", ".html", ".cho", ".chopro"):
        assert extension in supported_extensions()


def test_decode_bytes_prefers_utf8(tmp_path: Path) -> None:
    text, warnings = decode_bytes("Café".encode(), tmp_path / "x.txt")
    assert text == "Café"
    assert not warnings


def test_decode_bytes_falls_back_and_warns(tmp_path: Path) -> None:
    text, warnings = decode_bytes(
        "Café chord chart in latin-1".encode("latin-1"), tmp_path / "x.txt"
    )
    assert "chord chart" in text
    assert warnings


def test_normalise_text_folds_exotic_whitespace_and_accidentals() -> None:
    assert normalise_text("B♭ maj7") == "Bb maj7"
    assert normalise_text("a\tb") == "a   b"


def test_strip_common_indent_keeps_relative_alignment() -> None:
    lines, indent = strip_common_indent(["    C   G", "    lyrics here", ""])
    assert indent == 4
    assert lines == ["C   G", "lyrics here", ""]
