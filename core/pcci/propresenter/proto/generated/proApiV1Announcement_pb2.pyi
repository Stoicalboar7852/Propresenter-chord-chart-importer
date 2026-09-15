import proApiV1Presentation_pb2 as _proApiV1Presentation_pb2
import proApiV1TimelineOperation_pb2 as _proApiV1TimelineOperation_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_Announcement_Request(_message.Message):
    __slots__ = ("active_timeline_operation", "active_timeline_status", "active", "slide_index", "active_focus", "active_trigger", "active_next_trigger", "active_previous_trigger", "active_index_trigger")
    class ActiveTimelineOperation(_message.Message):
        __slots__ = ("operation",)
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class ActiveTimelineStatus(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Active(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class AnnouncementIndex(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveFocus(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveNextTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActivePreviousTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveIndexTrigger(_message.Message):
        __slots__ = ("index",)
        INDEX_FIELD_NUMBER: _ClassVar[int]
        index: int
        def __init__(self, index: _Optional[int] = ...) -> None: ...
    ACTIVE_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SLIDE_INDEX_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    active_timeline_operation: API_v1_Announcement_Request.ActiveTimelineOperation
    active_timeline_status: API_v1_Announcement_Request.ActiveTimelineStatus
    active: API_v1_Announcement_Request.Active
    slide_index: API_v1_Announcement_Request.AnnouncementIndex
    active_focus: API_v1_Announcement_Request.ActiveFocus
    active_trigger: API_v1_Announcement_Request.ActiveTrigger
    active_next_trigger: API_v1_Announcement_Request.ActiveNextTrigger
    active_previous_trigger: API_v1_Announcement_Request.ActivePreviousTrigger
    active_index_trigger: API_v1_Announcement_Request.ActiveIndexTrigger
    def __init__(self, active_timeline_operation: _Optional[_Union[API_v1_Announcement_Request.ActiveTimelineOperation, _Mapping]] = ..., active_timeline_status: _Optional[_Union[API_v1_Announcement_Request.ActiveTimelineStatus, _Mapping]] = ..., active: _Optional[_Union[API_v1_Announcement_Request.Active, _Mapping]] = ..., slide_index: _Optional[_Union[API_v1_Announcement_Request.AnnouncementIndex, _Mapping]] = ..., active_focus: _Optional[_Union[API_v1_Announcement_Request.ActiveFocus, _Mapping]] = ..., active_trigger: _Optional[_Union[API_v1_Announcement_Request.ActiveTrigger, _Mapping]] = ..., active_next_trigger: _Optional[_Union[API_v1_Announcement_Request.ActiveNextTrigger, _Mapping]] = ..., active_previous_trigger: _Optional[_Union[API_v1_Announcement_Request.ActivePreviousTrigger, _Mapping]] = ..., active_index_trigger: _Optional[_Union[API_v1_Announcement_Request.ActiveIndexTrigger, _Mapping]] = ...) -> None: ...

class API_v1_Announcement_Response(_message.Message):
    __slots__ = ("active_timeline_operation", "active_timeline_status", "active", "slide_index", "active_focus", "active_trigger", "active_next_trigger", "active_previous_trigger", "active_index_trigger")
    class ActiveTimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveTimelineStatus(_message.Message):
        __slots__ = ("is_running", "current_time")
        IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        is_running: bool
        current_time: float
        def __init__(self, is_running: _Optional[bool] = ..., current_time: _Optional[float] = ...) -> None: ...
    class Active(_message.Message):
        __slots__ = ("announcement",)
        ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
        announcement: _proApiV1Presentation_pb2.API_v1_Presentation
        def __init__(self, announcement: _Optional[_Union[_proApiV1Presentation_pb2.API_v1_Presentation, _Mapping]] = ...) -> None: ...
    class SlideIndex(_message.Message):
        __slots__ = ("announcement_index",)
        ANNOUNCEMENT_INDEX_FIELD_NUMBER: _ClassVar[int]
        announcement_index: _proApiV1Presentation_pb2.API_v1_SlideIndex
        def __init__(self, announcement_index: _Optional[_Union[_proApiV1Presentation_pb2.API_v1_SlideIndex, _Mapping]] = ...) -> None: ...
    class ActiveFocus(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveNextTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActivePreviousTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActiveIndexTrigger(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ACTIVE_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SLIDE_INDEX_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FOCUS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_NEXT_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PREVIOUS_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_INDEX_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    active_timeline_operation: API_v1_Announcement_Response.ActiveTimelineOperation
    active_timeline_status: API_v1_Announcement_Response.ActiveTimelineStatus
    active: API_v1_Announcement_Response.Active
    slide_index: API_v1_Announcement_Response.SlideIndex
    active_focus: API_v1_Announcement_Response.ActiveFocus
    active_trigger: API_v1_Announcement_Response.ActiveTrigger
    active_next_trigger: API_v1_Announcement_Response.ActiveNextTrigger
    active_previous_trigger: API_v1_Announcement_Response.ActivePreviousTrigger
    active_index_trigger: API_v1_Announcement_Response.ActiveIndexTrigger
    def __init__(self, active_timeline_operation: _Optional[_Union[API_v1_Announcement_Response.ActiveTimelineOperation, _Mapping]] = ..., active_timeline_status: _Optional[_Union[API_v1_Announcement_Response.ActiveTimelineStatus, _Mapping]] = ..., active: _Optional[_Union[API_v1_Announcement_Response.Active, _Mapping]] = ..., slide_index: _Optional[_Union[API_v1_Announcement_Response.SlideIndex, _Mapping]] = ..., active_focus: _Optional[_Union[API_v1_Announcement_Response.ActiveFocus, _Mapping]] = ..., active_trigger: _Optional[_Union[API_v1_Announcement_Response.ActiveTrigger, _Mapping]] = ..., active_next_trigger: _Optional[_Union[API_v1_Announcement_Response.ActiveNextTrigger, _Mapping]] = ..., active_previous_trigger: _Optional[_Union[API_v1_Announcement_Response.ActivePreviousTrigger, _Mapping]] = ..., active_index_trigger: _Optional[_Union[API_v1_Announcement_Response.ActiveIndexTrigger, _Mapping]] = ...) -> None: ...
