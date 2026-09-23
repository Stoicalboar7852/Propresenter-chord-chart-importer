"""Writing FreeShow shows.

FreeShow (https://freeshow.app) keeps a song as JSON rather than Protocol Buffers, and
has its own chords element on the stage. Everything in this package was read out of
FreeShow's own source - the types in ``src/types/Show.ts`` and the importers in
``src/frontend/converters`` - and is documented in docs/FORMAT_NOTES.md section 6.
"""

from pcci.freeshow.verify import verify_bytes, verify_or_raise
from pcci.freeshow.writer import build_show, show_bytes

__all__ = ["build_show", "show_bytes", "verify_bytes", "verify_or_raise"]
