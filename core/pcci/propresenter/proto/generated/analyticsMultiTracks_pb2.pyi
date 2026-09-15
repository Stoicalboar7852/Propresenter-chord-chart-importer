from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISABLED: _ClassVar[Status]
    CANCELLED: _ClassVar[Status]
    ACTIVE: _ClassVar[Status]
DISABLED: Status
CANCELLED: Status
ACTIVE: Status

class Startup(_message.Message):
    __slots__ = ("chart_pro", "propresenter_addon")
    CHART_PRO_FIELD_NUMBER: _ClassVar[int]
    PROPRESENTER_ADDON_FIELD_NUMBER: _ClassVar[int]
    chart_pro: Status
    propresenter_addon: Status
    def __init__(self, chart_pro: _Optional[_Union[Status, str]] = ..., propresenter_addon: _Optional[_Union[Status, str]] = ...) -> None: ...

class Import(_message.Message):
    __slots__ = ("chart_pro", "propresenter_addon", "charts_automation", "lines")
    CHART_PRO_FIELD_NUMBER: _ClassVar[int]
    PROPRESENTER_ADDON_FIELD_NUMBER: _ClassVar[int]
    CHARTS_AUTOMATION_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    chart_pro: Status
    propresenter_addon: Status
    charts_automation: bool
    lines: int
    def __init__(self, chart_pro: _Optional[_Union[Status, str]] = ..., propresenter_addon: _Optional[_Union[Status, str]] = ..., charts_automation: _Optional[bool] = ..., lines: _Optional[int] = ...) -> None: ...
