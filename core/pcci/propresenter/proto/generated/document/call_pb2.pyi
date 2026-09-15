from document import entities_pb2 as _entities_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ("code", "description")
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Error.Code]
    UNKNOWN: Error.Code
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    code: Error.Code
    description: str
    def __init__(self, code: _Optional[_Union[Error.Code, str]] = ..., description: _Optional[str] = ...) -> None: ...

class Patch(_message.Message):
    __slots__ = ("uuid", "patch")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Patch.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Patch.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    patch: bytes
    def __init__(self, uuid: _Optional[str] = ..., patch: _Optional[bytes] = ...) -> None: ...

class Load(_message.Message):
    __slots__ = ("uuid", "blob")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Load.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Load.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    BLOB_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    blob: bytes
    def __init__(self, uuid: _Optional[str] = ..., blob: _Optional[bytes] = ...) -> None: ...

class Add(_message.Message):
    __slots__ = ("uuid", "kind", "path", "data")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Add.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Add.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    kind: _entities_pb2.Document.Kind
    path: str
    data: bytes
    def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[_entities_pb2.Document.Kind, str]] = ..., path: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class Remove(_message.Message):
    __slots__ = ("uuid", "kind")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Remove.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Remove.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    kind: _entities_pb2.Document.Kind
    def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[_entities_pb2.Document.Kind, str]] = ...) -> None: ...

class Relocate(_message.Message):
    __slots__ = ("uuid", "kind", "path")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Relocate.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Relocate.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    kind: _entities_pb2.Document.Kind
    path: str
    def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[_entities_pb2.Document.Kind, str]] = ..., path: _Optional[str] = ...) -> None: ...
