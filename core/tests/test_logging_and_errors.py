"""Logging contract and the error hierarchy.

The desktop apps parse stderr as JSON Lines, so the shape of a log record is part of
the public interface, not an implementation detail.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from pcci.errors import (
    EmptyDocumentError,
    ImageOnlyPdfError,
    PcciError,
    UnsupportedFormatError,
    UserInputError,
    VerificationFailedError,
)
from pcci.logging_setup import configure_logging, get_logger, log_directory


def test_log_lines_are_json_with_the_agreed_keys(capsys: pytest.CaptureFixture[str]) -> None:
    logger = configure_logging(json_logs=True, to_file=False)
    logger.info("converting %s", "chart.pdf")
    payload = json.loads(capsys.readouterr().err.strip())
    assert payload["level"] == "info"
    assert payload["msg"] == "converting chart.pdf"
    assert payload["ts"].endswith("Z")


def test_verbose_enables_debug(capsys: pytest.CaptureFixture[str]) -> None:
    logger = configure_logging(verbose=True, json_logs=True, to_file=False)
    logger.debug("detail")
    assert json.loads(capsys.readouterr().err.strip())["level"] == "debug"
    configure_logging(verbose=False, json_logs=True, to_file=False)
    get_logger().debug("hidden")
    assert capsys.readouterr().err == ""


def test_human_readable_mode_is_not_json(capsys: pytest.CaptureFixture[str]) -> None:
    logger = configure_logging(json_logs=False, to_file=False)
    logger.warning("watch out")
    assert "watch out" in capsys.readouterr().err


def test_configuring_twice_does_not_duplicate_handlers() -> None:
    configure_logging(to_file=False)
    first = len(logging.getLogger("pcci").handlers)
    configure_logging(to_file=False)
    assert len(logging.getLogger("pcci").handlers) == first


def test_log_directory_is_platform_specific() -> None:
    directory = log_directory()
    assert isinstance(directory, Path)
    assert "PCCI" in str(directory) or "pcci" in str(directory)


def test_file_logging_survives_an_unwritable_home(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def explode() -> Path:
        raise OSError("read-only file system")

    monkeypatch.setattr("pcci.logging_setup.log_directory", explode)
    logger = configure_logging(to_file=True, json_logs=True)
    logger.info("still working")
    assert "still working" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("error", "code"),
    [
        (UnsupportedFormatError("no", ""), 3),
        (EmptyDocumentError("no", ""), 2),
        (ImageOnlyPdfError("no", ""), 2),
        (VerificationFailedError("no", ""), 4),
        (PcciError("no", ""), 4),
    ],
)
def test_exit_codes_follow_the_cli_contract(error: PcciError, code: int) -> None:
    assert error.exit_code == code


def test_errors_carry_user_and_technical_detail() -> None:
    error = ImageOnlyPdfError(
        "This PDF is a scan.", "no glyphs on page 1", context={"path": "/tmp/x.pdf"}
    )
    payload = error.to_dict()
    assert payload["kind"] == "image_only_pdf"
    assert payload["user_message"] == "This PDF is a scan."
    assert payload["technical_detail"] == "no glyphs on page 1"
    assert payload["context"]["path"] == "/tmp/x.pdf"
    assert str(error) == "This PDF is a scan."


def test_input_errors_are_a_family() -> None:
    assert issubclass(ImageOnlyPdfError, UserInputError)
    assert issubclass(UserInputError, PcciError)
