import url_pb2 as _url_pb2
import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AdvertisementGroup(_message.Message):
    __slots__ = ("uuid", "name", "url", "start_index", "duration")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    uuid: _uuid_pb2.UUID
    name: str
    url: _url_pb2.URL
    start_index: int
    duration: float
    def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., name: _Optional[str] = ..., url: _Optional[_Union[_url_pb2.URL, _Mapping]] = ..., start_index: _Optional[int] = ..., duration: _Optional[float] = ...) -> None: ...
