import effects_pb2 as _effects_pb2
import alphaType_pb2 as _alphaType_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Background: _ClassVar[Priority]
    UserInitiated: _ClassVar[Priority]
Background: Priority
UserInitiated: Priority

class ProductInformation(_message.Message):
    __slots__ = ("product_name", "major_version", "minor_version", "patch_version", "build_number", "build_date")
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    MINOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PATCH_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BUILD_DATE_FIELD_NUMBER: _ClassVar[int]
    product_name: str
    major_version: str
    minor_version: str
    patch_version: str
    build_number: str
    build_date: int
    def __init__(self, product_name: _Optional[str] = ..., major_version: _Optional[str] = ..., minor_version: _Optional[str] = ..., patch_version: _Optional[str] = ..., build_number: _Optional[str] = ..., build_date: _Optional[int] = ...) -> None: ...

class Version(_message.Message):
    __slots__ = ("major", "minor", "patch")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...) -> None: ...

class CreationOption(_message.Message):
    __slots__ = ("show_directory", "name", "seconds")
    SHOW_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    show_directory: str
    name: str
    seconds: int
    def __init__(self, show_directory: _Optional[str] = ..., name: _Optional[str] = ..., seconds: _Optional[int] = ...) -> None: ...

class MediaReferenceInfo(_message.Message):
    __slots__ = ("media_info", "thumbnail_info")
    class MediaInfo(_message.Message):
        __slots__ = ("url", "width", "height", "fps", "duration", "num_audio_channels", "codec", "artist", "title", "rotation", "content_type", "has_alpha_channel", "supports_hw_decode", "color_format")
        class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            CONTENT_TYPE_UNKNOWN: _ClassVar[MediaReferenceInfo.MediaInfo.ContentType]
            CONTENT_TYPE_AUDIO: _ClassVar[MediaReferenceInfo.MediaInfo.ContentType]
            CONTENT_TYPE_IMAGE: _ClassVar[MediaReferenceInfo.MediaInfo.ContentType]
            CONTENT_TYPE_VIDEO: _ClassVar[MediaReferenceInfo.MediaInfo.ContentType]
        CONTENT_TYPE_UNKNOWN: MediaReferenceInfo.MediaInfo.ContentType
        CONTENT_TYPE_AUDIO: MediaReferenceInfo.MediaInfo.ContentType
        CONTENT_TYPE_IMAGE: MediaReferenceInfo.MediaInfo.ContentType
        CONTENT_TYPE_VIDEO: MediaReferenceInfo.MediaInfo.ContentType
        class ColorFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SDR: _ClassVar[MediaReferenceInfo.MediaInfo.ColorFormat]
            HDR_REC2100_HLG: _ClassVar[MediaReferenceInfo.MediaInfo.ColorFormat]
            HDR_REC2100_PQ: _ClassVar[MediaReferenceInfo.MediaInfo.ColorFormat]
        SDR: MediaReferenceInfo.MediaInfo.ColorFormat
        HDR_REC2100_HLG: MediaReferenceInfo.MediaInfo.ColorFormat
        HDR_REC2100_PQ: MediaReferenceInfo.MediaInfo.ColorFormat
        URL_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        FPS_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        NUM_AUDIO_CHANNELS_FIELD_NUMBER: _ClassVar[int]
        CODEC_FIELD_NUMBER: _ClassVar[int]
        ARTIST_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        HAS_ALPHA_CHANNEL_FIELD_NUMBER: _ClassVar[int]
        SUPPORTS_HW_DECODE_FIELD_NUMBER: _ClassVar[int]
        COLOR_FORMAT_FIELD_NUMBER: _ClassVar[int]
        url: str
        width: int
        height: int
        fps: float
        duration: float
        num_audio_channels: int
        codec: str
        artist: str
        title: str
        rotation: int
        content_type: MediaReferenceInfo.MediaInfo.ContentType
        has_alpha_channel: bool
        supports_hw_decode: bool
        color_format: MediaReferenceInfo.MediaInfo.ColorFormat
        def __init__(self, url: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., fps: _Optional[float] = ..., duration: _Optional[float] = ..., num_audio_channels: _Optional[int] = ..., codec: _Optional[str] = ..., artist: _Optional[str] = ..., title: _Optional[str] = ..., rotation: _Optional[int] = ..., content_type: _Optional[_Union[MediaReferenceInfo.MediaInfo.ContentType, str]] = ..., has_alpha_channel: _Optional[bool] = ..., supports_hw_decode: _Optional[bool] = ..., color_format: _Optional[_Union[MediaReferenceInfo.MediaInfo.ColorFormat, str]] = ...) -> None: ...
    class ThumbnailInfo(_message.Message):
        __slots__ = ("url",)
        URL_FIELD_NUMBER: _ClassVar[int]
        url: str
        def __init__(self, url: _Optional[str] = ...) -> None: ...
    MEDIA_INFO_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_INFO_FIELD_NUMBER: _ClassVar[int]
    media_info: MediaReferenceInfo.MediaInfo
    thumbnail_info: MediaReferenceInfo.ThumbnailInfo
    def __init__(self, media_info: _Optional[_Union[MediaReferenceInfo.MediaInfo, _Mapping]] = ..., thumbnail_info: _Optional[_Union[MediaReferenceInfo.ThumbnailInfo, _Mapping]] = ...) -> None: ...

class RequestError(_message.Message):
    __slots__ = ("code", "description")
    class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[RequestError.ErrorCode]
        CANT_CREATE_MEDIA_FOLDER: _ClassVar[RequestError.ErrorCode]
        CANT_CREATE_META_FOLDER: _ClassVar[RequestError.ErrorCode]
        CANT_CREATE_THUMBNAILS_FOLDER: _ClassVar[RequestError.ErrorCode]
        CANT_DELETE_ACTIVE_WORKSPACE: _ClassVar[RequestError.ErrorCode]
        SERVICE_INTERNAL_ERROR: _ClassVar[RequestError.ErrorCode]
        SERVICE_HANDSHAKE_ERROR: _ClassVar[RequestError.ErrorCode]
        SERVICE_VERSION_MISMATCH: _ClassVar[RequestError.ErrorCode]
        SERVICE_CANT_SEND_REQUEST: _ClassVar[RequestError.ErrorCode]
        SERVICE_MISSING_RESPONSE: _ClassVar[RequestError.ErrorCode]
        BAD_REQUEST: _ClassVar[RequestError.ErrorCode]
        INVALID_UUID: _ClassVar[RequestError.ErrorCode]
        INVALID_REQUEST: _ClassVar[RequestError.ErrorCode]
        NOT_FOUND: _ClassVar[RequestError.ErrorCode]
        CONFLICT: _ClassVar[RequestError.ErrorCode]
        INTERNAL_ERROR: _ClassVar[RequestError.ErrorCode]
        NOT_IMPLEMENTED: _ClassVar[RequestError.ErrorCode]
        GENERATOR_ERROR: _ClassVar[RequestError.ErrorCode]
    UNKNOWN: RequestError.ErrorCode
    CANT_CREATE_MEDIA_FOLDER: RequestError.ErrorCode
    CANT_CREATE_META_FOLDER: RequestError.ErrorCode
    CANT_CREATE_THUMBNAILS_FOLDER: RequestError.ErrorCode
    CANT_DELETE_ACTIVE_WORKSPACE: RequestError.ErrorCode
    SERVICE_INTERNAL_ERROR: RequestError.ErrorCode
    SERVICE_HANDSHAKE_ERROR: RequestError.ErrorCode
    SERVICE_VERSION_MISMATCH: RequestError.ErrorCode
    SERVICE_CANT_SEND_REQUEST: RequestError.ErrorCode
    SERVICE_MISSING_RESPONSE: RequestError.ErrorCode
    BAD_REQUEST: RequestError.ErrorCode
    INVALID_UUID: RequestError.ErrorCode
    INVALID_REQUEST: RequestError.ErrorCode
    NOT_FOUND: RequestError.ErrorCode
    CONFLICT: RequestError.ErrorCode
    INTERNAL_ERROR: RequestError.ErrorCode
    NOT_IMPLEMENTED: RequestError.ErrorCode
    GENERATOR_ERROR: RequestError.ErrorCode
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    code: RequestError.ErrorCode
    description: str
    def __init__(self, code: _Optional[_Union[RequestError.ErrorCode, str]] = ..., description: _Optional[str] = ...) -> None: ...

class MediaReference(_message.Message):
    __slots__ = ("uuid", "success", "error", "progress", "deleted")
    class Progress(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Deleted(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Error(_message.Message):
        __slots__ = ("code", "description")
        class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            INTERNAL_ERROR: _ClassVar[MediaReference.Error.ErrorCode]
            SNAPSHOT_FAILED_ERROR: _ClassVar[MediaReference.Error.ErrorCode]
        INTERNAL_ERROR: MediaReference.Error.ErrorCode
        SNAPSHOT_FAILED_ERROR: MediaReference.Error.ErrorCode
        CODE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        code: MediaReference.Error.ErrorCode
        description: str
        def __init__(self, code: _Optional[_Union[MediaReference.Error.ErrorCode, str]] = ..., description: _Optional[str] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    success: MediaReferenceInfo
    error: MediaReference.Error
    progress: MediaReference.Progress
    deleted: MediaReference.Deleted
    def __init__(self, uuid: _Optional[str] = ..., success: _Optional[_Union[MediaReferenceInfo, _Mapping]] = ..., error: _Optional[_Union[MediaReference.Error, _Mapping]] = ..., progress: _Optional[_Union[MediaReference.Progress, _Mapping]] = ..., deleted: _Optional[_Union[MediaReference.Deleted, _Mapping]] = ...) -> None: ...

class GenerationStatus(_message.Message):
    __slots__ = ("idle", "processing", "paused")
    class Idle(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Processing(_message.Message):
        __slots__ = ("count", "total")
        COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        count: int
        total: int
        def __init__(self, count: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...
    class Paused(_message.Message):
        __slots__ = ("until_time_utc",)
        UNTIL_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
        until_time_utc: int
        def __init__(self, until_time_utc: _Optional[int] = ...) -> None: ...
    IDLE_FIELD_NUMBER: _ClassVar[int]
    PROCESSING_FIELD_NUMBER: _ClassVar[int]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    idle: GenerationStatus.Idle
    processing: GenerationStatus.Processing
    paused: GenerationStatus.Paused
    def __init__(self, idle: _Optional[_Union[GenerationStatus.Idle, _Mapping]] = ..., processing: _Optional[_Union[GenerationStatus.Processing, _Mapping]] = ..., paused: _Optional[_Union[GenerationStatus.Paused, _Mapping]] = ...) -> None: ...

class ChangeShowDirectory(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class UpdateWorkspaces(_message.Message):
    __slots__ = ("workspaces",)
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    workspaces: _containers.RepeatedCompositeFieldContainer[Workspace]
    def __init__(self, workspaces: _Optional[_Iterable[_Union[Workspace, _Mapping]]] = ...) -> None: ...

class PauseGeneration(_message.Message):
    __slots__ = ("until_time_utc",)
    UNTIL_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    until_time_utc: int
    def __init__(self, until_time_utc: _Optional[int] = ...) -> None: ...

class ResumeGeneration(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AddMediaReference(_message.Message):
    __slots__ = ("uuid", "url", "priority", "transformation")
    UUID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    url: str
    priority: Priority
    transformation: Transformation
    def __init__(self, uuid: _Optional[str] = ..., url: _Optional[str] = ..., priority: _Optional[_Union[Priority, str]] = ..., transformation: _Optional[_Union[Transformation, _Mapping]] = ...) -> None: ...

class DuplicateMediaReference(_message.Message):
    __slots__ = ("source_uuid", "dest_uuid", "priority")
    SOURCE_UUID_FIELD_NUMBER: _ClassVar[int]
    DEST_UUID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    source_uuid: str
    dest_uuid: str
    priority: Priority
    def __init__(self, source_uuid: _Optional[str] = ..., dest_uuid: _Optional[str] = ..., priority: _Optional[_Union[Priority, str]] = ...) -> None: ...

class Transformation(_message.Message):
    __slots__ = ("effects", "position", "rotation", "width", "height", "insets_top", "insets_left", "insets_right", "insets_bottom", "flip_horizontally", "flip_vertically", "alpha_type", "use_default_native_rotation")
    EFFECTS_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INSETS_TOP_FIELD_NUMBER: _ClassVar[int]
    INSETS_LEFT_FIELD_NUMBER: _ClassVar[int]
    INSETS_RIGHT_FIELD_NUMBER: _ClassVar[int]
    INSETS_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    FLIP_HORIZONTALLY_FIELD_NUMBER: _ClassVar[int]
    FLIP_VERTICALLY_FIELD_NUMBER: _ClassVar[int]
    ALPHA_TYPE_FIELD_NUMBER: _ClassVar[int]
    USE_DEFAULT_NATIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    effects: _containers.RepeatedCompositeFieldContainer[_effects_pb2.Effect]
    position: float
    rotation: int
    width: int
    height: int
    insets_top: float
    insets_left: float
    insets_right: float
    insets_bottom: float
    flip_horizontally: bool
    flip_vertically: bool
    alpha_type: _alphaType_pb2.AlphaType
    use_default_native_rotation: bool
    def __init__(self, effects: _Optional[_Iterable[_Union[_effects_pb2.Effect, _Mapping]]] = ..., position: _Optional[float] = ..., rotation: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., insets_top: _Optional[float] = ..., insets_left: _Optional[float] = ..., insets_right: _Optional[float] = ..., insets_bottom: _Optional[float] = ..., flip_horizontally: _Optional[bool] = ..., flip_vertically: _Optional[bool] = ..., alpha_type: _Optional[_Union[_alphaType_pb2.AlphaType, str]] = ..., use_default_native_rotation: _Optional[bool] = ...) -> None: ...

class ApplyTransformation(_message.Message):
    __slots__ = ("uuid", "transformation", "priority")
    UUID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    transformation: Transformation
    priority: Priority
    def __init__(self, uuid: _Optional[str] = ..., transformation: _Optional[_Union[Transformation, _Mapping]] = ..., priority: _Optional[_Union[Priority, str]] = ...) -> None: ...

class RemoveMediaReferences(_message.Message):
    __slots__ = ("uuid", "purge_asset")
    UUID_FIELD_NUMBER: _ClassVar[int]
    PURGE_ASSET_FIELD_NUMBER: _ClassVar[int]
    uuid: _containers.RepeatedScalarFieldContainer[str]
    purge_asset: bool
    def __init__(self, uuid: _Optional[_Iterable[str]] = ..., purge_asset: _Optional[bool] = ...) -> None: ...

class TriggerMediaReference(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid: _Optional[_Iterable[str]] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class AddMediaReferenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DuplicateMediaReferenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ApplyTransformationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveMediaReferenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TriggerMediaReferenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateWorkspacesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PauseGenerationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeGenerationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdatePrefsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Pong(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
