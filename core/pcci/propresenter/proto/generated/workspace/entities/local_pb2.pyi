from document import entities_pb2 as _entities_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metadata(_message.Message):
    __slots__ = ("pro_version", "name", "path", "uuid")
    PRO_VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    pro_version: str
    name: str
    path: str
    uuid: str
    def __init__(self, pro_version: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("metadata", "documents")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    documents: _entities_pb2.DocumentSet
    def __init__(self, metadata: _Optional[_Union[Metadata, _Mapping]] = ..., documents: _Optional[_Union[_entities_pb2.DocumentSet, _Mapping]] = ...) -> None: ...
