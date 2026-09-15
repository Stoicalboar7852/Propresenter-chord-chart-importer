from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_LayerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    audio: _ClassVar[API_v1_LayerType]
    props: _ClassVar[API_v1_LayerType]
    messages: _ClassVar[API_v1_LayerType]
    announcements: _ClassVar[API_v1_LayerType]
    slide: _ClassVar[API_v1_LayerType]
    media: _ClassVar[API_v1_LayerType]
    video_input: _ClassVar[API_v1_LayerType]
audio: API_v1_LayerType
props: API_v1_LayerType
messages: API_v1_LayerType
announcements: API_v1_LayerType
slide: API_v1_LayerType
media: API_v1_LayerType
video_input: API_v1_LayerType
