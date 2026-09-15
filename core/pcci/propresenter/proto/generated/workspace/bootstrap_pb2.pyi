from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreationOption(_message.Message):
    __slots__ = ("min_pro_version",)
    MIN_PRO_VERSION_FIELD_NUMBER: _ClassVar[int]
    min_pro_version: str
    def __init__(self, min_pro_version: _Optional[str] = ...) -> None: ...
