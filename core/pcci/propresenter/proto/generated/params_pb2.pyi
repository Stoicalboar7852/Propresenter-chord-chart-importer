import v1_helper_common_pb2 as _v1_helper_common_pb2
import v2_helper_common_pb2 as _v2_helper_common_pb2
import feature_flags_pb2 as _feature_flags_pb2
from document import bootstrap_pb2 as _bootstrap_pb2
from workspace import bootstrap_pb2 as _bootstrap_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProductInformation(_message.Message):
    __slots__ = ("product_name", "major_version", "minor_version", "patch_version", "build_number", "build_date")
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    MINOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PATCH_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BUILD_DATE_FIELD_NUMBER: _ClassVar[int]
    product_name: str
    major_version: str
    minor_version: str
    patch_version: str
    build_number: str
    build_date: int
    def __init__(self, product_name: _Optional[str] = ..., major_version: _Optional[str] = ..., minor_version: _Optional[str] = ..., patch_version: _Optional[str] = ..., build_number: _Optional[str] = ..., build_date: _Optional[int] = ...) -> None: ...

class ApplicationParams(_message.Message):
    __slots__ = ("product_info", "enabled_features", "peer_id")
    PRODUCT_INFO_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FEATURES_FIELD_NUMBER: _ClassVar[int]
    PEER_ID_FIELD_NUMBER: _ClassVar[int]
    product_info: ProductInformation
    enabled_features: _containers.RepeatedScalarFieldContainer[str]
    peer_id: int
    def __init__(self, product_info: _Optional[_Union[ProductInformation, _Mapping]] = ..., enabled_features: _Optional[_Iterable[str]] = ..., peer_id: _Optional[int] = ...) -> None: ...

class ApplicationStartParams(_message.Message):
    __slots__ = ("application", "media_v1", "media", "feature_flags", "registration", "document", "workspace")
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    MEDIA_V1_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    application: ApplicationParams
    media_v1: _v1_helper_common_pb2.CreationOption
    media: _v2_helper_common_pb2.CreationOption
    feature_flags: _feature_flags_pb2.CreationOption
    registration: RegistrationCreationOption
    document: _bootstrap_pb2.CreationOption
    workspace: _bootstrap_pb2_1.CreationOption
    def __init__(self, application: _Optional[_Union[ApplicationParams, _Mapping]] = ..., media_v1: _Optional[_Union[_v1_helper_common_pb2.CreationOption, _Mapping]] = ..., media: _Optional[_Union[_v2_helper_common_pb2.CreationOption, _Mapping]] = ..., feature_flags: _Optional[_Union[_feature_flags_pb2.CreationOption, _Mapping]] = ..., registration: _Optional[_Union[RegistrationCreationOption, _Mapping]] = ..., document: _Optional[_Union[_bootstrap_pb2.CreationOption, _Mapping]] = ..., workspace: _Optional[_Union[_bootstrap_pb2_1.CreationOption, _Mapping]] = ...) -> None: ...

class RegistrationCreationOption(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Shutdown(_message.Message):
    __slots__ = ("ok", "error")
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ok: str
    error: str
    def __init__(self, ok: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...
