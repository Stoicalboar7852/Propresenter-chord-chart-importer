from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionCaptureStart(_message.Message):
    __slots__ = ("preset_type",)
    class PresetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ActionCaptureStart.PresetType]
        ACTIVE_SETTINGS: _ClassVar[ActionCaptureStart.PresetType]
        CAPTURE_PRESET: _ClassVar[ActionCaptureStart.PresetType]
    UNKNOWN: ActionCaptureStart.PresetType
    ACTIVE_SETTINGS: ActionCaptureStart.PresetType
    CAPTURE_PRESET: ActionCaptureStart.PresetType
    PRESET_TYPE_FIELD_NUMBER: _ClassVar[int]
    preset_type: ActionCaptureStart.PresetType
    def __init__(self, preset_type: _Optional[_Union[ActionCaptureStart.PresetType, str]] = ...) -> None: ...

class ActionCaptureStop(_message.Message):
    __slots__ = ("confirm_before_stopping",)
    CONFIRM_BEFORE_STOPPING_FIELD_NUMBER: _ClassVar[int]
    confirm_before_stopping: bool
    def __init__(self, confirm_before_stopping: _Optional[bool] = ...) -> None: ...

class ActionClear(_message.Message):
    __slots__ = ("type",)
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ActionClear.Type]
        AUDIO: _ClassVar[ActionClear.Type]
        MESSAGES: _ClassVar[ActionClear.Type]
        PROPS: _ClassVar[ActionClear.Type]
        ANNOUNCEMENTS: _ClassVar[ActionClear.Type]
        SLIDE: _ClassVar[ActionClear.Type]
        MEDIA: _ClassVar[ActionClear.Type]
        VIDEO_INPUT: _ClassVar[ActionClear.Type]
        CLEAR_TO_LOGO: _ClassVar[ActionClear.Type]
        CLEAR_GROUP: _ClassVar[ActionClear.Type]
    UNKNOWN: ActionClear.Type
    AUDIO: ActionClear.Type
    MESSAGES: ActionClear.Type
    PROPS: ActionClear.Type
    ANNOUNCEMENTS: ActionClear.Type
    SLIDE: ActionClear.Type
    MEDIA: ActionClear.Type
    VIDEO_INPUT: ActionClear.Type
    CLEAR_TO_LOGO: ActionClear.Type
    CLEAR_GROUP: ActionClear.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: ActionClear.Type
    def __init__(self, type: _Optional[_Union[ActionClear.Type, str]] = ...) -> None: ...

class ActionClearGroup(_message.Message):
    __slots__ = ("layer_audio", "layer_messages", "layer_props", "layer_announcement", "layer_slide", "layer_media", "layer_video_input")
    LAYER_AUDIO_FIELD_NUMBER: _ClassVar[int]
    LAYER_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    LAYER_PROPS_FIELD_NUMBER: _ClassVar[int]
    LAYER_ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    LAYER_SLIDE_FIELD_NUMBER: _ClassVar[int]
    LAYER_MEDIA_FIELD_NUMBER: _ClassVar[int]
    LAYER_VIDEO_INPUT_FIELD_NUMBER: _ClassVar[int]
    layer_audio: bool
    layer_messages: bool
    layer_props: bool
    layer_announcement: bool
    layer_slide: bool
    layer_media: bool
    layer_video_input: bool
    def __init__(self, layer_audio: _Optional[bool] = ..., layer_messages: _Optional[bool] = ..., layer_props: _Optional[bool] = ..., layer_announcement: _Optional[bool] = ..., layer_slide: _Optional[bool] = ..., layer_media: _Optional[bool] = ..., layer_video_input: _Optional[bool] = ...) -> None: ...

class ActionCommunications(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ActionLook(_message.Message):
    __slots__ = ("total_screen_count", "mask", "messages", "props", "announcements", "presentation_theme", "slide", "media", "video_input")
    class Setting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[ActionLook.Setting]
        SOME: _ClassVar[ActionLook.Setting]
        ALL: _ClassVar[ActionLook.Setting]
    NONE: ActionLook.Setting
    SOME: ActionLook.Setting
    ALL: ActionLook.Setting
    TOTAL_SCREEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_THEME_FIELD_NUMBER: _ClassVar[int]
    SLIDE_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    VIDEO_INPUT_FIELD_NUMBER: _ClassVar[int]
    total_screen_count: int
    mask: ActionLook.Setting
    messages: ActionLook.Setting
    props: ActionLook.Setting
    announcements: ActionLook.Setting
    presentation_theme: ActionLook.Setting
    slide: ActionLook.Setting
    media: ActionLook.Setting
    video_input: ActionLook.Setting
    def __init__(self, total_screen_count: _Optional[int] = ..., mask: _Optional[_Union[ActionLook.Setting, str]] = ..., messages: _Optional[_Union[ActionLook.Setting, str]] = ..., props: _Optional[_Union[ActionLook.Setting, str]] = ..., announcements: _Optional[_Union[ActionLook.Setting, str]] = ..., presentation_theme: _Optional[_Union[ActionLook.Setting, str]] = ..., slide: _Optional[_Union[ActionLook.Setting, str]] = ..., media: _Optional[_Union[ActionLook.Setting, str]] = ..., video_input: _Optional[_Union[ActionLook.Setting, str]] = ...) -> None: ...

class ActionMacro(_message.Message):
    __slots__ = ("action_count", "cue_action_count", "total_action_count")
    ACTION_COUNT_FIELD_NUMBER: _ClassVar[int]
    CUE_ACTION_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ACTION_COUNT_FIELD_NUMBER: _ClassVar[int]
    action_count: int
    cue_action_count: int
    total_action_count: int
    def __init__(self, action_count: _Optional[int] = ..., cue_action_count: _Optional[int] = ..., total_action_count: _Optional[int] = ...) -> None: ...

class ActionMessage(_message.Message):
    __slots__ = ("token_count", "text_token_count", "timer_token_count", "clock_token_count", "showing_count")
    TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    TEXT_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIMER_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    CLOCK_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    SHOWING_COUNT_FIELD_NUMBER: _ClassVar[int]
    token_count: int
    text_token_count: int
    timer_token_count: int
    clock_token_count: int
    showing_count: int
    def __init__(self, token_count: _Optional[int] = ..., text_token_count: _Optional[int] = ..., timer_token_count: _Optional[int] = ..., clock_token_count: _Optional[int] = ..., showing_count: _Optional[int] = ...) -> None: ...

class ActionProp(_message.Message):
    __slots__ = ("transition", "type", "auto_clear")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[ActionProp.Type]
        TRIGGER: _ClassVar[ActionProp.Type]
        CLEAR: _ClassVar[ActionProp.Type]
        TRIGGER_FROM_PROP_BIN: _ClassVar[ActionProp.Type]
    TYPE_UNKNOWN: ActionProp.Type
    TRIGGER: ActionProp.Type
    CLEAR: ActionProp.Type
    TRIGGER_FROM_PROP_BIN: ActionProp.Type
    class AutoClear(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ActionProp.AutoClear]
        DEFAULT_DISABLED: _ClassVar[ActionProp.AutoClear]
        DEFAULT_ENABLED: _ClassVar[ActionProp.AutoClear]
        DISABLED: _ClassVar[ActionProp.AutoClear]
        ENABLED: _ClassVar[ActionProp.AutoClear]
        DISABLED_OVERRIDE: _ClassVar[ActionProp.AutoClear]
        ENABLED_OVERRIDE: _ClassVar[ActionProp.AutoClear]
        CLEAR_ACTION: _ClassVar[ActionProp.AutoClear]
    UNKNOWN: ActionProp.AutoClear
    DEFAULT_DISABLED: ActionProp.AutoClear
    DEFAULT_ENABLED: ActionProp.AutoClear
    DISABLED: ActionProp.AutoClear
    ENABLED: ActionProp.AutoClear
    DISABLED_OVERRIDE: ActionProp.AutoClear
    ENABLED_OVERRIDE: ActionProp.AutoClear
    CLEAR_ACTION: ActionProp.AutoClear
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLEAR_FIELD_NUMBER: _ClassVar[int]
    transition: str
    type: ActionProp.Type
    auto_clear: ActionProp.AutoClear
    def __init__(self, transition: _Optional[str] = ..., type: _Optional[_Union[ActionProp.Type, str]] = ..., auto_clear: _Optional[_Union[ActionProp.AutoClear, str]] = ...) -> None: ...

class ActionSlideDestination(_message.Message):
    __slots__ = ("change_slide_destination",)
    class ChangeSlideDestination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ActionSlideDestination.ChangeSlideDestination]
        NO_CHANGE: _ClassVar[ActionSlideDestination.ChangeSlideDestination]
        STAGE_ONLY: _ClassVar[ActionSlideDestination.ChangeSlideDestination]
        STAGE_AUDIENCE: _ClassVar[ActionSlideDestination.ChangeSlideDestination]
    UNKNOWN: ActionSlideDestination.ChangeSlideDestination
    NO_CHANGE: ActionSlideDestination.ChangeSlideDestination
    STAGE_ONLY: ActionSlideDestination.ChangeSlideDestination
    STAGE_AUDIENCE: ActionSlideDestination.ChangeSlideDestination
    CHANGE_SLIDE_DESTINATION_FIELD_NUMBER: _ClassVar[int]
    change_slide_destination: ActionSlideDestination.ChangeSlideDestination
    def __init__(self, change_slide_destination: _Optional[_Union[ActionSlideDestination.ChangeSlideDestination, str]] = ...) -> None: ...

class ActionStage(_message.Message):
    __slots__ = ("layouts", "total_stage_screens")
    LAYOUTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_STAGE_SCREENS_FIELD_NUMBER: _ClassVar[int]
    layouts: int
    total_stage_screens: int
    def __init__(self, layouts: _Optional[int] = ..., total_stage_screens: _Optional[int] = ...) -> None: ...

class ActionTimer(_message.Message):
    __slots__ = ("type",)
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ActionTimer.Type]
        START_SET_CONFIGURATION: _ClassVar[ActionTimer.Type]
        START: _ClassVar[ActionTimer.Type]
        STOP: _ClassVar[ActionTimer.Type]
        RESET: _ClassVar[ActionTimer.Type]
        STOP_SET_CONFIGURATION: _ClassVar[ActionTimer.Type]
        INCREMENT: _ClassVar[ActionTimer.Type]
    UNKNOWN: ActionTimer.Type
    START_SET_CONFIGURATION: ActionTimer.Type
    START: ActionTimer.Type
    STOP: ActionTimer.Type
    RESET: ActionTimer.Type
    STOP_SET_CONFIGURATION: ActionTimer.Type
    INCREMENT: ActionTimer.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: ActionTimer.Type
    def __init__(self, type: _Optional[_Union[ActionTimer.Type, str]] = ...) -> None: ...

class TestPattern(_message.Message):
    __slots__ = ("pattern", "logo")
    class Pattern(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AUDIO_VIDEO_SYNC: _ClassVar[TestPattern.Pattern]
        BLEND_GRID: _ClassVar[TestPattern.Pattern]
        COLOR_BARS: _ClassVar[TestPattern.Pattern]
        CUSTOM_COLORS: _ClassVar[TestPattern.Pattern]
        FOCUS: _ClassVar[TestPattern.Pattern]
        GRAY_SCALE: _ClassVar[TestPattern.Pattern]
        LINES: _ClassVar[TestPattern.Pattern]
        LOGO_BOUNCE: _ClassVar[TestPattern.Pattern]
        RADAR: _ClassVar[TestPattern.Pattern]
        TEXT: _ClassVar[TestPattern.Pattern]
    AUDIO_VIDEO_SYNC: TestPattern.Pattern
    BLEND_GRID: TestPattern.Pattern
    COLOR_BARS: TestPattern.Pattern
    CUSTOM_COLORS: TestPattern.Pattern
    FOCUS: TestPattern.Pattern
    GRAY_SCALE: TestPattern.Pattern
    LINES: TestPattern.Pattern
    LOGO_BOUNCE: TestPattern.Pattern
    RADAR: TestPattern.Pattern
    TEXT: TestPattern.Pattern
    class Logo(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[TestPattern.Logo]
        PROPRESENTER: _ClassVar[TestPattern.Logo]
        CUSTOM: _ClassVar[TestPattern.Logo]
    NONE: TestPattern.Logo
    PROPRESENTER: TestPattern.Logo
    CUSTOM: TestPattern.Logo
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    pattern: TestPattern.Pattern
    logo: TestPattern.Logo
    def __init__(self, pattern: _Optional[_Union[TestPattern.Pattern, str]] = ..., logo: _Optional[_Union[TestPattern.Logo, str]] = ...) -> None: ...
