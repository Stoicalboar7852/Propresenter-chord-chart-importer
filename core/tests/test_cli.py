"""The CLI, and the JSON contract the desktop front-ends depend on.

The contract is the point of these tests: stdout carries exactly one JSON object,
stderr carries JSON Lines, and the exit code says what kind of failure happened. The
UIs must never have to parse prose.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from pcci.cli import EXIT_INTERNAL, EXIT_UNSUPPORTED, EXIT_USER_INPUT, cli
from pcci.propresenter.bindings import load_bindings

CHART = "GOODBYE YESTERDAY A.docx"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def invoke(runner: CliRunner, *args: str):
    return runner.invoke(cli, list(args), obj={}, catch_exceptions=False)


def test_doctor_reports_a_healthy_install(runner: CliRunner) -> None:
    result = invoke(runner, "doctor", "--json")
    payload = json.loads(result.stdout)
    assert result.exit_code == 0
    assert payload["ok"] is True
    assert any(check["check"] == "schema version" for check in payload["checks"])


def test_analyze_emits_one_json_object(runner: CliRunner, fixtures_dir: Path) -> None:
    result = invoke(runner, "analyze", str(fixtures_dir / CHART), "--json")
    assert result.exit_code == 0
    payload = json.loads(result.stdout)  # raises if stdout is not exactly one object
    assert payload["title"] == "GOODBYE YESTERDAY"
    assert len(payload["sections"]) == 14


def test_plan_emits_a_slide_plan(runner: CliRunner, fixtures_dir: Path) -> None:
    result = invoke(runner, "plan", str(fixtures_dir / CHART), "-n", "2", "--json")
    payload = json.loads(result.stdout)
    assert result.exit_code == 0
    assert payload["config"]["lines_per_slide"] == 2
    assert all(len(slide["lines"]) <= 2 for slide in payload["slides"])


def test_convert_writes_a_presentation(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    output = tmp_path / "song.pro"
    result = invoke(runner, "convert", str(fixtures_dir / CHART), "-o", str(output), "--json")
    payload = json.loads(result.stdout)
    assert result.exit_code == 0
    assert Path(payload["output"]) == output
    assert output.exists()

    presentation = load_bindings().presentation.Presentation()
    presentation.ParseFromString(output.read_bytes())
    assert len(presentation.cues) == payload["slides"]


def test_the_analyze_plan_build_flow(runner: CliRunner, fixtures_dir: Path, tmp_path: Path) -> None:
    """The flow the review screen depends on: plan, edit, build."""
    plan_result = invoke(runner, "plan", str(fixtures_dir / CHART), "--json")
    plan = json.loads(plan_result.stdout)

    # The user renames a section and drops a slide, as the review screen would.
    plan["song"]["sections"][0]["type"] = "Pre-Chorus"
    plan["slides"][0]["section_label"] = "Pre-Chorus"
    removed = plan["slides"].pop()
    assert removed

    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    output = tmp_path / "edited.pro"
    build_result = invoke(runner, "build", "--plan", str(plan_path), "-o", str(output), "--json")
    assert build_result.exit_code == 0
    payload = json.loads(build_result.stdout)
    assert payload["slides"] == len(plan["slides"])

    presentation = load_bindings().presentation.Presentation()
    presentation.ParseFromString(output.read_bytes())
    # The section keeps its number, so renaming the type gives "Pre-Chorus 1".
    assert presentation.cue_groups[0].group.name == "Pre-Chorus 1"


def test_lines_per_slide_is_respected(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    for count in (1, 2, 6):
        output = tmp_path / f"song-{count}.pro"
        result = invoke(
            runner,
            "convert",
            str(fixtures_dir / CHART),
            "-o",
            str(output),
            "-n",
            str(count),
            "--json",
        )
        payload = json.loads(result.stdout)
        assert payload["slides"] >= 14
        assert output.exists()


def test_chords_none_writes_no_notes_and_no_images(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    output = tmp_path / "song.pro"
    result = invoke(
        runner,
        "convert",
        str(fixtures_dir / CHART),
        "-o",
        str(output),
        "--chords",
        "none",
        "--json",
    )
    payload = json.loads(result.stdout)
    assert payload["chart_pages"] == []
    assert not list(tmp_path.glob("*.png"))


def test_style_options_reach_the_file(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    output = tmp_path / "song.pro"
    invoke(
        runner,
        "convert",
        str(fixtures_dir / CHART),
        "-o",
        str(output),
        "--font",
        "Helvetica-Bold",
        "--font-family",
        "Helvetica",
        "--font-size",
        "48",
        "--outline",
        "2.5",
        "--slide-size",
        "1280x720",
        "--json",
    )
    presentation = load_bindings().presentation.Presentation()
    presentation.ParseFromString(output.read_bytes())
    element = presentation.cues[0].actions[0].slide.presentation.base_slide.elements[0].element
    assert element.text.attributes.font.name == "Helvetica-Bold"
    assert element.text.attributes.font.size == 48.0
    assert element.text.attributes.stroke_width == 2.5
    slide = presentation.cues[0].actions[0].slide.presentation.base_slide
    assert (slide.size.width, slide.size.height) == (1280.0, 720.0)


def test_chordpro_sidecar(runner: CliRunner, fixtures_dir: Path, tmp_path: Path) -> None:
    output = tmp_path / "song.pro"
    result = invoke(
        runner, "convert", str(fixtures_dir / CHART), "-o", str(output), "--chordpro", "--json"
    )
    payload = json.loads(result.stdout)
    sidecar = Path(payload["chordpro"])
    assert sidecar.exists()
    assert sidecar.read_text(encoding="utf-8").startswith("{title:")


def test_logs_go_to_stderr_as_json_lines(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    result = invoke(
        runner, "convert", str(fixtures_dir / CHART), "-o", str(tmp_path / "s.pro"), "--json"
    )
    assert result.exit_code == 0
    # stdout stays a single JSON object even while progress is being reported.
    json.loads(result.stdout)
    lines = [line for line in result.stderr.splitlines() if line.strip()]
    assert lines, "expected progress logs on stderr"
    for line in lines:
        payload = json.loads(line)
        assert set(payload) >= {"level", "msg", "ts"}


def test_unsupported_format_exits_three(runner: CliRunner, tmp_path: Path) -> None:
    source = tmp_path / "chart.pages"
    source.write_text("nope")
    result = invoke(runner, "convert", str(source), "-o", str(tmp_path / "x.pro"), "--json")
    assert result.exit_code == EXIT_UNSUPPORTED
    payload = json.loads(result.stdout)
    assert payload["error"]["kind"] == "unsupported_format"
    assert payload["error"]["user_message"]


def test_scanned_pdf_exits_two_with_advice(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    result = invoke(
        runner,
        "convert",
        str(fixtures_dir / "pdf" / "scanned_no_text_layer.pdf"),
        "-o",
        str(tmp_path / "x.pro"),
        "--json",
    )
    assert result.exit_code == EXIT_USER_INPUT
    payload = json.loads(result.stdout)
    assert payload["error"]["kind"] == "image_only_pdf"
    assert "scan" in payload["error"]["user_message"]


def test_a_broken_plan_file_is_a_user_error(runner: CliRunner, tmp_path: Path) -> None:
    plan_path = tmp_path / "plan.json"
    plan_path.write_text("{not json", encoding="utf-8")
    result = invoke(
        runner, "build", "--plan", str(plan_path), "-o", str(tmp_path / "x.pro"), "--json"
    )
    assert result.exit_code == EXIT_USER_INPUT
    assert json.loads(result.stdout)["error"]["kind"] == "user_input"


def test_an_unexpected_failure_exits_four(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def explode(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr("pcci.cli.run_conversion", explode)
    result = invoke(
        runner, "convert", str(fixtures_dir / CHART), "-o", str(tmp_path / "x.pro"), "--json"
    )
    assert result.exit_code == EXIT_INTERNAL
    payload = json.loads(result.stdout)
    assert payload["error"]["kind"] == "internal"
    assert "boom" in payload["error"]["technical_detail"]


def test_bad_slide_size_is_reported(runner: CliRunner, fixtures_dir: Path, tmp_path: Path) -> None:
    result = invoke(
        runner,
        "convert",
        str(fixtures_dir / CHART),
        "-o",
        str(tmp_path / "x.pro"),
        "--slide-size",
        "huge",
        "--json",
    )
    assert result.exit_code == EXIT_USER_INPUT
    assert "1920x1080" in json.loads(result.stdout)["error"]["user_message"]


def test_human_output_is_not_json(runner: CliRunner, fixtures_dir: Path) -> None:
    result = invoke(runner, "analyze", str(fixtures_dir / CHART))
    assert result.exit_code == 0
    assert "GOODBYE YESTERDAY" in result.stdout
    with pytest.raises(json.JSONDecodeError):
        json.loads(result.stdout)


def test_convert_all_writes_every_chart_into_one_folder(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    """The batch the app's Convert All button drives: one setting, many charts."""
    inbox = tmp_path / "in"
    (inbox / "nested").mkdir(parents=True)
    for name in (CHART, "chordpro/goodbye_yesterday.cho"):
        shutil.copy(fixtures_dir / name, inbox / Path(name).name)
    # Same stem as the file above, in a subfolder: batches routinely hit this.
    shutil.copy(fixtures_dir / "chordpro/goodbye_yesterday.cho", inbox / "nested")
    # Something the engine has no reader for is skipped, not fatal.
    (inbox / "set list.pptx").write_bytes(b"not a chart")

    outbox = tmp_path / "out"
    result = invoke(runner, "convert-all", str(inbox), "-d", str(outbox), "-n", "6", "--json")
    payload = json.loads(result.stdout)

    assert result.exit_code == 0
    assert payload["failed"] == 0
    assert payload["converted"] == 3
    written = sorted(path.name for path in outbox.glob("*.pro"))
    assert written == [
        "GOODBYE YESTERDAY A.pro",
        "goodbye_yesterday 2.pro",
        "goodbye_yesterday.pro",
    ]
    assert all(entry["ok"] for entry in payload["results"])


def test_convert_all_keeps_going_after_one_bad_chart(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    inbox = tmp_path / "in"
    inbox.mkdir()
    shutil.copy(fixtures_dir / CHART, inbox)
    (inbox / "empty.txt").write_text("nothing that looks like a song\n", encoding="utf-8")

    outbox = tmp_path / "out"
    result = invoke(runner, "convert-all", str(inbox), "-d", str(outbox), "--json")
    payload = json.loads(result.stdout)

    assert result.exit_code == EXIT_USER_INPUT
    assert payload["converted"] == 1
    assert payload["failed"] == 1
    failure = next(entry for entry in payload["results"] if not entry["ok"])
    assert failure["error"]["user_message"]
    assert (outbox / "GOODBYE YESTERDAY A.pro").exists()


def test_convert_all_rejects_a_folder_with_nothing_readable(
    runner: CliRunner, tmp_path: Path
) -> None:
    inbox = tmp_path / "in"
    inbox.mkdir()
    (inbox / "slides.pptx").write_bytes(b"not a chart")

    result = invoke(runner, "convert-all", str(inbox), "-d", str(tmp_path / "out"), "--json")
    payload = json.loads(result.stdout)

    assert result.exit_code == EXIT_USER_INPUT
    assert "chart" in payload["error"]["user_message"]


def test_convert_all_never_overwrites_an_existing_presentation(
    runner: CliRunner, fixtures_dir: Path, tmp_path: Path
) -> None:
    outbox = tmp_path / "out"
    outbox.mkdir()
    existing = outbox / "GOODBYE YESTERDAY A.pro"
    existing.write_bytes(b"older export")

    result = invoke(runner, "convert-all", str(fixtures_dir / CHART), "-d", str(outbox), "--json")
    payload = json.loads(result.stdout)

    assert result.exit_code == 0
    assert existing.read_bytes() == b"older export"
    assert Path(payload["results"][0]["output"]).name == "GOODBYE YESTERDAY A 2.pro"
