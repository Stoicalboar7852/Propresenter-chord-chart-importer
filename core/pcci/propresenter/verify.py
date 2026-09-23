"""Checking a generated presentation before it reaches disk.

Nothing here trusts the writer. The serialised bytes are parsed again with the same
bindings and the result is checked against the plan that produced it. A failure aborts
the write: a half-valid ``.pro`` that crashes ProPresenter on a Sunday morning is worse
than no file at all.
"""

from __future__ import annotations

from typing import Any

from pcci.errors import VerificationFailedError
from pcci.propresenter.bindings import load_bindings
from pcci.slides import SlidePlan
from pcci.verification import VerificationReport

__all__ = ["VerificationReport", "verify_bytes", "verify_or_raise"]

UUID_LENGTH = 36
ZERO_UUID = "00000000-0000-0000-0000-000000000000"


def verify_bytes(payload: bytes, plan: SlidePlan) -> VerificationReport:
    """Re-parse ``payload`` and assert every structural invariant."""
    bindings = load_bindings()
    report = VerificationReport()

    presentation = bindings.presentation.Presentation()
    try:
        presentation.ParseFromString(payload)
    except Exception as exc:  # protobuf raises DecodeError and friends
        report.check("the file parses as a ProPresenter presentation", False, str(exc))
        return report
    report.check("the file parses as a ProPresenter presentation", True)

    report.check(
        "the presentation has a name",
        bool(presentation.name.strip()),
        "name is empty",
    )
    report.check(
        "slide count matches the plan",
        len(presentation.cues) == plan.slide_count,
        f"{len(presentation.cues)} cues for {plan.slide_count} planned slides",
    )

    cue_uuids = [cue.uuid.string for cue in presentation.cues]
    report.check(
        "every cue has a unique UUID",
        len(set(cue_uuids)) == len(cue_uuids),
        f"{len(cue_uuids) - len(set(cue_uuids))} duplicates",
    )
    report.check(
        "every UUID is well formed",
        all(len(value) == UUID_LENGTH and value != ZERO_UUID for value in cue_uuids),
        "a cue UUID is empty, zero or malformed",
    )

    grouped: list[str] = [
        identifier.string
        for cue_group in presentation.cue_groups
        for identifier in cue_group.cue_identifiers
    ]
    report.check(
        "every cue belongs to exactly one group",
        sorted(grouped) == sorted(cue_uuids),
        f"{len(grouped)} group memberships for {len(cue_uuids)} cues",
    )
    report.check(
        "no cue is in two groups",
        len(set(grouped)) == len(grouped),
        "a cue identifier appears in more than one group",
    )

    group_uuids = {cue_group.group.uuid.string for cue_group in presentation.cue_groups}
    report.check(
        "every group has a name",
        all(cue_group.group.name.strip() for cue_group in presentation.cue_groups),
        "a group name is empty",
    )
    for arrangement in presentation.arrangements:
        referenced = [identifier.string for identifier in arrangement.group_identifiers]
        dangling = [value for value in referenced if value not in group_uuids]
        report.check(
            "the arrangement references only existing groups",
            not dangling,
            f"{len(dangling)} dangling group reference(s)",
        )
        report.check(
            "the arrangement covers every group",
            set(referenced) == group_uuids,
            "the arrangement and the group list disagree",
        )
    if presentation.arrangements:
        selected = presentation.selected_arrangement.string
        report.check(
            "the selected arrangement exists",
            selected in {a.uuid.string for a in presentation.arrangements},
            f"selected_arrangement {selected!r} not found",
        )

    _verify_slides(presentation, plan, report)
    return report


def _verify_slides(presentation: Any, plan: SlidePlan, report: VerificationReport) -> None:
    missing_text = 0
    missing_notes: list[str] = []
    for cue, slide in zip(presentation.cues, plan.slides, strict=False):
        actions = [action for action in cue.actions if action.HasField("slide")]
        if not actions:
            missing_text += 1
            continue
        presentation_slide = actions[0].slide.presentation
        elements = presentation_slide.base_slide.elements
        has_text = any(element.element.text.rtf_data for element in elements)
        if not has_text:
            missing_text += 1
        needs_notes = plan.config.chord_delivery.writes_notes and slide.has_chords
        if needs_notes and not presentation_slide.notes.rtf_data:
            missing_notes.append(slide.label)

    report.check(
        "every slide carries a text element",
        missing_text == 0,
        f"{missing_text} slide(s) have no text",
    )
    if plan.config.chord_delivery.writes_notes:
        report.check(
            "every slide with chords carries notes",
            not missing_notes,
            f"missing on: {', '.join(missing_notes[:5])}",
        )


def verify_or_raise(payload: bytes, plan: SlidePlan) -> VerificationReport:
    """Verify, and refuse to continue if anything is wrong."""
    report = verify_bytes(payload, plan)
    if not report.ok:
        raise VerificationFailedError(
            "The presentation pcci built did not pass its own checks, so nothing was "
            "written. This is a bug in pcci, not a problem with your chart.",
            "; ".join(report.failures),
            context={"failures": report.failures, "checks": len(report.checks)},
        )
    return report
