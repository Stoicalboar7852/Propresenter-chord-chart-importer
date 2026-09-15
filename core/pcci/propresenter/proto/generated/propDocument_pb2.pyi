import applicationInfo_pb2 as _applicationInfo_pb2
import cue_pb2 as _cue_pb2
import customOptions_pb2 as _customOptions_pb2
import effects_pb2 as _effects_pb2
import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PropDocument(_message.Message):
    __slots__ = ("application_info", "cues", "transition", "prop_collections")
    class PropCollection(_message.Message):
        __slots__ = ("uuid", "name", "items", "single_prop_enabled", "cues")
        class Item(_message.Message):
            __slots__ = ("prop_cue_uuid",)
            PROP_CUE_UUID_FIELD_NUMBER: _ClassVar[int]
            prop_cue_uuid: _uuid_pb2.UUID
            def __init__(self, prop_cue_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ...) -> None: ...
        UUID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        SINGLE_PROP_ENABLED_FIELD_NUMBER: _ClassVar[int]
        CUES_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        name: str
        items: _containers.RepeatedCompositeFieldContainer[PropDocument.PropCollection.Item]
        single_prop_enabled: bool
        cues: _containers.RepeatedCompositeFieldContainer[_cue_pb2.Cue]
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., name: _Optional[str] = ..., items: _Optional[_Iterable[_Union[PropDocument.PropCollection.Item, _Mapping]]] = ..., single_prop_enabled: _Optional[bool] = ..., cues: _Optional[_Iterable[_Union[_cue_pb2.Cue, _Mapping]]] = ...) -> None: ...
    APPLICATION_INFO_FIELD_NUMBER: _ClassVar[int]
    CUES_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    PROP_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    application_info: _applicationInfo_pb2.ApplicationInfo
    cues: _containers.RepeatedCompositeFieldContainer[_cue_pb2.Cue]
    transition: _effects_pb2.Transition
    prop_collections: _containers.RepeatedCompositeFieldContainer[PropDocument.PropCollection]
    def __init__(self, application_info: _Optional[_Union[_applicationInfo_pb2.ApplicationInfo, _Mapping]] = ..., cues: _Optional[_Iterable[_Union[_cue_pb2.Cue, _Mapping]]] = ..., transition: _Optional[_Union[_effects_pb2.Transition, _Mapping]] = ..., prop_collections: _Optional[_Iterable[_Union[PropDocument.PropCollection, _Mapping]]] = ...) -> None: ...
