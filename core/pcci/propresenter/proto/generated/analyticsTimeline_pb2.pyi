from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(_message.Message):
    __slots__ = ("action_type",)
    class ActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLAY: _ClassVar[Action.ActionType]
        STOP: _ClassVar[Action.ActionType]
        RESET: _ClassVar[Action.ActionType]
    PLAY: Action.ActionType
    STOP: Action.ActionType
    RESET: Action.ActionType
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    action_type: Action.ActionType
    def __init__(self, action_type: _Optional[_Union[Action.ActionType, str]] = ...) -> None: ...

class RecordCue(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CueTrigger(_message.Message):
    __slots__ = ("trigger_type", "timing_source")
    class TriggerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SLIDE: _ClassVar[CueTrigger.TriggerType]
        MEDIA: _ClassVar[CueTrigger.TriggerType]
        AUDIO: _ClassVar[CueTrigger.TriggerType]
        ACTION: _ClassVar[CueTrigger.TriggerType]
    SLIDE: CueTrigger.TriggerType
    MEDIA: CueTrigger.TriggerType
    AUDIO: CueTrigger.TriggerType
    ACTION: CueTrigger.TriggerType
    class TimingSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INTERNAL: _ClassVar[CueTrigger.TimingSource]
        SMPTE: _ClassVar[CueTrigger.TimingSource]
    INTERNAL: CueTrigger.TimingSource
    SMPTE: CueTrigger.TimingSource
    TRIGGER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMING_SOURCE_FIELD_NUMBER: _ClassVar[int]
    trigger_type: CueTrigger.TriggerType
    timing_source: CueTrigger.TimingSource
    def __init__(self, trigger_type: _Optional[_Union[CueTrigger.TriggerType, str]] = ..., timing_source: _Optional[_Union[CueTrigger.TimingSource, str]] = ...) -> None: ...
