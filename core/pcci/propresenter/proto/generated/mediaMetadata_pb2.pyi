import effects_pb2 as _effects_pb2
import graphicsData_pb2 as _graphicsData_pb2
import alphaType_pb2 as _alphaType_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MediaMetadataRequestInfo(_message.Message):
    __slots__ = ("file_path", "time", "width", "height", "effects", "crop_insets", "native_rotation", "flipped_horizontally", "flipped_vertically", "alpha_type", "buffer_format")
    class BufferFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BUFFER_FORMAT_RAW: _ClassVar[MediaMetadataRequestInfo.BufferFormat]
        BUFFER_FORMAT_PNG: _ClassVar[MediaMetadataRequestInfo.BufferFormat]
        BUFFER_FORMAT_NONE: _ClassVar[MediaMetadataRequestInfo.BufferFormat]
    BUFFER_FORMAT_RAW: MediaMetadataRequestInfo.BufferFormat
    BUFFER_FORMAT_PNG: MediaMetadataRequestInfo.BufferFormat
    BUFFER_FORMAT_NONE: MediaMetadataRequestInfo.BufferFormat
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    EFFECTS_FIELD_NUMBER: _ClassVar[int]
    CROP_INSETS_FIELD_NUMBER: _ClassVar[int]
    NATIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    FLIPPED_HORIZONTALLY_FIELD_NUMBER: _ClassVar[int]
    FLIPPED_VERTICALLY_FIELD_NUMBER: _ClassVar[int]
    ALPHA_TYPE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_FORMAT_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    time: float
    width: int
    height: int
    effects: _containers.RepeatedCompositeFieldContainer[_effects_pb2.Effect]
    crop_insets: _graphicsData_pb2.Graphics.EdgeInsets
    native_rotation: _graphicsData_pb2.Media.DrawingProperties.NativeRotationType
    flipped_horizontally: bool
    flipped_vertically: bool
    alpha_type: _alphaType_pb2.AlphaType
    buffer_format: MediaMetadataRequestInfo.BufferFormat
    def __init__(self, file_path: _Optional[str] = ..., time: _Optional[float] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., effects: _Optional[_Iterable[_Union[_effects_pb2.Effect, _Mapping]]] = ..., crop_insets: _Optional[_Union[_graphicsData_pb2.Graphics.EdgeInsets, _Mapping]] = ..., native_rotation: _Optional[_Union[_graphicsData_pb2.Media.DrawingProperties.NativeRotationType, str]] = ..., flipped_horizontally: _Optional[bool] = ..., flipped_vertically: _Optional[bool] = ..., alpha_type: _Optional[_Union[_alphaType_pb2.AlphaType, str]] = ..., buffer_format: _Optional[_Union[MediaMetadataRequestInfo.BufferFormat, str]] = ...) -> None: ...

class MediaMetadataRequestResponse(_message.Message):
    __slots__ = ("metadata", "generated_bitmap_info")
    class Metadata(_message.Message):
        __slots__ = ("width", "height", "fps", "duration", "number_audio_channels", "codec", "artist", "title", "rotation", "content_type", "has_alpha_channel")
        class ContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            CONTENT_TYPE_UNKNOWN: _ClassVar[MediaMetadataRequestResponse.Metadata.ContentType]
            CONTENT_TYPE_AUDIO: _ClassVar[MediaMetadataRequestResponse.Metadata.ContentType]
            CONTENT_TYPE_IMAGE: _ClassVar[MediaMetadataRequestResponse.Metadata.ContentType]
            CONTENT_TYPE_VIDEO: _ClassVar[MediaMetadataRequestResponse.Metadata.ContentType]
        CONTENT_TYPE_UNKNOWN: MediaMetadataRequestResponse.Metadata.ContentType
        CONTENT_TYPE_AUDIO: MediaMetadataRequestResponse.Metadata.ContentType
        CONTENT_TYPE_IMAGE: MediaMetadataRequestResponse.Metadata.ContentType
        CONTENT_TYPE_VIDEO: MediaMetadataRequestResponse.Metadata.ContentType
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        FPS_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        NUMBER_AUDIO_CHANNELS_FIELD_NUMBER: _ClassVar[int]
        CODEC_FIELD_NUMBER: _ClassVar[int]
        ARTIST_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        HAS_ALPHA_CHANNEL_FIELD_NUMBER: _ClassVar[int]
        width: int
        height: int
        fps: float
        duration: float
        number_audio_channels: int
        codec: str
        artist: str
        title: str
        rotation: float
        content_type: MediaMetadataRequestResponse.Metadata.ContentType
        has_alpha_channel: bool
        def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., fps: _Optional[float] = ..., duration: _Optional[float] = ..., number_audio_channels: _Optional[int] = ..., codec: _Optional[str] = ..., artist: _Optional[str] = ..., title: _Optional[str] = ..., rotation: _Optional[float] = ..., content_type: _Optional[_Union[MediaMetadataRequestResponse.Metadata.ContentType, str]] = ..., has_alpha_channel: _Optional[bool] = ...) -> None: ...
    class BitmapInfo(_message.Message):
        __slots__ = ("width", "height", "size")
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        width: int
        height: int
        size: int
        def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BITMAP_INFO_FIELD_NUMBER: _ClassVar[int]
    metadata: MediaMetadataRequestResponse.Metadata
    generated_bitmap_info: MediaMetadataRequestResponse.BitmapInfo
    def __init__(self, metadata: _Optional[_Union[MediaMetadataRequestResponse.Metadata, _Mapping]] = ..., generated_bitmap_info: _Optional[_Union[MediaMetadataRequestResponse.BitmapInfo, _Mapping]] = ...) -> None: ...
