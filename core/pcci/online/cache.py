"""A small on-disk cache for things fetched from the web.

Searching and then importing a result would otherwise fetch the same page twice, a
second or two apart, for no reason anybody benefits from - least of all the site
answering it. Entries are keyed by URL, expire, and are pure optimisation: every
caller works exactly the same way with the cache turned off.

Nothing sensitive lands here. It holds public song pages, under the user's own cache
directory, which the operating system is free to clear whenever it likes.
"""

from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path

from pcci.logging_setup import current_platform, get_logger

#: A song page does not change between a search and the import two seconds later.
CHART_TTL_SECONDS = 24 * 60 * 60
SEARCH_TTL_SECONDS = 60 * 60


def cache_directory() -> Path:
    """Platform cache directory, alongside where the logs go."""
    platform = current_platform()
    if platform == "darwin":
        return Path.home() / "Library" / "Caches" / "PCCI" / "online"
    if platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        root = Path(base) if base else Path.home() / "AppData" / "Local"
        return root / "PCCI" / "Cache" / "online"
    base = os.environ.get("XDG_CACHE_HOME")
    root = Path(base) if base else Path.home() / ".cache"
    return root / "pcci" / "online"


def _entry(key: str) -> Path:
    return cache_directory() / (hashlib.sha256(key.encode("utf-8")).hexdigest()[:32] + ".bin")


class Cache:
    """Read-through storage. Every failure is a miss, never an error."""

    def __init__(self, *, enabled: bool = True, directory: Path | None = None) -> None:
        self.enabled = enabled
        self._directory = directory

    def _path(self, key: str) -> Path:
        if self._directory is not None:
            name = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32] + ".bin"
            return self._directory / name
        return _entry(key)

    def get(self, key: str, *, ttl: int) -> bytes | None:
        if not self.enabled:
            return None
        path = self._path(key)
        try:
            age = time.time() - path.stat().st_mtime
            if age > ttl:
                return None
            return path.read_bytes()
        except OSError:
            return None

    def put(self, key: str, payload: bytes) -> None:
        if not self.enabled:
            return
        path = self._path(key)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix(".tmp")
            temporary.write_bytes(payload)
            temporary.replace(path)
        except OSError as error:  # a full or read-only disk must not fail a search
            get_logger().debug("cache write skipped: %s", error)

    def clear(self) -> int:
        """Empty the cache. Returns how many entries went."""
        directory = self._directory or cache_directory()
        removed = 0
        try:
            entries = list(directory.glob("*.bin"))
        except OSError:
            return 0
        for entry in entries:
            try:
                entry.unlink()
                removed += 1
            except OSError:
                continue
        return removed
