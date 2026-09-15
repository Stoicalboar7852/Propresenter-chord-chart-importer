from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReportedError(_message.Message):
    __slots__ = ("description", "type", "file", "line", "severity")
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        HANDLED: _ClassVar[ReportedError.Severity]
        FATAL: _ClassVar[ReportedError.Severity]
    HANDLED: ReportedError.Severity
    FATAL: ReportedError.Severity
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    description: str
    type: str
    file: str
    line: int
    severity: ReportedError.Severity
    def __init__(self, description: _Optional[str] = ..., type: _Optional[str] = ..., file: _Optional[str] = ..., line: _Optional[int] = ..., severity: _Optional[_Union[ReportedError.Severity, str]] = ...) -> None: ...
