"""Format readers.

Importing this package registers every ingester, so ``ingest(path)`` works for any
supported extension without the caller knowing which module handles it.
"""

from __future__ import annotations

from pathlib import Path

from pcci.ingest import chordpro, docx, html, markdown, odt, pdf, rtf, txt
from pcci.ingest.base import Ingester, ingester_for, register, supported_extensions
from pcci.ir import RawDocument

__all__ = [
    "Ingester",
    "chordpro",
    "docx",
    "html",
    "ingest",
    "ingester_for",
    "markdown",
    "odt",
    "pdf",
    "register",
    "rtf",
    "supported_extensions",
    "txt",
]


def ingest(path: Path) -> RawDocument:
    """Read any supported chord chart into a ``RawDocument``."""
    return ingester_for(path).load(path)
