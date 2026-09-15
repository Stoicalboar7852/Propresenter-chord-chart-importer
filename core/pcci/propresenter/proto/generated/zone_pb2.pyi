import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Zone(_message.Message):
    __slots__ = ("uuid", "name", "hex_color")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HEX_COLOR_FIELD_NUMBER: _ClassVar[int]
    uuid: _uuid_pb2.UUID
    name: str
    hex_color: str
    def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., name: _Optional[str] = ..., hex_color: _Optional[str] = ...) -> None: ...
