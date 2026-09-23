"""docs/NETWORK.md has to stay true, because somebody hands it to an IT department.

A source added to the engine without its domain going in that list is a support call
from a school where the search half works. This test is the thing that notices.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

import pytest

from pcci.online.sources import genius, itunes, lrclib, musixmatch, ultimate_guitar

DOC = Path(__file__).resolve().parents[2] / "docs" / "NETWORK.md"

MODULES = (genius, itunes, lrclib, musixmatch, ultimate_guitar)
ENDPOINT_NAMES = ("SEARCH_ENDPOINT", "RECORD_ENDPOINT", "API_ROOT", "SITE", "PAGE_ROOT")


def documented_hosts() -> set[str]:
    if not DOC.exists():  # pragma: no cover - only when the docs are not checked out
        pytest.skip("docs/NETWORK.md is not part of this checkout")
    text = DOC.read_text(encoding="utf-8")
    return {line.strip() for line in text.splitlines() if line.strip()}


def hosts_in_the_code() -> set[str]:
    """Every host the online sources name, read out of the modules themselves."""
    found: set[str] = set()
    for module in MODULES:
        for name in ENDPOINT_NAMES:
            value = getattr(module, name, None)
            if isinstance(value, str) and value.startswith("http"):
                found.add(urlsplit(value).netloc)
        for provider in vars(module).values():
            site = getattr(provider, "site", None)
            if isinstance(site, str) and site.startswith("http"):
                found.add(urlsplit(site).netloc)
        for value in vars(module).values():
            if isinstance(value, tuple) and all(isinstance(entry, str) for entry in value):
                found.update(entry for entry in value if entry.endswith(".com"))
    return {host for host in found if host}


def covered(host: str, documented: str) -> bool:
    """A host counts as documented literally, or under a wildcard that includes it."""
    if host in documented:
        return True
    parts = host.split(".")
    return any(f"*.{'.'.join(parts[index:])}" in documented for index in range(1, len(parts) - 1))


def test_every_host_the_engine_contacts_is_in_the_network_doc() -> None:
    text = documented_hosts()
    joined = "\n".join(text)
    missing = sorted(host for host in hosts_in_the_code() if not covered(host, joined))
    assert not missing, f"docs/NETWORK.md does not mention: {', '.join(missing)}"


def test_the_paste_list_is_a_plain_list_of_hostnames() -> None:
    """The block people copy has to be hostnames and nothing else: no scheme, no path."""
    if not DOC.exists():  # pragma: no cover
        pytest.skip("docs/NETWORK.md is not part of this checkout")
    text = DOC.read_text(encoding="utf-8")
    # Odd indexes are what sits between a pair of fences.
    fenced = text.split("```")[1::2]
    lists = [block for block in fenced if "lrclib.net" in block and "curl" not in block]
    assert lists, "the doc should carry a copy-and-paste list"
    for block in lists:
        for line in block.splitlines():
            entry = line.strip()
            if not entry:
                continue
            assert "/" not in entry and ":" not in entry, f"{entry!r} is not a bare hostname"
