import analyticsMultiTracks_pb2 as _analyticsMultiTracks_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SongSelect(_message.Message):
    __slots__ = ("template_slide_text_element_count", "import_into_playlist", "line_delimiter", "line_delimiter_count", "did_open_edit_view", "multitracks")
    class LineDelimiter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[SongSelect.LineDelimiter]
        LINE_BREAK: _ClassVar[SongSelect.LineDelimiter]
        PARAGRAPH_BREAK: _ClassVar[SongSelect.LineDelimiter]
    UNKNOWN: SongSelect.LineDelimiter
    LINE_BREAK: SongSelect.LineDelimiter
    PARAGRAPH_BREAK: SongSelect.LineDelimiter
    TEMPLATE_SLIDE_TEXT_ELEMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    IMPORT_INTO_PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    LINE_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    LINE_DELIMITER_COUNT_FIELD_NUMBER: _ClassVar[int]
    DID_OPEN_EDIT_VIEW_FIELD_NUMBER: _ClassVar[int]
    MULTITRACKS_FIELD_NUMBER: _ClassVar[int]
    template_slide_text_element_count: int
    import_into_playlist: bool
    line_delimiter: SongSelect.LineDelimiter
    line_delimiter_count: int
    did_open_edit_view: bool
    multitracks: _analyticsMultiTracks_pb2.Import
    def __init__(self, template_slide_text_element_count: _Optional[int] = ..., import_into_playlist: _Optional[bool] = ..., line_delimiter: _Optional[_Union[SongSelect.LineDelimiter, str]] = ..., line_delimiter_count: _Optional[int] = ..., did_open_edit_view: _Optional[bool] = ..., multitracks: _Optional[_Union[_analyticsMultiTracks_pb2.Import, _Mapping]] = ...) -> None: ...
