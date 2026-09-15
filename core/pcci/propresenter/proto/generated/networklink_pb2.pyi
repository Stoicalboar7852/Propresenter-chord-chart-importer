import applicationInfo_pb2 as _applicationInfo_pb2
import customOptions_pb2 as _customOptions_pb2
import proApi_pb2 as _proApi_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NetworkLinkDocument(_message.Message):
    __slots__ = ("group_info", "application_info", "enabled")
    GROUP_INFO_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_INFO_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    group_info: _proApi_pb2.ProLink.GroupDefinition
    application_info: _applicationInfo_pb2.ApplicationInfo
    enabled: bool
    def __init__(self, group_info: _Optional[_Union[_proApi_pb2.ProLink.GroupDefinition, _Mapping]] = ..., application_info: _Optional[_Union[_applicationInfo_pb2.ApplicationInfo, _Mapping]] = ..., enabled: _Optional[bool] = ...) -> None: ...

class NetworkLinkStatus(_message.Message):
    __slots__ = ("status_pairs",)
    class LinkedClientInformation(_message.Message):
        __slots__ = ("platform", "os_version", "version", "description")
        PLATFORM_FIELD_NUMBER: _ClassVar[int]
        OS_VERSION_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        platform: _applicationInfo_pb2.ApplicationInfo.Platform
        os_version: str
        version: str
        description: str
        def __init__(self, platform: _Optional[_Union[_applicationInfo_pb2.ApplicationInfo.Platform, str]] = ..., os_version: _Optional[str] = ..., version: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...
    class StatusPair(_message.Message):
        __slots__ = ("ip_address", "port", "linked_client_information")
        IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        LINKED_CLIENT_INFORMATION_FIELD_NUMBER: _ClassVar[int]
        ip_address: str
        port: int
        linked_client_information: NetworkLinkStatus.LinkedClientInformation
        def __init__(self, ip_address: _Optional[str] = ..., port: _Optional[int] = ..., linked_client_information: _Optional[_Union[NetworkLinkStatus.LinkedClientInformation, _Mapping]] = ...) -> None: ...
    STATUS_PAIRS_FIELD_NUMBER: _ClassVar[int]
    status_pairs: _containers.RepeatedCompositeFieldContainer[NetworkLinkStatus.StatusPair]
    def __init__(self, status_pairs: _Optional[_Iterable[_Union[NetworkLinkStatus.StatusPair, _Mapping]]] = ...) -> None: ...
