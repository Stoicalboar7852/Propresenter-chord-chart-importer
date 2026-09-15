from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScreenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCREEN_TYPE_UNKNOWN: _ClassVar[ScreenType]
    AUDIENCE: _ClassVar[ScreenType]
    STAGE: _ClassVar[ScreenType]
SCREEN_TYPE_UNKNOWN: ScreenType
AUDIENCE: ScreenType
STAGE: ScreenType

class Looks(_message.Message):
    __slots__ = ("number_presets",)
    NUMBER_PRESETS_FIELD_NUMBER: _ClassVar[int]
    number_presets: int
    def __init__(self, number_presets: _Optional[int] = ...) -> None: ...

class Summary(_message.Message):
    __slots__ = ("total_screens", "audience_screen_count", "stage_screen_count")
    TOTAL_SCREENS_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_SCREEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    STAGE_SCREEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    total_screens: int
    audience_screen_count: int
    stage_screen_count: int
    def __init__(self, total_screens: _Optional[int] = ..., audience_screen_count: _Optional[int] = ..., stage_screen_count: _Optional[int] = ...) -> None: ...

class Output(_message.Message):
    __slots__ = ("proscreen_type", "output_type", "color_correction_enabled", "corner_pin_enabled", "alignment", "width", "height", "alpha_key_mode", "alpha_device", "is_disabled")
    class ProScreenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRO_SCREEN_TYPE_UNKNOWN: _ClassVar[Output.ProScreenType]
        SINGLE: _ClassVar[Output.ProScreenType]
        MIRRORED: _ClassVar[Output.ProScreenType]
        EDGE_BLEND: _ClassVar[Output.ProScreenType]
        GROUPED: _ClassVar[Output.ProScreenType]
    PRO_SCREEN_TYPE_UNKNOWN: Output.ProScreenType
    SINGLE: Output.ProScreenType
    MIRRORED: Output.ProScreenType
    EDGE_BLEND: Output.ProScreenType
    GROUPED: Output.ProScreenType
    class OutputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OUTPUT_TYPE_UNKNOWN: _ClassVar[Output.OutputType]
        SDI: _ClassVar[Output.OutputType]
        NDI: _ClassVar[Output.OutputType]
        SYPHON: _ClassVar[Output.OutputType]
        SYSTEM: _ClassVar[Output.OutputType]
        PLACEHOLDER: _ClassVar[Output.OutputType]
        DVI: _ClassVar[Output.OutputType]
    OUTPUT_TYPE_UNKNOWN: Output.OutputType
    SDI: Output.OutputType
    NDI: Output.OutputType
    SYPHON: Output.OutputType
    SYSTEM: Output.OutputType
    PLACEHOLDER: Output.OutputType
    DVI: Output.OutputType
    class Alignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALIGNMENT_UNKNOWN: _ClassVar[Output.Alignment]
        FULL: _ClassVar[Output.Alignment]
        _2X1: _ClassVar[Output.Alignment]
        _3X1: _ClassVar[Output.Alignment]
        _2X2: _ClassVar[Output.Alignment]
        CUSTOM: _ClassVar[Output.Alignment]
    ALIGNMENT_UNKNOWN: Output.Alignment
    FULL: Output.Alignment
    _2X1: Output.Alignment
    _3X1: Output.Alignment
    _2X2: Output.Alignment
    CUSTOM: Output.Alignment
    class AlphaKeyMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALPHA_KEY_MODE_NONE: _ClassVar[Output.AlphaKeyMode]
        PREMULTIPLIED: _ClassVar[Output.AlphaKeyMode]
        STRAIGHT: _ClassVar[Output.AlphaKeyMode]
    ALPHA_KEY_MODE_NONE: Output.AlphaKeyMode
    PREMULTIPLIED: Output.AlphaKeyMode
    STRAIGHT: Output.AlphaKeyMode
    class AlphaDevice(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALPHA_DEVICE_NONE: _ClassVar[Output.AlphaDevice]
        SELF: _ClassVar[Output.AlphaDevice]
        OTHER: _ClassVar[Output.AlphaDevice]
    ALPHA_DEVICE_NONE: Output.AlphaDevice
    SELF: Output.AlphaDevice
    OTHER: Output.AlphaDevice
    PROSCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    COLOR_CORRECTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CORNER_PIN_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ALPHA_KEY_MODE_FIELD_NUMBER: _ClassVar[int]
    ALPHA_DEVICE_FIELD_NUMBER: _ClassVar[int]
    IS_DISABLED_FIELD_NUMBER: _ClassVar[int]
    proscreen_type: Output.ProScreenType
    output_type: Output.OutputType
    color_correction_enabled: bool
    corner_pin_enabled: bool
    alignment: Output.Alignment
    width: int
    height: int
    alpha_key_mode: Output.AlphaKeyMode
    alpha_device: Output.AlphaDevice
    is_disabled: bool
    def __init__(self, proscreen_type: _Optional[_Union[Output.ProScreenType, str]] = ..., output_type: _Optional[_Union[Output.OutputType, str]] = ..., color_correction_enabled: _Optional[bool] = ..., corner_pin_enabled: _Optional[bool] = ..., alignment: _Optional[_Union[Output.Alignment, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., alpha_key_mode: _Optional[_Union[Output.AlphaKeyMode, str]] = ..., alpha_device: _Optional[_Union[Output.AlphaDevice, str]] = ..., is_disabled: _Optional[bool] = ...) -> None: ...

class Single(_message.Message):
    __slots__ = ("screen_type", "screen_color_enabled")
    SCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCREEN_COLOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    screen_type: ScreenType
    screen_color_enabled: bool
    def __init__(self, screen_type: _Optional[_Union[ScreenType, str]] = ..., screen_color_enabled: _Optional[bool] = ...) -> None: ...

class Mirrored(_message.Message):
    __slots__ = ("screen_type", "screen_color_enabled", "count")
    SCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCREEN_COLOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    screen_type: ScreenType
    screen_color_enabled: bool
    count: int
    def __init__(self, screen_type: _Optional[_Union[ScreenType, str]] = ..., screen_color_enabled: _Optional[bool] = ..., count: _Optional[int] = ...) -> None: ...

class EdgeBlend(_message.Message):
    __slots__ = ("screen_type", "screen_color_enabled", "count")
    SCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCREEN_COLOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    screen_type: ScreenType
    screen_color_enabled: bool
    count: int
    def __init__(self, screen_type: _Optional[_Union[ScreenType, str]] = ..., screen_color_enabled: _Optional[bool] = ..., count: _Optional[int] = ...) -> None: ...

class Grouped(_message.Message):
    __slots__ = ("screen_type", "screen_color_enabled", "columns", "rows")
    SCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCREEN_COLOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    screen_type: ScreenType
    screen_color_enabled: bool
    columns: int
    rows: int
    def __init__(self, screen_type: _Optional[_Union[ScreenType, str]] = ..., screen_color_enabled: _Optional[bool] = ..., columns: _Optional[int] = ..., rows: _Optional[int] = ...) -> None: ...

class Preferences(_message.Message):
    __slots__ = ("house_of_worship", "has_custom_logo", "copyright_enabled", "copyright_style", "copyright_has_license", "render_mode", "suppress_auto_start", "manage_media_automatically", "search_paths_relink", "update_channel")
    class CopyrightStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COPYRIGHT_STYLE_UNKNOWN: _ClassVar[Preferences.CopyrightStyle]
        FIRST: _ClassVar[Preferences.CopyrightStyle]
        LAST: _ClassVar[Preferences.CopyrightStyle]
        FIRST_AND_LAST: _ClassVar[Preferences.CopyrightStyle]
        ALL_SLIDES: _ClassVar[Preferences.CopyrightStyle]
    COPYRIGHT_STYLE_UNKNOWN: Preferences.CopyrightStyle
    FIRST: Preferences.CopyrightStyle
    LAST: Preferences.CopyrightStyle
    FIRST_AND_LAST: Preferences.CopyrightStyle
    ALL_SLIDES: Preferences.CopyrightStyle
    class RenderMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RENDER_MODE_UNKNOWN: _ClassVar[Preferences.RenderMode]
        OPENGL: _ClassVar[Preferences.RenderMode]
        METAL: _ClassVar[Preferences.RenderMode]
        DIRECTX: _ClassVar[Preferences.RenderMode]
    RENDER_MODE_UNKNOWN: Preferences.RenderMode
    OPENGL: Preferences.RenderMode
    METAL: Preferences.RenderMode
    DIRECTX: Preferences.RenderMode
    class UpdateChannel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UPDATE_CHANNEL_UNKNOWN: _ClassVar[Preferences.UpdateChannel]
        RELEASE: _ClassVar[Preferences.UpdateChannel]
        BETA: _ClassVar[Preferences.UpdateChannel]
    UPDATE_CHANNEL_UNKNOWN: Preferences.UpdateChannel
    RELEASE: Preferences.UpdateChannel
    BETA: Preferences.UpdateChannel
    HOUSE_OF_WORSHIP_FIELD_NUMBER: _ClassVar[int]
    HAS_CUSTOM_LOGO_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_STYLE_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_HAS_LICENSE_FIELD_NUMBER: _ClassVar[int]
    RENDER_MODE_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_AUTO_START_FIELD_NUMBER: _ClassVar[int]
    MANAGE_MEDIA_AUTOMATICALLY_FIELD_NUMBER: _ClassVar[int]
    SEARCH_PATHS_RELINK_FIELD_NUMBER: _ClassVar[int]
    UPDATE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    house_of_worship: bool
    has_custom_logo: bool
    copyright_enabled: bool
    copyright_style: Preferences.CopyrightStyle
    copyright_has_license: bool
    render_mode: Preferences.RenderMode
    suppress_auto_start: bool
    manage_media_automatically: bool
    search_paths_relink: bool
    update_channel: Preferences.UpdateChannel
    def __init__(self, house_of_worship: _Optional[bool] = ..., has_custom_logo: _Optional[bool] = ..., copyright_enabled: _Optional[bool] = ..., copyright_style: _Optional[_Union[Preferences.CopyrightStyle, str]] = ..., copyright_has_license: _Optional[bool] = ..., render_mode: _Optional[_Union[Preferences.RenderMode, str]] = ..., suppress_auto_start: _Optional[bool] = ..., manage_media_automatically: _Optional[bool] = ..., search_paths_relink: _Optional[bool] = ..., update_channel: _Optional[_Union[Preferences.UpdateChannel, str]] = ...) -> None: ...

class Screens(_message.Message):
    __slots__ = ("show_screens_launch", "show_performance_on_screen", "ignore_background_colors", "show_keynote_ppt_screens")
    SHOW_SCREENS_LAUNCH_FIELD_NUMBER: _ClassVar[int]
    SHOW_PERFORMANCE_ON_SCREEN_FIELD_NUMBER: _ClassVar[int]
    IGNORE_BACKGROUND_COLORS_FIELD_NUMBER: _ClassVar[int]
    SHOW_KEYNOTE_PPT_SCREENS_FIELD_NUMBER: _ClassVar[int]
    show_screens_launch: bool
    show_performance_on_screen: bool
    ignore_background_colors: bool
    show_keynote_ppt_screens: bool
    def __init__(self, show_screens_launch: _Optional[bool] = ..., show_performance_on_screen: _Optional[bool] = ..., ignore_background_colors: _Optional[bool] = ..., show_keynote_ppt_screens: _Optional[bool] = ...) -> None: ...

class SongSelect(_message.Message):
    __slots__ = ("logged_in", "auto_reporting_enabled")
    LOGGED_IN_FIELD_NUMBER: _ClassVar[int]
    AUTO_REPORTING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    logged_in: bool
    auto_reporting_enabled: bool
    def __init__(self, logged_in: _Optional[bool] = ..., auto_reporting_enabled: _Optional[bool] = ...) -> None: ...

class Content(_message.Message):
    __slots__ = ("library_count", "library_playlist_count", "library_playlist_folder_count", "library_playlist_max_depth", "media_bin_total_playlist_count", "media_bin_playlist_folder_count", "media_bin_playlist_max_depth", "media_bin_normal_playlist_count", "media_bin_smart_playlist_count", "media_bin_video_input_count", "audio_bin_playlist_count", "audio_bin_playlist_folder_count", "audio_bin_playlist_max_depth", "timer_count", "messages_count", "props_count", "props_auto_clear_count", "prop_collections_count", "prop_collections_single_prop_enabled_count", "stage_layout_count", "macros_count", "macros_collections_count", "macros_custom_icons", "ubiquitous_show_directory")
    LIBRARY_COUNT_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_COUNT_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_FOLDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_TOTAL_PLAYLIST_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_PLAYLIST_FOLDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_PLAYLIST_MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_NORMAL_PLAYLIST_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_SMART_PLAYLIST_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_VIDEO_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUDIO_BIN_PLAYLIST_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUDIO_BIN_PLAYLIST_FOLDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUDIO_BIN_PLAYLIST_MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    TIMER_COUNT_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROPS_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROPS_AUTO_CLEAR_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROP_COLLECTIONS_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROP_COLLECTIONS_SINGLE_PROP_ENABLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    STAGE_LAYOUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    MACROS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MACROS_COLLECTIONS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MACROS_CUSTOM_ICONS_FIELD_NUMBER: _ClassVar[int]
    UBIQUITOUS_SHOW_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    library_count: int
    library_playlist_count: int
    library_playlist_folder_count: int
    library_playlist_max_depth: int
    media_bin_total_playlist_count: int
    media_bin_playlist_folder_count: int
    media_bin_playlist_max_depth: int
    media_bin_normal_playlist_count: int
    media_bin_smart_playlist_count: int
    media_bin_video_input_count: int
    audio_bin_playlist_count: int
    audio_bin_playlist_folder_count: int
    audio_bin_playlist_max_depth: int
    timer_count: int
    messages_count: int
    props_count: int
    props_auto_clear_count: int
    prop_collections_count: int
    prop_collections_single_prop_enabled_count: int
    stage_layout_count: int
    macros_count: int
    macros_collections_count: int
    macros_custom_icons: int
    ubiquitous_show_directory: bool
    def __init__(self, library_count: _Optional[int] = ..., library_playlist_count: _Optional[int] = ..., library_playlist_folder_count: _Optional[int] = ..., library_playlist_max_depth: _Optional[int] = ..., media_bin_total_playlist_count: _Optional[int] = ..., media_bin_playlist_folder_count: _Optional[int] = ..., media_bin_playlist_max_depth: _Optional[int] = ..., media_bin_normal_playlist_count: _Optional[int] = ..., media_bin_smart_playlist_count: _Optional[int] = ..., media_bin_video_input_count: _Optional[int] = ..., audio_bin_playlist_count: _Optional[int] = ..., audio_bin_playlist_folder_count: _Optional[int] = ..., audio_bin_playlist_max_depth: _Optional[int] = ..., timer_count: _Optional[int] = ..., messages_count: _Optional[int] = ..., props_count: _Optional[int] = ..., props_auto_clear_count: _Optional[int] = ..., prop_collections_count: _Optional[int] = ..., prop_collections_single_prop_enabled_count: _Optional[int] = ..., stage_layout_count: _Optional[int] = ..., macros_count: _Optional[int] = ..., macros_collections_count: _Optional[int] = ..., macros_custom_icons: _Optional[int] = ..., ubiquitous_show_directory: _Optional[bool] = ...) -> None: ...

class Themes(_message.Message):
    __slots__ = ("theme_count", "theme_folder_count", "theme_folder_max_depth", "theme_slides_count")
    THEME_COUNT_FIELD_NUMBER: _ClassVar[int]
    THEME_FOLDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    THEME_FOLDER_MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    THEME_SLIDES_COUNT_FIELD_NUMBER: _ClassVar[int]
    theme_count: int
    theme_folder_count: int
    theme_folder_max_depth: int
    theme_slides_count: int
    def __init__(self, theme_count: _Optional[int] = ..., theme_folder_count: _Optional[int] = ..., theme_folder_max_depth: _Optional[int] = ..., theme_slides_count: _Optional[int] = ...) -> None: ...

class Macro(_message.Message):
    __slots__ = ("trigger_on_startup_count",)
    TRIGGER_ON_STARTUP_COUNT_FIELD_NUMBER: _ClassVar[int]
    trigger_on_startup_count: int
    def __init__(self, trigger_on_startup_count: _Optional[int] = ...) -> None: ...

class ClearGroup(_message.Message):
    __slots__ = ("clear_group_count", "hidden_clear_group_count", "default_icon_count", "custom_icon_count", "icon_tint_count")
    CLEAR_GROUP_COUNT_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_CLEAR_GROUP_COUNT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ICON_COUNT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ICON_COUNT_FIELD_NUMBER: _ClassVar[int]
    ICON_TINT_COUNT_FIELD_NUMBER: _ClassVar[int]
    clear_group_count: int
    hidden_clear_group_count: int
    default_icon_count: int
    custom_icon_count: int
    icon_tint_count: int
    def __init__(self, clear_group_count: _Optional[int] = ..., hidden_clear_group_count: _Optional[int] = ..., default_icon_count: _Optional[int] = ..., custom_icon_count: _Optional[int] = ..., icon_tint_count: _Optional[int] = ...) -> None: ...

class KeyMapping(_message.Message):
    __slots__ = ("total_mapped", "clear_groups", "groups", "macros", "props", "menus")
    TOTAL_MAPPED_FIELD_NUMBER: _ClassVar[int]
    CLEAR_GROUPS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    MACROS_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    MENUS_FIELD_NUMBER: _ClassVar[int]
    total_mapped: int
    clear_groups: int
    groups: int
    macros: int
    props: int
    menus: int
    def __init__(self, total_mapped: _Optional[int] = ..., clear_groups: _Optional[int] = ..., groups: _Optional[int] = ..., macros: _Optional[int] = ..., props: _Optional[int] = ..., menus: _Optional[int] = ...) -> None: ...

class NetworkLink(_message.Message):
    __slots__ = ("enabled", "member_count")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    member_count: int
    def __init__(self, enabled: _Optional[bool] = ..., member_count: _Optional[int] = ...) -> None: ...

class Capture(_message.Message):
    __slots__ = ("presets_count", "disk_presets_count", "rtmp_presets_count", "resi_presets_count")
    PRESETS_COUNT_FIELD_NUMBER: _ClassVar[int]
    DISK_PRESETS_COUNT_FIELD_NUMBER: _ClassVar[int]
    RTMP_PRESETS_COUNT_FIELD_NUMBER: _ClassVar[int]
    RESI_PRESETS_COUNT_FIELD_NUMBER: _ClassVar[int]
    presets_count: int
    disk_presets_count: int
    rtmp_presets_count: int
    resi_presets_count: int
    def __init__(self, presets_count: _Optional[int] = ..., disk_presets_count: _Optional[int] = ..., rtmp_presets_count: _Optional[int] = ..., resi_presets_count: _Optional[int] = ...) -> None: ...

class Versioning(_message.Message):
    __slots__ = ("highest_version",)
    HIGHEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    highest_version: str
    def __init__(self, highest_version: _Optional[str] = ...) -> None: ...

class DiskUsage(_message.Message):
    __slots__ = ("bytes_of_show_files", "bytes_of_media_asset_files", "number_of_media_asset_files", "bytes_of_unmanaged_media_asset_files")
    BYTES_OF_SHOW_FILES_FIELD_NUMBER: _ClassVar[int]
    BYTES_OF_MEDIA_ASSET_FILES_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MEDIA_ASSET_FILES_FIELD_NUMBER: _ClassVar[int]
    BYTES_OF_UNMANAGED_MEDIA_ASSET_FILES_FIELD_NUMBER: _ClassVar[int]
    bytes_of_show_files: int
    bytes_of_media_asset_files: int
    number_of_media_asset_files: int
    bytes_of_unmanaged_media_asset_files: int
    def __init__(self, bytes_of_show_files: _Optional[int] = ..., bytes_of_media_asset_files: _Optional[int] = ..., number_of_media_asset_files: _Optional[int] = ..., bytes_of_unmanaged_media_asset_files: _Optional[int] = ...) -> None: ...

class LibraryUsage(_message.Message):
    __slots__ = ("number_of_presentations", "bytes_of_presentations")
    NUMBER_OF_PRESENTATIONS_FIELD_NUMBER: _ClassVar[int]
    BYTES_OF_PRESENTATIONS_FIELD_NUMBER: _ClassVar[int]
    number_of_presentations: int
    bytes_of_presentations: int
    def __init__(self, number_of_presentations: _Optional[int] = ..., bytes_of_presentations: _Optional[int] = ...) -> None: ...

class Interface(_message.Message):
    __slots__ = ("library_outline", "media_outline", "audio_outline", "continuous_playlist", "media_bin", "presentation_view_style", "presentation_grid_column_count", "media_bin_view_style", "media_bin_grid_column_count", "media_bin_table_column_count", "presentation_transition", "media_transition", "audio_shuffle")
    class SplitViewState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SPLIT_VIEW_STATE_UNKNOWN: _ClassVar[Interface.SplitViewState]
        SPLIT_VIEW_STATE_COLLAPSED: _ClassVar[Interface.SplitViewState]
        SPLIT_VIEW_STATE_EXPANDED: _ClassVar[Interface.SplitViewState]
    SPLIT_VIEW_STATE_UNKNOWN: Interface.SplitViewState
    SPLIT_VIEW_STATE_COLLAPSED: Interface.SplitViewState
    SPLIT_VIEW_STATE_EXPANDED: Interface.SplitViewState
    class PresentationViewStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESENTATION_VIEW_STYLE_UNKNOWN: _ClassVar[Interface.PresentationViewStyle]
        PRESENTATION_VIEW_STYLE_GRID: _ClassVar[Interface.PresentationViewStyle]
        PRESENTATION_VIEW_STYLE_EASY: _ClassVar[Interface.PresentationViewStyle]
        PRESENTATION_VIEW_STYLE_TABLE: _ClassVar[Interface.PresentationViewStyle]
    PRESENTATION_VIEW_STYLE_UNKNOWN: Interface.PresentationViewStyle
    PRESENTATION_VIEW_STYLE_GRID: Interface.PresentationViewStyle
    PRESENTATION_VIEW_STYLE_EASY: Interface.PresentationViewStyle
    PRESENTATION_VIEW_STYLE_TABLE: Interface.PresentationViewStyle
    class MediaBinViewStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MEDIA_BIN_VIEW_STYLE_UNKNOWN: _ClassVar[Interface.MediaBinViewStyle]
        MEDIA_BIN_VIEW_STYLE_GRID: _ClassVar[Interface.MediaBinViewStyle]
        MEDIA_BIN_VIEW_STYLE_TABLE: _ClassVar[Interface.MediaBinViewStyle]
    MEDIA_BIN_VIEW_STYLE_UNKNOWN: Interface.MediaBinViewStyle
    MEDIA_BIN_VIEW_STYLE_GRID: Interface.MediaBinViewStyle
    MEDIA_BIN_VIEW_STYLE_TABLE: Interface.MediaBinViewStyle
    LIBRARY_OUTLINE_FIELD_NUMBER: _ClassVar[int]
    MEDIA_OUTLINE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_OUTLINE_FIELD_NUMBER: _ClassVar[int]
    CONTINUOUS_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_VIEW_STYLE_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_GRID_COLUMN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_VIEW_STYLE_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_GRID_COLUMN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_BIN_TABLE_COLUMN_COUNT_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    AUDIO_SHUFFLE_FIELD_NUMBER: _ClassVar[int]
    library_outline: Interface.SplitViewState
    media_outline: Interface.SplitViewState
    audio_outline: Interface.SplitViewState
    continuous_playlist: bool
    media_bin: Interface.SplitViewState
    presentation_view_style: Interface.PresentationViewStyle
    presentation_grid_column_count: int
    media_bin_view_style: Interface.MediaBinViewStyle
    media_bin_grid_column_count: int
    media_bin_table_column_count: int
    presentation_transition: str
    media_transition: str
    audio_shuffle: bool
    def __init__(self, library_outline: _Optional[_Union[Interface.SplitViewState, str]] = ..., media_outline: _Optional[_Union[Interface.SplitViewState, str]] = ..., audio_outline: _Optional[_Union[Interface.SplitViewState, str]] = ..., continuous_playlist: _Optional[bool] = ..., media_bin: _Optional[_Union[Interface.SplitViewState, str]] = ..., presentation_view_style: _Optional[_Union[Interface.PresentationViewStyle, str]] = ..., presentation_grid_column_count: _Optional[int] = ..., media_bin_view_style: _Optional[_Union[Interface.MediaBinViewStyle, str]] = ..., media_bin_grid_column_count: _Optional[int] = ..., media_bin_table_column_count: _Optional[int] = ..., presentation_transition: _Optional[str] = ..., media_transition: _Optional[str] = ..., audio_shuffle: _Optional[bool] = ...) -> None: ...
