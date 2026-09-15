from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ready(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class Remote(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Local(_message.Message):
    __slots__ = ("timestamp",)
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    def __init__(self, timestamp: _Optional[int] = ...) -> None: ...

class Intrinsic(_message.Message):
    __slots__ = ("uuid", "kind", "body")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Calendar: _ClassVar[Intrinsic.Kind]
        CCLI: _ClassVar[Intrinsic.Kind]
        ClearGroups: _ClassVar[Intrinsic.Kind]
        Groups: _ClassVar[Intrinsic.Kind]
        KeyMappings: _ClassVar[Intrinsic.Kind]
        Labels: _ClassVar[Intrinsic.Kind]
        Macros: _ClassVar[Intrinsic.Kind]
        Messages: _ClassVar[Intrinsic.Kind]
        Props: _ClassVar[Intrinsic.Kind]
        Stage: _ClassVar[Intrinsic.Kind]
        Timers: _ClassVar[Intrinsic.Kind]
        Workspace: _ClassVar[Intrinsic.Kind]
        LibraryData: _ClassVar[Intrinsic.Kind]
        PlaylistAudio: _ClassVar[Intrinsic.Kind]
        PlaylistLibrary: _ClassVar[Intrinsic.Kind]
        PlaylistMedia: _ClassVar[Intrinsic.Kind]
        PlaylistTemplates: _ClassVar[Intrinsic.Kind]
    Calendar: Intrinsic.Kind
    CCLI: Intrinsic.Kind
    ClearGroups: Intrinsic.Kind
    Groups: Intrinsic.Kind
    KeyMappings: Intrinsic.Kind
    Labels: Intrinsic.Kind
    Macros: Intrinsic.Kind
    Messages: Intrinsic.Kind
    Props: Intrinsic.Kind
    Stage: Intrinsic.Kind
    Timers: Intrinsic.Kind
    Workspace: Intrinsic.Kind
    LibraryData: Intrinsic.Kind
    PlaylistAudio: Intrinsic.Kind
    PlaylistLibrary: Intrinsic.Kind
    PlaylistMedia: Intrinsic.Kind
    PlaylistTemplates: Intrinsic.Kind
    UUID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    kind: Intrinsic.Kind
    body: bytes
    def __init__(self, uuid: _Optional[str] = ..., kind: _Optional[_Union[Intrinsic.Kind, str]] = ..., body: _Optional[bytes] = ...) -> None: ...

class Document(_message.Message):
    __slots__ = ("uuid", "path", "ready", "local", "remote")
    class Kind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESENTATION: _ClassVar[Document.Kind]
        THEME: _ClassVar[Document.Kind]
    PRESENTATION: Document.Kind
    THEME: Document.Kind
    UUID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    LOCAL_FIELD_NUMBER: _ClassVar[int]
    REMOTE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    path: str
    ready: Ready
    local: Local
    remote: Remote
    def __init__(self, uuid: _Optional[str] = ..., path: _Optional[str] = ..., ready: _Optional[_Union[Ready, _Mapping]] = ..., local: _Optional[_Union[Local, _Mapping]] = ..., remote: _Optional[_Union[Remote, _Mapping]] = ...) -> None: ...

class DocumentSet(_message.Message):
    __slots__ = ("intrinsics", "presentations", "themes")
    INTRINSICS_FIELD_NUMBER: _ClassVar[int]
    PRESENTATIONS_FIELD_NUMBER: _ClassVar[int]
    THEMES_FIELD_NUMBER: _ClassVar[int]
    intrinsics: _containers.RepeatedCompositeFieldContainer[Intrinsic]
    presentations: _containers.RepeatedCompositeFieldContainer[Document]
    themes: _containers.RepeatedCompositeFieldContainer[Document]
    def __init__(self, intrinsics: _Optional[_Iterable[_Union[Intrinsic, _Mapping]]] = ..., presentations: _Optional[_Iterable[_Union[Document, _Mapping]]] = ..., themes: _Optional[_Iterable[_Union[Document, _Mapping]]] = ...) -> None: ...
