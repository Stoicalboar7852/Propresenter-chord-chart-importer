from google.protobuf import wrappers_pb2 as _wrappers_pb2
import proApiV1Identifier_pb2 as _proApiV1Identifier_pb2
import proApiV1MediaPlaylistItem_pb2 as _proApiV1MediaPlaylistItem_pb2
import proApiV1Playlist_pb2 as _proApiV1Playlist_pb2
import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_Media_Request(_message.Message):
    __slots__ = ("playlists", "get_playlist", "get_playlist_updates", "get_thumbnail", "playlist_focused", "playlist_active", "focus", "trigger")
    class Playlists(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GetPlaylist(_message.Message):
        __slots__ = ("id", "start")
        ID_FIELD_NUMBER: _ClassVar[int]
        START_FIELD_NUMBER: _ClassVar[int]
        id: str
        start: int
        def __init__(self, id: _Optional[str] = ..., start: _Optional[int] = ...) -> None: ...
    class GetPlaylistUpdates(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class GetThumbnail(_message.Message):
        __slots__ = ("uuid", "quality")
        UUID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        quality: int
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., quality: _Optional[int] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FocusMessage(_message.Message):
        __slots__ = ("next", "previous", "active", "id")
        NEXT_FIELD_NUMBER: _ClassVar[int]
        PREVIOUS_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        next: API_v1_Media_Request.EmptyMessage
        previous: API_v1_Media_Request.EmptyMessage
        active: API_v1_Media_Request.EmptyMessage
        id: _wrappers_pb2.StringValue
        def __init__(self, next: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., previous: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., active: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...
    class TriggerMessage(_message.Message):
        __slots__ = ("focused", "active", "playlist_id", "start", "next", "previous", "media_id")
        FOCUSED_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
        START_FIELD_NUMBER: _ClassVar[int]
        NEXT_FIELD_NUMBER: _ClassVar[int]
        PREVIOUS_FIELD_NUMBER: _ClassVar[int]
        MEDIA_ID_FIELD_NUMBER: _ClassVar[int]
        focused: API_v1_Media_Request.EmptyMessage
        active: API_v1_Media_Request.EmptyMessage
        playlist_id: _wrappers_pb2.StringValue
        start: API_v1_Media_Request.EmptyMessage
        next: API_v1_Media_Request.EmptyMessage
        previous: API_v1_Media_Request.EmptyMessage
        media_id: _wrappers_pb2.StringValue
        def __init__(self, focused: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., active: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., playlist_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., start: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., next: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., previous: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., media_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    GET_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    GET_PLAYLIST_UPDATES_FIELD_NUMBER: _ClassVar[int]
    GET_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FOCUS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    playlists: API_v1_Media_Request.Playlists
    get_playlist: API_v1_Media_Request.GetPlaylist
    get_playlist_updates: API_v1_Media_Request.GetPlaylistUpdates
    get_thumbnail: API_v1_Media_Request.GetThumbnail
    playlist_focused: API_v1_Media_Request.EmptyMessage
    playlist_active: API_v1_Media_Request.EmptyMessage
    focus: API_v1_Media_Request.FocusMessage
    trigger: API_v1_Media_Request.TriggerMessage
    def __init__(self, playlists: _Optional[_Union[API_v1_Media_Request.Playlists, _Mapping]] = ..., get_playlist: _Optional[_Union[API_v1_Media_Request.GetPlaylist, _Mapping]] = ..., get_playlist_updates: _Optional[_Union[API_v1_Media_Request.GetPlaylistUpdates, _Mapping]] = ..., get_thumbnail: _Optional[_Union[API_v1_Media_Request.GetThumbnail, _Mapping]] = ..., playlist_focused: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., playlist_active: _Optional[_Union[API_v1_Media_Request.EmptyMessage, _Mapping]] = ..., focus: _Optional[_Union[API_v1_Media_Request.FocusMessage, _Mapping]] = ..., trigger: _Optional[_Union[API_v1_Media_Request.TriggerMessage, _Mapping]] = ...) -> None: ...

class API_v1_Media_Response(_message.Message):
    __slots__ = ("playlists", "get_playlist", "get_playlist_updates", "get_thumbnail", "playlist_focused", "playlist_active", "focus", "trigger")
    class Playlists(_message.Message):
        __slots__ = ("playlists",)
        PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
        playlists: _containers.RepeatedCompositeFieldContainer[_proApiV1Playlist_pb2.API_v1_Playlist]
        def __init__(self, playlists: _Optional[_Iterable[_Union[_proApiV1Playlist_pb2.API_v1_Playlist, _Mapping]]] = ...) -> None: ...
    class GetPlaylist(_message.Message):
        __slots__ = ("id", "items")
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        items: _containers.RepeatedCompositeFieldContainer[_proApiV1MediaPlaylistItem_pb2.API_v1_MediaPlaylistItem]
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_proApiV1MediaPlaylistItem_pb2.API_v1_MediaPlaylistItem, _Mapping]]] = ...) -> None: ...
    class GetPlaylistUpdates(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class GetThumbnail(_message.Message):
        __slots__ = ("uuid", "thumbnail_data")
        UUID_FIELD_NUMBER: _ClassVar[int]
        THUMBNAIL_DATA_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        thumbnail_data: bytes
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., thumbnail_data: _Optional[bytes] = ...) -> None: ...
    class GetFocusedPlaylist(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class GetActivePlaylist(_message.Message):
        __slots__ = ("playlist", "item")
        PLAYLIST_FIELD_NUMBER: _ClassVar[int]
        ITEM_FIELD_NUMBER: _ClassVar[int]
        playlist: _proApiV1Identifier_pb2.API_v1_Identifier
        item: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, playlist: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., item: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    GET_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    GET_PLAYLIST_UPDATES_FIELD_NUMBER: _ClassVar[int]
    GET_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FOCUS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    playlists: API_v1_Media_Response.Playlists
    get_playlist: API_v1_Media_Response.GetPlaylist
    get_playlist_updates: API_v1_Media_Response.GetPlaylistUpdates
    get_thumbnail: API_v1_Media_Response.GetThumbnail
    playlist_focused: API_v1_Media_Response.GetFocusedPlaylist
    playlist_active: API_v1_Media_Response.GetActivePlaylist
    focus: API_v1_Media_Response.EmptyMessage
    trigger: API_v1_Media_Response.EmptyMessage
    def __init__(self, playlists: _Optional[_Union[API_v1_Media_Response.Playlists, _Mapping]] = ..., get_playlist: _Optional[_Union[API_v1_Media_Response.GetPlaylist, _Mapping]] = ..., get_playlist_updates: _Optional[_Union[API_v1_Media_Response.GetPlaylistUpdates, _Mapping]] = ..., get_thumbnail: _Optional[_Union[API_v1_Media_Response.GetThumbnail, _Mapping]] = ..., playlist_focused: _Optional[_Union[API_v1_Media_Response.GetFocusedPlaylist, _Mapping]] = ..., playlist_active: _Optional[_Union[API_v1_Media_Response.GetActivePlaylist, _Mapping]] = ..., focus: _Optional[_Union[API_v1_Media_Response.EmptyMessage, _Mapping]] = ..., trigger: _Optional[_Union[API_v1_Media_Response.EmptyMessage, _Mapping]] = ...) -> None: ...
