import proApiV1Identifier_pb2 as _proApiV1Identifier_pb2
import proApiV1MediaPlaylistItem_pb2 as _proApiV1MediaPlaylistItem_pb2
import proApiV1Playlist_pb2 as _proApiV1Playlist_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_Audio_Request(_message.Message):
    __slots__ = ("playlists", "playlist", "playlist_updates", "playlist_focused", "playlist_active", "playlist_next_focus", "playlist_previous_focus", "playlist_active_focus", "playlist_id_focus", "playlist_focused_trigger", "playlist_active_trigger", "playlist_id_trigger", "playlist_focused_next_trigger", "playlist_focused_previous_trigger", "playlist_focused_id_trigger", "playlist_active_next_trigger", "playlist_active_previous_trigger", "playlist_active_id_trigger", "playlist_id_next_trigger", "playlist_id_previous_trigger")
    class Playlists(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Playlist(_message.Message):
        __slots__ = ("id", "start")
        ID_FIELD_NUMBER: _ClassVar[int]
        START_FIELD_NUMBER: _ClassVar[int]
        id: str
        start: int
        def __init__(self, id: _Optional[str] = ..., start: _Optional[int] = ...) -> None: ...
    class PlaylistUpdates(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class IdentifierMessage(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: str
        def __init__(self, id: _Optional[str] = ...) -> None: ...
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_UPDATES_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_NEXT_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_PREVIOUS_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    playlists: API_v1_Audio_Request.Playlists
    playlist: API_v1_Audio_Request.Playlist
    playlist_updates: API_v1_Audio_Request.PlaylistUpdates
    playlist_focused: API_v1_Audio_Request.EmptyMessage
    playlist_active: API_v1_Audio_Request.EmptyMessage
    playlist_next_focus: API_v1_Audio_Request.EmptyMessage
    playlist_previous_focus: API_v1_Audio_Request.EmptyMessage
    playlist_active_focus: API_v1_Audio_Request.EmptyMessage
    playlist_id_focus: API_v1_Audio_Request.IdentifierMessage
    playlist_focused_trigger: API_v1_Audio_Request.EmptyMessage
    playlist_active_trigger: API_v1_Audio_Request.EmptyMessage
    playlist_id_trigger: API_v1_Audio_Request.IdentifierMessage
    playlist_focused_next_trigger: API_v1_Audio_Request.EmptyMessage
    playlist_focused_previous_trigger: API_v1_Audio_Request.EmptyMessage
    playlist_focused_id_trigger: API_v1_Audio_Request.IdentifierMessage
    playlist_active_next_trigger: API_v1_Audio_Request.EmptyMessage
    playlist_active_previous_trigger: API_v1_Audio_Request.EmptyMessage
    playlist_active_id_trigger: API_v1_Audio_Request.IdentifierMessage
    playlist_id_next_trigger: API_v1_Audio_Request.IdentifierMessage
    playlist_id_previous_trigger: API_v1_Audio_Request.IdentifierMessage
    def __init__(self, playlists: _Optional[_Union[API_v1_Audio_Request.Playlists, _Mapping]] = ..., playlist: _Optional[_Union[API_v1_Audio_Request.Playlist, _Mapping]] = ..., playlist_updates: _Optional[_Union[API_v1_Audio_Request.PlaylistUpdates, _Mapping]] = ..., playlist_focused: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_active: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_next_focus: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_previous_focus: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_active_focus: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_id_focus: _Optional[_Union[API_v1_Audio_Request.IdentifierMessage, _Mapping]] = ..., playlist_focused_trigger: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_active_trigger: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_id_trigger: _Optional[_Union[API_v1_Audio_Request.IdentifierMessage, _Mapping]] = ..., playlist_focused_next_trigger: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_focused_previous_trigger: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_focused_id_trigger: _Optional[_Union[API_v1_Audio_Request.IdentifierMessage, _Mapping]] = ..., playlist_active_next_trigger: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_active_previous_trigger: _Optional[_Union[API_v1_Audio_Request.EmptyMessage, _Mapping]] = ..., playlist_active_id_trigger: _Optional[_Union[API_v1_Audio_Request.IdentifierMessage, _Mapping]] = ..., playlist_id_next_trigger: _Optional[_Union[API_v1_Audio_Request.IdentifierMessage, _Mapping]] = ..., playlist_id_previous_trigger: _Optional[_Union[API_v1_Audio_Request.IdentifierMessage, _Mapping]] = ...) -> None: ...

class API_v1_Audio_Response(_message.Message):
    __slots__ = ("playlists", "playlist", "update", "playlist_focused", "playlist_active", "playlist_next_focus", "playlist_previous_focus", "playlist_active_focus", "playlist_id_focus", "playlist_focused_trigger", "playlist_active_trigger", "playlist_id_trigger", "playlist_focused_next_trigger", "playlist_focused_previous_trigger", "playlist_focused_id_trigger", "playlist_active_next_trigger", "playlist_active_previous_trigger", "playlist_active_id_trigger", "playlist_id_next_trigger", "playlist_id_previous_trigger")
    class Playlists(_message.Message):
        __slots__ = ("playlists",)
        PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
        playlists: _containers.RepeatedCompositeFieldContainer[_proApiV1Playlist_pb2.API_v1_Playlist]
        def __init__(self, playlists: _Optional[_Iterable[_Union[_proApiV1Playlist_pb2.API_v1_Playlist, _Mapping]]] = ...) -> None: ...
    class Playlist(_message.Message):
        __slots__ = ("id", "items")
        ID_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        items: _containers.RepeatedCompositeFieldContainer[_proApiV1MediaPlaylistItem_pb2.API_v1_MediaPlaylistItem]
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_proApiV1MediaPlaylistItem_pb2.API_v1_MediaPlaylistItem, _Mapping]]] = ...) -> None: ...
    class PlaylistUpdate(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FocusedPlaylist(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class ActivePlaylist(_message.Message):
        __slots__ = ("playlist", "item")
        PLAYLIST_FIELD_NUMBER: _ClassVar[int]
        ITEM_FIELD_NUMBER: _ClassVar[int]
        playlist: _proApiV1Identifier_pb2.API_v1_Identifier
        item: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, playlist: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., item: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_NEXT_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_PREVIOUS_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FOCUSED_ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ACTIVE_ID_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_ID_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    playlists: API_v1_Audio_Response.Playlists
    playlist: API_v1_Audio_Response.Playlist
    update: API_v1_Audio_Response.PlaylistUpdate
    playlist_focused: API_v1_Audio_Response.FocusedPlaylist
    playlist_active: API_v1_Audio_Response.ActivePlaylist
    playlist_next_focus: API_v1_Audio_Response.EmptyMessage
    playlist_previous_focus: API_v1_Audio_Response.EmptyMessage
    playlist_active_focus: API_v1_Audio_Response.EmptyMessage
    playlist_id_focus: API_v1_Audio_Response.EmptyMessage
    playlist_focused_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_active_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_id_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_focused_next_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_focused_previous_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_focused_id_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_active_next_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_active_previous_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_active_id_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_id_next_trigger: API_v1_Audio_Response.EmptyMessage
    playlist_id_previous_trigger: API_v1_Audio_Response.EmptyMessage
    def __init__(self, playlists: _Optional[_Union[API_v1_Audio_Response.Playlists, _Mapping]] = ..., playlist: _Optional[_Union[API_v1_Audio_Response.Playlist, _Mapping]] = ..., update: _Optional[_Union[API_v1_Audio_Response.PlaylistUpdate, _Mapping]] = ..., playlist_focused: _Optional[_Union[API_v1_Audio_Response.FocusedPlaylist, _Mapping]] = ..., playlist_active: _Optional[_Union[API_v1_Audio_Response.ActivePlaylist, _Mapping]] = ..., playlist_next_focus: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_previous_focus: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_active_focus: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_id_focus: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_focused_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_active_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_id_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_focused_next_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_focused_previous_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_focused_id_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_active_next_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_active_previous_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_active_id_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_id_next_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ..., playlist_id_previous_trigger: _Optional[_Union[API_v1_Audio_Response.EmptyMessage, _Mapping]] = ...) -> None: ...
