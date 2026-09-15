from document import entities_pb2 as _entities_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Notification(_message.Message):
    __slots__ = ("unsubscribe", "patch", "required", "available", "added", "moved", "removed")
    class UnsubscribeComplete(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Patch(_message.Message):
        __slots__ = ("uuid", "blob")
        UUID_FIELD_NUMBER: _ClassVar[int]
        BLOB_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        blob: bytes
        def __init__(self, uuid: _Optional[str] = ..., blob: _Optional[bytes] = ...) -> None: ...
    class Required(_message.Message):
        __slots__ = ("uuid",)
        UUID_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        def __init__(self, uuid: _Optional[str] = ...) -> None: ...
    class Available(_message.Message):
        __slots__ = ("uuid", "blob")
        UUID_FIELD_NUMBER: _ClassVar[int]
        BLOB_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        blob: bytes
        def __init__(self, uuid: _Optional[str] = ..., blob: _Optional[bytes] = ...) -> None: ...
    class Added(_message.Message):
        __slots__ = ("uuid", "kind", "path")
        UUID_FIELD_NUMBER: _ClassVar[int]
        KIND_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        kind: _entities_pb2.Document.Kind
        path: str
        def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[_entities_pb2.Document.Kind, str]] = ..., path: _Optional[str] = ...) -> None: ...
    class Moved(_message.Message):
        __slots__ = ("uuid", "kind", "path")
        UUID_FIELD_NUMBER: _ClassVar[int]
        KIND_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        kind: _entities_pb2.Document.Kind
        path: str
        def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[_entities_pb2.Document.Kind, str]] = ..., path: _Optional[str] = ...) -> None: ...
    class Removed(_message.Message):
        __slots__ = ("uuid", "kind", "path")
        UUID_FIELD_NUMBER: _ClassVar[int]
        KIND_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        kind: _entities_pb2.Document.Kind
        path: str
        def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[_entities_pb2.Document.Kind, str]] = ..., path: _Optional[str] = ...) -> None: ...
    UNSUBSCRIBE_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    ADDED_FIELD_NUMBER: _ClassVar[int]
    MOVED_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    unsubscribe: Notification.UnsubscribeComplete
    patch: Notification.Patch
    required: Notification.Required
    available: Notification.Available
    added: Notification.Added
    moved: Notification.Moved
    removed: Notification.Removed
    def __init__(self, unsubscribe: _Optional[_Union[Notification.UnsubscribeComplete, _Mapping]] = ..., patch: _Optional[_Union[Notification.Patch, _Mapping]] = ..., required: _Optional[_Union[Notification.Required, _Mapping]] = ..., available: _Optional[_Union[Notification.Available, _Mapping]] = ..., added: _Optional[_Union[Notification.Added, _Mapping]] = ..., moved: _Optional[_Union[Notification.Moved, _Mapping]] = ..., removed: _Optional[_Union[Notification.Removed, _Mapping]] = ...) -> None: ...
