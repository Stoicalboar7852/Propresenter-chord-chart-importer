from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Codec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    H264: _ClassVar[Codec]
    H264SOFTWARE: _ClassVar[Codec]
    H265: _ClassVar[Codec]
    H265SOFTWARE: _ClassVar[Codec]
    PRORES422PROXY: _ClassVar[Codec]
    PRORES422LT: _ClassVar[Codec]
    PRORES422: _ClassVar[Codec]
    PRORES422HQ: _ClassVar[Codec]
    PRORES4444: _ClassVar[Codec]
    PRORES4444XQ: _ClassVar[Codec]
    HAP: _ClassVar[Codec]
    HAPALPHA: _ClassVar[Codec]
    NOTCH: _ClassVar[Codec]
    AUTOMATIC: _ClassVar[Codec]
    HAPQ: _ClassVar[Codec]
    HAPQALPHA: _ClassVar[Codec]

class FrameRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[FrameRate]
    _24FPS: _ClassVar[FrameRate]
    _25FPS: _ClassVar[FrameRate]
    _2997FPS: _ClassVar[FrameRate]
    _30FPS: _ClassVar[FrameRate]
    _50FPS: _ClassVar[FrameRate]
    _5994FPS: _ClassVar[FrameRate]
    _60FPS: _ClassVar[FrameRate]
H264: Codec
H264SOFTWARE: Codec
H265: Codec
H265SOFTWARE: Codec
PRORES422PROXY: Codec
PRORES422LT: Codec
PRORES422: Codec
PRORES422HQ: Codec
PRORES4444: Codec
PRORES4444XQ: Codec
HAP: Codec
HAPALPHA: Codec
NOTCH: Codec
AUTOMATIC: Codec
HAPQ: Codec
HAPQALPHA: Codec
UNSPECIFIED: FrameRate
_24FPS: FrameRate
_25FPS: FrameRate
_2997FPS: FrameRate
_30FPS: FrameRate
_50FPS: FrameRate
_5994FPS: FrameRate
_60FPS: FrameRate

class GenericEvent(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ApplicationLaunch(_message.Message):
    __slots__ = ("hardware_id", "channel", "platform", "app_version", "os_version", "build_number", "location", "language", "hardware_model", "physical_memory", "video_controller", "video_controller_ram", "blackmagic_desktop_version", "enabled_feature_flags", "organization_id")
    class Channel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BETA: _ClassVar[ApplicationLaunch.Channel]
        RELEASE: _ClassVar[ApplicationLaunch.Channel]
    BETA: ApplicationLaunch.Channel
    RELEASE: ApplicationLaunch.Channel
    class Platform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        WINDOWS: _ClassVar[ApplicationLaunch.Platform]
        MACOS: _ClassVar[ApplicationLaunch.Platform]
    WINDOWS: ApplicationLaunch.Platform
    MACOS: ApplicationLaunch.Platform
    HARDWARE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_MODEL_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_MEMORY_FIELD_NUMBER: _ClassVar[int]
    VIDEO_CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    VIDEO_CONTROLLER_RAM_FIELD_NUMBER: _ClassVar[int]
    BLACKMAGIC_DESKTOP_VERSION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    hardware_id: str
    channel: ApplicationLaunch.Channel
    platform: ApplicationLaunch.Platform
    app_version: str
    os_version: str
    build_number: str
    location: str
    language: str
    hardware_model: str
    physical_memory: int
    video_controller: str
    video_controller_ram: int
    blackmagic_desktop_version: str
    enabled_feature_flags: _containers.RepeatedScalarFieldContainer[str]
    organization_id: str
    def __init__(self, hardware_id: _Optional[str] = ..., channel: _Optional[_Union[ApplicationLaunch.Channel, str]] = ..., platform: _Optional[_Union[ApplicationLaunch.Platform, str]] = ..., app_version: _Optional[str] = ..., os_version: _Optional[str] = ..., build_number: _Optional[str] = ..., location: _Optional[str] = ..., language: _Optional[str] = ..., hardware_model: _Optional[str] = ..., physical_memory: _Optional[int] = ..., video_controller: _Optional[str] = ..., video_controller_ram: _Optional[int] = ..., blackmagic_desktop_version: _Optional[str] = ..., enabled_feature_flags: _Optional[_Iterable[str]] = ..., organization_id: _Optional[str] = ...) -> None: ...

class VideoInputTriggered(_message.Message):
    __slots__ = ("audio_source",)
    class AudioSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[VideoInputTriggered.AudioSource]
        SELF: _ClassVar[VideoInputTriggered.AudioSource]
        OTHER: _ClassVar[VideoInputTriggered.AudioSource]
    NONE: VideoInputTriggered.AudioSource
    SELF: VideoInputTriggered.AudioSource
    OTHER: VideoInputTriggered.AudioSource
    AUDIO_SOURCE_FIELD_NUMBER: _ClassVar[int]
    audio_source: VideoInputTriggered.AudioSource
    def __init__(self, audio_source: _Optional[_Union[VideoInputTriggered.AudioSource, str]] = ...) -> None: ...

class VideoInputCustomMap(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: _Optional[bool] = ...) -> None: ...

class VideoInputStartUp(_message.Message):
    __slots__ = ("input_count",)
    INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    input_count: int
    def __init__(self, input_count: _Optional[int] = ...) -> None: ...

class VideoInputThumbnailUpdate(_message.Message):
    __slots__ = ("type",)
    class UpdateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CAPTURE: _ClassVar[VideoInputThumbnailUpdate.UpdateType]
        DISK: _ClassVar[VideoInputThumbnailUpdate.UpdateType]
        RESET: _ClassVar[VideoInputThumbnailUpdate.UpdateType]
    CAPTURE: VideoInputThumbnailUpdate.UpdateType
    DISK: VideoInputThumbnailUpdate.UpdateType
    RESET: VideoInputThumbnailUpdate.UpdateType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: VideoInputThumbnailUpdate.UpdateType
    def __init__(self, type: _Optional[_Union[VideoInputThumbnailUpdate.UpdateType, str]] = ...) -> None: ...

class AudioInputAutoOnChange(_message.Message):
    __slots__ = ("input_count",)
    INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    input_count: int
    def __init__(self, input_count: _Optional[int] = ...) -> None: ...

class AudioSettingsSdiNdiActive(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: _Optional[bool] = ...) -> None: ...

class AudioSettingsCustomMap(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: _Optional[bool] = ...) -> None: ...

class AudioInputModeSelection(_message.Message):
    __slots__ = ("mode_type",)
    class ModeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ON: _ClassVar[AudioInputModeSelection.ModeType]
        OFF: _ClassVar[AudioInputModeSelection.ModeType]
        AUTOOFF: _ClassVar[AudioInputModeSelection.ModeType]
        AUTOON: _ClassVar[AudioInputModeSelection.ModeType]
    ON: AudioInputModeSelection.ModeType
    OFF: AudioInputModeSelection.ModeType
    AUTOOFF: AudioInputModeSelection.ModeType
    AUTOON: AudioInputModeSelection.ModeType
    MODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    mode_type: AudioInputModeSelection.ModeType
    def __init__(self, mode_type: _Optional[_Union[AudioInputModeSelection.ModeType, str]] = ...) -> None: ...

class AudioInputAutoOnStartup(_message.Message):
    __slots__ = ("input_count",)
    INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    input_count: int
    def __init__(self, input_count: _Optional[int] = ...) -> None: ...

class AudioSettingsSdiNdiState(_message.Message):
    __slots__ = ("bus_count",)
    BUS_COUNT_FIELD_NUMBER: _ClassVar[int]
    bus_count: int
    def __init__(self, bus_count: _Optional[int] = ...) -> None: ...

class AudioInputStartUp(_message.Message):
    __slots__ = ("total_input_count", "on_input_count", "off_input_count", "auto_on_input_count", "auto_off_input_count")
    TOTAL_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    ON_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    OFF_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTO_ON_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTO_OFF_INPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
    total_input_count: int
    on_input_count: int
    off_input_count: int
    auto_on_input_count: int
    auto_off_input_count: int
    def __init__(self, total_input_count: _Optional[int] = ..., on_input_count: _Optional[int] = ..., off_input_count: _Optional[int] = ..., auto_on_input_count: _Optional[int] = ..., auto_off_input_count: _Optional[int] = ...) -> None: ...

class CueTriggered(_message.Message):
    __slots__ = ("trigger_delay",)
    TRIGGER_DELAY_FIELD_NUMBER: _ClassVar[int]
    trigger_delay: float
    def __init__(self, trigger_delay: _Optional[float] = ...) -> None: ...

class InputAudioMonitoring(_message.Message):
    __slots__ = ("type",)
    class InputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AUDIO: _ClassVar[InputAudioMonitoring.InputType]
        VIDEO: _ClassVar[InputAudioMonitoring.InputType]
    AUDIO: InputAudioMonitoring.InputType
    VIDEO: InputAudioMonitoring.InputType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: InputAudioMonitoring.InputType
    def __init__(self, type: _Optional[_Union[InputAudioMonitoring.InputType, str]] = ...) -> None: ...

class ResiStartUp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResiLoginChange(_message.Message):
    __slots__ = ("state",)
    class LoginState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOGGEDIN: _ClassVar[ResiLoginChange.LoginState]
        LOGGEDOUT: _ClassVar[ResiLoginChange.LoginState]
    LOGGEDIN: ResiLoginChange.LoginState
    LOGGEDOUT: ResiLoginChange.LoginState
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: ResiLoginChange.LoginState
    def __init__(self, state: _Optional[_Union[ResiLoginChange.LoginState, str]] = ...) -> None: ...

class RemoteStreamStart(_message.Message):
    __slots__ = ("result",)
    class StartResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[RemoteStreamStart.StartResult]
        FAILED: _ClassVar[RemoteStreamStart.StartResult]
        USERCANCELED: _ClassVar[RemoteStreamStart.StartResult]
    SUCCESS: RemoteStreamStart.StartResult
    FAILED: RemoteStreamStart.StartResult
    USERCANCELED: RemoteStreamStart.StartResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RemoteStreamStart.StartResult
    def __init__(self, result: _Optional[_Union[RemoteStreamStart.StartResult, str]] = ...) -> None: ...

class RemoteStreamStop(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: _Optional[bool] = ...) -> None: ...

class StartCaptureDisk(_message.Message):
    __slots__ = ("codec", "resolution_width", "resolution_height", "frame_rate", "stream_started", "video_bitrate")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_WIDTH_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    STREAM_STARTED_FIELD_NUMBER: _ClassVar[int]
    VIDEO_BITRATE_FIELD_NUMBER: _ClassVar[int]
    codec: Codec
    resolution_width: int
    resolution_height: int
    frame_rate: FrameRate
    stream_started: bool
    video_bitrate: int
    def __init__(self, codec: _Optional[_Union[Codec, str]] = ..., resolution_width: _Optional[int] = ..., resolution_height: _Optional[int] = ..., frame_rate: _Optional[_Union[FrameRate, str]] = ..., stream_started: _Optional[bool] = ..., video_bitrate: _Optional[int] = ...) -> None: ...

class StartCaptureRtmp(_message.Message):
    __slots__ = ("codec", "resolution_width", "resolution_height", "frame_rate", "stream_started", "video_bitrate")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_WIDTH_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    STREAM_STARTED_FIELD_NUMBER: _ClassVar[int]
    VIDEO_BITRATE_FIELD_NUMBER: _ClassVar[int]
    codec: Codec
    resolution_width: int
    resolution_height: int
    frame_rate: FrameRate
    stream_started: bool
    video_bitrate: int
    def __init__(self, codec: _Optional[_Union[Codec, str]] = ..., resolution_width: _Optional[int] = ..., resolution_height: _Optional[int] = ..., frame_rate: _Optional[_Union[FrameRate, str]] = ..., stream_started: _Optional[bool] = ..., video_bitrate: _Optional[int] = ...) -> None: ...

class StartCaptureResi(_message.Message):
    __slots__ = ("codec", "resolution_width", "resolution_height", "frame_rate", "stream_started", "video_bitrate")
    CODEC_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_WIDTH_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
    STREAM_STARTED_FIELD_NUMBER: _ClassVar[int]
    VIDEO_BITRATE_FIELD_NUMBER: _ClassVar[int]
    codec: Codec
    resolution_width: int
    resolution_height: int
    frame_rate: FrameRate
    stream_started: bool
    video_bitrate: int
    def __init__(self, codec: _Optional[_Union[Codec, str]] = ..., resolution_width: _Optional[int] = ..., resolution_height: _Optional[int] = ..., frame_rate: _Optional[_Union[FrameRate, str]] = ..., stream_started: _Optional[bool] = ..., video_bitrate: _Optional[int] = ...) -> None: ...

class StopCapture(_message.Message):
    __slots__ = ("duration", "dropped_frames", "percent_dropped_frames")
    DURATION_FIELD_NUMBER: _ClassVar[int]
    DROPPED_FRAMES_FIELD_NUMBER: _ClassVar[int]
    PERCENT_DROPPED_FRAMES_FIELD_NUMBER: _ClassVar[int]
    duration: float
    dropped_frames: int
    percent_dropped_frames: float
    def __init__(self, duration: _Optional[float] = ..., dropped_frames: _Optional[int] = ..., percent_dropped_frames: _Optional[float] = ...) -> None: ...

class Print(_message.Message):
    __slots__ = ("document_count", "mode", "include_metadata", "include_presentation_notes", "include_currentDate", "include_slide_labels", "include_slide_notes", "include_disabled_slides", "number_columns", "print_to_device")
    class PrintMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        THUMBNAIL: _ClassVar[Print.PrintMode]
        OUTLINE: _ClassVar[Print.PrintMode]
    THUMBNAIL: Print.PrintMode
    OUTLINE: Print.PrintMode
    DOCUMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_METADATA_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PRESENTATION_NOTES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CURRENTDATE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SLIDE_LABELS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SLIDE_NOTES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISABLED_SLIDES_FIELD_NUMBER: _ClassVar[int]
    NUMBER_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    PRINT_TO_DEVICE_FIELD_NUMBER: _ClassVar[int]
    document_count: int
    mode: Print.PrintMode
    include_metadata: bool
    include_presentation_notes: bool
    include_currentDate: bool
    include_slide_labels: bool
    include_slide_notes: bool
    include_disabled_slides: bool
    number_columns: int
    print_to_device: str
    def __init__(self, document_count: _Optional[int] = ..., mode: _Optional[_Union[Print.PrintMode, str]] = ..., include_metadata: _Optional[bool] = ..., include_presentation_notes: _Optional[bool] = ..., include_currentDate: _Optional[bool] = ..., include_slide_labels: _Optional[bool] = ..., include_slide_notes: _Optional[bool] = ..., include_disabled_slides: _Optional[bool] = ..., number_columns: _Optional[int] = ..., print_to_device: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("protocol", "device_name", "device_protocol")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    protocol: str
    device_name: str
    device_protocol: str
    def __init__(self, protocol: _Optional[str] = ..., device_name: _Optional[str] = ..., device_protocol: _Optional[str] = ...) -> None: ...

class Downgrade(_message.Message):
    __slots__ = ("from_version_type",)
    class FromVersionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FROM_VERSION_TYPE_UNKNOWN: _ClassVar[Downgrade.FromVersionType]
        FROM_VERSION_TYPE_BETA: _ClassVar[Downgrade.FromVersionType]
        FROM_VERSION_TYPE_RELEASE: _ClassVar[Downgrade.FromVersionType]
    FROM_VERSION_TYPE_UNKNOWN: Downgrade.FromVersionType
    FROM_VERSION_TYPE_BETA: Downgrade.FromVersionType
    FROM_VERSION_TYPE_RELEASE: Downgrade.FromVersionType
    FROM_VERSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    from_version_type: Downgrade.FromVersionType
    def __init__(self, from_version_type: _Optional[_Union[Downgrade.FromVersionType, str]] = ...) -> None: ...

class CCLIReport(_message.Message):
    __slots__ = ("action",)
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REPORT_WINDOW_OPENED: _ClassVar[CCLIReport.Action]
        REPORT_CLEARED: _ClassVar[CCLIReport.Action]
        REPORT_EXPORTED: _ClassVar[CCLIReport.Action]
    REPORT_WINDOW_OPENED: CCLIReport.Action
    REPORT_CLEARED: CCLIReport.Action
    REPORT_EXPORTED: CCLIReport.Action
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: CCLIReport.Action
    def __init__(self, action: _Optional[_Union[CCLIReport.Action, str]] = ...) -> None: ...

class TransitionWindow(_message.Message):
    __slots__ = ("duration_seconds",)
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    duration_seconds: int
    def __init__(self, duration_seconds: _Optional[int] = ...) -> None: ...

class EditorObjectAdded(_message.Message):
    __slots__ = ("from_insertion_source", "inserted_type")
    class FromInsertionSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EDITOR_TOOLBAR: _ClassVar[EditorObjectAdded.FromInsertionSource]
        EDITOR_MAIN_MENU: _ClassVar[EditorObjectAdded.FromInsertionSource]
        EDITOR_HOTKEY: _ClassVar[EditorObjectAdded.FromInsertionSource]
        EDITOR_COPY_PASTE: _ClassVar[EditorObjectAdded.FromInsertionSource]
    EDITOR_TOOLBAR: EditorObjectAdded.FromInsertionSource
    EDITOR_MAIN_MENU: EditorObjectAdded.FromInsertionSource
    EDITOR_HOTKEY: EditorObjectAdded.FromInsertionSource
    EDITOR_COPY_PASTE: EditorObjectAdded.FromInsertionSource
    class InsertedType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EDITOR_TEXT: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_SHAPE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_CUSTOM_SHAPE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_MEDIA: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_VIDEO_INPUT: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_WEB: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_CURRENT_SLIDE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_NEXT_SLIDE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_SCREEN_PREVIEW: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_TIMER: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_SYSTEM_CLOCK: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_VIDEO_COUNTDOWN: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_AUDIO_COUNTDOWN: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_PLAYBACK_MARKER: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_CHORD_CHART: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_STAGE_MESSAGE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_PLANNING_CENTER_LIVE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_TIMECODE: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_GROUP: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_LABEL: _ClassVar[EditorObjectAdded.InsertedType]
        EDITOR_CAPTURE_STATUS: _ClassVar[EditorObjectAdded.InsertedType]
    EDITOR_TEXT: EditorObjectAdded.InsertedType
    EDITOR_SHAPE: EditorObjectAdded.InsertedType
    EDITOR_CUSTOM_SHAPE: EditorObjectAdded.InsertedType
    EDITOR_MEDIA: EditorObjectAdded.InsertedType
    EDITOR_VIDEO_INPUT: EditorObjectAdded.InsertedType
    EDITOR_WEB: EditorObjectAdded.InsertedType
    EDITOR_CURRENT_SLIDE: EditorObjectAdded.InsertedType
    EDITOR_NEXT_SLIDE: EditorObjectAdded.InsertedType
    EDITOR_SCREEN_PREVIEW: EditorObjectAdded.InsertedType
    EDITOR_TIMER: EditorObjectAdded.InsertedType
    EDITOR_SYSTEM_CLOCK: EditorObjectAdded.InsertedType
    EDITOR_VIDEO_COUNTDOWN: EditorObjectAdded.InsertedType
    EDITOR_AUDIO_COUNTDOWN: EditorObjectAdded.InsertedType
    EDITOR_PLAYBACK_MARKER: EditorObjectAdded.InsertedType
    EDITOR_CHORD_CHART: EditorObjectAdded.InsertedType
    EDITOR_STAGE_MESSAGE: EditorObjectAdded.InsertedType
    EDITOR_PLANNING_CENTER_LIVE: EditorObjectAdded.InsertedType
    EDITOR_TIMECODE: EditorObjectAdded.InsertedType
    EDITOR_GROUP: EditorObjectAdded.InsertedType
    EDITOR_LABEL: EditorObjectAdded.InsertedType
    EDITOR_CAPTURE_STATUS: EditorObjectAdded.InsertedType
    FROM_INSERTION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    INSERTED_TYPE_FIELD_NUMBER: _ClassVar[int]
    from_insertion_source: EditorObjectAdded.FromInsertionSource
    inserted_type: EditorObjectAdded.InsertedType
    def __init__(self, from_insertion_source: _Optional[_Union[EditorObjectAdded.FromInsertionSource, str]] = ..., inserted_type: _Optional[_Union[EditorObjectAdded.InsertedType, str]] = ...) -> None: ...

class DataIdDuplicated(_message.Message):
    __slots__ = ("Type", "number_duplicates")
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DATA_TYPE_PRESENTATION: _ClassVar[DataIdDuplicated.DataType]
        DATA_TYPE_MEDIA: _ClassVar[DataIdDuplicated.DataType]
    DATA_TYPE_PRESENTATION: DataIdDuplicated.DataType
    DATA_TYPE_MEDIA: DataIdDuplicated.DataType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_DUPLICATES_FIELD_NUMBER: _ClassVar[int]
    Type: DataIdDuplicated.DataType
    number_duplicates: int
    def __init__(self, Type: _Optional[_Union[DataIdDuplicated.DataType, str]] = ..., number_duplicates: _Optional[int] = ...) -> None: ...

class ForceQuit(_message.Message):
    __slots__ = ("reason",)
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ForceQuit.Reason]
        HOSTS_FILE: _ClassVar[ForceQuit.Reason]
        SYSTEM_TIME_SKEW: _ClassVar[ForceQuit.Reason]
        INVALID_WATERMARK: _ClassVar[ForceQuit.Reason]
        PIRATED_SOFTWARE: _ClassVar[ForceQuit.Reason]
        METAL_UNAVAILABLE: _ClassVar[ForceQuit.Reason]
        UBIQUITY_DOWNLOAD_ABORTED: _ClassVar[ForceQuit.Reason]
        CORE_RUST_CONTROLLER_FAILURE: _ClassVar[ForceQuit.Reason]
    UNKNOWN: ForceQuit.Reason
    HOSTS_FILE: ForceQuit.Reason
    SYSTEM_TIME_SKEW: ForceQuit.Reason
    INVALID_WATERMARK: ForceQuit.Reason
    PIRATED_SOFTWARE: ForceQuit.Reason
    METAL_UNAVAILABLE: ForceQuit.Reason
    UBIQUITY_DOWNLOAD_ABORTED: ForceQuit.Reason
    CORE_RUST_CONTROLLER_FAILURE: ForceQuit.Reason
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: ForceQuit.Reason
    def __init__(self, reason: _Optional[_Union[ForceQuit.Reason, str]] = ...) -> None: ...

class MediaCleanupSize(_message.Message):
    __slots__ = ("bytes_of_media_files_cleaned_up",)
    BYTES_OF_MEDIA_FILES_CLEANED_UP_FIELD_NUMBER: _ClassVar[int]
    bytes_of_media_files_cleaned_up: int
    def __init__(self, bytes_of_media_files_cleaned_up: _Optional[int] = ...) -> None: ...

class NetworkApp(_message.Message):
    __slots__ = ("app_id", "device_id")
    class AppID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[NetworkApp.AppID]
        PROREMOTE: _ClassVar[NetworkApp.AppID]
        PROSTAGE: _ClassVar[NetworkApp.AppID]
    UNKNOWN: NetworkApp.AppID
    PROREMOTE: NetworkApp.AppID
    PROSTAGE: NetworkApp.AppID
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: NetworkApp.AppID
    device_id: str
    def __init__(self, app_id: _Optional[_Union[NetworkApp.AppID, str]] = ..., device_id: _Optional[str] = ...) -> None: ...

class LocalWorkspaceStats(_message.Message):
    __slots__ = ("total_workspaces", "number_of_workspace_switches")
    TOTAL_WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_WORKSPACE_SWITCHES_FIELD_NUMBER: _ClassVar[int]
    total_workspaces: int
    number_of_workspace_switches: int
    def __init__(self, total_workspaces: _Optional[int] = ..., number_of_workspace_switches: _Optional[int] = ...) -> None: ...

class FontReplacement(_message.Message):
    __slots__ = ("source", "missing_font", "replacement_font")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IMPORT: _ClassVar[FontReplacement.Source]
        BANNER: _ClassVar[FontReplacement.Source]
    IMPORT: FontReplacement.Source
    BANNER: FontReplacement.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    MISSING_FONT_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_FONT_FIELD_NUMBER: _ClassVar[int]
    source: FontReplacement.Source
    missing_font: str
    replacement_font: str
    def __init__(self, source: _Optional[_Union[FontReplacement.Source, str]] = ..., missing_font: _Optional[str] = ..., replacement_font: _Optional[str] = ...) -> None: ...

class TriggerExternalPresentation(_message.Message):
    __slots__ = ("type",)
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        POWERPOINT: _ClassVar[TriggerExternalPresentation.Type]
        KEYNOTE: _ClassVar[TriggerExternalPresentation.Type]
    POWERPOINT: TriggerExternalPresentation.Type
    KEYNOTE: TriggerExternalPresentation.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: TriggerExternalPresentation.Type
    def __init__(self, type: _Optional[_Union[TriggerExternalPresentation.Type, str]] = ...) -> None: ...

class WorkspaceCreation(_message.Message):
    __slots__ = ("source", "duration_seconds")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CLOUD_ONBOARDING: _ClassVar[WorkspaceCreation.Source]
        USER_ONBOARDING: _ClassVar[WorkspaceCreation.Source]
        SETTINGS: _ClassVar[WorkspaceCreation.Source]
    CLOUD_ONBOARDING: WorkspaceCreation.Source
    USER_ONBOARDING: WorkspaceCreation.Source
    SETTINGS: WorkspaceCreation.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    source: WorkspaceCreation.Source
    duration_seconds: int
    def __init__(self, source: _Optional[_Union[WorkspaceCreation.Source, str]] = ..., duration_seconds: _Optional[int] = ...) -> None: ...

class AvailableWorkspace(_message.Message):
    __slots__ = ("type", "size_in_bytes", "is_current")
    class WorkspaceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOCAL: _ClassVar[AvailableWorkspace.WorkspaceType]
        CLOUD_UNDOWNLOADED: _ClassVar[AvailableWorkspace.WorkspaceType]
        CLOUD_DOWNLOADED: _ClassVar[AvailableWorkspace.WorkspaceType]
    LOCAL: AvailableWorkspace.WorkspaceType
    CLOUD_UNDOWNLOADED: AvailableWorkspace.WorkspaceType
    CLOUD_DOWNLOADED: AvailableWorkspace.WorkspaceType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_IN_BYTES_FIELD_NUMBER: _ClassVar[int]
    IS_CURRENT_FIELD_NUMBER: _ClassVar[int]
    type: AvailableWorkspace.WorkspaceType
    size_in_bytes: int
    is_current: bool
    def __init__(self, type: _Optional[_Union[AvailableWorkspace.WorkspaceType, str]] = ..., size_in_bytes: _Optional[int] = ..., is_current: _Optional[bool] = ...) -> None: ...

class OnboardingFlowOutcome(_message.Message):
    __slots__ = ("onboarding_type", "result")
    class OnboardingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NEW_TO_CLOUD: _ClassVar[OnboardingFlowOutcome.OnboardingType]
        NEW_USER: _ClassVar[OnboardingFlowOutcome.OnboardingType]
    NEW_TO_CLOUD: OnboardingFlowOutcome.OnboardingType
    NEW_USER: OnboardingFlowOutcome.OnboardingType
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SKIP_FOR_NOW: _ClassVar[OnboardingFlowOutcome.Result]
        CONTINUE_WITH_LOCAL: _ClassVar[OnboardingFlowOutcome.Result]
        CREATE_CLOUD: _ClassVar[OnboardingFlowOutcome.Result]
        JOIN_CLOUD: _ClassVar[OnboardingFlowOutcome.Result]
    SKIP_FOR_NOW: OnboardingFlowOutcome.Result
    CONTINUE_WITH_LOCAL: OnboardingFlowOutcome.Result
    CREATE_CLOUD: OnboardingFlowOutcome.Result
    JOIN_CLOUD: OnboardingFlowOutcome.Result
    ONBOARDING_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    onboarding_type: OnboardingFlowOutcome.OnboardingType
    result: OnboardingFlowOutcome.Result
    def __init__(self, onboarding_type: _Optional[_Union[OnboardingFlowOutcome.OnboardingType, str]] = ..., result: _Optional[_Union[OnboardingFlowOutcome.Result, str]] = ...) -> None: ...

class SyncingUnpaused(_message.Message):
    __slots__ = ("duration",)
    DURATION_FIELD_NUMBER: _ClassVar[int]
    duration: int
    def __init__(self, duration: _Optional[int] = ...) -> None: ...

class UserWorkspaceTreeModification(_message.Message):
    __slots__ = ("bucket", "operation")
    class Bucket(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OTHER: _ClassVar[UserWorkspaceTreeModification.Bucket]
        LIBRARIES: _ClassVar[UserWorkspaceTreeModification.Bucket]
        THEMES: _ClassVar[UserWorkspaceTreeModification.Bucket]
        PLAYLISTS: _ClassVar[UserWorkspaceTreeModification.Bucket]
        PLAYLIST_TEMPLATES: _ClassVar[UserWorkspaceTreeModification.Bucket]
        CONFIGURATION: _ClassVar[UserWorkspaceTreeModification.Bucket]
        MEDIA: _ClassVar[UserWorkspaceTreeModification.Bucket]
        PRESETS: _ClassVar[UserWorkspaceTreeModification.Bucket]
        DOWNLOADS: _ClassVar[UserWorkspaceTreeModification.Bucket]
    OTHER: UserWorkspaceTreeModification.Bucket
    LIBRARIES: UserWorkspaceTreeModification.Bucket
    THEMES: UserWorkspaceTreeModification.Bucket
    PLAYLISTS: UserWorkspaceTreeModification.Bucket
    PLAYLIST_TEMPLATES: UserWorkspaceTreeModification.Bucket
    CONFIGURATION: UserWorkspaceTreeModification.Bucket
    MEDIA: UserWorkspaceTreeModification.Bucket
    PRESETS: UserWorkspaceTreeModification.Bucket
    DOWNLOADS: UserWorkspaceTreeModification.Bucket
    class Operation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MODIFIED: _ClassVar[UserWorkspaceTreeModification.Operation]
        CREATED: _ClassVar[UserWorkspaceTreeModification.Operation]
        RENAMED: _ClassVar[UserWorkspaceTreeModification.Operation]
        REMOVED: _ClassVar[UserWorkspaceTreeModification.Operation]
    MODIFIED: UserWorkspaceTreeModification.Operation
    CREATED: UserWorkspaceTreeModification.Operation
    RENAMED: UserWorkspaceTreeModification.Operation
    REMOVED: UserWorkspaceTreeModification.Operation
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    bucket: UserWorkspaceTreeModification.Bucket
    operation: UserWorkspaceTreeModification.Operation
    def __init__(self, bucket: _Optional[_Union[UserWorkspaceTreeModification.Bucket, str]] = ..., operation: _Optional[_Union[UserWorkspaceTreeModification.Operation, str]] = ...) -> None: ...
