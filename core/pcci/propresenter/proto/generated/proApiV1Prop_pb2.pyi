import proApiV1Identifier_pb2 as _proApiV1Identifier_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_Transition(_message.Message):
    __slots__ = ("uuid", "name", "duration")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    name: str
    duration: float
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., duration: _Optional[float] = ...) -> None: ...

class API_v1_PropData(_message.Message):
    __slots__ = ("id", "is_active", "auto_clear_enabled", "auto_clear_duration", "transition")
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLEAR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLEAR_DURATION_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    id: _proApiV1Identifier_pb2.API_v1_Identifier
    is_active: bool
    auto_clear_enabled: bool
    auto_clear_duration: float
    transition: API_v1_Transition
    def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., is_active: _Optional[bool] = ..., auto_clear_enabled: _Optional[bool] = ..., auto_clear_duration: _Optional[float] = ..., transition: _Optional[_Union[API_v1_Transition, _Mapping]] = ...) -> None: ...

class API_v1_PropCollection(_message.Message):
    __slots__ = ("id", "props", "single_prop_enabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    SINGLE_PROP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: _proApiV1Identifier_pb2.API_v1_Identifier
    props: _containers.RepeatedCompositeFieldContainer[API_v1_PropData]
    single_prop_enabled: bool
    def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., props: _Optional[_Iterable[_Union[API_v1_PropData, _Mapping]]] = ..., single_prop_enabled: _Optional[bool] = ...) -> None: ...

class API_v1_Prop_Request(_message.Message):
    __slots__ = ("props", "get_prop", "put_prop", "delete_prop", "trigger_prop", "clear_prop", "get_thumbnail", "get_prop_collections", "get_prop_collection", "post_prop_collections", "put_prop_collection", "delete_prop_collection", "pause_prop", "resume_prop")
    class Props(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GetProp(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class PutProp(_message.Message):
        __slots__ = ("id", "name_change", "auto_clear_change")
        class AutoClearChange(_message.Message):
            __slots__ = ("auto_clear_enabled", "auto_clear_duration")
            AUTO_CLEAR_ENABLED_FIELD_NUMBER: _ClassVar[int]
            AUTO_CLEAR_DURATION_FIELD_NUMBER: _ClassVar[int]
            auto_clear_enabled: bool
            auto_clear_duration: float
            def __init__(self, auto_clear_enabled: _Optional[bool] = ..., auto_clear_duration: _Optional[float] = ...) -> None: ...
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_CHANGE_FIELD_NUMBER: _ClassVar[int]
        AUTO_CLEAR_CHANGE_FIELD_NUMBER: _ClassVar[int]
        id: str
        name_change: str
        auto_clear_change: API_v1_Prop_Request.PutProp.AutoClearChange
        def __init__(self, id: _Optional[str] = ..., name_change: _Optional[str] = ..., auto_clear_change: _Optional[_Union[API_v1_Prop_Request.PutProp.AutoClearChange, _Mapping]] = ...) -> None: ...
    class DeleteProp(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class TriggerProp(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class ClearProp(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class PauseProp(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class ResumeProp(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class GetThumbnail(_message.Message):
        __slots__ = ("id", "quality")
        ID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        id: str
        quality: int
        def __init__(self, id: _Optional[str] = ..., quality: _Optional[int] = ...) -> None: ...
    class GetPropCollections(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GetPropCollection(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class PostPropCollections(_message.Message):
        __slots__ = ("name",)
        NAME_FIELD_NUMBER: _ClassVar[int]
        name: str
        def __init__(self, name: _Optional[str] = ...) -> None: ...
    class PutPropCollection(_message.Message):
        __slots__ = ("id", "changes")
        ID_FIELD_NUMBER: _ClassVar[int]
        CHANGES_FIELD_NUMBER: _ClassVar[int]
        id: str
        changes: API_v1_PropCollection
        def __init__(self, id: _Optional[str] = ..., changes: _Optional[_Union[API_v1_PropCollection, _Mapping]] = ...) -> None: ...
    class DeletePropCollection(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    PROPS_FIELD_NUMBER: _ClassVar[int]
    GET_PROP_FIELD_NUMBER: _ClassVar[int]
    PUT_PROP_FIELD_NUMBER: _ClassVar[int]
    DELETE_PROP_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PROP_FIELD_NUMBER: _ClassVar[int]
    CLEAR_PROP_FIELD_NUMBER: _ClassVar[int]
    GET_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    GET_PROP_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    GET_PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    POST_PROP_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    PUT_PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DELETE_PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    PAUSE_PROP_FIELD_NUMBER: _ClassVar[int]
    RESUME_PROP_FIELD_NUMBER: _ClassVar[int]
    props: API_v1_Prop_Request.Props
    get_prop: API_v1_Prop_Request.GetProp
    put_prop: API_v1_Prop_Request.PutProp
    delete_prop: API_v1_Prop_Request.DeleteProp
    trigger_prop: API_v1_Prop_Request.TriggerProp
    clear_prop: API_v1_Prop_Request.ClearProp
    get_thumbnail: API_v1_Prop_Request.GetThumbnail
    get_prop_collections: API_v1_Prop_Request.GetPropCollections
    get_prop_collection: API_v1_Prop_Request.GetPropCollection
    post_prop_collections: API_v1_Prop_Request.PostPropCollections
    put_prop_collection: API_v1_Prop_Request.PutPropCollection
    delete_prop_collection: API_v1_Prop_Request.DeletePropCollection
    pause_prop: API_v1_Prop_Request.PauseProp
    resume_prop: API_v1_Prop_Request.ResumeProp
    def __init__(self, props: _Optional[_Union[API_v1_Prop_Request.Props, _Mapping]] = ..., get_prop: _Optional[_Union[API_v1_Prop_Request.GetProp, _Mapping]] = ..., put_prop: _Optional[_Union[API_v1_Prop_Request.PutProp, _Mapping]] = ..., delete_prop: _Optional[_Union[API_v1_Prop_Request.DeleteProp, _Mapping]] = ..., trigger_prop: _Optional[_Union[API_v1_Prop_Request.TriggerProp, _Mapping]] = ..., clear_prop: _Optional[_Union[API_v1_Prop_Request.ClearProp, _Mapping]] = ..., get_thumbnail: _Optional[_Union[API_v1_Prop_Request.GetThumbnail, _Mapping]] = ..., get_prop_collections: _Optional[_Union[API_v1_Prop_Request.GetPropCollections, _Mapping]] = ..., get_prop_collection: _Optional[_Union[API_v1_Prop_Request.GetPropCollection, _Mapping]] = ..., post_prop_collections: _Optional[_Union[API_v1_Prop_Request.PostPropCollections, _Mapping]] = ..., put_prop_collection: _Optional[_Union[API_v1_Prop_Request.PutPropCollection, _Mapping]] = ..., delete_prop_collection: _Optional[_Union[API_v1_Prop_Request.DeletePropCollection, _Mapping]] = ..., pause_prop: _Optional[_Union[API_v1_Prop_Request.PauseProp, _Mapping]] = ..., resume_prop: _Optional[_Union[API_v1_Prop_Request.ResumeProp, _Mapping]] = ...) -> None: ...

class API_v1_Prop_Response(_message.Message):
    __slots__ = ("props", "get_prop", "put_prop", "delete_prop", "trigger_prop", "clear_prop", "get_thumbnail", "get_prop_collections", "get_prop_collection", "post_prop_collections", "put_prop_collection", "delete_prop_collection", "pause_prop", "resume_prop")
    class Props(_message.Message):
        __slots__ = ("props",)
        PROPS_FIELD_NUMBER: _ClassVar[int]
        props: _containers.RepeatedCompositeFieldContainer[API_v1_PropData]
        def __init__(self, props: _Optional[_Iterable[_Union[API_v1_PropData, _Mapping]]] = ...) -> None: ...
    class GetProp(_message.Message):
        __slots__ = ("prop",)
        PROP_FIELD_NUMBER: _ClassVar[int]
        prop: API_v1_PropData
        def __init__(self, prop: _Optional[_Union[API_v1_PropData, _Mapping]] = ...) -> None: ...
    class PutProp(_message.Message):
        __slots__ = ("prop",)
        PROP_FIELD_NUMBER: _ClassVar[int]
        prop: API_v1_PropData
        def __init__(self, prop: _Optional[_Union[API_v1_PropData, _Mapping]] = ...) -> None: ...
    class DeleteProp(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class TriggerProp(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ClearProp(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class PauseProp(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ResumeProp(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GetThumbnail(_message.Message):
        __slots__ = ("data",)
        DATA_FIELD_NUMBER: _ClassVar[int]
        data: bytes
        def __init__(self, data: _Optional[bytes] = ...) -> None: ...
    class GetPropCollections(_message.Message):
        __slots__ = ("prop_collections",)
        class Collections(_message.Message):
            __slots__ = ("collections",)
            COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
            collections: _containers.RepeatedCompositeFieldContainer[API_v1_PropCollection]
            def __init__(self, collections: _Optional[_Iterable[_Union[API_v1_PropCollection, _Mapping]]] = ...) -> None: ...
        PROP_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
        prop_collections: API_v1_Prop_Response.GetPropCollections.Collections
        def __init__(self, prop_collections: _Optional[_Union[API_v1_Prop_Response.GetPropCollections.Collections, _Mapping]] = ...) -> None: ...
    class GetPropCollection(_message.Message):
        __slots__ = ("prop_collection",)
        PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
        prop_collection: API_v1_PropCollection
        def __init__(self, prop_collection: _Optional[_Union[API_v1_PropCollection, _Mapping]] = ...) -> None: ...
    class PostPropCollections(_message.Message):
        __slots__ = ("prop_collection",)
        PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
        prop_collection: API_v1_PropCollection
        def __init__(self, prop_collection: _Optional[_Union[API_v1_PropCollection, _Mapping]] = ...) -> None: ...
    class PutPropCollection(_message.Message):
        __slots__ = ("prop_collection",)
        PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
        prop_collection: API_v1_PropCollection
        def __init__(self, prop_collection: _Optional[_Union[API_v1_PropCollection, _Mapping]] = ...) -> None: ...
    class DeletePropCollection(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    PROPS_FIELD_NUMBER: _ClassVar[int]
    GET_PROP_FIELD_NUMBER: _ClassVar[int]
    PUT_PROP_FIELD_NUMBER: _ClassVar[int]
    DELETE_PROP_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PROP_FIELD_NUMBER: _ClassVar[int]
    CLEAR_PROP_FIELD_NUMBER: _ClassVar[int]
    GET_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    GET_PROP_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    GET_PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    POST_PROP_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    PUT_PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DELETE_PROP_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    PAUSE_PROP_FIELD_NUMBER: _ClassVar[int]
    RESUME_PROP_FIELD_NUMBER: _ClassVar[int]
    props: API_v1_Prop_Response.Props
    get_prop: API_v1_Prop_Response.GetProp
    put_prop: API_v1_Prop_Response.PutProp
    delete_prop: API_v1_Prop_Response.DeleteProp
    trigger_prop: API_v1_Prop_Response.TriggerProp
    clear_prop: API_v1_Prop_Response.ClearProp
    get_thumbnail: API_v1_Prop_Response.GetThumbnail
    get_prop_collections: API_v1_Prop_Response.GetPropCollections
    get_prop_collection: API_v1_Prop_Response.GetPropCollection
    post_prop_collections: API_v1_Prop_Response.PostPropCollections
    put_prop_collection: API_v1_Prop_Response.PutPropCollection
    delete_prop_collection: API_v1_Prop_Response.DeletePropCollection
    pause_prop: API_v1_Prop_Response.PauseProp
    resume_prop: API_v1_Prop_Response.ResumeProp
    def __init__(self, props: _Optional[_Union[API_v1_Prop_Response.Props, _Mapping]] = ..., get_prop: _Optional[_Union[API_v1_Prop_Response.GetProp, _Mapping]] = ..., put_prop: _Optional[_Union[API_v1_Prop_Response.PutProp, _Mapping]] = ..., delete_prop: _Optional[_Union[API_v1_Prop_Response.DeleteProp, _Mapping]] = ..., trigger_prop: _Optional[_Union[API_v1_Prop_Response.TriggerProp, _Mapping]] = ..., clear_prop: _Optional[_Union[API_v1_Prop_Response.ClearProp, _Mapping]] = ..., get_thumbnail: _Optional[_Union[API_v1_Prop_Response.GetThumbnail, _Mapping]] = ..., get_prop_collections: _Optional[_Union[API_v1_Prop_Response.GetPropCollections, _Mapping]] = ..., get_prop_collection: _Optional[_Union[API_v1_Prop_Response.GetPropCollection, _Mapping]] = ..., post_prop_collections: _Optional[_Union[API_v1_Prop_Response.PostPropCollections, _Mapping]] = ..., put_prop_collection: _Optional[_Union[API_v1_Prop_Response.PutPropCollection, _Mapping]] = ..., delete_prop_collection: _Optional[_Union[API_v1_Prop_Response.DeletePropCollection, _Mapping]] = ..., pause_prop: _Optional[_Union[API_v1_Prop_Response.PauseProp, _Mapping]] = ..., resume_prop: _Optional[_Union[API_v1_Prop_Response.ResumeProp, _Mapping]] = ...) -> None: ...
