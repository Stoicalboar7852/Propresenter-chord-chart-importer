"""Checking a generated FreeShow show before it reaches disk.

Nothing here trusts the writer. The bytes are parsed again as ordinary JSON and checked
against the plan that produced them, and against FreeShow's own expectations: the
importer's ``fixShowIssues`` will quietly repair a malformed show rather than refuse it,
which is exactly how a file with half its slides missing ends up on a stage.
"""

from __future__ import annotations

import json
from typing import Any

from pcci.errors import VerificationFailedError
from pcci.slides import SlidePlan
from pcci.verification import VerificationReport

__all__ = ["VerificationReport", "verify_bytes", "verify_or_raise"]


def _text_of(slide: dict[str, Any]) -> list[str]:
    return [
        "".join(chunk.get("value", "") for chunk in line.get("text", []))
        for item in slide.get("items", [])
        for line in item.get("lines", [])
    ]


def _chord_count(slide: dict[str, Any]) -> int:
    return sum(
        len(line.get("chords", []))
        for item in slide.get("items", [])
        for line in item.get("lines", [])
    )


def _ordered_slides(show: dict[str, Any]) -> list[dict[str, Any]]:
    """Every slide in playing order: each layout entry, then its children."""
    slides = show.get("slides", {})
    layout_id = show.get("settings", {}).get("activeLayout", "")
    layout = show.get("layouts", {}).get(layout_id, {})
    ordered: list[dict[str, Any]] = []
    for entry in layout.get("slides", []):
        parent = slides.get(entry.get("id"))
        if parent is None:
            continue
        ordered.append(parent)
        for child_id in parent.get("children", []):
            child = slides.get(child_id)
            if child is not None:
                ordered.append(child)
    return ordered


def verify_bytes(payload: bytes, plan: SlidePlan) -> VerificationReport:
    """Re-read ``payload`` and assert every structural invariant."""
    report = VerificationReport()

    try:
        parsed = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        report.check("the file parses as JSON", False, str(exc))
        return report
    report.check("the file parses as JSON", True)

    if not (isinstance(parsed, list) and len(parsed) == 2 and isinstance(parsed[1], dict)):
        report.check("the file is the [id, show] pair FreeShow saves", False, "wrong shape")
        return report
    report.check("the file is the [id, show] pair FreeShow saves", True)

    show_id, show = parsed[0], parsed[1]
    report.check("the show has an id", bool(isinstance(show_id, str) and show_id), "id is empty")
    report.check("the show has a name", bool(show.get("name", "").strip()), "name is empty")

    for key in ("slides", "layouts", "settings", "timestamps", "meta", "media"):
        report.check(f"the show has {key}", key in show, f"{key} is missing")

    slides = show.get("slides", {})
    layouts = show.get("layouts", {})
    active = show.get("settings", {}).get("activeLayout", "")
    report.check("the active layout exists", active in layouts, f"activeLayout {active!r}")

    referenced = [entry.get("id") for entry in layouts.get(active, {}).get("slides", [])]
    dangling = [value for value in referenced if value not in slides]
    report.check(
        "the layout references only existing slides",
        not dangling,
        f"{len(dangling)} dangling slide reference(s)",
    )

    parents = [slides[value] for value in referenced if value in slides]
    children = [child for parent in parents for child in parent.get("children", [])]
    missing_children = [child for child in children if child not in slides]
    report.check(
        "every child slide exists",
        not missing_children,
        f"{len(missing_children)} missing child slide(s)",
    )
    # fixShowIssues deletes a slide that is neither in the layout nor a child of one.
    reachable = set(referenced) | set(children)
    orphans = [key for key in slides if key not in reachable]
    report.check(
        "no slide is unreachable",
        not orphans,
        f"{len(orphans)} slide(s) FreeShow would discard",
    )
    report.check(
        "every child slide is a child of exactly one parent",
        len(set(children)) == len(children),
        "a slide is a child of two parents",
    )
    report.check(
        "only the first slide of a section carries a group",
        all(slides[value].get("group") for value in referenced if value in slides)
        and all(slides[child].get("group") is None for child in children if child in slides),
        "a parent has no group, or a child has one",
    )

    ordered = _ordered_slides(show)
    expected = plan.slides
    # A section repeated note for note is written once and played twice, so the file
    # holds no more slides than the plan and every planned slide is still accounted for.
    report.check(
        "the layout plays every planned slide",
        len(ordered) == len(expected),
        f"{len(ordered)} slides played for {len(expected)} planned",
    )

    mismatched: list[str] = []
    for written, planned in zip(ordered, expected, strict=False):
        lyrics = _text_of(written)
        wanted = [
            line.lyrics.upper() if plan.config.style.all_caps else line.lyrics
            for line in planned.lines
        ]
        if lyrics != wanted:
            mismatched.append(planned.label)
    report.check(
        "every slide carries its own words",
        not mismatched,
        f"different on: {', '.join(mismatched[:5])}",
    )

    if plan.config.chord_delivery.writes_inline:
        written_chords = sum(_chord_count(slide) for slide in slides.values())
        report.check(
            "the chords are stored on the words",
            written_chords > 0 or plan.song.chord_count == 0,
            f"{written_chords} chords written for {plan.song.chord_count} in the song",
        )

    drawn = [
        key
        for key, slide in slides.items()
        for item in slide.get("items", [])
        if item.get("chords", {}).get("enabled")
    ]
    report.check(
        "chords are only drawn on the slide when asked for",
        plan.config.chords_on_slide or not drawn,
        f"{len(drawn)} slide(s) would draw chords on the audience output",
    )

    if plan.config.chord_delivery.writes_notes:
        missing_notes = [
            planned.label
            for written, planned in zip(ordered, expected, strict=False)
            if planned.has_chords and not written.get("notes", "").strip()
        ]
        report.check(
            "every slide with chords carries notes",
            not missing_notes,
            f"missing on: {', '.join(missing_notes[:5])}",
        )

    return report


def verify_or_raise(payload: bytes, plan: SlidePlan) -> VerificationReport:
    """Verify, and refuse to continue if anything is wrong."""
    report = verify_bytes(payload, plan)
    if not report.ok:
        raise VerificationFailedError(
            "The show pcci built did not pass its own checks, so nothing was written. "
            "This is a bug in pcci, not a problem with your chart.",
            "; ".join(report.failures),
            context={"failures": report.failures, "checks": len(report.checks)},
        )
    return report
