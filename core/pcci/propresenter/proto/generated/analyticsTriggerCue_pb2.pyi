from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DestinationLayer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESTINATION_LAYER_UNKNOWN: _ClassVar[DestinationLayer]
    ANNOUNCEMENT: _ClassVar[DestinationLayer]
    PRESENTATION: _ClassVar[DestinationLayer]
    STAGE: _ClassVar[DestinationLayer]
    PROPS: _ClassVar[DestinationLayer]
    MESSAGES: _ClassVar[DestinationLayer]
    MASK: _ClassVar[DestinationLayer]
DESTINATION_LAYER_UNKNOWN: DestinationLayer
ANNOUNCEMENT: DestinationLayer
PRESENTATION: DestinationLayer
STAGE: DestinationLayer
PROPS: DestinationLayer
MESSAGES: DestinationLayer
MASK: DestinationLayer

class Slide(_message.Message):
    __slots__ = ("object_count", "scrolling_object_count", "background_fx_object_count", "action_count", "has_text_fx", "media_text_fill_object_count", "cut_out_text_fill_object_count", "background_blur_text_fill_object_count", "background_invert_text_fill_object_count")
    OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    SCROLLING_OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_FX_OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACTION_COUNT_FIELD_NUMBER: _ClassVar[int]
    HAS_TEXT_FX_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TEXT_FILL_OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    CUT_OUT_TEXT_FILL_OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_BLUR_TEXT_FILL_OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_INVERT_TEXT_FILL_OBJECT_COUNT_FIELD_NUMBER: _ClassVar[int]
    object_count: int
    scrolling_object_count: int
    background_fx_object_count: int
    action_count: int
    has_text_fx: bool
    media_text_fill_object_count: int
    cut_out_text_fill_object_count: int
    background_blur_text_fill_object_count: int
    background_invert_text_fill_object_count: int
    def __init__(self, object_count: _Optional[int] = ..., scrolling_object_count: _Optional[int] = ..., background_fx_object_count: _Optional[int] = ..., action_count: _Optional[int] = ..., has_text_fx: _Optional[bool] = ..., media_text_fill_object_count: _Optional[int] = ..., cut_out_text_fill_object_count: _Optional[int] = ..., background_blur_text_fill_object_count: _Optional[int] = ..., background_invert_text_fill_object_count: _Optional[int] = ...) -> None: ...

class SlideFileFeedElement(_message.Message):
    __slots__ = ("destination_layer",)
    DESTINATION_LAYER_FIELD_NUMBER: _ClassVar[int]
    destination_layer: DestinationLayer
    def __init__(self, destination_layer: _Optional[_Union[DestinationLayer, str]] = ...) -> None: ...

class SlideRssFeedElement(_message.Message):
    __slots__ = ("content", "is_delimiter_enabled", "destination_layer")
    class Content(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONTENT_UNKNOWN: _ClassVar[SlideRssFeedElement.Content]
        TITLE: _ClassVar[SlideRssFeedElement.Content]
        TITLE_AND_DESCRIPTION: _ClassVar[SlideRssFeedElement.Content]
    CONTENT_UNKNOWN: SlideRssFeedElement.Content
    TITLE: SlideRssFeedElement.Content
    TITLE_AND_DESCRIPTION: SlideRssFeedElement.Content
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IS_DELIMITER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_LAYER_FIELD_NUMBER: _ClassVar[int]
    content: SlideRssFeedElement.Content
    is_delimiter_enabled: bool
    destination_layer: DestinationLayer
    def __init__(self, content: _Optional[_Union[SlideRssFeedElement.Content, str]] = ..., is_delimiter_enabled: _Optional[bool] = ..., destination_layer: _Optional[_Union[DestinationLayer, str]] = ...) -> None: ...

class SlideScrollingTextElement(_message.Message):
    __slots__ = ("direction", "start_position", "is_repeat_enabled", "speed", "destination_layer")
    class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIRECTION_UNKNOWN: _ClassVar[SlideScrollingTextElement.Direction]
        LEFT: _ClassVar[SlideScrollingTextElement.Direction]
        RIGHT: _ClassVar[SlideScrollingTextElement.Direction]
        UP: _ClassVar[SlideScrollingTextElement.Direction]
        DOWN: _ClassVar[SlideScrollingTextElement.Direction]
    DIRECTION_UNKNOWN: SlideScrollingTextElement.Direction
    LEFT: SlideScrollingTextElement.Direction
    RIGHT: SlideScrollingTextElement.Direction
    UP: SlideScrollingTextElement.Direction
    DOWN: SlideScrollingTextElement.Direction
    class StartPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        START_POSITION_UNKNOWN: _ClassVar[SlideScrollingTextElement.StartPosition]
        AUTOMATIC: _ClassVar[SlideScrollingTextElement.StartPosition]
        OFF_SCREEN: _ClassVar[SlideScrollingTextElement.StartPosition]
    START_POSITION_UNKNOWN: SlideScrollingTextElement.StartPosition
    AUTOMATIC: SlideScrollingTextElement.StartPosition
    OFF_SCREEN: SlideScrollingTextElement.StartPosition
    class Speed(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SPEED_UNKNOWN: _ClassVar[SlideScrollingTextElement.Speed]
        VERY_SLOW: _ClassVar[SlideScrollingTextElement.Speed]
        SLOW: _ClassVar[SlideScrollingTextElement.Speed]
        MEDIUM: _ClassVar[SlideScrollingTextElement.Speed]
        FAST: _ClassVar[SlideScrollingTextElement.Speed]
        VERY_FAST: _ClassVar[SlideScrollingTextElement.Speed]
    SPEED_UNKNOWN: SlideScrollingTextElement.Speed
    VERY_SLOW: SlideScrollingTextElement.Speed
    SLOW: SlideScrollingTextElement.Speed
    MEDIUM: SlideScrollingTextElement.Speed
    FAST: SlideScrollingTextElement.Speed
    VERY_FAST: SlideScrollingTextElement.Speed
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    START_POSITION_FIELD_NUMBER: _ClassVar[int]
    IS_REPEAT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_LAYER_FIELD_NUMBER: _ClassVar[int]
    direction: SlideScrollingTextElement.Direction
    start_position: SlideScrollingTextElement.StartPosition
    is_repeat_enabled: bool
    speed: SlideScrollingTextElement.Speed
    destination_layer: DestinationLayer
    def __init__(self, direction: _Optional[_Union[SlideScrollingTextElement.Direction, str]] = ..., start_position: _Optional[_Union[SlideScrollingTextElement.StartPosition, str]] = ..., is_repeat_enabled: _Optional[bool] = ..., speed: _Optional[_Union[SlideScrollingTextElement.Speed, str]] = ..., destination_layer: _Optional[_Union[DestinationLayer, str]] = ...) -> None: ...
