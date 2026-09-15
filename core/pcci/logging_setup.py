"""Logging.

Two sinks, deliberately different:

* **stderr** — JSON Lines (``{"level","msg","ts"}``), the contract the desktop
  front-ends parse. Human-readable text goes here only when ``json_logs`` is off.
* **a rotating file** — 5 x 2 MB under the platform log directory.

File *contents* are never logged. Paths and structural metadata only.
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import sys
import time
from pathlib import Path

LOGGER_NAME = "pcci"
_MAX_BYTES = 2 * 1024 * 1024
_BACKUP_COUNT = 5


class JsonLinesFormatter(logging.Formatter):
    """One JSON object per line, exactly the keys the UI bridge expects."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname.lower(),
            "msg": record.getMessage(),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created))
            + f".{int(record.msecs):03d}Z",
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        for key, value in getattr(record, "extra_fields", {}).items():
            payload[key] = value
        return json.dumps(payload, ensure_ascii=False)


def log_directory() -> Path:
    """Platform log directory, per the spec's error-handling contract."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Logs" / "PCCI"
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        root = Path(base) if base else Path.home() / "AppData" / "Local"
        return root / "PCCI" / "Logs"
    base = os.environ.get("XDG_STATE_HOME")
    root = Path(base) if base else Path.home() / ".local" / "state"
    return root / "pcci" / "logs"


def configure_logging(
    *,
    verbose: bool = False,
    json_logs: bool = True,
    to_file: bool = True,
) -> logging.Logger:
    """Configure and return the ``pcci`` logger. Safe to call more than once."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(
        JsonLinesFormatter() if json_logs else logging.Formatter("%(levelname)-8s %(message)s")
    )
    logger.addHandler(stream)

    if to_file:
        try:
            directory = log_directory()
            directory.mkdir(parents=True, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                directory / "pcci.log",
                maxBytes=_MAX_BYTES,
                backupCount=_BACKUP_COUNT,
                encoding="utf-8",
            )
            file_handler.setFormatter(JsonLinesFormatter())
            logger.addHandler(file_handler)
        except OSError as exc:  # a read-only home should never kill a conversion
            logger.warning("file logging disabled: %s", exc)

    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)
