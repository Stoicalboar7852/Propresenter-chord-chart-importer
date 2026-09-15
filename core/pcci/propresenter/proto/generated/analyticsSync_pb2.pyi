from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WebSocketFailureReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[WebSocketFailureReason]
    AUTHENTICATION: _ClassVar[WebSocketFailureReason]
    TIMEOUT: _ClassVar[WebSocketFailureReason]
    NO_INTERNET: _ClassVar[WebSocketFailureReason]
    SERVER_ERROR: _ClassVar[WebSocketFailureReason]
UNKNOWN: WebSocketFailureReason
AUTHENTICATION: WebSocketFailureReason
TIMEOUT: WebSocketFailureReason
NO_INTERNET: WebSocketFailureReason
SERVER_ERROR: WebSocketFailureReason

class Local(_message.Message):
    __slots__ = ("sync_type", "include_library", "include_media", "include_playlists", "include_themes", "include_support_files", "replace_files")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UP: _ClassVar[Local.Type]
        DOWN: _ClassVar[Local.Type]
    UP: Local.Type
    DOWN: Local.Type
    SYNC_TYPE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_LIBRARY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MEDIA_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_THEMES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SUPPORT_FILES_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FILES_FIELD_NUMBER: _ClassVar[int]
    sync_type: Local.Type
    include_library: bool
    include_media: bool
    include_playlists: bool
    include_themes: bool
    include_support_files: bool
    replace_files: bool
    def __init__(self, sync_type: _Optional[_Union[Local.Type, str]] = ..., include_library: _Optional[bool] = ..., include_media: _Optional[bool] = ..., include_playlists: _Optional[bool] = ..., include_themes: _Optional[bool] = ..., include_support_files: _Optional[bool] = ..., replace_files: _Optional[bool] = ...) -> None: ...

class WebSocketConnectionFailed(_message.Message):
    __slots__ = ("reason", "url", "error_description")
    REASON_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    ERROR_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    reason: WebSocketFailureReason
    url: str
    error_description: str
    def __init__(self, reason: _Optional[_Union[WebSocketFailureReason, str]] = ..., url: _Optional[str] = ..., error_description: _Optional[str] = ...) -> None: ...
