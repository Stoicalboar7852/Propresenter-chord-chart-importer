from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Presentation(_message.Message):
    __slots__ = ("changeType", "uuid")
    class ChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EDIT: _ClassVar[Presentation.ChangeType]
        UNDO: _ClassVar[Presentation.ChangeType]
        REDO: _ClassVar[Presentation.ChangeType]
    EDIT: Presentation.ChangeType
    UNDO: Presentation.ChangeType
    REDO: Presentation.ChangeType
    CHANGETYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    changeType: Presentation.ChangeType
    uuid: str
    def __init__(self, changeType: _Optional[_Union[Presentation.ChangeType, str]] = ..., uuid: _Optional[str] = ...) -> None: ...
