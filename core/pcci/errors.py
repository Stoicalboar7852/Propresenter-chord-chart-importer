"""Typed errors.

Every failure the engine can produce is one of these. Each carries a
``user_message`` written for a worship-team volunteer (what went wrong, what to
do about it) and a ``technical_detail`` for the log and the disclosure triangle
in the UI. The CLI maps ``exit_code`` straight onto its process exit status.
"""

from __future__ import annotations

from typing import Any


class PcciError(Exception):
    """Base class for every error the engine raises deliberately."""

    exit_code = 4
    kind = "internal"

    def __init__(
        self,
        user_message: str,
        technical_detail: str = "",
        *,
        context: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(user_message)
        self.user_message = user_message
        self.technical_detail = technical_detail
        self.context: dict[str, Any] = context or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "user_message": self.user_message,
            "technical_detail": self.technical_detail,
            "context": self.context,
        }

    def __str__(self) -> str:
        return self.user_message


class UserInputError(PcciError):
    """Something about the file the user chose. Exit code 2."""

    exit_code = 2
    kind = "user_input"


class UnsupportedFormatError(PcciError):
    exit_code = 3
    kind = "unsupported_format"


class EncodingDetectionError(UserInputError):
    kind = "encoding_detection"


class ImageOnlyPdfError(UserInputError):
    kind = "image_only_pdf"


class EmptyDocumentError(UserInputError):
    kind = "empty_document"


class NoSectionsDetectedError(UserInputError):
    kind = "no_sections_detected"


class DocumentReadError(UserInputError):
    """The file exists but the format library could not open it."""

    kind = "document_read"


class NetworkError(UserInputError):
    """Something on the web did not answer, or answered with nothing usable.

    Exit code 2 with everything else the user can fix: a typo in a pasted link, a
    site that is down and a laptop with no wifi all land here, and the front-ends
    already treat 2 as "tell them what you told me" rather than "something is broken
    inside pcci".
    """

    kind = "network"


class NoChartFoundError(UserInputError):
    """The page was fetched and read, and had no song in it."""

    kind = "no_chart_found"


class ProtoSchemaMismatchError(PcciError):
    kind = "proto_schema_mismatch"


class VerificationFailedError(PcciError):
    kind = "verification_failed"


class OutputWriteError(PcciError):
    kind = "output_write"


class ChordAlignmentWarning(UserWarning):
    """Non-fatal: alignment was ambiguous. Accumulated on ``Song.warnings``."""
