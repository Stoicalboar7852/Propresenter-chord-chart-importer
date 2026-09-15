from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_TimelineOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    play: _ClassVar[API_v1_TimelineOperation]
    pause: _ClassVar[API_v1_TimelineOperation]
    rewind: _ClassVar[API_v1_TimelineOperation]
play: API_v1_TimelineOperation
pause: API_v1_TimelineOperation
rewind: API_v1_TimelineOperation
