from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateMarker(_message.Message):
    __slots__ = ("location",)
    class Location(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INSPECTOR: _ClassVar[CreateMarker.Location]
        SIDEBAR: _ClassVar[CreateMarker.Location]
        UNKNOWN: _ClassVar[CreateMarker.Location]
    INSPECTOR: CreateMarker.Location
    SIDEBAR: CreateMarker.Location
    UNKNOWN: CreateMarker.Location
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: CreateMarker.Location
    def __init__(self, location: _Optional[_Union[CreateMarker.Location, str]] = ...) -> None: ...
