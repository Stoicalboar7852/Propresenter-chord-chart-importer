from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PPTImportParams(_message.Message):
    __slots__ = ("pptx_path", "result_folder_path", "slide_width", "slide_height", "ignore_backgrounds")
    PPTX_PATH_FIELD_NUMBER: _ClassVar[int]
    RESULT_FOLDER_PATH_FIELD_NUMBER: _ClassVar[int]
    SLIDE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    SLIDE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IGNORE_BACKGROUNDS_FIELD_NUMBER: _ClassVar[int]
    pptx_path: str
    result_folder_path: str
    slide_width: int
    slide_height: int
    ignore_backgrounds: bool
    def __init__(self, pptx_path: _Optional[str] = ..., result_folder_path: _Optional[str] = ..., slide_width: _Optional[int] = ..., slide_height: _Optional[int] = ..., ignore_backgrounds: _Optional[bool] = ...) -> None: ...
