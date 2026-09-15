from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreationOption(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Flag(_message.Message):
    __slots__ = ("name", "enabled")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    name: str
    enabled: bool
    def __init__(self, name: _Optional[str] = ..., enabled: _Optional[bool] = ...) -> None: ...

class AllFlags(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: _containers.RepeatedCompositeFieldContainer[Flag]
    def __init__(self, flags: _Optional[_Iterable[_Union[Flag, _Mapping]]] = ...) -> None: ...

class Notification(_message.Message):
    __slots__ = ("all_flags", "unsubscribe_complete")
    class UnsubscribeComplete(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ALL_FLAGS_FIELD_NUMBER: _ClassVar[int]
    UNSUBSCRIBE_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    all_flags: AllFlags
    unsubscribe_complete: Notification.UnsubscribeComplete
    def __init__(self, all_flags: _Optional[_Union[AllFlags, _Mapping]] = ..., unsubscribe_complete: _Optional[_Union[Notification.UnsubscribeComplete, _Mapping]] = ...) -> None: ...
