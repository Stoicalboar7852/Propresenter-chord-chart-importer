from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_PlaylistPresentationItem(_message.Message):
    __slots__ = ("presentation_uuid", "arrangement_name", "arrangement_uuid")
    PRESENTATION_UUID_FIELD_NUMBER: _ClassVar[int]
    ARRANGEMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    ARRANGEMENT_UUID_FIELD_NUMBER: _ClassVar[int]
    presentation_uuid: str
    arrangement_name: str
    arrangement_uuid: str
    def __init__(self, presentation_uuid: _Optional[str] = ..., arrangement_name: _Optional[str] = ..., arrangement_uuid: _Optional[str] = ...) -> None: ...
