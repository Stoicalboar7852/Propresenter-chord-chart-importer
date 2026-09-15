from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResolvedFeatureFlags(_message.Message):
    __slots__ = ("content_store_staging_enabled", "staging_api_endpoint_enabled", "pro_content_staging_enabled", "core_networkapi_playlist", "core_networkapi_presentation", "core_client_sync", "hdr_rendering_enabled", "server_driven_feature_flags")
    CONTENT_STORE_STAGING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STAGING_API_ENDPOINT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PRO_CONTENT_STAGING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CORE_NETWORKAPI_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    CORE_NETWORKAPI_PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    CORE_CLIENT_SYNC_FIELD_NUMBER: _ClassVar[int]
    HDR_RENDERING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SERVER_DRIVEN_FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    content_store_staging_enabled: bool
    staging_api_endpoint_enabled: bool
    pro_content_staging_enabled: bool
    core_networkapi_playlist: bool
    core_networkapi_presentation: bool
    core_client_sync: bool
    hdr_rendering_enabled: bool
    server_driven_feature_flags: bool
    def __init__(self, content_store_staging_enabled: _Optional[bool] = ..., staging_api_endpoint_enabled: _Optional[bool] = ..., pro_content_staging_enabled: _Optional[bool] = ..., core_networkapi_playlist: _Optional[bool] = ..., core_networkapi_presentation: _Optional[bool] = ..., core_client_sync: _Optional[bool] = ..., hdr_rendering_enabled: _Optional[bool] = ..., server_driven_feature_flags: _Optional[bool] = ...) -> None: ...
