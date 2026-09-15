from document import entities_pb2 as _entities_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metadata(_message.Message):
    __slots__ = ("uuid", "pro_version", "name", "size", "created", "updated")
    UUID_FIELD_NUMBER: _ClassVar[int]
    PRO_VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    pro_version: str
    name: str
    size: int
    created: int
    updated: int
    def __init__(self, uuid: _Optional[str] = ..., pro_version: _Optional[str] = ..., name: _Optional[str] = ..., size: _Optional[int] = ..., created: _Optional[int] = ..., updated: _Optional[int] = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("metadata", "documents")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    documents: _entities_pb2.DocumentSet
    def __init__(self, metadata: _Optional[_Union[Metadata, _Mapping]] = ..., documents: _Optional[_Union[_entities_pb2.DocumentSet, _Mapping]] = ...) -> None: ...
