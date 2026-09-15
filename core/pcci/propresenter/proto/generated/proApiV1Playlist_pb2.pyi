from google.protobuf import wrappers_pb2 as _wrappers_pb2
import proApiV1Color_pb2 as _proApiV1Color_pb2
import proApiV1ContentType_pb2 as _proApiV1ContentType_pb2
import proApiV1Identifier_pb2 as _proApiV1Identifier_pb2
import proApiV1PresentationPlaylistItem_pb2 as _proApiV1PresentationPlaylistItem_pb2
import proApiV1Presentation_pb2 as _proApiV1Presentation_pb2
import proApiV1TimelineOperation_pb2 as _proApiV1TimelineOperation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_Playlist(_message.Message):
    __slots__ = ("id", "type", "children")
    class API_v1_PlaylistType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        group: _ClassVar[API_v1_Playlist.API_v1_PlaylistType]
        playlist: _ClassVar[API_v1_Playlist.API_v1_PlaylistType]
    group: API_v1_Playlist.API_v1_PlaylistType
    playlist: API_v1_Playlist.API_v1_PlaylistType
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    id: _proApiV1Identifier_pb2.API_v1_Identifier
    type: API_v1_Playlist.API_v1_PlaylistType
    children: _containers.RepeatedCompositeFieldContainer[API_v1_Playlist]
    def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., type: _Optional[_Union[API_v1_Playlist.API_v1_PlaylistType, str]] = ..., children: _Optional[_Iterable[_Union[API_v1_Playlist, _Mapping]]] = ...) -> None: ...

class API_v1_PlaylistAndItem(_message.Message):
    __slots__ = ("playlist", "item", "playlist_item")
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ITEM_FIELD_NUMBER: _ClassVar[int]
    playlist: _proApiV1Identifier_pb2.API_v1_Identifier
    item: _proApiV1Identifier_pb2.API_v1_Identifier
    playlist_item: API_v1_PlaylistItem
    def __init__(self, playlist: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., item: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., playlist_item: _Optional[_Union[API_v1_PlaylistItem, _Mapping]] = ...) -> None: ...

class API_v1_PlaylistItem(_message.Message):
    __slots__ = ("id", "type", "is_hidden", "is_pco", "header_color", "duration", "presentation_info", "target_uuid", "destination")
    class API_v1_PlaylistItemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        presentation: _ClassVar[API_v1_PlaylistItem.API_v1_PlaylistItemType]
        placeholder: _ClassVar[API_v1_PlaylistItem.API_v1_PlaylistItemType]
        header: _ClassVar[API_v1_PlaylistItem.API_v1_PlaylistItemType]
        media: _ClassVar[API_v1_PlaylistItem.API_v1_PlaylistItemType]
        audio: _ClassVar[API_v1_PlaylistItem.API_v1_PlaylistItemType]
        livevideo: _ClassVar[API_v1_PlaylistItem.API_v1_PlaylistItemType]
    presentation: API_v1_PlaylistItem.API_v1_PlaylistItemType
    placeholder: API_v1_PlaylistItem.API_v1_PlaylistItemType
    header: API_v1_PlaylistItem.API_v1_PlaylistItemType
    media: API_v1_PlaylistItem.API_v1_PlaylistItemType
    audio: API_v1_PlaylistItem.API_v1_PlaylistItemType
    livevideo: API_v1_PlaylistItem.API_v1_PlaylistItemType
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    IS_PCO_FIELD_NUMBER: _ClassVar[int]
    HEADER_COLOR_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_INFO_FIELD_NUMBER: _ClassVar[int]
    TARGET_UUID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    id: _proApiV1Identifier_pb2.API_v1_Identifier
    type: API_v1_PlaylistItem.API_v1_PlaylistItemType
    is_hidden: bool
    is_pco: bool
    header_color: _proApiV1Color_pb2.API_v1_Color
    duration: _wrappers_pb2.UInt32Value
    presentation_info: _proApiV1PresentationPlaylistItem_pb2.API_v1_PlaylistPresentationItem
    target_uuid: str
    destination: _proApiV1Presentation_pb2.API_v1_Presentation.Destination
    def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., type: _Optional[_Union[API_v1_PlaylistItem.API_v1_PlaylistItemType, str]] = ..., is_hidden: _Optional[bool] = ..., is_pco: _Optional[bool] = ..., header_color: _Optional[_Union[_proApiV1Color_pb2.API_v1_Color, _Mapping]] = ..., duration: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., presentation_info: _Optional[_Union[_proApiV1PresentationPlaylistItem_pb2.API_v1_PlaylistPresentationItem, _Mapping]] = ..., target_uuid: _Optional[str] = ..., destination: _Optional[_Union[_proApiV1Presentation_pb2.API_v1_Presentation.Destination, str]] = ...) -> None: ...

class API_v1_Playlist_Request(_message.Message):
    __slots__ = ("playlists", "create_playlist", "get_playlist", "put_playlist", "post_playlist", "get_active_playlist", "focused", "next_focus", "previous_focus", "active_presentation_focus", "active_announcement_focus", "focused_trigger", "active_presentation_trigger", "active_announcement_trigger", "focused_next_trigger", "focused_previous_trigger", "active_presentation_next_trigger", "active_announcement_next_trigger", "active_presentation_previous_trigger", "active_announcement_previous_trigger", "id_focus", "id_trigger", "id_next_trigger", "id_previous_trigger", "focused_index_trigger", "active_presentation_index_trigger", "active_announcement_index_trigger", "id_updates", "active_presentation_thumbnail", "active_announcement_thumbnail", "focused_next", "focused_previous", "id_thumbnail", "timeline_operation", "active_playlist_presentation_timeline_operation", "active_playlist_announcement_timeline_operation", "focused_playlist_timeline_operation", "active_playlist_presentation_timeline_status", "active_playlist_announcement_timeline_status", "focused_playlist_timeline_status")
    class Playlists(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class CreatePlaylist(_message.Message):
        __slots__ = ("name", "type")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: API_v1_Playlist.API_v1_PlaylistType
        def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[API_v1_Playlist.API_v1_PlaylistType, str]] = ...) -> None: ...
    class GetActivePlaylist(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GetPlaylist(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class PutPlaylist(_message.Message):
        __slots__ = ("id", "items")
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        id: str
        items: _containers.RepeatedCompositeFieldContainer[API_v1_PlaylistItem]
        def __init__(self, id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[API_v1_PlaylistItem, _Mapping]]] = ...) -> None: ...
    class PostPlaylist(_message.Message):
        __slots__ = ("id", "name", "type")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        type: API_v1_Playlist.API_v1_PlaylistType
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[API_v1_Playlist.API_v1_PlaylistType, str]] = ...) -> None: ...
    class Thumbnail(_message.Message):
        __slots__ = ("index", "cue_index", "quality", "content_type")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        CUE_INDEX_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        index: int
        cue_index: int
        quality: int
        content_type: _proApiV1ContentType_pb2.API_v1_ContentType
        def __init__(self, index: _Optional[int] = ..., cue_index: _Optional[int] = ..., quality: _Optional[int] = ..., content_type: _Optional[_Union[_proApiV1ContentType_pb2.API_v1_ContentType, str]] = ...) -> None: ...
    class IdThumbnail(_message.Message):
        __slots__ = ("id", "index", "cue_index", "quality", "content_type")
        ID_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        CUE_INDEX_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        id: str
        index: int
        cue_index: int
        quality: int
        content_type: _proApiV1ContentType_pb2.API_v1_ContentType
        def __init__(self, id: _Optional[str] = ..., index: _Optional[int] = ..., cue_index: _Optional[int] = ..., quality: _Optional[int] = ..., content_type: _Optional[_Union[_proApiV1ContentType_pb2.API_v1_ContentType, str]] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class IdMessage(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class IndexMessage(_message.Message):
        __slots__ = ("index", "cue_index")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        CUE_INDEX_FIELD_NUMBER: _ClassVar[int]
        index: int
        cue_index: int
        def __init__(self, index: _Optional[int] = ..., cue_index: _Optional[int] = ...) -> None: ...
    class TimelineOperation(_message.Message):
        __slots__ = ("id", "index", "operation")
        ID_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        id: str
        index: int
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, id: _Optional[str] = ..., index: _Optional[int] = ..., operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class ActivePlaylistTimelineOperation(_message.Message):
        __slots__ = ("index", "operation")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        index: int
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, index: _Optional[int] = ..., operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class FocusedPlaylistTimelineOperation(_message.Message):
        __slots__ = ("index", "operation")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        index: int
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, index: _Optional[int] = ..., operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class ActivePlaylistTimelineStatus(_message.Message):
        __slots__ = ("index",)
        INDEX_FIELD_NUMBER: _ClassVar[int]
        index: int
        def __init__(self, index: _Optional[int] = ...) -> None: ...
    class FocusedPlaylistTimelineStatus(_message.Message):
        __slots__ = ("index",)
        INDEX_FIELD_NUMBER: _ClassVar[int]
        index: int
        def __init__(self, index: _Optional[int] = ...) -> None: ...
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    CREATE_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    GET_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    PUT_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    POST_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    GET_ACTIVE_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_FIELD_NUMBER: _ClassVar[int]
    NEXT_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_FOCUS_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_UPDATES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_NEXT_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PREVIOUS_FIELD_NUMBER: _ClassVar[int]
    ID_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_PRESENTATION_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_ANNOUNCEMENT_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PLAYLIST_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_PRESENTATION_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_ANNOUNCEMENT_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PLAYLIST_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    playlists: API_v1_Playlist_Request.Playlists
    create_playlist: API_v1_Playlist_Request.CreatePlaylist
    get_playlist: API_v1_Playlist_Request.GetPlaylist
    put_playlist: API_v1_Playlist_Request.PutPlaylist
    post_playlist: API_v1_Playlist_Request.PostPlaylist
    get_active_playlist: API_v1_Playlist_Request.GetActivePlaylist
    focused: API_v1_Playlist_Request.GetActivePlaylist
    next_focus: API_v1_Playlist_Request.EmptyMessage
    previous_focus: API_v1_Playlist_Request.EmptyMessage
    active_presentation_focus: API_v1_Playlist_Request.EmptyMessage
    active_announcement_focus: API_v1_Playlist_Request.EmptyMessage
    focused_trigger: API_v1_Playlist_Request.EmptyMessage
    active_presentation_trigger: API_v1_Playlist_Request.EmptyMessage
    active_announcement_trigger: API_v1_Playlist_Request.EmptyMessage
    focused_next_trigger: API_v1_Playlist_Request.EmptyMessage
    focused_previous_trigger: API_v1_Playlist_Request.EmptyMessage
    active_presentation_next_trigger: API_v1_Playlist_Request.EmptyMessage
    active_announcement_next_trigger: API_v1_Playlist_Request.EmptyMessage
    active_presentation_previous_trigger: API_v1_Playlist_Request.EmptyMessage
    active_announcement_previous_trigger: API_v1_Playlist_Request.EmptyMessage
    id_focus: API_v1_Playlist_Request.IdMessage
    id_trigger: API_v1_Playlist_Request.IdMessage
    id_next_trigger: API_v1_Playlist_Request.IdMessage
    id_previous_trigger: API_v1_Playlist_Request.IdMessage
    focused_index_trigger: API_v1_Playlist_Request.IndexMessage
    active_presentation_index_trigger: API_v1_Playlist_Request.IndexMessage
    active_announcement_index_trigger: API_v1_Playlist_Request.IndexMessage
    id_updates: API_v1_Playlist_Request.IdMessage
    active_presentation_thumbnail: API_v1_Playlist_Request.Thumbnail
    active_announcement_thumbnail: API_v1_Playlist_Request.Thumbnail
    focused_next: API_v1_Playlist_Request.EmptyMessage
    focused_previous: API_v1_Playlist_Request.EmptyMessage
    id_thumbnail: API_v1_Playlist_Request.IdThumbnail
    timeline_operation: API_v1_Playlist_Request.TimelineOperation
    active_playlist_presentation_timeline_operation: API_v1_Playlist_Request.ActivePlaylistTimelineOperation
    active_playlist_announcement_timeline_operation: API_v1_Playlist_Request.ActivePlaylistTimelineOperation
    focused_playlist_timeline_operation: API_v1_Playlist_Request.FocusedPlaylistTimelineOperation
    active_playlist_presentation_timeline_status: API_v1_Playlist_Request.ActivePlaylistTimelineStatus
    active_playlist_announcement_timeline_status: API_v1_Playlist_Request.ActivePlaylistTimelineStatus
    focused_playlist_timeline_status: API_v1_Playlist_Request.FocusedPlaylistTimelineStatus
    def __init__(self, playlists: _Optional[_Union[API_v1_Playlist_Request.Playlists, _Mapping]] = ..., create_playlist: _Optional[_Union[API_v1_Playlist_Request.CreatePlaylist, _Mapping]] = ..., get_playlist: _Optional[_Union[API_v1_Playlist_Request.GetPlaylist, _Mapping]] = ..., put_playlist: _Optional[_Union[API_v1_Playlist_Request.PutPlaylist, _Mapping]] = ..., post_playlist: _Optional[_Union[API_v1_Playlist_Request.PostPlaylist, _Mapping]] = ..., get_active_playlist: _Optional[_Union[API_v1_Playlist_Request.GetActivePlaylist, _Mapping]] = ..., focused: _Optional[_Union[API_v1_Playlist_Request.GetActivePlaylist, _Mapping]] = ..., next_focus: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., previous_focus: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_presentation_focus: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_announcement_focus: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., focused_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_presentation_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_announcement_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., focused_next_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., focused_previous_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_presentation_next_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_announcement_next_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_presentation_previous_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., active_announcement_previous_trigger: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., id_focus: _Optional[_Union[API_v1_Playlist_Request.IdMessage, _Mapping]] = ..., id_trigger: _Optional[_Union[API_v1_Playlist_Request.IdMessage, _Mapping]] = ..., id_next_trigger: _Optional[_Union[API_v1_Playlist_Request.IdMessage, _Mapping]] = ..., id_previous_trigger: _Optional[_Union[API_v1_Playlist_Request.IdMessage, _Mapping]] = ..., focused_index_trigger: _Optional[_Union[API_v1_Playlist_Request.IndexMessage, _Mapping]] = ..., active_presentation_index_trigger: _Optional[_Union[API_v1_Playlist_Request.IndexMessage, _Mapping]] = ..., active_announcement_index_trigger: _Optional[_Union[API_v1_Playlist_Request.IndexMessage, _Mapping]] = ..., id_updates: _Optional[_Union[API_v1_Playlist_Request.IdMessage, _Mapping]] = ..., active_presentation_thumbnail: _Optional[_Union[API_v1_Playlist_Request.Thumbnail, _Mapping]] = ..., active_announcement_thumbnail: _Optional[_Union[API_v1_Playlist_Request.Thumbnail, _Mapping]] = ..., focused_next: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., focused_previous: _Optional[_Union[API_v1_Playlist_Request.EmptyMessage, _Mapping]] = ..., id_thumbnail: _Optional[_Union[API_v1_Playlist_Request.IdThumbnail, _Mapping]] = ..., timeline_operation: _Optional[_Union[API_v1_Playlist_Request.TimelineOperation, _Mapping]] = ..., active_playlist_presentation_timeline_operation: _Optional[_Union[API_v1_Playlist_Request.ActivePlaylistTimelineOperation, _Mapping]] = ..., active_playlist_announcement_timeline_operation: _Optional[_Union[API_v1_Playlist_Request.ActivePlaylistTimelineOperation, _Mapping]] = ..., focused_playlist_timeline_operation: _Optional[_Union[API_v1_Playlist_Request.FocusedPlaylistTimelineOperation, _Mapping]] = ..., active_playlist_presentation_timeline_status: _Optional[_Union[API_v1_Playlist_Request.ActivePlaylistTimelineStatus, _Mapping]] = ..., active_playlist_announcement_timeline_status: _Optional[_Union[API_v1_Playlist_Request.ActivePlaylistTimelineStatus, _Mapping]] = ..., focused_playlist_timeline_status: _Optional[_Union[API_v1_Playlist_Request.FocusedPlaylistTimelineStatus, _Mapping]] = ...) -> None: ...

class API_v1_Playlist_Response(_message.Message):
    __slots__ = ("playlists", "create_playlist", "get_playlist", "put_playlist", "post_playlist", "get_active_playlist", "focused", "next_focus", "previous_focus", "active_presentation_focus", "active_announcement_focus", "focused_trigger", "active_presentation_trigger", "active_announcement_trigger", "focused_next_trigger", "focused_previous_trigger", "active_presentation_next_trigger", "active_announcement_next_trigger", "active_presentation_previous_trigger", "active_announcement_previous_trigger", "id_focus", "id_trigger", "id_next_trigger", "id_previous_trigger", "focused_index_trigger", "active_presentation_index_trigger", "active_announcement_index_trigger", "id_updates", "active_presentation_thumbnail", "active_announcement_thumbnail", "focused_next", "focused_previous", "id_thumbnail", "timeline_operation", "active_playlist_presentation_timeline_operation", "active_playlist_announcement_timeline_operation", "focused_playlist_timeline_operation", "active_playlist_presentation_timeline_status", "active_playlist_announcement_timeline_status", "focused_playlist_timeline_status")
    class Playlists(_message.Message):
        __slots__ = ("playlists",)
        PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
        playlists: _containers.RepeatedCompositeFieldContainer[API_v1_Playlist]
        def __init__(self, playlists: _Optional[_Iterable[_Union[API_v1_Playlist, _Mapping]]] = ...) -> None: ...
    class CreatePlaylist(_message.Message):
        __slots__ = ("playlist",)
        PLAYLIST_FIELD_NUMBER: _ClassVar[int]
        playlist: API_v1_Playlist
        def __init__(self, playlist: _Optional[_Union[API_v1_Playlist, _Mapping]] = ...) -> None: ...
    class GetActivePlaylist(_message.Message):
        __slots__ = ("presentation", "announcements")
        PRESENTATION_FIELD_NUMBER: _ClassVar[int]
        ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
        presentation: API_v1_PlaylistAndItem
        announcements: API_v1_PlaylistAndItem
        def __init__(self, presentation: _Optional[_Union[API_v1_PlaylistAndItem, _Mapping]] = ..., announcements: _Optional[_Union[API_v1_PlaylistAndItem, _Mapping]] = ...) -> None: ...
    class GetPlaylist(_message.Message):
        __slots__ = ("id", "items")
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        items: _containers.RepeatedCompositeFieldContainer[API_v1_PlaylistItem]
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., items: _Optional[_Iterable[_Union[API_v1_PlaylistItem, _Mapping]]] = ...) -> None: ...
    class PutPlaylist(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class PostPlaylist(_message.Message):
        __slots__ = ("playlist",)
        PLAYLIST_FIELD_NUMBER: _ClassVar[int]
        playlist: API_v1_Playlist
        def __init__(self, playlist: _Optional[_Union[API_v1_Playlist, _Mapping]] = ...) -> None: ...
    class GetFocusedPlaylist(_message.Message):
        __slots__ = ("playlist",)
        PLAYLIST_FIELD_NUMBER: _ClassVar[int]
        playlist: API_v1_PlaylistAndItem
        def __init__(self, playlist: _Optional[_Union[API_v1_PlaylistAndItem, _Mapping]] = ...) -> None: ...
    class GetProximalPlaylistItem(_message.Message):
        __slots__ = ("item",)
        ITEM_FIELD_NUMBER: _ClassVar[int]
        item: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, item: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class Thumbnail(_message.Message):
        __slots__ = ("data", "content_type")
        DATA_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        data: bytes
        content_type: _proApiV1ContentType_pb2.API_v1_ContentType
        def __init__(self, data: _Optional[bytes] = ..., content_type: _Optional[_Union[_proApiV1ContentType_pb2.API_v1_ContentType, str]] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class TimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActivePlaylistTimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FocusedPlaylistTimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActivePlaylistTimelineStatus(_message.Message):
        __slots__ = ("is_running", "current_time")
        IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        is_running: bool
        current_time: float
        def __init__(self, is_running: _Optional[bool] = ..., current_time: _Optional[float] = ...) -> None: ...
    class FocusedPlaylistTimelineStatus(_message.Message):
        __slots__ = ("is_running", "current_time")
        IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        is_running: bool
        current_time: float
        def __init__(self, is_running: _Optional[bool] = ..., current_time: _Optional[float] = ...) -> None: ...
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    CREATE_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    GET_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    PUT_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    POST_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    GET_ACTIVE_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_FIELD_NUMBER: _ClassVar[int]
    NEXT_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_FOCUS_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ID_UPDATES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ANNOUNCEMENT_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_NEXT_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PREVIOUS_FIELD_NUMBER: _ClassVar[int]
    ID_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_PRESENTATION_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_ANNOUNCEMENT_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PLAYLIST_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_PRESENTATION_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PLAYLIST_ANNOUNCEMENT_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PLAYLIST_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    playlists: API_v1_Playlist_Response.Playlists
    create_playlist: API_v1_Playlist_Response.CreatePlaylist
    get_playlist: API_v1_Playlist_Response.GetPlaylist
    put_playlist: API_v1_Playlist_Response.PutPlaylist
    post_playlist: API_v1_Playlist_Response.PostPlaylist
    get_active_playlist: API_v1_Playlist_Response.GetActivePlaylist
    focused: API_v1_Playlist_Response.GetFocusedPlaylist
    next_focus: API_v1_Playlist_Response.EmptyMessage
    previous_focus: API_v1_Playlist_Response.EmptyMessage
    active_presentation_focus: API_v1_Playlist_Response.EmptyMessage
    active_announcement_focus: API_v1_Playlist_Response.EmptyMessage
    focused_trigger: API_v1_Playlist_Response.EmptyMessage
    active_presentation_trigger: API_v1_Playlist_Response.EmptyMessage
    active_announcement_trigger: API_v1_Playlist_Response.EmptyMessage
    focused_next_trigger: API_v1_Playlist_Response.EmptyMessage
    focused_previous_trigger: API_v1_Playlist_Response.EmptyMessage
    active_presentation_next_trigger: API_v1_Playlist_Response.EmptyMessage
    active_announcement_next_trigger: API_v1_Playlist_Response.EmptyMessage
    active_presentation_previous_trigger: API_v1_Playlist_Response.EmptyMessage
    active_announcement_previous_trigger: API_v1_Playlist_Response.EmptyMessage
    id_focus: API_v1_Playlist_Response.EmptyMessage
    id_trigger: API_v1_Playlist_Response.EmptyMessage
    id_next_trigger: API_v1_Playlist_Response.EmptyMessage
    id_previous_trigger: API_v1_Playlist_Response.EmptyMessage
    focused_index_trigger: API_v1_Playlist_Response.EmptyMessage
    active_presentation_index_trigger: API_v1_Playlist_Response.EmptyMessage
    active_announcement_index_trigger: API_v1_Playlist_Response.EmptyMessage
    id_updates: API_v1_Playlist_Response.EmptyMessage
    active_presentation_thumbnail: API_v1_Playlist_Response.Thumbnail
    active_announcement_thumbnail: API_v1_Playlist_Response.Thumbnail
    focused_next: API_v1_Playlist_Response.GetProximalPlaylistItem
    focused_previous: API_v1_Playlist_Response.GetProximalPlaylistItem
    id_thumbnail: API_v1_Playlist_Response.Thumbnail
    timeline_operation: API_v1_Playlist_Response.TimelineOperation
    active_playlist_presentation_timeline_operation: API_v1_Playlist_Response.ActivePlaylistTimelineOperation
    active_playlist_announcement_timeline_operation: API_v1_Playlist_Response.ActivePlaylistTimelineOperation
    focused_playlist_timeline_operation: API_v1_Playlist_Response.FocusedPlaylistTimelineOperation
    active_playlist_presentation_timeline_status: API_v1_Playlist_Response.ActivePlaylistTimelineStatus
    active_playlist_announcement_timeline_status: API_v1_Playlist_Response.ActivePlaylistTimelineStatus
    focused_playlist_timeline_status: API_v1_Playlist_Response.FocusedPlaylistTimelineStatus
    def __init__(self, playlists: _Optional[_Union[API_v1_Playlist_Response.Playlists, _Mapping]] = ..., create_playlist: _Optional[_Union[API_v1_Playlist_Response.CreatePlaylist, _Mapping]] = ..., get_playlist: _Optional[_Union[API_v1_Playlist_Response.GetPlaylist, _Mapping]] = ..., put_playlist: _Optional[_Union[API_v1_Playlist_Response.PutPlaylist, _Mapping]] = ..., post_playlist: _Optional[_Union[API_v1_Playlist_Response.PostPlaylist, _Mapping]] = ..., get_active_playlist: _Optional[_Union[API_v1_Playlist_Response.GetActivePlaylist, _Mapping]] = ..., focused: _Optional[_Union[API_v1_Playlist_Response.GetFocusedPlaylist, _Mapping]] = ..., next_focus: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., previous_focus: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_presentation_focus: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_announcement_focus: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., focused_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_presentation_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_announcement_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., focused_next_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., focused_previous_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_presentation_next_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_announcement_next_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_presentation_previous_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_announcement_previous_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., id_focus: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., id_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., id_next_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., id_previous_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., focused_index_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_presentation_index_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_announcement_index_trigger: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., id_updates: _Optional[_Union[API_v1_Playlist_Response.EmptyMessage, _Mapping]] = ..., active_presentation_thumbnail: _Optional[_Union[API_v1_Playlist_Response.Thumbnail, _Mapping]] = ..., active_announcement_thumbnail: _Optional[_Union[API_v1_Playlist_Response.Thumbnail, _Mapping]] = ..., focused_next: _Optional[_Union[API_v1_Playlist_Response.GetProximalPlaylistItem, _Mapping]] = ..., focused_previous: _Optional[_Union[API_v1_Playlist_Response.GetProximalPlaylistItem, _Mapping]] = ..., id_thumbnail: _Optional[_Union[API_v1_Playlist_Response.Thumbnail, _Mapping]] = ..., timeline_operation: _Optional[_Union[API_v1_Playlist_Response.TimelineOperation, _Mapping]] = ..., active_playlist_presentation_timeline_operation: _Optional[_Union[API_v1_Playlist_Response.ActivePlaylistTimelineOperation, _Mapping]] = ..., active_playlist_announcement_timeline_operation: _Optional[_Union[API_v1_Playlist_Response.ActivePlaylistTimelineOperation, _Mapping]] = ..., focused_playlist_timeline_operation: _Optional[_Union[API_v1_Playlist_Response.FocusedPlaylistTimelineOperation, _Mapping]] = ..., active_playlist_presentation_timeline_status: _Optional[_Union[API_v1_Playlist_Response.ActivePlaylistTimelineStatus, _Mapping]] = ..., active_playlist_announcement_timeline_status: _Optional[_Union[API_v1_Playlist_Response.ActivePlaylistTimelineStatus, _Mapping]] = ..., focused_playlist_timeline_status: _Optional[_Union[API_v1_Playlist_Response.FocusedPlaylistTimelineStatus, _Mapping]] = ...) -> None: ...
