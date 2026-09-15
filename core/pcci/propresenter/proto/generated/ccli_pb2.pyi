import applicationInfo_pb2 as _applicationInfo_pb2
import customOptions_pb2 as _customOptions_pb2
import template_pb2 as _template_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CCLIDocument(_message.Message):
    __slots__ = ("application_info", "enable_ccli_display", "ccli_license", "display_type", "template", "layout")
    class DisplayType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DISPLAY_TYPE_FIRST_SLIDE: _ClassVar[CCLIDocument.DisplayType]
        DISPLAY_TYPE_LAST_SLIDE: _ClassVar[CCLIDocument.DisplayType]
        DISPLAY_TYPE_FIRST_AND_LAST_SLIDE: _ClassVar[CCLIDocument.DisplayType]
        DISPLAY_TYPE_ALL_SLIDES: _ClassVar[CCLIDocument.DisplayType]
    DISPLAY_TYPE_FIRST_SLIDE: CCLIDocument.DisplayType
    DISPLAY_TYPE_LAST_SLIDE: CCLIDocument.DisplayType
    DISPLAY_TYPE_FIRST_AND_LAST_SLIDE: CCLIDocument.DisplayType
    DISPLAY_TYPE_ALL_SLIDES: CCLIDocument.DisplayType
    APPLICATION_INFO_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CCLI_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    CCLI_LICENSE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    application_info: _applicationInfo_pb2.ApplicationInfo
    enable_ccli_display: bool
    ccli_license: str
    display_type: CCLIDocument.DisplayType
    template: _template_pb2.Template.Slide
    layout: CopyrightLayout
    def __init__(self, application_info: _Optional[_Union[_applicationInfo_pb2.ApplicationInfo, _Mapping]] = ..., enable_ccli_display: _Optional[bool] = ..., ccli_license: _Optional[str] = ..., display_type: _Optional[_Union[CCLIDocument.DisplayType, str]] = ..., template: _Optional[_Union[_template_pb2.Template.Slide, _Mapping]] = ..., layout: _Optional[_Union[CopyrightLayout, _Mapping]] = ...) -> None: ...

class CopyrightLayout(_message.Message):
    __slots__ = ("tokens",)
    class TokenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Text: _ClassVar[CopyrightLayout.TokenType]
        Artist: _ClassVar[CopyrightLayout.TokenType]
        Author: _ClassVar[CopyrightLayout.TokenType]
        Publisher: _ClassVar[CopyrightLayout.TokenType]
        Title: _ClassVar[CopyrightLayout.TokenType]
        CopyrightYear: _ClassVar[CopyrightLayout.TokenType]
        LicenseNumber: _ClassVar[CopyrightLayout.TokenType]
        SongNumber: _ClassVar[CopyrightLayout.TokenType]
    Text: CopyrightLayout.TokenType
    Artist: CopyrightLayout.TokenType
    Author: CopyrightLayout.TokenType
    Publisher: CopyrightLayout.TokenType
    Title: CopyrightLayout.TokenType
    CopyrightYear: CopyrightLayout.TokenType
    LicenseNumber: CopyrightLayout.TokenType
    SongNumber: CopyrightLayout.TokenType
    class Token(_message.Message):
        __slots__ = ("token_type", "text")
        TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        token_type: CopyrightLayout.TokenType
        text: str
        def __init__(self, token_type: _Optional[_Union[CopyrightLayout.TokenType, str]] = ..., text: _Optional[str] = ...) -> None: ...
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[CopyrightLayout.Token]
    def __init__(self, tokens: _Optional[_Iterable[_Union[CopyrightLayout.Token, _Mapping]]] = ...) -> None: ...
