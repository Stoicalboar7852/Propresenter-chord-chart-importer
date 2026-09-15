from workspace.entities import remote_pb2 as _remote_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Notification(_message.Message):
    __slots__ = ("unsubscribe", "workspaces", "collaborators", "syncing")
    class UnsubscribeComplete(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Workspaces(_message.Message):
        __slots__ = ("initialized", "uninitialized", "error")
        class WorkspaceList(_message.Message):
            __slots__ = ("workspaces",)
            WORKSPACES_FIELD_NUMBER: _ClassVar[int]
            workspaces: _containers.RepeatedCompositeFieldContainer[_remote_pb2.Metadata]
            def __init__(self, workspaces: _Optional[_Iterable[_Union[_remote_pb2.Metadata, _Mapping]]] = ...) -> None: ...
        class Uninitialized(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class Error(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        INITIALIZED_FIELD_NUMBER: _ClassVar[int]
        UNINITIALIZED_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        initialized: Notification.Workspaces.WorkspaceList
        uninitialized: Notification.Workspaces.Uninitialized
        error: Notification.Workspaces.Error
        def __init__(self, initialized: _Optional[_Union[Notification.Workspaces.WorkspaceList, _Mapping]] = ..., uninitialized: _Optional[_Union[Notification.Workspaces.Uninitialized, _Mapping]] = ..., error: _Optional[_Union[Notification.Workspaces.Error, _Mapping]] = ...) -> None: ...
    class Collaborators(_message.Message):
        __slots__ = ("online",)
        ONLINE_FIELD_NUMBER: _ClassVar[int]
        online: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, online: _Optional[_Iterable[str]] = ...) -> None: ...
    class Syncing(_message.Message):
        __slots__ = ("paused",)
        class Paused(_message.Message):
            __slots__ = ("until_time_utc", "at_time_utc")
            UNTIL_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
            AT_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
            until_time_utc: int
            at_time_utc: int
            def __init__(self, until_time_utc: _Optional[int] = ..., at_time_utc: _Optional[int] = ...) -> None: ...
        PAUSED_FIELD_NUMBER: _ClassVar[int]
        paused: Notification.Syncing.Paused
        def __init__(self, paused: _Optional[_Union[Notification.Syncing.Paused, _Mapping]] = ...) -> None: ...
    UNSUBSCRIBE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACES_FIELD_NUMBER: _ClassVar[int]
    COLLABORATORS_FIELD_NUMBER: _ClassVar[int]
    SYNCING_FIELD_NUMBER: _ClassVar[int]
    unsubscribe: Notification.UnsubscribeComplete
    workspaces: Notification.Workspaces
    collaborators: Notification.Collaborators
    syncing: Notification.Syncing
    def __init__(self, unsubscribe: _Optional[_Union[Notification.UnsubscribeComplete, _Mapping]] = ..., workspaces: _Optional[_Union[Notification.Workspaces, _Mapping]] = ..., collaborators: _Optional[_Union[Notification.Collaborators, _Mapping]] = ..., syncing: _Optional[_Union[Notification.Syncing, _Mapping]] = ...) -> None: ...
