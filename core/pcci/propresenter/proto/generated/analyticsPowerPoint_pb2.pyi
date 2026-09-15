from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SLIDES_AS_IMAGES: _ClassVar[ImportType]
    TEXT_ONLY: _ClassVar[ImportType]
    TEXT_AND_IMAGES: _ClassVar[ImportType]
    CORE_OPEN_XML: _ClassVar[ImportType]

class ImportFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKOWN: _ClassVar[ImportFormat]
    PPT: _ClassVar[ImportFormat]
    PPTX: _ClassVar[ImportFormat]
SLIDES_AS_IMAGES: ImportType
TEXT_ONLY: ImportType
TEXT_AND_IMAGES: ImportType
CORE_OPEN_XML: ImportType
UNKOWN: ImportFormat
PPT: ImportFormat
PPTX: ImportFormat

class ImportPowerPoint(_message.Message):
    __slots__ = ("type", "format")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    type: ImportType
    format: ImportFormat
    def __init__(self, type: _Optional[_Union[ImportType, str]] = ..., format: _Optional[_Union[ImportFormat, str]] = ...) -> None: ...
