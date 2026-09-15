#!/usr/bin/env python3
"""Decode a ProPresenter ``.pro`` (or ``.probundle``) and print what is inside it.

    core/.venv/bin/python scripts/dump_pro.py FILE [--full] [--cue N]

``--full`` prints the entire message tree in protobuf text format; the default is a
structural summary (groups, colours, cues, notes, chord charts) that fits on a screen.
Every claim in docs/FORMAT_NOTES.md is reproducible with this script.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zipfile
import zlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from pcci.propresenter.bindings import load_bindings  # noqa: E402


def read_bundle(path: Path) -> dict[str, bytes]:
    """Extract a .probundle.

    ProPresenter writes zip64 headers that Python's zipfile rejects ("corrupt zip64
    end of central directory record"), so the central directory is walked by hand.
    """
    data = path.read_bytes()
    entries: dict[str, bytes] = {}
    offset = 0
    while True:
        offset = data.find(b"PK\x01\x02", offset)
        if offset < 0:
            break
        (
            _ver,
            _need,
            _flags,
            method,
            _mt,
            _md,
            _crc,
            csize,
            usize,
            name_len,
            extra_len,
            comment_len,
            _disk,
            _iattr,
            _eattr,
            local_offset,
        ) = struct.unpack_from("<HHHHHHIIIHHHHHII", data, offset + 4)
        name = data[offset + 46 : offset + 46 + name_len].decode("utf-8", "replace")
        extra = data[offset + 46 + name_len : offset + 46 + name_len + extra_len]
        real_c, real_local = csize, local_offset
        cursor = 0
        while cursor + 4 <= len(extra):
            header_id, header_size = struct.unpack_from("<HH", extra, cursor)
            body = extra[cursor + 4 : cursor + 4 + header_size]
            if header_id == 0x0001:
                values = list(struct.unpack_from("<" + "Q" * (len(body) // 8), body))
                iterator = iter(values)
                if usize == 0xFFFFFFFF:
                    next(iterator)
                if csize == 0xFFFFFFFF:
                    real_c = next(iterator)
                if local_offset == 0xFFFFFFFF:
                    real_local = next(iterator)
            cursor += 4 + header_size
        local_name_len, local_extra_len = struct.unpack_from("<HH", data, real_local + 26)
        start = real_local + 30 + local_name_len + local_extra_len
        blob = data[start : start + real_c]
        if method == 8:
            blob = zlib.decompress(blob, -15)
        entries[name] = blob
        offset += 46 + name_len + extra_len + comment_len
    return entries


def load_presentation(path: Path) -> tuple[object, bytes]:
    bindings = load_bindings()
    if path.suffix == ".probundle" or zipfile.is_zipfile(path):
        entries = read_bundle(path)
        pro = next((v for k, v in entries.items() if k.endswith(".pro")), None)
        if pro is None:
            msg = f"no .pro inside {path.name}"
            raise SystemExit(msg)
        print(f"# bundle contains {len(entries)} entries:")
        for name in entries:
            print(f"#   {name}")
        payload = pro
    else:
        payload = path.read_bytes()
    presentation = bindings.presentation.Presentation()
    presentation.ParseFromString(payload)
    return presentation, payload


def summarise(presentation, payload: bytes) -> None:  # noqa: ANN001 - protobuf message
    bindings = load_bindings()
    info = presentation.application_info
    version = info.application_version
    platform_version = info.platform_version
    app_enum = bindings.application_info.ApplicationInfo
    print(f"name           : {presentation.name!r}")
    print(f"uuid           : {presentation.uuid.string}")
    print(f"category       : {presentation.category!r}")
    print(
        "application    : "
        f"{app_enum.Application.Name(info.application)} "
        f"{version.major_version}.{version.minor_version}.{version.patch_version} "
        f"build {version.build}"
    )
    print(
        "platform       : "
        f"{app_enum.Platform.Name(info.platform)} "
        f"{platform_version.major_version}.{platform_version.minor_version}."
        f"{platform_version.patch_version}"
    )
    print(f"cues           : {len(presentation.cues)}")
    print(f"cue groups     : {len(presentation.cue_groups)}")
    print(f"arrangements   : {len(presentation.arrangements)}")
    print(f"round-trip     : {'byte-identical' if presentation.SerializeToString() == payload else 'DIFFERS'}")

    print("\n== cue groups ==")
    for index, cue_group in enumerate(presentation.cue_groups):
        group = cue_group.group
        colour = group.color
        hex_value = "#%02X%02X%02X" % (
            round(colour.red * 255),
            round(colour.green * 255),
            round(colour.blue * 255),
        )
        hot_key = group.hotKey.code if group.HasField("hotKey") else None
        print(
            f"{index:2d} {group.name:<14} {hex_value} "
            f"rgba=({colour.red:.6f},{colour.green:.6f},{colour.blue:.6f},{colour.alpha:g}) "
            f"hotkey={hot_key} cues={len(cue_group.cue_identifiers)} "
            f"app_group={group.application_group_identifier.string or '-'}"
        )

    print("\n== cues ==")
    for index, cue in enumerate(presentation.cues):
        texts: list[str] = []
        notes = ""
        chart = ""
        for action in cue.actions:
            slide = action.slide.presentation
            for element in slide.base_slide.elements:
                if element.element.HasField("text"):
                    texts.append(rtf_plain_text(element.element.text.rtf_data))
            if slide.notes.rtf_data:
                notes = rtf_plain_text(slide.notes.rtf_data)
            if slide.chord_chart.absolute_string or slide.chord_chart.local.path:
                chart = slide.chord_chart.local.path or slide.chord_chart.absolute_string
        joined = " / ".join(t.replace("\n", " ⏎ ") for t in texts if t)
        print(f"{index:2d} {cue.uuid.string[:8]} {joined[:70]!r}")
        if notes:
            print(f"     notes: {notes[:70]!r}")
        if chart:
            print(f"     chord_chart: {chart}")


def rtf_plain_text(rtf: bytes) -> str:
    """Crude RTF-to-text, good enough for inspection output."""
    if not rtf:
        return ""
    text = rtf.decode("utf-8", "replace")
    body = text.rsplit("\\cf2 ", 1)[-1] if "\\cf2 " in text else text
    body = body.replace("\\CocoaLigature0 ", "").replace("\\\n", "\n")
    out: list[str] = []
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\":
            index += 1
            word = ""
            while index < len(body) and body[index].isalpha():
                word += body[index]
                index += 1
            if word == "line" or word == "par":
                out.append("\n")
            if index < len(body) and body[index] == " ":
                index += 1
            continue
        if char in "{}":
            index += 1
            continue
        out.append(char)
        index += 1
    return "".join(out).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--full", action="store_true", help="print the whole message tree")
    parser.add_argument("--cue", type=int, help="print one cue's full message tree")
    args = parser.parse_args()

    presentation, payload = load_presentation(args.file)
    if args.full:
        from google.protobuf import text_format

        print(text_format.MessageToString(presentation, as_utf8=True))
        return 0
    if args.cue is not None:
        from google.protobuf import text_format

        print(text_format.MessageToString(presentation.cues[args.cue], as_utf8=True))
        return 0
    summarise(presentation, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
