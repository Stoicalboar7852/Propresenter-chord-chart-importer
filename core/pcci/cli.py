"""The ``pcci`` command line, and the JSON protocol the desktop apps speak.

The four-step flow is deliberate: ``analyze`` parses, the user corrects what the
parser guessed, ``plan`` turns a corrected song into slides, and ``build`` writes the
presentation. ``convert`` is the shortcut that runs all four in one go.

**Bridge contract.** With ``--json``, stdout carries exactly one JSON object and
nothing else; every log line and progress message goes to stderr as JSON Lines. Exit
codes: 0 success, 2 a problem with the user's file, 3 an unsupported format, 4 an
internal error. The front-ends must never parse human-readable text.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from pcci import __version__
from pcci.config import (
    MAX_LINES_PER_SLIDE,
    MIN_LINES_PER_SLIDE,
    ChordDelivery,
    ChordPlacementStyle,
    ConversionConfig,
    FontSpec,
)
from pcci.convert import build as build_from_plan
from pcci.convert import convert as run_conversion
from pcci.errors import OutputWriteError, PcciError, UserInputError
from pcci.ingest import supported_extensions
from pcci.ir import Song
from pcci.logging_setup import configure_logging, get_logger
from pcci.online import Cache, FetchedChart, Http
from pcci.online import search as search_online
from pcci.online.cache import cache_directory
from pcci.online.http import normalise_url
from pcci.online.retrieve import import_text, import_url, imports_directory
from pcci.parse.pipeline import analyze
from pcci.propresenter.bindings import PROTO_SOURCE_BUILD, PROTO_SOURCE_VERSION, load_bindings
from pcci.slides import SlidePlan, plan_slides

EXIT_OK = 0
EXIT_USER_INPUT = 2
EXIT_UNSUPPORTED = 3
EXIT_INTERNAL = 4


def emit(payload: dict[str, Any], *, as_json: bool, human: Callable[[], None]) -> None:
    """Write the single stdout object, or a human-readable summary."""
    if as_json:
        click.echo(json.dumps(payload, ensure_ascii=False))
    else:
        human()


def fail(error: PcciError, *, as_json: bool) -> int:
    """Report a typed error and return its exit code."""
    get_logger().error("%s: %s", type(error).__name__, error.technical_detail or error.user_message)
    if as_json:
        click.echo(json.dumps({"error": error.to_dict()}, ensure_ascii=False))
    else:
        click.echo(f"error: {error.user_message}", err=True)
        if error.technical_detail:
            click.echo(f"  detail: {error.technical_detail}", err=True)
    return error.exit_code


def run(action: Callable[[], int], *, as_json: bool) -> int:
    """Run a command body, turning every failure into an exit code."""
    try:
        return action()
    except PcciError as error:
        return fail(error, as_json=as_json)
    except Exception as exc:
        get_logger().exception("unexpected failure")
        wrapped = PcciError(
            "Something went wrong inside pcci. The log file has the details.",
            f"{type(exc).__name__}: {exc}",
        )
        return fail(wrapped, as_json=as_json)


def _style_options(function: Callable[..., Any]) -> Callable[..., Any]:
    """Options that describe how slides look."""
    function = click.option(
        "--font", default=None, help="PostScript font name, e.g. WorkSans-Black."
    )(function)
    function = click.option(
        "--font-family", default=None, help="Display font family, e.g. 'Work Sans'."
    )(function)
    function = click.option("--font-size", type=float, default=None, help="Lyric size in points.")(
        function
    )
    function = click.option(
        "--outline", type=float, default=None, help="Text outline width in points (0 for none)."
    )(function)
    function = click.option(
        "--slide-size", default=None, help="Slide size as WIDTHxHEIGHT, e.g. 1920x1080."
    )(function)
    function = click.option(
        "--all-caps/--no-all-caps", default=None, help="Force lyrics to upper case."
    )(function)
    return function


def _plan_options(function: Callable[..., Any]) -> Callable[..., Any]:
    """Options that describe how the song is split and how chords travel."""
    function = click.option(
        "-n",
        "--lines-per-slide",
        type=click.IntRange(MIN_LINES_PER_SLIDE, MAX_LINES_PER_SLIDE),
        default=None,
        help="Lyric lines per slide (default 4).",
    )(function)
    function = click.option(
        "--balance/--no-balance",
        default=None,
        help="Even out a section whose last slide would hold a single line.",
    )(function)
    function = click.option(
        "--chords",
        type=click.Choice([choice.value for choice in ChordDelivery]),
        default=None,
        help="How chords reach the stage screen (default both).",
    )(function)
    function = click.option(
        "--chords-on-slide/--no-chords-on-slide",
        default=None,
        help="Draw inline chords on the slide itself. This puts them on the AUDIENCE "
        "output too. Off by default.",
    )(function)
    function = click.option(
        "--chord-placement",
        type=click.Choice([choice.value for choice in ChordPlacementStyle]),
        default=None,
        help="Chords above or below the lyric in the notes block (default above).",
    )(function)
    return function


def build_config(**options: Any) -> ConversionConfig:
    """Turn CLI options into a ConversionConfig, leaving unset options at their default."""
    config = ConversionConfig()
    if options.get("lines_per_slide") is not None:
        config.lines_per_slide = options["lines_per_slide"]
    if options.get("balance") is not None:
        config.balance_last_slide = options["balance"]
    if options.get("chords") is not None:
        config.chord_delivery = ChordDelivery(options["chords"])
    if options.get("chord_placement") is not None:
        config.chord_placement = ChordPlacementStyle(options["chord_placement"])
    if options.get("chords_on_slide") is not None:
        config.chords_on_slide = options["chords_on_slide"]

    font = config.style.font
    requested_size = options.get("font_size")
    config.style.font = FontSpec(
        postscript_name=options.get("font") or font.postscript_name,
        family_name=options.get("font_family") or font.family_name,
        size=float(requested_size) if requested_size is not None else font.size,
        bold=font.bold,
        italic=font.italic,
    )
    if options.get("outline") is not None:
        config.style.outline_width = options["outline"]
    if options.get("all_caps") is not None:
        config.style.all_caps = options["all_caps"]
    if options.get("slide_size"):
        config.style.width, config.style.height = _parse_size(options["slide_size"])
    return config


def _parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = value.lower().replace(" ", "").split("x")
        return int(width), int(height)
    except ValueError as exc:
        raise UserInputError(
            f"Slide size {value!r} is not in the form WIDTHxHEIGHT, for example 1920x1080.",
            str(exc),
            context={"value": value},
        ) from exc


def expand_sources(sources: tuple[Path, ...]) -> list[Path]:
    """Every readable chart in the paths given, files and folders alike.

    A folder contributes every chart under it, at any depth, in a stable order.
    Anything the engine has no reader for is skipped rather than reported: dropping a
    folder of service files should not fail because the folder also holds a PowerPoint.
    """
    readable = supported_extensions()
    found: list[Path] = []
    seen: set[Path] = set()
    for source in sources:
        candidates = (
            sorted(path for path in source.rglob("*") if path.is_file())
            if source.is_dir()
            else [source]
        )
        for candidate in candidates:
            if candidate.name.startswith("."):
                continue
            if candidate.suffix.lower() not in readable:
                continue
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            found.append(candidate)
    return found


def unique_destination(directory: Path, source: Path, taken: set[str]) -> Path:
    """``directory/<name>.pro``, with a number appended rather than overwriting.

    Two folders can easily hold a Verse 1 and a Verse 1, and a batch that silently
    wrote one over the other would be worse than useless.
    """
    stem = source.stem
    candidate = stem
    counter = 2
    while candidate.casefold() in taken or (directory / f"{candidate}.pro").exists():
        candidate = f"{stem} {counter}"
        counter += 1
    taken.add(candidate.casefold())
    return directory / f"{candidate}.pro"


def _load_song(path: Path) -> Song:
    """Read a Song JSON produced by ``pcci analyze`` and possibly edited since."""
    try:
        return Song.from_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise UserInputError(
            f"{path.name} is not a song file pcci can read.",
            f"{type(exc).__name__}: {exc}",
            context={"path": str(path)},
        ) from exc


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="pcci")
@click.option("-v", "--verbose", is_flag=True, help="Log at debug level.")
@click.pass_context
def cli(context: click.Context, /, verbose: bool) -> None:
    """Turn chord charts into ProPresenter presentations."""
    context.ensure_object(dict)
    context.obj["verbose"] = verbose


@cli.command()
@click.argument("source", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("-o", "--output", type=click.Path(dir_okay=False, path_type=Path), default=None)
@_plan_options
@_style_options
@click.option("--chordpro", is_flag=True, help="Also write a .cho sidecar next to the .pro.")
@click.option("--json", "as_json", is_flag=True, help="Emit one JSON object on stdout.")
@click.pass_context
def convert(
    context: click.Context,
    /,
    source: Path,
    output: Path | None,
    as_json: bool,
    chordpro: bool,
    **options: Any,
) -> None:
    """Read a chord chart and write a ProPresenter presentation."""
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        config = build_config(**options)
        destination = output or source.with_suffix(".pro")
        result = run_conversion(source, destination, config, write_chordpro=chordpro)

        def human() -> None:
            click.echo(f"{result.plan.song.title} -> {result.output_path}")
            click.echo(
                f"  {result.plan.slide_count} slides in "
                f"{len(result.plan.song.sections)} sections, "
                f"{len(result.report.checks)} checks passed"
            )
            for page in result.chart_pages:
                click.echo(f"  chord chart page: {page}")
            for warning in result.warnings:
                click.echo(f"  note: {warning}")

        emit(result.to_dict(), as_json=as_json, human=human)
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="convert-all")
@click.argument("sources", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
@click.option(
    "-d",
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    required=True,
    help="Folder every presentation is written to.",
)
@_plan_options
@_style_options
@click.option("--chordpro", is_flag=True, help="Also write a .cho sidecar beside each .pro.")
@click.option("--json", "as_json", is_flag=True, help="Emit one JSON object on stdout.")
@click.pass_context
def convert_all(
    context: click.Context,
    /,
    sources: tuple[Path, ...],
    output_dir: Path,
    as_json: bool,
    chordpro: bool,
    **options: Any,
) -> None:
    """Convert many charts with one set of settings into one folder.

    Folders are searched for charts; files are taken as given. A chart that fails is
    reported and the rest still convert, because one unreadable file in a service
    folder should not cost you the other eleven.
    """
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        config = build_config(**options)
        charts = expand_sources(sources)
        if not charts:
            raise UserInputError(
                "None of those paths held a chart I can read.",
                f"looked at {len(sources)} path(s) for {', '.join(sorted(supported_extensions()))}",
            )
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise OutputWriteError(
                f"I could not make the folder {output_dir}.",
                f"{type(error).__name__}: {error}",
            ) from error

        results: list[dict[str, Any]] = []
        taken: set[str] = set()
        first_failure = EXIT_OK
        for chart in charts:
            destination = unique_destination(output_dir, chart, taken)
            try:
                result = run_conversion(chart, destination, config, write_chordpro=chordpro)
            except PcciError as error:
                get_logger().error("%s failed: %s", chart, error.user_message)
                results.append({"source": str(chart), "ok": False, "error": error.to_dict()})
                first_failure = first_failure or error.exit_code
            else:
                entry = result.to_dict()
                entry.update({"source": str(chart), "ok": True})
                results.append(entry)

        converted = sum(1 for entry in results if entry["ok"])
        payload: dict[str, Any] = {
            "output_dir": str(output_dir),
            "converted": converted,
            "failed": len(results) - converted,
            "results": results,
        }

        def human() -> None:
            for entry in results:
                name = Path(str(entry["source"])).name
                if entry["ok"]:
                    click.echo(f"  ok    {name} -> {Path(str(entry['output'])).name}")
                else:
                    click.echo(f"  FAIL  {name}: {entry['error']['user_message']}")
            click.echo(
                f"{converted} of {len(results)} converted into {output_dir}"
                if results
                else "nothing to convert"
            )

        emit(payload, as_json=as_json, human=human)
        return first_failure

    context.exit(run(action, as_json=as_json))


@cli.command(name="analyze")
@click.argument("source", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Emit the Song as JSON on stdout.")
@click.pass_context
def analyze_command(context: click.Context, /, source: Path, as_json: bool) -> None:
    """Parse a chart and print what was detected. Writes nothing."""
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        song = analyze(source)

        def human() -> None:
            click.echo(f"{song.title}" + (f" — {song.artist}" if song.artist else ""))
            for section in song.sections:
                flag = "" if section.confidence >= 0.95 else f"  (guessed, {section.confidence:g})"
                click.echo(f"  {section.label}: {len(section.lines)} lines{flag}")
            for warning in song.warnings:
                click.echo(f"  note: {warning}")

        emit(json.loads(song.to_json()), as_json=as_json, human=human)
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="plan")
@click.argument(
    "source", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=False
)
@click.option(
    "--song",
    "song_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
    help="Plan from a Song JSON the user has corrected, instead of a source document.",
)
@_plan_options
@_style_options
@click.option("--json", "as_json", is_flag=True, help="Emit the SlidePlan as JSON on stdout.")
@click.pass_context
def plan_command(
    context: click.Context,
    /,
    source: Path | None,
    song_path: Path | None,
    as_json: bool,
    **options: Any,
) -> None:
    """Parse a chart and print the slide plan. Writes nothing.

    Give it a document, or ``--song`` with a Song JSON the review screen has edited.
    Re-planning corrected sections is the engine's job, not the front-end's, so the
    chunking rules live in exactly one place.
    """
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        if (source is None) == (song_path is None):
            raise UserInputError(
                "Give pcci plan either a document or --song with a song file, not both.",
                f"source={source} song={song_path}",
            )
        song = _load_song(song_path) if song_path is not None else analyze(source)  # type: ignore[arg-type]
        plan = plan_slides(song, build_config(**options))

        def human() -> None:
            click.echo(f"{plan.song.title}: {plan.slide_count} slides")
            for slide in plan.slides:
                first = slide.lyrics[0] if slide.lyrics else "(instrumental)"
                click.echo(f"  {slide.label}: {len(slide.lines)} lines — {first}")

        emit(json.loads(plan.to_json()), as_json=as_json, human=human)
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="build")
@click.option(
    "--plan",
    "plan_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="A slide plan, as produced by `pcci plan --json` and edited by the user.",
)
@click.option("-o", "--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--chordpro", is_flag=True, help="Also write a .cho sidecar next to the .pro.")
@click.option("--json", "as_json", is_flag=True, help="Emit one JSON object on stdout.")
@click.pass_context
def build_command(
    context: click.Context, /, plan_path: Path, output: Path, chordpro: bool, as_json: bool
) -> None:
    """Write a presentation from a slide plan the user has reviewed."""
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        try:
            plan = SlidePlan.from_json(plan_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise UserInputError(
                f"{plan_path.name} is not a slide plan pcci can read.",
                f"{type(exc).__name__}: {exc}",
                context={"path": str(plan_path)},
            ) from exc
        result = build_from_plan(plan, output, write_chordpro=chordpro)

        def human() -> None:
            click.echo(f"{result.plan.song.title} -> {result.output_path}")
            click.echo(
                f"  {result.plan.slide_count} slides, {len(result.report.checks)} checks passed"
            )

        emit(result.to_dict(), as_json=as_json, human=human)
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="search")
@click.argument("query", nargs=-1, required=True)
@click.option("--limit", type=click.IntRange(1, 60), default=20, help="How many results.")
@click.option("--artist", default=None, help="Only songs by this artist. Also improves the search.")
@click.option("--album", default=None, help="Only songs from this album.")
@click.option("--year", type=int, default=None, help="Only songs released in this year.")
@click.option("--no-cache", is_flag=True, help="Ask the sites again rather than reusing answers.")
@click.option("--json", "as_json", is_flag=True, help="Emit the results as JSON on stdout.")
@click.pass_context
def search_command(
    context: click.Context,
    /,
    query: tuple[str, ...],
    limit: int,
    artist: str | None,
    album: str | None,
    year: int | None,
    no_cache: bool,
    as_json: bool,
) -> None:
    """Find a song online by name, or describe a link you have pasted.

    Every source is asked at once and the answers are merged into one row per song, so
    a result can carry chords from one site and its cover art from another. A site
    that is down contributes a note and the search carries on without it.
    """
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        text = " ".join(query).strip()
        cache = Cache(enabled=not no_cache)
        # A pasted link goes through the same call: search recognises one and describes
        # that page instead of searching for it.
        outcome = search_online(
            text,
            limit=limit,
            artist=artist,
            album=album,
            year=year,
            http=Http(),
            cache=cache,
        )

        def human() -> None:
            for match in outcome.results:
                words = "chords" if match.has_chords else match.chart_kind
                mark = f"[{words}]" if match.importable else "[no words]"
                click.echo(f"{mark:>10}  {match.title}")
                if match.subtitle:
                    click.echo(f"            {match.subtitle}")
                click.echo(f"            via {', '.join(match.source_names)}")
                if match.chart_url:
                    click.echo(f"            {match.chart_url}")
            for note in outcome.notes:
                click.echo(f"  note: {note}")
            if not outcome.results:
                click.echo("Nothing found.")
            elif outcome.has_more:
                click.echo(
                    f"  showing {len(outcome.results)} of {outcome.total_found}; "
                    f"--limit {min(outcome.total_found, 60)} for the rest"
                )

        emit(json.loads(outcome.model_dump_json()), as_json=as_json, human=human)
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


def _import_options(function: Callable[..., Any]) -> Callable[..., Any]:
    """Options shared by the two commands that bring a chart in from outside."""
    function = click.option(
        "-d",
        "--dir",
        "directory",
        type=click.Path(file_okay=False, path_type=Path),
        default=None,
        help="Where to save the downloaded chart (default: the app's own cache).",
    )(function)
    function = click.option(
        "-o",
        "--output",
        type=click.Path(dir_okay=False, path_type=Path),
        default=None,
        help="Also convert it straight to a .pro at this path.",
    )(function)
    function = click.option("--json", "as_json", is_flag=True, help="Emit one JSON object.")(
        function
    )
    return function


def _imported_payload(
    path: Path, chart: FetchedChart, converted: dict[str, Any] | None
) -> dict[str, Any]:
    """The one object ``fetch`` and ``paste`` put on stdout."""
    payload: dict[str, Any] = {
        "path": str(path),
        "title": chart.title,
        "artist": chart.artist,
        "chart_kind": chart.chart_kind,
        "has_chords": chart.has_chords,
        "source": chart.source.model_dump(),
        "notes": chart.notes,
    }
    if converted is not None:
        payload["converted"] = converted
    return payload


def _maybe_convert(
    path: Path, output: Path | None, options: dict[str, Any]
) -> dict[str, Any] | None:
    if output is None:
        return None
    return run_conversion(path, output, build_config(**options)).to_dict()


def _report_import(path: Path, chart: FetchedChart, converted: dict[str, Any] | None) -> None:
    click.echo(f"{chart.title} -> {path}")
    if chart.artist:
        click.echo(f"  by {chart.artist}, from {chart.source.name}")
    else:
        click.echo(f"  from {chart.source.name}")
    if not chart.has_chords:
        click.echo("  words only: this source had no chords for it")
    for note in chart.notes:
        click.echo(f"  note: {note}")
    if converted is not None:
        click.echo(f"  converted to {converted['output']} ({converted['slides']} slides)")


@cli.command(name="fetch")
@click.argument("url")
@click.option("--no-cache", is_flag=True, help="Download again rather than reusing a saved copy.")
@_import_options
@_plan_options
@_style_options
@click.pass_context
def fetch_command(
    context: click.Context,
    /,
    url: str,
    directory: Path | None,
    output: Path | None,
    no_cache: bool,
    as_json: bool,
    **options: Any,
) -> None:
    """Download the chart at a link and save it where the rest of pcci can read it.

    This writes a chart file and prints where it went; ``analyze``, ``plan`` and
    ``build`` then work on it exactly as they would on a file you dropped in
    yourself. Pass ``-o`` to go straight to a presentation instead.
    """
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        cache = Cache(enabled=not no_cache)
        path, chart = import_url(normalise_url(url), directory, http=Http(), cache=cache)
        converted = _maybe_convert(path, output, options)
        emit(
            _imported_payload(path, chart, converted),
            as_json=as_json,
            human=lambda: _report_import(path, chart, converted),
        )
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="paste")
@click.option("--title", default=None, help="Name the song, instead of reading it off the top.")
@_import_options
@_plan_options
@_style_options
@click.pass_context
def paste_command(
    context: click.Context,
    /,
    title: str | None,
    directory: Path | None,
    output: Path | None,
    as_json: bool,
    **options: Any,
) -> None:
    """Read a chart from standard input - what the apps' Import from Clipboard sends.

    Text copied out of a browser, an email or a PDF is the same problem as a link:
    some words, possibly some chords, and no file. This makes it a file.
    """
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json)

    def action() -> int:
        pasted = sys.stdin.read()
        path, chart = import_text(pasted, directory, title=title)
        converted = _maybe_convert(path, output, options)
        emit(
            _imported_payload(path, chart, converted),
            as_json=as_json,
            human=lambda: _report_import(path, chart, converted),
        )
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="cache")
@click.option("--clear", is_flag=True, help="Delete everything pcci has downloaded.")
@click.option("--json", "as_json", is_flag=True, help="Emit one JSON object on stdout.")
@click.pass_context
def cache_command(context: click.Context, /, clear: bool, as_json: bool) -> None:
    """Show, or empty, the copies pcci keeps of pages it has downloaded.

    Worth emptying when a site has corrected a chart and pcci keeps handing you
    yesterday's. Nothing here is ever the only copy of anything.
    """
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json, to_file=False)

    def action() -> int:
        pages = cache_directory()
        charts = imports_directory()
        removed = Cache().clear() if clear else 0
        payload = {
            "pages": str(pages),
            "imported_charts": str(charts),
            "cleared": removed if clear else None,
        }

        def human() -> None:
            click.echo(f"downloaded pages:  {pages}")
            click.echo(f"imported charts:   {charts}")
            if clear:
                click.echo(f"cleared {removed} page(s)")

        emit(payload, as_json=as_json, human=human)
        return EXIT_OK

    context.exit(run(action, as_json=as_json))


@cli.command(name="doctor")
@click.option("--json", "as_json", is_flag=True, help="Emit the report as JSON on stdout.")
@click.pass_context
def doctor_command(context: click.Context, /, as_json: bool) -> None:
    """Check that this installation can actually do its job."""
    configure_logging(verbose=context.obj["verbose"], json_logs=as_json, to_file=False)

    def action() -> int:
        checks: list[dict[str, Any]] = []

        def record(name: str, ok: bool, detail: str) -> None:
            checks.append({"check": name, "ok": ok, "detail": detail})

        record("python", sys.version_info >= (3, 12), sys.version.split()[0])
        try:
            bindings = load_bindings()
            fields = len(bindings.presentation.Presentation.DESCRIPTOR.fields)
            record("protobuf bindings", True, f"{fields} presentation fields")
            record(
                "schema version",
                True,
                f"ProPresenter {PROTO_SOURCE_VERSION} build {PROTO_SOURCE_BUILD}",
            )
        except PcciError as error:
            record("protobuf bindings", False, error.technical_detail)

        for module, label in (
            ("pymupdf", "PDF"),
            ("docx", "Word"),
            ("odf", "OpenDocument"),
            ("striprtf", "RTF"),
            ("bs4", "HTML"),
            ("charset_normalizer", "encoding detection"),
        ):
            try:
                __import__(module)
                record(f"{label} support", True, module)
            except ImportError as exc:
                record(f"{label} support", False, str(exc))

        record("formats", True, " ".join(supported_extensions()))
        healthy = all(check["ok"] for check in checks)

        def human() -> None:
            for check in checks:
                mark = "ok  " if check["ok"] else "FAIL"
                click.echo(f"{mark} {check['check']}: {check['detail']}")

        emit({"ok": healthy, "checks": checks}, as_json=as_json, human=human)
        return EXIT_OK if healthy else EXIT_INTERNAL

    context.exit(run(action, as_json=as_json))


def main() -> None:
    """Console-script entry point."""
    cli(obj={}, standalone_mode=True)


if __name__ == "__main__":
    main()
