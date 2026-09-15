from google.protobuf import wrappers_pb2 as _wrappers_pb2
import proApiV1Color_pb2 as _proApiV1Color_pb2
import proApiV1ContentType_pb2 as _proApiV1ContentType_pb2
import proApiV1Identifier_pb2 as _proApiV1Identifier_pb2
import proApiV1Size_pb2 as _proApiV1Size_pb2
import proApiV1TimelineOperation_pb2 as _proApiV1TimelineOperation_pb2
import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class API_v1_SlideIndex(_message.Message):
    __slots__ = ("index", "presentation_id", "total_cues", "remaining_cues")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CUES_FIELD_NUMBER: _ClassVar[int]
    REMAINING_CUES_FIELD_NUMBER: _ClassVar[int]
    index: int
    presentation_id: _proApiV1Identifier_pb2.API_v1_Identifier
    total_cues: int
    remaining_cues: int
    def __init__(self, index: _Optional[int] = ..., presentation_id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., total_cues: _Optional[int] = ..., remaining_cues: _Optional[int] = ...) -> None: ...

class API_v1_Presentation(_message.Message):
    __slots__ = ("id", "groups", "has_timeline", "presentation_path", "destination", "arrangements", "current_arrangement", "type", "is_authorized", "total_cues")
    class Destination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        presentation: _ClassVar[API_v1_Presentation.Destination]
        announcements: _ClassVar[API_v1_Presentation.Destination]
    presentation: API_v1_Presentation.Destination
    announcements: API_v1_Presentation.Destination
    class SlideGroup(_message.Message):
        __slots__ = ("name", "color", "slides", "uuid")
        class Slide(_message.Message):
            __slots__ = ("enabled", "notes", "text", "label", "size")
            ENABLED_FIELD_NUMBER: _ClassVar[int]
            NOTES_FIELD_NUMBER: _ClassVar[int]
            TEXT_FIELD_NUMBER: _ClassVar[int]
            LABEL_FIELD_NUMBER: _ClassVar[int]
            SIZE_FIELD_NUMBER: _ClassVar[int]
            enabled: bool
            notes: str
            text: str
            label: str
            size: _proApiV1Size_pb2.API_v1_Size
            def __init__(self, enabled: _Optional[bool] = ..., notes: _Optional[str] = ..., text: _Optional[str] = ..., label: _Optional[str] = ..., size: _Optional[_Union[_proApiV1Size_pb2.API_v1_Size, _Mapping]] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        SLIDES_FIELD_NUMBER: _ClassVar[int]
        UUID_FIELD_NUMBER: _ClassVar[int]
        name: str
        color: _proApiV1Color_pb2.API_v1_Color
        slides: _containers.RepeatedCompositeFieldContainer[API_v1_Presentation.SlideGroup.Slide]
        uuid: str
        def __init__(self, name: _Optional[str] = ..., color: _Optional[_Union[_proApiV1Color_pb2.API_v1_Color, _Mapping]] = ..., slides: _Optional[_Iterable[_Union[API_v1_Presentation.SlideGroup.Slide, _Mapping]]] = ..., uuid: _Optional[str] = ...) -> None: ...
    class Arrangement(_message.Message):
        __slots__ = ("id", "groups", "total_cues")
        ID_FIELD_NUMBER: _ClassVar[int]
        GROUPS_FIELD_NUMBER: _ClassVar[int]
        TOTAL_CUES_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        groups: _containers.RepeatedScalarFieldContainer[str]
        total_cues: int
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., groups: _Optional[_Iterable[str]] = ..., total_cues: _Optional[int] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    HAS_TIMELINE_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_PATH_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    ARRANGEMENTS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ARRANGEMENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTHORIZED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CUES_FIELD_NUMBER: _ClassVar[int]
    id: _proApiV1Identifier_pb2.API_v1_Identifier
    groups: _containers.RepeatedCompositeFieldContainer[API_v1_Presentation.SlideGroup]
    has_timeline: bool
    presentation_path: str
    destination: API_v1_Presentation.Destination
    arrangements: _containers.RepeatedCompositeFieldContainer[API_v1_Presentation.Arrangement]
    current_arrangement: str
    type: str
    is_authorized: bool
    total_cues: int
    def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[API_v1_Presentation.SlideGroup, _Mapping]]] = ..., has_timeline: _Optional[bool] = ..., presentation_path: _Optional[str] = ..., destination: _Optional[_Union[API_v1_Presentation.Destination, str]] = ..., arrangements: _Optional[_Iterable[_Union[API_v1_Presentation.Arrangement, _Mapping]]] = ..., current_arrangement: _Optional[str] = ..., type: _Optional[str] = ..., is_authorized: _Optional[bool] = ..., total_cues: _Optional[int] = ...) -> None: ...

class API_v1_Presentation_Request(_message.Message):
    __slots__ = ("active", "focused", "slide_index", "chord_chart", "chord_chart_updates", "presentation", "delete_presentation", "timeline_operation", "active_presentation_timeline_operation", "focused_presentation_timeline_operation", "active_presentation_timeline_status", "focused_presentation_timeline_status", "thumbnail", "focus", "trigger")
    class Active(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class SlideIndex(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ChordChart(_message.Message):
        __slots__ = ("quality",)
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        quality: int
        def __init__(self, quality: _Optional[int] = ...) -> None: ...
    class ChordChartUpdates(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Presentation(_message.Message):
        __slots__ = ("uuid",)
        UUID_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ...) -> None: ...
    class DeletePresentation(_message.Message):
        __slots__ = ("uuid",)
        UUID_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ...) -> None: ...
    class TimelineOperation(_message.Message):
        __slots__ = ("uuid", "operation")
        UUID_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class ActivePresentationTimelineOperation(_message.Message):
        __slots__ = ("operation",)
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class FocusedPresentationTimelineOperation(_message.Message):
        __slots__ = ("operation",)
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        operation: _proApiV1TimelineOperation_pb2.API_v1_TimelineOperation
        def __init__(self, operation: _Optional[_Union[_proApiV1TimelineOperation_pb2.API_v1_TimelineOperation, str]] = ...) -> None: ...
    class ActivePresentationTimelineStatus(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FocusedPresentationTimelineStatus(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Thumbnail(_message.Message):
        __slots__ = ("uuid", "cue_index", "quality", "content_type")
        UUID_FIELD_NUMBER: _ClassVar[int]
        CUE_INDEX_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        uuid: _uuid_pb2.UUID
        cue_index: int
        quality: int
        content_type: _proApiV1ContentType_pb2.API_v1_ContentType
        def __init__(self, uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., cue_index: _Optional[int] = ..., quality: _Optional[int] = ..., content_type: _Optional[_Union[_proApiV1ContentType_pb2.API_v1_ContentType, str]] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FocusMessage(_message.Message):
        __slots__ = ("next", "previous", "active", "uuid")
        NEXT_FIELD_NUMBER: _ClassVar[int]
        PREVIOUS_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        UUID_FIELD_NUMBER: _ClassVar[int]
        next: API_v1_Presentation_Request.EmptyMessage
        previous: API_v1_Presentation_Request.EmptyMessage
        active: API_v1_Presentation_Request.EmptyMessage
        uuid: str
        def __init__(self, next: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., previous: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., active: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., uuid: _Optional[str] = ...) -> None: ...
    class TriggerMessage(_message.Message):
        __slots__ = ("focused", "active", "uuid", "first", "next", "previous", "index", "group")
        FOCUSED_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        UUID_FIELD_NUMBER: _ClassVar[int]
        FIRST_FIELD_NUMBER: _ClassVar[int]
        NEXT_FIELD_NUMBER: _ClassVar[int]
        PREVIOUS_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        GROUP_FIELD_NUMBER: _ClassVar[int]
        focused: API_v1_Presentation_Request.EmptyMessage
        active: API_v1_Presentation_Request.EmptyMessage
        uuid: _wrappers_pb2.StringValue
        first: API_v1_Presentation_Request.EmptyMessage
        next: API_v1_Presentation_Request.EmptyMessage
        previous: API_v1_Presentation_Request.EmptyMessage
        index: _wrappers_pb2.UInt32Value
        group: _wrappers_pb2.StringValue
        def __init__(self, focused: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., active: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., uuid: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., first: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., next: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., previous: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., index: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., group: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_FIELD_NUMBER: _ClassVar[int]
    SLIDE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CHORD_CHART_FIELD_NUMBER: _ClassVar[int]
    CHORD_CHART_UPDATES_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    DELETE_PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PRESENTATION_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PRESENTATION_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    FOCUS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    active: API_v1_Presentation_Request.Active
    focused: API_v1_Presentation_Request.EmptyMessage
    slide_index: API_v1_Presentation_Request.SlideIndex
    chord_chart: API_v1_Presentation_Request.ChordChart
    chord_chart_updates: API_v1_Presentation_Request.ChordChartUpdates
    presentation: API_v1_Presentation_Request.Presentation
    delete_presentation: API_v1_Presentation_Request.DeletePresentation
    timeline_operation: API_v1_Presentation_Request.TimelineOperation
    active_presentation_timeline_operation: API_v1_Presentation_Request.ActivePresentationTimelineOperation
    focused_presentation_timeline_operation: API_v1_Presentation_Request.FocusedPresentationTimelineOperation
    active_presentation_timeline_status: API_v1_Presentation_Request.ActivePresentationTimelineStatus
    focused_presentation_timeline_status: API_v1_Presentation_Request.FocusedPresentationTimelineStatus
    thumbnail: API_v1_Presentation_Request.Thumbnail
    focus: API_v1_Presentation_Request.FocusMessage
    trigger: API_v1_Presentation_Request.TriggerMessage
    def __init__(self, active: _Optional[_Union[API_v1_Presentation_Request.Active, _Mapping]] = ..., focused: _Optional[_Union[API_v1_Presentation_Request.EmptyMessage, _Mapping]] = ..., slide_index: _Optional[_Union[API_v1_Presentation_Request.SlideIndex, _Mapping]] = ..., chord_chart: _Optional[_Union[API_v1_Presentation_Request.ChordChart, _Mapping]] = ..., chord_chart_updates: _Optional[_Union[API_v1_Presentation_Request.ChordChartUpdates, _Mapping]] = ..., presentation: _Optional[_Union[API_v1_Presentation_Request.Presentation, _Mapping]] = ..., delete_presentation: _Optional[_Union[API_v1_Presentation_Request.DeletePresentation, _Mapping]] = ..., timeline_operation: _Optional[_Union[API_v1_Presentation_Request.TimelineOperation, _Mapping]] = ..., active_presentation_timeline_operation: _Optional[_Union[API_v1_Presentation_Request.ActivePresentationTimelineOperation, _Mapping]] = ..., focused_presentation_timeline_operation: _Optional[_Union[API_v1_Presentation_Request.FocusedPresentationTimelineOperation, _Mapping]] = ..., active_presentation_timeline_status: _Optional[_Union[API_v1_Presentation_Request.ActivePresentationTimelineStatus, _Mapping]] = ..., focused_presentation_timeline_status: _Optional[_Union[API_v1_Presentation_Request.FocusedPresentationTimelineStatus, _Mapping]] = ..., thumbnail: _Optional[_Union[API_v1_Presentation_Request.Thumbnail, _Mapping]] = ..., focus: _Optional[_Union[API_v1_Presentation_Request.FocusMessage, _Mapping]] = ..., trigger: _Optional[_Union[API_v1_Presentation_Request.TriggerMessage, _Mapping]] = ...) -> None: ...

class API_v1_Presentation_Response(_message.Message):
    __slots__ = ("active", "slide_index", "chord_chart", "chord_chart_update", "presentation", "delete_presentation", "trigger_presentation", "trigger_cue", "timeline_operation", "active_presentation_timeline_operation", "focused_presentation_timeline_operation", "active_presentation_timeline_status", "focused_presentation_timeline_status", "thumbnail", "focused", "focus", "trigger")
    class Active(_message.Message):
        __slots__ = ("presentation",)
        PRESENTATION_FIELD_NUMBER: _ClassVar[int]
        presentation: API_v1_Presentation
        def __init__(self, presentation: _Optional[_Union[API_v1_Presentation, _Mapping]] = ...) -> None: ...
    class SlideIndex(_message.Message):
        __slots__ = ("presentation_index",)
        PRESENTATION_INDEX_FIELD_NUMBER: _ClassVar[int]
        presentation_index: API_v1_SlideIndex
        def __init__(self, presentation_index: _Optional[_Union[API_v1_SlideIndex, _Mapping]] = ...) -> None: ...
    class ChordChart(_message.Message):
        __slots__ = ("chord_chart",)
        CHORD_CHART_FIELD_NUMBER: _ClassVar[int]
        chord_chart: bytes
        def __init__(self, chord_chart: _Optional[bytes] = ...) -> None: ...
    class ChordChartUpdates(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Presentation(_message.Message):
        __slots__ = ("presentation",)
        PRESENTATION_FIELD_NUMBER: _ClassVar[int]
        presentation: API_v1_Presentation
        def __init__(self, presentation: _Optional[_Union[API_v1_Presentation, _Mapping]] = ...) -> None: ...
    class DeletePresentation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class TriggerPresentation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class TriggerCue(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class TimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActivePresentationTimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FocusedPresentationTimelineOperation(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ActivePresentationTimelineStatus(_message.Message):
        __slots__ = ("is_running", "current_time")
        IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        is_running: bool
        current_time: float
        def __init__(self, is_running: _Optional[bool] = ..., current_time: _Optional[float] = ...) -> None: ...
    class FocusedPresentationTimelineStatus(_message.Message):
        __slots__ = ("is_running", "current_time")
        IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        is_running: bool
        current_time: float
        def __init__(self, is_running: _Optional[bool] = ..., current_time: _Optional[float] = ...) -> None: ...
    class Thumbnail(_message.Message):
        __slots__ = ("data", "content_type")
        DATA_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        data: bytes
        content_type: _proApiV1ContentType_pb2.API_v1_ContentType
        def __init__(self, data: _Optional[bytes] = ..., content_type: _Optional[_Union[_proApiV1ContentType_pb2.API_v1_ContentType, str]] = ...) -> None: ...
    class Focused(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: _proApiV1Identifier_pb2.API_v1_Identifier
        def __init__(self, id: _Optional[_Union[_proApiV1Identifier_pb2.API_v1_Identifier, _Mapping]] = ...) -> None: ...
    class EmptyMessage(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SLIDE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CHORD_CHART_FIELD_NUMBER: _ClassVar[int]
    CHORD_CHART_UPDATE_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    DELETE_PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_CUE_FIELD_NUMBER: _ClassVar[int]
    TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PRESENTATION_TIMELINE_OPERATION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PRESENTATION_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_PRESENTATION_TIMELINE_STATUS_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    FOCUSED_FIELD_NUMBER: _ClassVar[int]
    FOCUS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    active: API_v1_Presentation_Response.Active
    slide_index: API_v1_Presentation_Response.SlideIndex
    chord_chart: API_v1_Presentation_Response.ChordChart
    chord_chart_update: API_v1_Presentation_Response.ChordChartUpdates
    presentation: API_v1_Presentation_Response.Presentation
    delete_presentation: API_v1_Presentation_Response.DeletePresentation
    trigger_presentation: API_v1_Presentation_Response.TriggerPresentation
    trigger_cue: API_v1_Presentation_Response.TriggerCue
    timeline_operation: API_v1_Presentation_Response.TimelineOperation
    active_presentation_timeline_operation: API_v1_Presentation_Response.ActivePresentationTimelineOperation
    focused_presentation_timeline_operation: API_v1_Presentation_Response.FocusedPresentationTimelineOperation
    active_presentation_timeline_status: API_v1_Presentation_Response.ActivePresentationTimelineStatus
    focused_presentation_timeline_status: API_v1_Presentation_Response.FocusedPresentationTimelineStatus
    thumbnail: API_v1_Presentation_Response.Thumbnail
    focused: API_v1_Presentation_Response.Focused
    focus: API_v1_Presentation_Response.EmptyMessage
    trigger: API_v1_Presentation_Response.EmptyMessage
    def __init__(self, active: _Optional[_Union[API_v1_Presentation_Response.Active, _Mapping]] = ..., slide_index: _Optional[_Union[API_v1_Presentation_Response.SlideIndex, _Mapping]] = ..., chord_chart: _Optional[_Union[API_v1_Presentation_Response.ChordChart, _Mapping]] = ..., chord_chart_update: _Optional[_Union[API_v1_Presentation_Response.ChordChartUpdates, _Mapping]] = ..., presentation: _Optional[_Union[API_v1_Presentation_Response.Presentation, _Mapping]] = ..., delete_presentation: _Optional[_Union[API_v1_Presentation_Response.DeletePresentation, _Mapping]] = ..., trigger_presentation: _Optional[_Union[API_v1_Presentation_Response.TriggerPresentation, _Mapping]] = ..., trigger_cue: _Optional[_Union[API_v1_Presentation_Response.TriggerCue, _Mapping]] = ..., timeline_operation: _Optional[_Union[API_v1_Presentation_Response.TimelineOperation, _Mapping]] = ..., active_presentation_timeline_operation: _Optional[_Union[API_v1_Presentation_Response.ActivePresentationTimelineOperation, _Mapping]] = ..., focused_presentation_timeline_operation: _Optional[_Union[API_v1_Presentation_Response.FocusedPresentationTimelineOperation, _Mapping]] = ..., active_presentation_timeline_status: _Optional[_Union[API_v1_Presentation_Response.ActivePresentationTimelineStatus, _Mapping]] = ..., focused_presentation_timeline_status: _Optional[_Union[API_v1_Presentation_Response.FocusedPresentationTimelineStatus, _Mapping]] = ..., thumbnail: _Optional[_Union[API_v1_Presentation_Response.Thumbnail, _Mapping]] = ..., focused: _Optional[_Union[API_v1_Presentation_Response.Focused, _Mapping]] = ..., focus: _Optional[_Union[API_v1_Presentation_Response.EmptyMessage, _Mapping]] = ..., trigger: _Optional[_Union[API_v1_Presentation_Response.EmptyMessage, _Mapping]] = ...) -> None: ...
