from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompletionTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[CompletionTarget]
    NEXT: _ClassVar[CompletionTarget]
    RANDOM: _ClassVar[CompletionTarget]
    CUE: _ClassVar[CompletionTarget]
    FIRST: _ClassVar[CompletionTarget]

class SourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCAL: _ClassVar[SourceType]
    PROCONTENT: _ClassVar[SourceType]
NONE: CompletionTarget
NEXT: CompletionTarget
RANDOM: CompletionTarget
CUE: CompletionTarget
FIRST: CompletionTarget
LOCAL: SourceType
PROCONTENT: SourceType

class Transition(_message.Message):
    __slots__ = ("is_default", "name")
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    is_default: bool
    name: str
    def __init__(self, is_default: _Optional[bool] = ..., name: _Optional[str] = ...) -> None: ...

class VisualMedia(_message.Message):
    __slots__ = ("behavior", "scale_mode", "flip_mode", "native_rotation", "resolution", "enabled_effects_count", "has_effect_preset", "transition")
    class Behavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BACKGROUND: _ClassVar[VisualMedia.Behavior]
        FOREGROUND: _ClassVar[VisualMedia.Behavior]
        VIDEO_INPUT: _ClassVar[VisualMedia.Behavior]
    BACKGROUND: VisualMedia.Behavior
    FOREGROUND: VisualMedia.Behavior
    VIDEO_INPUT: VisualMedia.Behavior
    class ScaleMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FIT: _ClassVar[VisualMedia.ScaleMode]
        FILL: _ClassVar[VisualMedia.ScaleMode]
        STRETCH: _ClassVar[VisualMedia.ScaleMode]
        BLUR: _ClassVar[VisualMedia.ScaleMode]
    FIT: VisualMedia.ScaleMode
    FILL: VisualMedia.ScaleMode
    STRETCH: VisualMedia.ScaleMode
    BLUR: VisualMedia.ScaleMode
    class FlipMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[VisualMedia.FlipMode]
        HORIZONTAL: _ClassVar[VisualMedia.FlipMode]
        VERTICAL: _ClassVar[VisualMedia.FlipMode]
        BOTH: _ClassVar[VisualMedia.FlipMode]
    NONE: VisualMedia.FlipMode
    HORIZONTAL: VisualMedia.FlipMode
    VERTICAL: VisualMedia.FlipMode
    BOTH: VisualMedia.FlipMode
    class NativeRotation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STANDARD: _ClassVar[VisualMedia.NativeRotation]
        _90: _ClassVar[VisualMedia.NativeRotation]
        _180: _ClassVar[VisualMedia.NativeRotation]
        _270: _ClassVar[VisualMedia.NativeRotation]
    STANDARD: VisualMedia.NativeRotation
    _90: VisualMedia.NativeRotation
    _180: VisualMedia.NativeRotation
    _270: VisualMedia.NativeRotation
    class Size(_message.Message):
        __slots__ = ("width", "height")
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        width: int
        height: int
        def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    SCALE_MODE_FIELD_NUMBER: _ClassVar[int]
    FLIP_MODE_FIELD_NUMBER: _ClassVar[int]
    NATIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_EFFECTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    HAS_EFFECT_PRESET_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    behavior: VisualMedia.Behavior
    scale_mode: VisualMedia.ScaleMode
    flip_mode: VisualMedia.FlipMode
    native_rotation: VisualMedia.NativeRotation
    resolution: VisualMedia.Size
    enabled_effects_count: int
    has_effect_preset: bool
    transition: Transition
    def __init__(self, behavior: _Optional[_Union[VisualMedia.Behavior, str]] = ..., scale_mode: _Optional[_Union[VisualMedia.ScaleMode, str]] = ..., flip_mode: _Optional[_Union[VisualMedia.FlipMode, str]] = ..., native_rotation: _Optional[_Union[VisualMedia.NativeRotation, str]] = ..., resolution: _Optional[_Union[VisualMedia.Size, _Mapping]] = ..., enabled_effects_count: _Optional[int] = ..., has_effect_preset: _Optional[bool] = ..., transition: _Optional[_Union[Transition, _Mapping]] = ...) -> None: ...

class Transport(_message.Message):
    __slots__ = ("source_duration_range", "has_audio_ramp_in", "has_audio_ramp_out", "has_in_point", "has_out_point", "play_rate", "playback_marker_count")
    class DurationRange(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDER_10S: _ClassVar[Transport.DurationRange]
        _10S_TO_30S: _ClassVar[Transport.DurationRange]
        _30S_TO_60S: _ClassVar[Transport.DurationRange]
        _1M_TO_5M: _ClassVar[Transport.DurationRange]
        _5M_TO_10M: _ClassVar[Transport.DurationRange]
        _10M_TO_30M: _ClassVar[Transport.DurationRange]
        _30M_TO_60M: _ClassVar[Transport.DurationRange]
        _1H_TO_2H: _ClassVar[Transport.DurationRange]
        OVER_2H: _ClassVar[Transport.DurationRange]
    UNDER_10S: Transport.DurationRange
    _10S_TO_30S: Transport.DurationRange
    _30S_TO_60S: Transport.DurationRange
    _1M_TO_5M: Transport.DurationRange
    _5M_TO_10M: Transport.DurationRange
    _10M_TO_30M: Transport.DurationRange
    _30M_TO_60M: Transport.DurationRange
    _1H_TO_2H: Transport.DurationRange
    OVER_2H: Transport.DurationRange
    SOURCE_DURATION_RANGE_FIELD_NUMBER: _ClassVar[int]
    HAS_AUDIO_RAMP_IN_FIELD_NUMBER: _ClassVar[int]
    HAS_AUDIO_RAMP_OUT_FIELD_NUMBER: _ClassVar[int]
    HAS_IN_POINT_FIELD_NUMBER: _ClassVar[int]
    HAS_OUT_POINT_FIELD_NUMBER: _ClassVar[int]
    PLAY_RATE_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_MARKER_COUNT_FIELD_NUMBER: _ClassVar[int]
    source_duration_range: Transport.DurationRange
    has_audio_ramp_in: bool
    has_audio_ramp_out: bool
    has_in_point: bool
    has_out_point: bool
    play_rate: float
    playback_marker_count: int
    def __init__(self, source_duration_range: _Optional[_Union[Transport.DurationRange, str]] = ..., has_audio_ramp_in: _Optional[bool] = ..., has_audio_ramp_out: _Optional[bool] = ..., has_in_point: _Optional[bool] = ..., has_out_point: _Optional[bool] = ..., play_rate: _Optional[float] = ..., playback_marker_count: _Optional[int] = ...) -> None: ...

class Video(_message.Message):
    __slots__ = ("visual_media", "playback_behavior", "completion_target", "soft_loop_enabled", "soft_loop_duration", "frame_rate", "audio_channel_count", "transport", "source_type", "hardware_decoding")
    class PlaybackBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STOP: _ClassVar[Video.PlaybackBehavior]
        LOOP: _ClassVar[Video.PlaybackBehavior]
        LOOP_FOR_PLAY_COUNT: _ClassVar[Video.PlaybackBehavior]
        LOOP_FOR_TIME: _ClassVar[Video.PlaybackBehavior]
    STOP: Video.PlaybackBehavior
    LOOP: Video.PlaybackBehavior
    LOOP_FOR_PLAY_COUNT: Video.PlaybackBehavior
    LOOP_FOR_TIME: Video.PlaybackBehavior
    class HardwareDecodingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AUTOMATIC: _ClassVar[Video.HardwareDecodingType]
        DISABLED: _ClassVar[Video.HardwareDecodingType]
    AUTOMATIC: Video.HardwareDecodingType
    DISABLED: Video.HardwareDecodingType
    VISUAL_MEDIA_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TARGET_FIELD_NUMBER: _ClassVar[int]
    SOFT_LOOP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SOFT_LOOP_DURATION_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_CHANNEL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_DECODING_FIELD_NUMBER: _ClassVar[int]
    visual_media: VisualMedia
    playback_behavior: Video.PlaybackBehavior
    completion_target: CompletionTarget
    soft_loop_enabled: bool
    soft_loop_duration: float
    frame_rate: float
    audio_channel_count: int
    transport: Transport
    source_type: SourceType
    hardware_decoding: Video.HardwareDecodingType
    def __init__(self, visual_media: _Optional[_Union[VisualMedia, _Mapping]] = ..., playback_behavior: _Optional[_Union[Video.PlaybackBehavior, str]] = ..., completion_target: _Optional[_Union[CompletionTarget, str]] = ..., soft_loop_enabled: _Optional[bool] = ..., soft_loop_duration: _Optional[float] = ..., frame_rate: _Optional[float] = ..., audio_channel_count: _Optional[int] = ..., transport: _Optional[_Union[Transport, _Mapping]] = ..., source_type: _Optional[_Union[SourceType, str]] = ..., hardware_decoding: _Optional[_Union[Video.HardwareDecodingType, str]] = ...) -> None: ...

class Audio(_message.Message):
    __slots__ = ("behavior", "playback_behavior", "transition", "audio_channel_count", "transport", "source_type")
    class Behavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TUNE: _ClassVar[Audio.Behavior]
        SOUND: _ClassVar[Audio.Behavior]
    TUNE: Audio.Behavior
    SOUND: Audio.Behavior
    class PlaybackBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STOP: _ClassVar[Audio.PlaybackBehavior]
        LOOP: _ClassVar[Audio.PlaybackBehavior]
        NEXT: _ClassVar[Audio.PlaybackBehavior]
    STOP: Audio.PlaybackBehavior
    LOOP: Audio.PlaybackBehavior
    NEXT: Audio.PlaybackBehavior
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    AUDIO_CHANNEL_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    behavior: Audio.Behavior
    playback_behavior: Audio.PlaybackBehavior
    transition: Transition
    audio_channel_count: int
    transport: Transport
    source_type: SourceType
    def __init__(self, behavior: _Optional[_Union[Audio.Behavior, str]] = ..., playback_behavior: _Optional[_Union[Audio.PlaybackBehavior, str]] = ..., transition: _Optional[_Union[Transition, _Mapping]] = ..., audio_channel_count: _Optional[int] = ..., transport: _Optional[_Union[Transport, _Mapping]] = ..., source_type: _Optional[_Union[SourceType, str]] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ("visual_media", "completion_target", "source_type")
    VISUAL_MEDIA_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TARGET_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    visual_media: VisualMedia
    completion_target: CompletionTarget
    source_type: SourceType
    def __init__(self, visual_media: _Optional[_Union[VisualMedia, _Mapping]] = ..., completion_target: _Optional[_Union[CompletionTarget, str]] = ..., source_type: _Optional[_Union[SourceType, str]] = ...) -> None: ...

class VideoInput(_message.Message):
    __slots__ = ("visual_media", "frame_rate", "audio_channel_count", "source_type")
    VISUAL_MEDIA_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    AUDIO_CHANNEL_COUNT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    visual_media: VisualMedia
    frame_rate: float
    audio_channel_count: int
    source_type: SourceType
    def __init__(self, visual_media: _Optional[_Union[VisualMedia, _Mapping]] = ..., frame_rate: _Optional[float] = ..., audio_channel_count: _Optional[int] = ..., source_type: _Optional[_Union[SourceType, str]] = ...) -> None: ...

class AirCastVideo(_message.Message):
    __slots__ = ("password_enabled",)
    PASSWORD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    password_enabled: bool
    def __init__(self, password_enabled: _Optional[bool] = ...) -> None: ...

class AirCastAudio(_message.Message):
    __slots__ = ("password_enabled",)
    PASSWORD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    password_enabled: bool
    def __init__(self, password_enabled: _Optional[bool] = ...) -> None: ...
