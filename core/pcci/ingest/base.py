"""Shared ingestion machinery: decoding, whitespace normalisation, dispatch.

Every ingester returns a ``RawDocument``. The helpers here handle the parts that are
identical whatever the source format, and the parts that are easy to get subtly wrong:

* **Decoding.** Never assume UTF-8. ``charset-normalizer`` guesses, BOMs are stripped.
* **Tabs.** Expanded at a stop of 4 *before* anything measures a column, because chord
  alignment in monospaced sources is entirely a column game.
* **A common leading indent.** Charts pasted out of a web page routinely carry the same
  deep indent on every line — the reference Word documents all start with sixteen tabs.
  Removing the shared prefix keeps relative alignment intact and makes columns mean
  something.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from charset_normalizer import from_bytes

from pcci.errors import (
    DocumentReadError,
    EmptyDocumentError,
    EncodingDetectionError,
    UnsupportedFormatError,
)
from pcci.ir import PositionedLine, RawDocument, SourceFormat
from pcci.parse.chords import normalise_accidentals

TAB_STOP = 4

# Whitespace characters that must become an ordinary space before columns are counted.
_SPACE_LIKE = {
    " ": " ",  # no-break space
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",  # thin space
    " ": " ",
    " ": " ",  # narrow no-break space
    " ": " ",
    "　": " ",
    "​": "",  # zero-width space
    "﻿": "",  # BOM as a character
}

# Homoglyphs seen in the reference charts: a Cyrillic е inside "Goodbyе yesterday".
_HOMOGLYPHS = {
    "е": "e",  # CYRILLIC SMALL LETTER IE
    "а": "a",  # CYRILLIC SMALL LETTER A
    "о": "o",  # CYRILLIC SMALL LETTER O
    "р": "p",  # CYRILLIC SMALL LETTER ER
    "с": "c",  # CYRILLIC SMALL LETTER ES
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "…": "...",
}


@runtime_checkable
class Ingester(Protocol):
    """What every format reader looks like."""

    extensions: tuple[str, ...]
    source_format: SourceFormat

    def load(self, path: Path) -> RawDocument: ...


def decode_bytes(data: bytes, path: Path) -> tuple[str, list[str]]:
    """Decode file bytes to text, guessing the encoding. Returns text and warnings."""
    warnings: list[str] = []
    if not data:
        raise EmptyDocumentError(
            f"{path.name} is empty.",
            "file contained zero bytes",
            context={"path": str(path)},
        )

    for bom, encoding in (
        (b"\xef\xbb\xbf", "utf-8-sig"),
        (b"\xff\xfe\x00\x00", "utf-32"),
        (b"\x00\x00\xfe\xff", "utf-32"),
        (b"\xff\xfe", "utf-16"),
        (b"\xfe\xff", "utf-16"),
    ):
        if data.startswith(bom):
            try:
                return data.decode(encoding), warnings
            except UnicodeDecodeError as exc:
                raise EncodingDetectionError(
                    f"{path.name} looks like {encoding} but could not be decoded.",
                    str(exc),
                    context={"path": str(path), "encoding": encoding},
                ) from exc

    try:
        return data.decode("utf-8"), warnings
    except UnicodeDecodeError:
        pass

    best = from_bytes(data).best()
    if best is None:
        raise EncodingDetectionError(
            f"Could not work out the text encoding of {path.name}.",
            "charset-normalizer returned no candidate",
            context={"path": str(path)},
        )
    warnings.append(f"Text encoding was detected as {best.encoding}, not UTF-8.")
    return str(best), warnings


def read_text(path: Path) -> tuple[str, list[str]]:
    """Read a text file from disk with encoding detection."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise DocumentReadError(
            f"Could not read {path.name}.",
            str(exc),
            context={"path": str(path)},
        ) from exc
    return decode_bytes(data, path)


def normalise_text(text: str) -> str:
    """Normalise one line: exotic spaces, homoglyphs, accidentals, tabs."""
    for source, target in _SPACE_LIKE.items():
        text = text.replace(source, target)
    for source, target in _HOMOGLYPHS.items():
        text = text.replace(source, target)
    text = normalise_accidentals(text)
    return text.expandtabs(TAB_STOP).rstrip()


def split_lines(text: str) -> list[str]:
    """Split into normalised lines, whatever the line endings were."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [normalise_text(line) for line in text.split("\n")]


def common_indent(lines: list[str]) -> int:
    """Width of the leading-space prefix shared by every non-blank line."""
    widths = [len(line) - len(line.lstrip(" ")) for line in lines if line.strip()]
    return min(widths) if widths else 0


def strip_common_indent(lines: list[str]) -> tuple[list[str], int]:
    """Remove the shared leading indent, preserving relative alignment."""
    indent = common_indent(lines)
    if indent == 0:
        return lines, 0
    return [line[indent:] if line.strip() else "" for line in lines], indent


def build_document(
    path: Path,
    source_format: SourceFormat,
    lines: list[PositionedLine],
    *,
    monospace: bool,
    warnings: list[str] | None = None,
) -> RawDocument:
    """Assemble a RawDocument, refusing one with nothing in it."""
    document = RawDocument(
        source_path=path,
        source_format=source_format,
        lines=lines,
        monospace=monospace,
        warnings=warnings or [],
    )
    if not document.non_empty_lines():
        raise EmptyDocumentError(
            f"{path.name} has no text in it.",
            f"{source_format} ingester produced {len(lines)} lines, all blank",
            context={"path": str(path), "format": source_format},
        )
    return document


_REGISTRY: dict[str, Ingester] = {}


def register(ingester: Ingester) -> Ingester:
    """Register an ingester for its file extensions."""
    for extension in ingester.extensions:
        _REGISTRY[extension.lower()] = ingester
    return ingester


def supported_extensions() -> list[str]:
    return sorted(_REGISTRY)


def ingester_for(path: Path) -> Ingester:
    """Pick the ingester for a path, by extension."""
    suffix = path.suffix.lower()
    ingester = _REGISTRY.get(suffix)
    if ingester is None:
        raise UnsupportedFormatError(
            f"pcci cannot read {suffix or 'files without an extension'} yet.",
            f"no ingester registered for {suffix!r}",
            context={"path": str(path), "supported": supported_extensions()},
        )
    return ingester
