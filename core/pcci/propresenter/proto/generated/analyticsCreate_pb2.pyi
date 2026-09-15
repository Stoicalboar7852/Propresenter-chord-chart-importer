from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Library(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Library.Source]
        APPLICATION_MENU: _ClassVar[Library.Source]
        LIBRARY_OUTLINE_ADD_BUTTON: _ClassVar[Library.Source]
    UNKNOWN: Library.Source
    APPLICATION_MENU: Library.Source
    LIBRARY_OUTLINE_ADD_BUTTON: Library.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: Library.Source
    def __init__(self, source: _Optional[_Union[Library.Source, str]] = ...) -> None: ...

class Playlist(_message.Message):
    __slots__ = ("source", "type")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[Playlist.Source]
        APPLICATION_MENU: _ClassVar[Playlist.Source]
        LIBRARY_OUTLINE_ADD_BUTTON: _ClassVar[Playlist.Source]
    SOURCE_UNKNOWN: Playlist.Source
    APPLICATION_MENU: Playlist.Source
    LIBRARY_OUTLINE_ADD_BUTTON: Playlist.Source
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[Playlist.Type]
        PRESENTATION: _ClassVar[Playlist.Type]
        PLANNING_CENTER: _ClassVar[Playlist.Type]
        FOLDER: _ClassVar[Playlist.Type]
        TEMPLATE_PLAYLIST: _ClassVar[Playlist.Type]
    TYPE_UNKNOWN: Playlist.Type
    PRESENTATION: Playlist.Type
    PLANNING_CENTER: Playlist.Type
    FOLDER: Playlist.Type
    TEMPLATE_PLAYLIST: Playlist.Type
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    source: Playlist.Source
    type: Playlist.Type
    def __init__(self, source: _Optional[_Union[Playlist.Source, str]] = ..., type: _Optional[_Union[Playlist.Type, str]] = ...) -> None: ...

class Presentation(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Presentation.Source]
        APPLICATION_MENU: _ClassVar[Presentation.Source]
        LIBRARY_OUTLINE_ADD_BUTTON: _ClassVar[Presentation.Source]
        DETAIL_ADD_BUTTON: _ClassVar[Presentation.Source]
        UNLINKED_HEADER: _ClassVar[Presentation.Source]
    UNKNOWN: Presentation.Source
    APPLICATION_MENU: Presentation.Source
    LIBRARY_OUTLINE_ADD_BUTTON: Presentation.Source
    DETAIL_ADD_BUTTON: Presentation.Source
    UNLINKED_HEADER: Presentation.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: Presentation.Source
    def __init__(self, source: _Optional[_Union[Presentation.Source, str]] = ...) -> None: ...

class TemplatePlaylist(_message.Message):
    __slots__ = ("total_item_count", "header_count", "placeholder_count", "presentation_count", "media_count")
    TOTAL_ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    HEADER_COUNT_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_COUNT_FIELD_NUMBER: _ClassVar[int]
    total_item_count: int
    header_count: int
    placeholder_count: int
    presentation_count: int
    media_count: int
    def __init__(self, total_item_count: _Optional[int] = ..., header_count: _Optional[int] = ..., placeholder_count: _Optional[int] = ..., presentation_count: _Optional[int] = ..., media_count: _Optional[int] = ...) -> None: ...
