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

class FeatureFlags(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, flags: _Optional[_Iterable[str]] = ...) -> None: ...

class ProContentToken(_message.Message):
    __slots__ = ("access", "refresh")
    ACCESS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_FIELD_NUMBER: _ClassVar[int]
    access: str
    refresh: str
    def __init__(self, access: _Optional[str] = ..., refresh: _Optional[str] = ...) -> None: ...

class Version(_message.Message):
    __slots__ = ("major", "minor", "patch")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...) -> None: ...

class Preferences(_message.Message):
    __slots__ = ("manage_media", "share_analytics")
    MANAGE_MEDIA_FIELD_NUMBER: _ClassVar[int]
    SHARE_ANALYTICS_FIELD_NUMBER: _ClassVar[int]
    manage_media: bool
    share_analytics: bool
    def __init__(self, manage_media: _Optional[bool] = ..., share_analytics: _Optional[bool] = ...) -> None: ...

class CreationOption(_message.Message):
    __slots__ = ("show_directory", "preferences", "name", "seconds", "workspace_id", "peer_id")
    SHOW_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    PEER_ID_FIELD_NUMBER: _ClassVar[int]
    show_directory: str
    preferences: Preferences
    name: str
    seconds: int
    workspace_id: str
    peer_id: int
    def __init__(self, show_directory: _Optional[str] = ..., preferences: _Optional[_Union[Preferences, _Mapping]] = ..., name: _Optional[str] = ..., seconds: _Optional[int] = ..., workspace_id: _Optional[str] = ..., peer_id: _Optional[int] = ...) -> None: ...

class MediaReferenceInfo(_message.Message):
    __slots__ = ("media_info", "thumbnail_info")
    class Availability(_message.Message):
        __slots__ = ("ready", "missing", "downloading")
        class Ready(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class Missing(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class Downloading(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        READY_FIELD_NUMBER: _ClassVar[int]
        MISSING_FIELD_NUMBER: _ClassVar[int]
        DOWNLOADING_FIELD_NUMBER: _ClassVar[int]
        ready: MediaReferenceInfo.Availability.Ready
        missing: MediaReferenceInfo.Availability.Missing
        downloading: MediaReferenceInfo.Availability.Downloading
        def __init__(self, ready: _Optional[_Union[MediaReferenceInfo.Availability.Ready, _Mapping]] = ..., missing: _Optional[_Union[MediaReferenceInfo.Availability.Missing, _Mapping]] = ..., downloading: _Optional[_Union[MediaReferenceInfo.Availability.Downloading, _Mapping]] = ...) -> None: ...
    class MediaInfo(_message.Message):
        __slots__ = ("url", "width", "height", "fps", "duration", "num_audio_channels", "codec", "artist", "title", "rotation", "content_type", "has_alpha_channel", "supports_hw_decode", "color_format", "availability")
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
        AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
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
        availability: MediaReferenceInfo.Availability
        def __init__(self, url: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., fps: _Optional[float] = ..., duration: _Optional[float] = ..., num_audio_channels: _Optional[int] = ..., codec: _Optional[str] = ..., artist: _Optional[str] = ..., title: _Optional[str] = ..., rotation: _Optional[int] = ..., content_type: _Optional[_Union[MediaReferenceInfo.MediaInfo.ContentType, str]] = ..., has_alpha_channel: _Optional[bool] = ..., supports_hw_decode: _Optional[bool] = ..., color_format: _Optional[_Union[MediaReferenceInfo.MediaInfo.ColorFormat, str]] = ..., availability: _Optional[_Union[MediaReferenceInfo.Availability, _Mapping]] = ...) -> None: ...
    class ThumbnailInfo(_message.Message):
        __slots__ = ("url", "availability")
        URL_FIELD_NUMBER: _ClassVar[int]
        AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
        url: str
        availability: MediaReferenceInfo.Availability
        def __init__(self, url: _Optional[str] = ..., availability: _Optional[_Union[MediaReferenceInfo.Availability, _Mapping]] = ...) -> None: ...
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

class ReferenceIdentifier(_message.Message):
    __slots__ = ("uuid", "container_id")
    UUID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    container_id: str
    def __init__(self, uuid: _Optional[str] = ..., container_id: _Optional[str] = ...) -> None: ...

class MediaReference(_message.Message):
    __slots__ = ("id", "success", "error", "progress", "deleted", "downloading")
    class Progress(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Deleted(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ProContentDownloading(_message.Message):
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
    ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADING_FIELD_NUMBER: _ClassVar[int]
    id: ReferenceIdentifier
    success: MediaReferenceInfo
    error: MediaReference.Error
    progress: MediaReference.Progress
    deleted: MediaReference.Deleted
    downloading: MediaReference.ProContentDownloading
    def __init__(self, id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., success: _Optional[_Union[MediaReferenceInfo, _Mapping]] = ..., error: _Optional[_Union[MediaReference.Error, _Mapping]] = ..., progress: _Optional[_Union[MediaReference.Progress, _Mapping]] = ..., deleted: _Optional[_Union[MediaReference.Deleted, _Mapping]] = ..., downloading: _Optional[_Union[MediaReference.ProContentDownloading, _Mapping]] = ...) -> None: ...

class AssetImported(_message.Message):
    __slots__ = ("id", "success", "error")
    class Error(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IMPORT_RESULT_UNKNOWN_ERROR: _ClassVar[AssetImported.Error]
        IMPORT_RESULT_INVALID_IMPORT_PATH: _ClassVar[AssetImported.Error]
        IMPORT_RESULT_READ_PERMISSION_DENIED: _ClassVar[AssetImported.Error]
        IMPORT_RESULT_WRITE_PERMISSION_DENIED: _ClassVar[AssetImported.Error]
        IMPORT_RESULT_FULL_STORAGE: _ClassVar[AssetImported.Error]
        IMPORT_RESULT_READ_ONLY_FILESYSTEM: _ClassVar[AssetImported.Error]
    IMPORT_RESULT_UNKNOWN_ERROR: AssetImported.Error
    IMPORT_RESULT_INVALID_IMPORT_PATH: AssetImported.Error
    IMPORT_RESULT_READ_PERMISSION_DENIED: AssetImported.Error
    IMPORT_RESULT_WRITE_PERMISSION_DENIED: AssetImported.Error
    IMPORT_RESULT_FULL_STORAGE: AssetImported.Error
    IMPORT_RESULT_READ_ONLY_FILESYSTEM: AssetImported.Error
    class Success(_message.Message):
        __slots__ = ("url",)
        URL_FIELD_NUMBER: _ClassVar[int]
        url: str
        def __init__(self, url: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    id: ReferenceIdentifier
    success: AssetImported.Success
    error: AssetImported.Error
    def __init__(self, id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., success: _Optional[_Union[AssetImported.Success, _Mapping]] = ..., error: _Optional[_Union[AssetImported.Error, str]] = ...) -> None: ...

class ChangeShowDirectory(_message.Message):
    __slots__ = ("path", "workspace_id")
    PATH_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    workspace_id: str
    def __init__(self, path: _Optional[str] = ..., workspace_id: _Optional[str] = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("path", "id")
    PATH_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    path: str
    id: str
    def __init__(self, path: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class UpdateWorkspaces(_message.Message):
    __slots__ = ("workspaces",)
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    workspaces: _containers.RepeatedCompositeFieldContainer[Workspace]
    def __init__(self, workspaces: _Optional[_Iterable[_Union[Workspace, _Mapping]]] = ...) -> None: ...

class PauseSync(_message.Message):
    __slots__ = ("until_time_utc",)
    UNTIL_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    until_time_utc: int
    def __init__(self, until_time_utc: _Optional[int] = ...) -> None: ...

class ResumeSync(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AddMediaReference(_message.Message):
    __slots__ = ("id", "url", "priority", "transformation", "manage_media", "user_initiated")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    MANAGE_MEDIA_FIELD_NUMBER: _ClassVar[int]
    USER_INITIATED_FIELD_NUMBER: _ClassVar[int]
    id: ReferenceIdentifier
    url: str
    priority: Priority
    transformation: Transformation
    manage_media: bool
    user_initiated: bool
    def __init__(self, id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., url: _Optional[str] = ..., priority: _Optional[_Union[Priority, str]] = ..., transformation: _Optional[_Union[Transformation, _Mapping]] = ..., manage_media: _Optional[bool] = ..., user_initiated: _Optional[bool] = ...) -> None: ...

class ProContentDownloadDetails(_message.Message):
    __slots__ = ("asset_identifier", "display_name", "relative_path", "download_url", "thumbnail_url", "asset_type")
    class AssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ASSET_TYPE_UNSPECIFIED: _ClassVar[ProContentDownloadDetails.AssetType]
        ASSET_TYPE_LOOP: _ClassVar[ProContentDownloadDetails.AssetType]
        ASSET_TYPE_COUNTDOWN: _ClassVar[ProContentDownloadDetails.AssetType]
        ASSET_TYPE_IMAGE: _ClassVar[ProContentDownloadDetails.AssetType]
        ASSET_TYPE_MOTION_TITLE: _ClassVar[ProContentDownloadDetails.AssetType]
        ASSET_TYPE_PACK: _ClassVar[ProContentDownloadDetails.AssetType]
        ASSET_TYPE_THEME: _ClassVar[ProContentDownloadDetails.AssetType]
    ASSET_TYPE_UNSPECIFIED: ProContentDownloadDetails.AssetType
    ASSET_TYPE_LOOP: ProContentDownloadDetails.AssetType
    ASSET_TYPE_COUNTDOWN: ProContentDownloadDetails.AssetType
    ASSET_TYPE_IMAGE: ProContentDownloadDetails.AssetType
    ASSET_TYPE_MOTION_TITLE: ProContentDownloadDetails.AssetType
    ASSET_TYPE_PACK: ProContentDownloadDetails.AssetType
    ASSET_TYPE_THEME: ProContentDownloadDetails.AssetType
    ASSET_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_PATH_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_URL_FIELD_NUMBER: _ClassVar[int]
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    asset_identifier: str
    display_name: str
    relative_path: str
    download_url: str
    thumbnail_url: str
    asset_type: ProContentDownloadDetails.AssetType
    def __init__(self, asset_identifier: _Optional[str] = ..., display_name: _Optional[str] = ..., relative_path: _Optional[str] = ..., download_url: _Optional[str] = ..., thumbnail_url: _Optional[str] = ..., asset_type: _Optional[_Union[ProContentDownloadDetails.AssetType, str]] = ...) -> None: ...

class AddProContentReference(_message.Message):
    __slots__ = ("id", "download_details", "transformation", "priority", "user_initiated")
    ID_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_DETAILS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    USER_INITIATED_FIELD_NUMBER: _ClassVar[int]
    id: ReferenceIdentifier
    download_details: ProContentDownloadDetails
    transformation: Transformation
    priority: Priority
    user_initiated: bool
    def __init__(self, id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., download_details: _Optional[_Union[ProContentDownloadDetails, _Mapping]] = ..., transformation: _Optional[_Union[Transformation, _Mapping]] = ..., priority: _Optional[_Union[Priority, str]] = ..., user_initiated: _Optional[bool] = ...) -> None: ...

class DuplicateMediaReference(_message.Message):
    __slots__ = ("src_id", "dest_id", "priority", "user_initiated")
    SRC_ID_FIELD_NUMBER: _ClassVar[int]
    DEST_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    USER_INITIATED_FIELD_NUMBER: _ClassVar[int]
    src_id: ReferenceIdentifier
    dest_id: ReferenceIdentifier
    priority: Priority
    user_initiated: bool
    def __init__(self, src_id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., dest_id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., priority: _Optional[_Union[Priority, str]] = ..., user_initiated: _Optional[bool] = ...) -> None: ...

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
    __slots__ = ("id", "transformation", "priority", "user_initiated")
    ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    USER_INITIATED_FIELD_NUMBER: _ClassVar[int]
    id: ReferenceIdentifier
    transformation: Transformation
    priority: Priority
    user_initiated: bool
    def __init__(self, id: _Optional[_Union[ReferenceIdentifier, _Mapping]] = ..., transformation: _Optional[_Union[Transformation, _Mapping]] = ..., priority: _Optional[_Union[Priority, str]] = ..., user_initiated: _Optional[bool] = ...) -> None: ...

class RemoveMediaReferences(_message.Message):
    __slots__ = ("id", "purge_asset", "delete_asset", "user_initiated")
    ID_FIELD_NUMBER: _ClassVar[int]
    PURGE_ASSET_FIELD_NUMBER: _ClassVar[int]
    DELETE_ASSET_FIELD_NUMBER: _ClassVar[int]
    USER_INITIATED_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedCompositeFieldContainer[ReferenceIdentifier]
    purge_asset: bool
    delete_asset: bool
    user_initiated: bool
    def __init__(self, id: _Optional[_Iterable[_Union[ReferenceIdentifier, _Mapping]]] = ..., purge_asset: _Optional[bool] = ..., delete_asset: _Optional[bool] = ..., user_initiated: _Optional[bool] = ...) -> None: ...

class TriggerMediaReference(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedCompositeFieldContainer[ReferenceIdentifier]
    def __init__(self, id: _Optional[_Iterable[_Union[ReferenceIdentifier, _Mapping]]] = ...) -> None: ...

class SmartPlaylist(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class UpdateSmartPlaylists(_message.Message):
    __slots__ = ("playlists",)
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    playlists: _containers.RepeatedCompositeFieldContainer[SmartPlaylist]
    def __init__(self, playlists: _Optional[_Iterable[_Union[SmartPlaylist, _Mapping]]] = ...) -> None: ...

class UpdatePrefs(_message.Message):
    __slots__ = ("preferences",)
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: Preferences
    def __init__(self, preferences: _Optional[_Union[Preferences, _Mapping]] = ...) -> None: ...

class MarkWorkspaceAsCloud(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class MarkWorkspaceAsLocal(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveContainer(_message.Message):
    __slots__ = ("container_id", "user_initiated")
    CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_INITIATED_FIELD_NUMBER: _ClassVar[int]
    container_id: _containers.RepeatedScalarFieldContainer[str]
    user_initiated: bool
    def __init__(self, container_id: _Optional[_Iterable[str]] = ..., user_initiated: _Optional[bool] = ...) -> None: ...

class ImportUnmanagedMedia(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

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

class PauseSyncResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResumeSyncResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateSmartPlaylistsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdatePrefsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MarkWorkspaceAsCloudResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MarkWorkspaceAsLocalResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AddProContentReferenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RemoveContainerResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ImportUnmanagedMediaResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Pong(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
