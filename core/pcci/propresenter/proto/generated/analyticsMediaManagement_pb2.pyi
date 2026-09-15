from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InstallationComplete(_message.Message):
    __slots__ = ("success", "failure")
    class Success(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Failure(_message.Message):
        __slots__ = ("error",)
        ERROR_FIELD_NUMBER: _ClassVar[int]
        error: str
        def __init__(self, error: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_FIELD_NUMBER: _ClassVar[int]
    success: InstallationComplete.Success
    failure: InstallationComplete.Failure
    def __init__(self, success: _Optional[_Union[InstallationComplete.Success, _Mapping]] = ..., failure: _Optional[_Union[InstallationComplete.Failure, _Mapping]] = ...) -> None: ...

class BootstrappingComplete(_message.Message):
    __slots__ = ("success", "failure")
    class Success(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Failure(_message.Message):
        __slots__ = ("error",)
        ERROR_FIELD_NUMBER: _ClassVar[int]
        error: str
        def __init__(self, error: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_FIELD_NUMBER: _ClassVar[int]
    success: BootstrappingComplete.Success
    failure: BootstrappingComplete.Failure
    def __init__(self, success: _Optional[_Union[BootstrappingComplete.Success, _Mapping]] = ..., failure: _Optional[_Union[BootstrappingComplete.Failure, _Mapping]] = ...) -> None: ...

class MessageFailure(_message.Message):
    __slots__ = ("error",)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: _Optional[str] = ...) -> None: ...

class UnexpectedlyNotRunning(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ConnectionChanged(_message.Message):
    __slots__ = ("state",)
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_CONNECTED: _ClassVar[ConnectionChanged.State]
        STATE_DISCONNECTED: _ClassVar[ConnectionChanged.State]
    STATE_CONNECTED: ConnectionChanged.State
    STATE_DISCONNECTED: ConnectionChanged.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: ConnectionChanged.State
    def __init__(self, state: _Optional[_Union[ConnectionChanged.State, str]] = ...) -> None: ...

class AddedMediaReference(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class NotResponding(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
