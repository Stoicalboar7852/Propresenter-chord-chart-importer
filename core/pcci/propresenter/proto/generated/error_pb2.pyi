from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APPLICATION: _ClassVar[ServiceID]
    MEDIA: _ClassVar[ServiceID]
    FEATURE_FLAGS: _ClassVar[ServiceID]
    REGISTRATION: _ClassVar[ServiceID]
    DOCUMENT: _ClassVar[ServiceID]
    WORKSPACE: _ClassVar[ServiceID]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNTIME: _ClassVar[ErrorCode]
    CALL: _ClassVar[ErrorCode]
    PARAMS: _ClassVar[ErrorCode]
    DATA: _ClassVar[ErrorCode]
    PANIC: _ClassVar[ErrorCode]
    JOIN: _ClassVar[ErrorCode]
    HID: _ClassVar[ErrorCode]
    REMOTE: _ClassVar[ErrorCode]
    DEPENDENCY: _ClassVar[ErrorCode]
    MEDIA_VERSION: _ClassVar[ErrorCode]
APPLICATION: ServiceID
MEDIA: ServiceID
FEATURE_FLAGS: ServiceID
REGISTRATION: ServiceID
DOCUMENT: ServiceID
WORKSPACE: ServiceID
RUNTIME: ErrorCode
CALL: ErrorCode
PARAMS: ErrorCode
DATA: ErrorCode
PANIC: ErrorCode
JOIN: ErrorCode
HID: ErrorCode
REMOTE: ErrorCode
DEPENDENCY: ErrorCode
MEDIA_VERSION: ErrorCode

class Error(_message.Message):
    __slots__ = ("service", "code", "description")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    service: ServiceID
    code: int
    description: str
    def __init__(self, service: _Optional[_Union[ServiceID, str]] = ..., code: _Optional[int] = ..., description: _Optional[str] = ...) -> None: ...

class ResultEnvelope(_message.Message):
    __slots__ = ("ok", "error")
    class Ok(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ok: ResultEnvelope.Ok
    error: Error
    def __init__(self, ok: _Optional[_Union[ResultEnvelope.Ok, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
