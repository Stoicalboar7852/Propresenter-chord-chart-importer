"""Building a ProPresenter presentation from a slide plan.

Every structure here was copied from a real 21.4 export and is documented in
docs/FORMAT_NOTES.md. Where the reference file sets a field that looks redundant
(``partightenfactor``, ``info = 3``, an empty ``hot_key``), this writer sets it too:
matching what the application itself writes is cheaper than finding out later which of
those fields mattered.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pcci.config import RGBA, ConversionConfig
from pcci.ir import Section
from pcci.logging_setup import current_platform
from pcci.notes import render_lines
from pcci.propresenter.bindings import PROTO_SOURCE_BUILD, Bindings, load_bindings
from pcci.propresenter.groups import GroupAssigner, new_uuid
from pcci.propresenter.rtf import build_notes_rtf, build_rtf
from pcci.slides import Slide, SlidePlan

ZERO_UUID = "00000000-0000-0000-0000-000000000000"

#: The ProPresenter release the vendored schema describes; written into every file.
APPLICATION_VERSION = (21, 4, 0)

#: The reference export marks its lyric element with this. Copied verbatim.
LYRIC_ELEMENT_INFO = 3

#: ProPresenter's own default for the delimiter used when a text transform joins lines.
TRANSFORM_DELIMITER = "  •  "


@dataclass(frozen=True, slots=True)
class ChordChartPage:
    """One rendered page of the chord chart, and where it will live."""

    absolute_path: Path
    show_relative_path: str


def _set_colour(target: Any, colour: RGBA) -> None:
    target.red = colour.red
    target.green = colour.green
    target.blue = colour.blue
    target.alpha = colour.alpha


def _set_uuid(target: Any, value: str) -> None:
    target.string = value


def _is_windows() -> bool:
    """Read the platform through a function so type checking keeps both branches.

    See ``pcci.logging_setup.current_platform`` — a checker running on one platform
    narrows ``sys.platform`` to a literal and calls the others dead code.
    """
    return current_platform() == "win32"


def _platform(bindings: Bindings) -> int:
    info = bindings.application_info.ApplicationInfo
    if _is_windows():
        return int(info.Platform.PLATFORM_WINDOWS)
    return int(info.Platform.PLATFORM_MACOS)


#: URL.Platform: PLATFORM_MACOS is 1, PLATFORM_WIN32 is 2.
def _url_platform() -> int:
    return 2 if _is_windows() else 1


def _fill_application_info(presentation: Any, bindings: Bindings) -> None:
    info = presentation.application_info
    enums = bindings.application_info.ApplicationInfo
    info.platform = _platform(bindings)
    info.application = enums.Application.APPLICATION_PROPRESENTER
    major, minor, patch = APPLICATION_VERSION
    info.application_version.major_version = major
    info.application_version.minor_version = minor
    info.application_version.patch_version = patch
    info.application_version.build = PROTO_SOURCE_BUILD


def _build_text_element(element: Any, slide: Slide, config: ConversionConfig) -> None:
    """The lyric text element: a centred, full-bleed text box inside the safe area."""
    style = config.style
    inset = style.safe_area_inset
    _set_uuid(element.uuid, new_uuid())
    element.name = "Text"
    element.bounds.origin.x = style.width * inset
    element.bounds.origin.y = style.height * inset
    element.bounds.size.width = style.width * (1 - 2 * inset)
    element.bounds.size.height = style.height * (1 - 2 * inset)
    element.opacity = 1.0

    element.path.closed = True
    element.path.shape.type = 1  # TYPE_RECTANGLE
    for x, y in ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)):
        point = element.path.points.add()
        point.point.x, point.point.y = x, y
        point.q0.x, point.q0.y = x, y
        point.q1.x, point.q1.y = x, y

    # Present but disabled, exactly as the reference writes them.
    _set_colour(element.fill.color, RGBA(red=0.0, green=0.0, blue=0.0, alpha=0.0))
    element.fill.enable = False
    element.stroke.width = 0.0
    element.stroke.enable = False

    if style.shadow_enabled:
        shadow = element.shadow
        shadow.angle = style.shadow_angle
        shadow.offset = style.shadow_offset
        shadow.radius = style.shadow_radius
        shadow.opacity = style.shadow_opacity
        shadow.enable = True
        _set_colour(shadow.color, RGBA(red=0.0, green=0.0, blue=0.0))

    text = element.text
    attributes = text.attributes
    attributes.font.name = style.font.postscript_name
    attributes.font.family = style.font.family_name
    attributes.font.size = style.font.size
    attributes.font.bold = style.font.bold
    attributes.font.italic = style.font.italic
    _set_colour(attributes.text_solid_fill, style.text_colour)
    attributes.paragraph_style.alignment = 2  # ALIGNMENT_CENTER
    attributes.paragraph_style.line_height_multiple = 1.0
    attributes.paragraph_style.default_tab_interval = style.font.size * 1.12
    if style.outline_width > 0:
        attributes.stroke_width = style.outline_width
        _set_colour(attributes.stroke_color, style.outline_colour)

    if style.shadow_enabled:
        text.shadow.angle = style.shadow_angle
        text.shadow.offset = style.shadow_offset
        text.shadow.radius = style.shadow_radius
        text.shadow.opacity = style.shadow_opacity
        text.shadow.enable = True
        _set_colour(text.shadow.color, RGBA(red=0.0, green=0.0, blue=0.0))

    lyrics = slide.lyrics or [""]
    if style.all_caps:
        lyrics = [line.upper() for line in lyrics]
    text.rtf_data = build_rtf(lyrics, font=style.font, colour=style.text_colour)
    text.vertical_alignment = 1  # VERTICAL_ALIGNMENT_MIDDLE
    text.is_superscript_standardized = True
    text.transformDelimiter = TRANSFORM_DELIMITER
    _set_colour(text.chord_pro.color, RGBA(red=0.0, green=0.0, blue=0.0))
    if config.chord_delivery.writes_inline:
        _write_inline_chords(text, slide, config)


def _word_end(lyric: str, index: int) -> int:
    """The end of the word starting at ``index``."""
    end = index
    while end < len(lyric) and not lyric[end].isspace():
        end += 1
    return end


def _write_inline_chords(text: Any, slide: Slide, config: ConversionConfig) -> int:
    """Chords as attributes of the slide's own text, for the Chords stage element.

    ProPresenter can hold a chord as a ``CustomAttribute`` on a range of the lyric
    text rather than as a separate chart, and its Chords stage element reads those.
    That is the only route of the three that can transpose or renotate, because the
    chords are data rather than a picture or a block of monospaced notes.

    Two things here are read off the schema rather than out of a real export, because
    no export this project has seen uses the feature at all:

    * ``IntRange`` calls its second field ``end``, which on a Mac-born format could
      equally be a length. Each chord is therefore anchored across the *word* it sits
      on: under either reading the chord lands on the right word rather than drifting.
    * ``chord_pro.enabled`` lives on the audience lyric element, so it may well draw
      the chords on the main output too. Nothing here turns it on by default.

    Chords on an instrumental line cannot be carried this way - there is no text on
    the slide to anchor them to - so those stay with the notes and the chart.
    """
    lines = [line for line in slide.lines if line.lyrics]
    offset = 0
    written = 0
    for line in lines:
        lyric = line.lyrics.upper() if config.style.all_caps else line.lyrics
        for placement in line.chords:
            index = min(placement.char_index, len(lyric))
            attribute = text.attributes.custom_attributes.add()
            attribute.range.start = offset + index
            attribute.range.end = offset + _word_end(lyric, index)
            attribute.chord = placement.chord
            written += 1
        # One character for the break between paragraphs, matching the plain text
        # ProPresenter reads out of the RTF.
        offset += len(lyric) + 1
    if written:
        text.chord_pro.enabled = True
        text.chord_pro.notation = 0  # NOTATION_CHORDS
    return written


def _build_cue(
    bindings: Bindings,
    slide: Slide,
    config: ConversionConfig,
    chart_page: ChordChartPage | None,
) -> Any:
    cue = bindings.cue.Cue()
    _set_uuid(cue.uuid, new_uuid())
    cue.name = slide.label
    cue.isEnabled = True
    _set_uuid(cue.completion_target_uuid, ZERO_UUID)
    cue.completion_action_type = 1  # COMPLETION_ACTION_TYPE_LAST
    _set_uuid(cue.completion_action_uuid, ZERO_UUID)
    cue.hot_key.SetInParent()

    action = cue.actions.add()
    _set_uuid(action.uuid, new_uuid())
    action.isEnabled = True
    action.type = 11  # ACTION_TYPE_PRESENTATION_SLIDE

    presentation_slide = action.slide.presentation
    base = presentation_slide.base_slide
    base.size.width = float(config.style.width)
    base.size.height = float(config.style.height)
    _set_uuid(base.uuid, new_uuid())
    _set_colour(base.background_color, RGBA(red=0.0, green=0.0, blue=0.0))

    slide_element = base.elements.add()
    _build_text_element(slide_element.element, slide, config)
    slide_element.info = LYRIC_ELEMENT_INFO

    if config.chord_delivery.writes_notes:
        block = render_lines(slide.lines, config.chord_placement)
        if block.strip():
            presentation_slide.notes.rtf_data = build_notes_rtf(block)

    if chart_page is not None:
        url = presentation_slide.chord_chart
        url.absolute_string = chart_page.absolute_path.as_uri()
        url.platform = _url_platform()
        url.local.root = 10  # ROOT_SHOW
        url.local.path = chart_page.show_relative_path
    return cue


def _build_group(bindings: Bindings, name: str, colour: RGBA, hot_key: int) -> Any:
    group = bindings.groups.Group()
    _set_uuid(group.uuid, new_uuid())
    group.name = name
    _set_colour(group.color, colour)
    if hot_key:
        group.hotKey.code = hot_key
    else:
        group.hotKey.SetInParent()
    return group


def build_presentation(
    plan: SlidePlan,
    *,
    chart_pages: list[ChordChartPage] | None = None,
    page_for_section: dict[int, int] | None = None,
) -> Any:
    """Build the ``Presentation`` message for a plan.

    ``chart_pages`` are the rendered chord-chart pages and ``page_for_section`` says
    which page each section was printed on, so every slide points at the page its own
    words are on.
    """
    bindings = load_bindings()
    config = plan.config
    song = plan.song

    presentation = bindings.presentation.Presentation()
    _fill_application_info(presentation, bindings)
    _set_uuid(presentation.uuid, new_uuid())
    presentation.name = song.title
    presentation.category = config.category
    _set_colour(presentation.background.color, RGBA(red=0.0, green=0.0, blue=0.0))

    if song.ccli_number or song.copyright or song.artist:
        ccli = presentation.ccli
        ccli.song_title = song.title
        if song.artist:
            ccli.author = song.artist
            ccli.artist_credits = song.artist
        if song.ccli_number and song.ccli_number.isdigit():
            ccli.song_number = int(song.ccli_number)
        if song.copyright:
            ccli.publisher = song.copyright
        ccli.display = False
    if song.key:
        presentation.music_key = song.key
        presentation.music.original_music_key = song.key
        presentation.music.user_music_key = song.key

    # ProPresenter's own export leaves the presentation-level chord chart empty and
    # attaches one per slide. Which of the two a stage-layout Chord Chart element reads
    # is not something the reference files can settle, so pcci populates both: the
    # per-slide reference points at the page that slide's words are on, and the
    # presentation-level one points at page 1. Setting both costs nothing and removes a
    # whole class of "it shows in the editor but not on stage".
    if chart_pages:
        first_page = chart_pages[0]
        presentation.chord_chart.absolute_string = first_page.absolute_path.as_uri()
        presentation.chord_chart.platform = _url_platform()
        presentation.chord_chart.local.root = 10  # ROOT_SHOW
        presentation.chord_chart.local.path = first_page.show_relative_path

    assigner = GroupAssigner(config=config)
    arrangement_group_uuids: list[str] = []
    section_pages = _pages_by_section(song.sections, chart_pages, page_for_section)

    for section_index, section in enumerate(song.sections):
        section_slides = plan.slides_for_section(section_index)
        if not section_slides:
            continue
        identity = assigner.identity_for(section)
        cue_group = presentation.cue_groups.add()
        cue_group.group.CopyFrom(
            _build_group(bindings, identity.name, identity.colour, identity.hot_key)
        )
        arrangement_group_uuids.append(cue_group.group.uuid.string)
        for slide in section_slides:
            cue = _build_cue(bindings, slide, config, section_pages.get(section_index))
            presentation.cues.append(cue)
            added = cue_group.cue_identifiers.add()
            added.string = cue.uuid.string

    if config.build_arrangement and arrangement_group_uuids:
        arrangement = presentation.arrangements.add()
        _set_uuid(arrangement.uuid, new_uuid())
        arrangement.name = config.arrangement_name
        for group_uuid in arrangement_group_uuids:
            added = arrangement.group_identifiers.add()
            added.string = group_uuid
        presentation.selected_arrangement.string = arrangement.uuid.string

    return presentation


def _pages_by_section(
    sections: list[Section],
    chart_pages: list[ChordChartPage] | None,
    page_for_section: dict[int, int] | None,
) -> dict[int, ChordChartPage]:
    """Point each section at the chart page it was rendered onto."""
    if not chart_pages:
        return {}
    lookup = page_for_section or {}
    mapping: dict[int, ChordChartPage] = {}
    for index in range(len(sections)):
        page = lookup.get(index, 0)
        mapping[index] = chart_pages[min(page, len(chart_pages) - 1)]
    return mapping


def presentation_bytes(presentation: Any) -> bytes:
    return bytes(presentation.SerializeToString())
