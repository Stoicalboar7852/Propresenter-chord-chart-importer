"""The whole conversion, start to finish.

``analyze`` -> ``plan_slides`` -> build -> ``verify`` -> write.

The build step is whichever writer the plan asks for - ProPresenter or FreeShow - and
both are held to the same rule: nothing reaches disk until the bytes have been read
back and checked against the plan, and the file itself is written through a temporary
and moved into place, so an interrupted run cannot leave a half-written presentation
where a working one used to be.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from pcci.chordpro_out import song_to_chordpro
from pcci.config import ConversionConfig, ExportTarget
from pcci.errors import OutputWriteError
from pcci.freeshow.verify import verify_or_raise as verify_show
from pcci.freeshow.writer import build_show, show_bytes
from pcci.ir import Song
from pcci.logging_setup import get_logger
from pcci.parse.pipeline import analyze
from pcci.propresenter.chart import ChartRender, render_chart_pages
from pcci.propresenter.verify import verify_or_raise
from pcci.propresenter.writer import build_presentation, presentation_bytes
from pcci.slides import SlidePlan, plan_slides
from pcci.verification import VerificationReport


@dataclass
class ConversionResult:
    """What a conversion produced."""

    output_path: Path
    plan: SlidePlan
    report: VerificationReport
    chart_pages: list[Path] = field(default_factory=list)
    chordpro_path: Path | None = None

    @property
    def warnings(self) -> list[str]:
        return self.plan.warnings

    def to_dict(self) -> dict[str, object]:
        return {
            "output": str(self.output_path),
            "target": self.plan.config.export_target.value,
            "slides": self.plan.slide_count,
            "sections": len(self.plan.song.sections),
            "title": self.plan.song.title,
            "chart_pages": [str(path) for path in self.chart_pages],
            "chordpro": str(self.chordpro_path) if self.chordpro_path else None,
            "checks": len(self.report.checks),
            "warnings": self.warnings,
        }


def convert(
    source: Path,
    output: Path,
    config: ConversionConfig | None = None,
    *,
    write_chordpro: bool = False,
) -> ConversionResult:
    """Read a chart and write a presentation for whichever program was asked for."""
    config = config or ConversionConfig()
    song = analyze(source)
    plan = plan_slides(song, config)
    return build(plan, output, write_chordpro=write_chordpro)


def build(
    plan: SlidePlan,
    output: Path,
    *,
    write_chordpro: bool = False,
) -> ConversionResult:
    """Write a presentation from a plan the user may already have edited."""
    logger = get_logger()
    config = plan.config
    target = config.export_target
    output = output if output.suffix == target.extension else output.with_suffix(target.extension)
    directory = output.parent

    if target is ExportTarget.FREESHOW:
        return _build_freeshow(plan, output, write_chordpro=write_chordpro)

    chart: ChartRender | None = None
    if config.chord_delivery.writes_chart and plan.song.chord_count:
        # The chart is a chord chart: it always carries the words, whatever the notes
        # block is set to. chord_placement describes the notes, not the chart.
        chart = render_chart_pages(plan.song, directory, stem=output.stem)
        logger.info("rendered %d chord chart page(s)", len(chart.pages))
    elif config.chord_delivery.writes_chart:
        # A lyrics-only song has no chart to attach. Rendering one anyway would leave
        # a PNG of the words beside the presentation and point every slide at it,
        # which is a puzzle for whoever opens the folder rather than a feature.
        logger.info("no chords in this song, so no chord chart page was rendered")

    presentation = build_presentation(
        plan,
        chart_pages=chart.pages if chart else None,
        page_for_section=chart.page_for_section if chart else None,
    )
    payload = presentation_bytes(presentation)
    report = verify_or_raise(payload, plan)
    logger.info("verification passed (%d checks)", len(report.checks))

    _write_atomically(output, payload)

    chordpro_path: Path | None = None
    if write_chordpro:
        chordpro_path = output.with_suffix(".cho")
        _write_atomically(chordpro_path, song_to_chordpro(plan.song).encode("utf-8"))

    return ConversionResult(
        output_path=output,
        plan=plan,
        report=report,
        chart_pages=[page.absolute_path for page in chart.pages] if chart else [],
        chordpro_path=chordpro_path,
    )


def _build_freeshow(
    plan: SlidePlan,
    output: Path,
    *,
    write_chordpro: bool = False,
) -> ConversionResult:
    """Write a FreeShow ``.show``.

    No chart pages: FreeShow has no per-slide chord-chart image to point at, so a route
    that asks for one says so rather than rendering PNGs nobody will ever see.
    """
    logger = get_logger()
    if plan.config.chord_delivery.writes_chart:
        plan.warnings.append(
            "FreeShow has no chord-chart element, so the chart was not rendered. "
            "The chords still travel in the slide text and the slide notes."
        )

    show_id, show = build_show(plan)
    payload = show_bytes(show_id, show)
    report = verify_show(payload, plan)
    logger.info("verification passed (%d checks)", len(report.checks))

    _write_atomically(output, payload)

    chordpro_path: Path | None = None
    if write_chordpro:
        chordpro_path = output.with_suffix(".cho")
        _write_atomically(chordpro_path, song_to_chordpro(plan.song).encode("utf-8"))

    return ConversionResult(
        output_path=output,
        plan=plan,
        report=report,
        chart_pages=[],
        chordpro_path=chordpro_path,
    )


def analyze_song(source: Path) -> Song:
    """Parse a chart without writing anything."""
    return analyze(source)


def plan_for(source: Path, config: ConversionConfig | None = None) -> SlidePlan:
    """Parse and plan, ready for the user to review."""
    return plan_slides(analyze(source), config or ConversionConfig())


def _write_atomically(path: Path, payload: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_bytes(payload)
        temporary.replace(path)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise OutputWriteError(
            f"pcci could not write {path.name}. Check that the folder exists and is writable.",
            str(exc),
            context={"path": str(path)},
        ) from exc
