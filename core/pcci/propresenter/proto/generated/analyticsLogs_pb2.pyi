from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Field(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ID: _ClassVar[Field]
    NAME: _ClassVar[Field]
    PATH: _ClassVar[Field]

class ConflictType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DUPLICATE_ID: _ClassVar[ConflictType]
    DUPLICATE_NAME: _ClassVar[ConflictType]
    DUPLICATE_PATH: _ClassVar[ConflictType]
    DOCUMENT_NOT_FOUND: _ClassVar[ConflictType]
    DOCUMENT_ALREADY_DELETED: _ClassVar[ConflictType]
    CONCURRENT_MODIFICATION: _ClassVar[ConflictType]

class ResyncCause(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WORKSPACE: _ClassVar[ResyncCause]
    SYNC: _ClassVar[ResyncCause]

class DiffApplicationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SUCCESS: _ClassVar[DiffApplicationResult]
    FAILURE: _ClassVar[DiffApplicationResult]
    AWAITING_OTHER_CHANGES: _ClassVar[DiffApplicationResult]

class LogSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIENT: _ClassVar[LogSource]
    CORE: _ClassVar[LogSource]
ID: Field
NAME: Field
PATH: Field
DUPLICATE_ID: ConflictType
DUPLICATE_NAME: ConflictType
DUPLICATE_PATH: ConflictType
DOCUMENT_NOT_FOUND: ConflictType
DOCUMENT_ALREADY_DELETED: ConflictType
CONCURRENT_MODIFICATION: ConflictType
WORKSPACE: ResyncCause
SYNC: ResyncCause
SUCCESS: DiffApplicationResult
FAILURE: DiffApplicationResult
AWAITING_OTHER_CHANGES: DiffApplicationResult
CLIENT: LogSource
CORE: LogSource

class LogError(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ...) -> None: ...

class LogWorkspacesPublished(_message.Message):
    __slots__ = ("metadata", "workspace_identifiers")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    workspace_identifiers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., workspace_identifiers: _Optional[_Iterable[str]] = ...) -> None: ...

class LogCollaboratorsPublished(_message.Message):
    __slots__ = ("metadata", "collaborator_names")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    COLLABORATOR_NAMES_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    collaborator_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., collaborator_names: _Optional[_Iterable[str]] = ...) -> None: ...

class LogDocumentUploaded(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ...) -> None: ...

class LogDocumentDownloaded(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ...) -> None: ...

class LogDiffPushed(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name", "diff_metadata", "from_version_vector")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DIFF_METADATA_FIELD_NUMBER: _ClassVar[int]
    FROM_VERSION_VECTOR_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    diff_metadata: DiffMetadata
    from_version_vector: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ..., diff_metadata: _Optional[_Union[DiffMetadata, _Mapping]] = ..., from_version_vector: _Optional[str] = ...) -> None: ...

class LogDiffReceived(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name", "version_vector", "import_result", "diff_metadata")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_VECTOR_FIELD_NUMBER: _ClassVar[int]
    IMPORT_RESULT_FIELD_NUMBER: _ClassVar[int]
    DIFF_METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    version_vector: str
    import_result: DiffApplicationResult
    diff_metadata: DiffMetadata
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ..., version_vector: _Optional[str] = ..., import_result: _Optional[_Union[DiffApplicationResult, str]] = ..., diff_metadata: _Optional[_Union[DiffMetadata, _Mapping]] = ...) -> None: ...

class LogConvertToCloud(_message.Message):
    __slots__ = ("metadata", "workspace_identifier", "workspace_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    workspace_identifier: str
    workspace_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., workspace_identifier: _Optional[str] = ..., workspace_name: _Optional[str] = ...) -> None: ...

class LogOpenedWorkspace(_message.Message):
    __slots__ = ("metadata", "workspace_identifier", "workspace_name", "is_local")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_LOCAL_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    workspace_identifier: str
    workspace_name: str
    is_local: bool
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., workspace_identifier: _Optional[str] = ..., workspace_name: _Optional[str] = ..., is_local: _Optional[bool] = ...) -> None: ...

class LogConvertToLocal(_message.Message):
    __slots__ = ("metadata", "workspace_identifier", "workspace_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    workspace_identifier: str
    workspace_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., workspace_identifier: _Optional[str] = ..., workspace_name: _Optional[str] = ...) -> None: ...

class LogSyncingChange(_message.Message):
    __slots__ = ("paused", "online")
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    paused: PauseState
    online: bool
    def __init__(self, paused: _Optional[_Union[PauseState, _Mapping]] = ..., online: _Optional[bool] = ...) -> None: ...

class PauseState(_message.Message):
    __slots__ = ("until_time_utc", "paused_at_utc")
    UNTIL_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    PAUSED_AT_UTC_FIELD_NUMBER: _ClassVar[int]
    until_time_utc: int
    paused_at_utc: int
    def __init__(self, until_time_utc: _Optional[int] = ..., paused_at_utc: _Optional[int] = ...) -> None: ...

class LogDocumentStored(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name", "version_vector")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_VECTOR_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    version_vector: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ..., version_vector: _Optional[str] = ...) -> None: ...

class LogDocumentCreated(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ...) -> None: ...

class LogDocumentRequested(_message.Message):
    __slots__ = ("metadata", "document_identifier")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ...) -> None: ...

class LogDocumentUpdated(_message.Message):
    __slots__ = ("metadata", "document_identifier", "previous_document_name", "updated_document_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    previous_document_name: str
    updated_document_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., previous_document_name: _Optional[str] = ..., updated_document_name: _Optional[str] = ...) -> None: ...

class LogDocumentDeleted(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ...) -> None: ...

class LogDocumentConflict(_message.Message):
    __slots__ = ("metadata", "document_identifier", "document_name", "field", "conflict_type")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_TYPE_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    document_identifier: str
    document_name: str
    field: Field
    conflict_type: ConflictType
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., document_identifier: _Optional[str] = ..., document_name: _Optional[str] = ..., field: _Optional[_Union[Field, str]] = ..., conflict_type: _Optional[_Union[ConflictType, str]] = ...) -> None: ...

class LogWorkspaceResynchronized(_message.Message):
    __slots__ = ("metadata", "cause")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CAUSE_FIELD_NUMBER: _ClassVar[int]
    metadata: LogMetadata
    cause: ResyncCause
    def __init__(self, metadata: _Optional[_Union[LogMetadata, _Mapping]] = ..., cause: _Optional[_Union[ResyncCause, str]] = ...) -> None: ...

class DiffMetadata(_message.Message):
    __slots__ = ("change_num", "partial_start_vv", "partial_end_vv")
    CHANGE_NUM_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_START_VV_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_END_VV_FIELD_NUMBER: _ClassVar[int]
    change_num: int
    partial_start_vv: str
    partial_end_vv: str
    def __init__(self, change_num: _Optional[int] = ..., partial_start_vv: _Optional[str] = ..., partial_end_vv: _Optional[str] = ...) -> None: ...

class LogMetadata(_message.Message):
    __slots__ = ("peer_id", "log_message", "workspace_identifier", "log_source")
    PEER_ID_FIELD_NUMBER: _ClassVar[int]
    LOG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    LOG_SOURCE_FIELD_NUMBER: _ClassVar[int]
    peer_id: str
    log_message: str
    workspace_identifier: str
    log_source: LogSource
    def __init__(self, peer_id: _Optional[str] = ..., log_message: _Optional[str] = ..., workspace_identifier: _Optional[str] = ..., log_source: _Optional[_Union[LogSource, str]] = ...) -> None: ...
