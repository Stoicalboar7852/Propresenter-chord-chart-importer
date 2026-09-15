from workspace.entities import local_pb2 as _local_pb2
from workspace.entities import remote_pb2 as _remote_pb2
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

class OpenLocal(_message.Message):
    __slots__ = ("workspace",)
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: OpenLocal.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[OpenLocal.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: _local_pb2.Workspace
    def __init__(self, workspace: _Optional[_Union[_local_pb2.Workspace, _Mapping]] = ...) -> None: ...

class OpenRemote(_message.Message):
    __slots__ = ("uuid", "path")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ("workspace",)
            WORKSPACE_FIELD_NUMBER: _ClassVar[int]
            workspace: _remote_pb2.Workspace
            def __init__(self, workspace: _Optional[_Union[_remote_pb2.Workspace, _Mapping]] = ...) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: OpenRemote.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[OpenRemote.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    path: str
    def __init__(self, uuid: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class Publish(_message.Message):
    __slots__ = ()
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ("uuid",)
            UUID_FIELD_NUMBER: _ClassVar[int]
            uuid: str
            def __init__(self, uuid: _Optional[str] = ...) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Publish.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Publish.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ConvertToLocal(_message.Message):
    __slots__ = ()
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: ConvertToLocal.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[ConvertToLocal.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    def __init__(self) -> None: ...

class Rename(_message.Message):
    __slots__ = ("name", "uuid")
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: Rename.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[Rename.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    name: str
    uuid: str
    def __init__(self, name: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class PauseSync(_message.Message):
    __slots__ = ("until_time_utc",)
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: PauseSync.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[PauseSync.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    UNTIL_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    until_time_utc: int
    def __init__(self, until_time_utc: _Optional[int] = ...) -> None: ...

class ResumeSync(_message.Message):
    __slots__ = ()
    class Result(_message.Message):
        __slots__ = ("ok", "error")
        class Ok(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        OK_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ok: ResumeSync.Result.Ok
        error: Error
        def __init__(self, ok: _Optional[_Union[ResumeSync.Result.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    def __init__(self) -> None: ...
