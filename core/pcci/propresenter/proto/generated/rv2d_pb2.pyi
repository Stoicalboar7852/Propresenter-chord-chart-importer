import action_pb2 as _action_pb2
import color_pb2 as _color_pb2
import cue_pb2 as _cue_pb2
import graphicsData_pb2 as _graphicsData_pb2
import musicKeyScale_pb2 as _musicKeyScale_pb2
import proCore_pb2 as _proCore_pb2
import slide_pb2 as _slide_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IdentificationOverlay(_message.Message):
    __slots__ = ("screen_name", "outputs")
    class Output(_message.Message):
        __slots__ = ("x", "y", "width", "height", "name", "frame_rate")
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        FRAME_RATE_FIELD_NUMBER: _ClassVar[int]
        x: int
        y: int
        width: int
        height: int
        name: str
        frame_rate: float
        def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., name: _Optional[str] = ..., frame_rate: _Optional[float] = ...) -> None: ...
    SCREEN_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    screen_name: str
    outputs: _containers.RepeatedCompositeFieldContainer[IdentificationOverlay.Output]
    def __init__(self, screen_name: _Optional[str] = ..., outputs: _Optional[_Iterable[_Union[IdentificationOverlay.Output, _Mapping]]] = ...) -> None: ...

class LayerIdentificationOverlay(_message.Message):
    __slots__ = ("layer", "layer_name")
    class Layer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LAYER_VIDEO_INPUT: _ClassVar[LayerIdentificationOverlay.Layer]
        LAYER_MEDIA: _ClassVar[LayerIdentificationOverlay.Layer]
        LAYER_PRESENTATION: _ClassVar[LayerIdentificationOverlay.Layer]
        LAYER_ANNOUNCEMENTS: _ClassVar[LayerIdentificationOverlay.Layer]
        LAYER_PROPS: _ClassVar[LayerIdentificationOverlay.Layer]
        LAYER_MESSAGES: _ClassVar[LayerIdentificationOverlay.Layer]
    LAYER_VIDEO_INPUT: LayerIdentificationOverlay.Layer
    LAYER_MEDIA: LayerIdentificationOverlay.Layer
    LAYER_PRESENTATION: LayerIdentificationOverlay.Layer
    LAYER_ANNOUNCEMENTS: LayerIdentificationOverlay.Layer
    LAYER_PROPS: LayerIdentificationOverlay.Layer
    LAYER_MESSAGES: LayerIdentificationOverlay.Layer
    LAYER_FIELD_NUMBER: _ClassVar[int]
    LAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    layer: LayerIdentificationOverlay.Layer
    layer_name: str
    def __init__(self, layer: _Optional[_Union[LayerIdentificationOverlay.Layer, str]] = ..., layer_name: _Optional[str] = ...) -> None: ...

class RenderLayer(_message.Message):
    __slots__ = ("bounds", "flip_mode", "rotation", "build_index", "build_out", "build_out_index", "composite", "media", "cut_out", "background_effect", "output_screen", "scrolling", "slide_image", "zone")
    class Composite(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Scrolling(_message.Message):
        __slots__ = ("segment_size",)
        SEGMENT_SIZE_FIELD_NUMBER: _ClassVar[int]
        segment_size: int
        def __init__(self, segment_size: _Optional[int] = ...) -> None: ...
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    FLIP_MODE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    BUILD_INDEX_FIELD_NUMBER: _ClassVar[int]
    BUILD_OUT_FIELD_NUMBER: _ClassVar[int]
    BUILD_OUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    COMPOSITE_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    CUT_OUT_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_EFFECT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCREEN_FIELD_NUMBER: _ClassVar[int]
    SCROLLING_FIELD_NUMBER: _ClassVar[int]
    SLIDE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    bounds: _graphicsData_pb2.Graphics.Rect
    flip_mode: _graphicsData_pb2.Graphics.Element.FlipMode
    rotation: float
    build_index: int
    build_out: bool
    build_out_index: int
    composite: RenderLayer.Composite
    media: _graphicsData_pb2.Media
    cut_out: _graphicsData_pb2.Graphics.Text.CutOutFill
    background_effect: _graphicsData_pb2.Graphics.BackgroundEffect
    output_screen: _slide_pb2.Slide.Element.DataLink.OutputScreen
    scrolling: RenderLayer.Scrolling
    slide_image: _slide_pb2.Slide.Element.DataLink.SlideImage
    zone: _slide_pb2.Slide.Element.DataLink.Zone
    def __init__(self, bounds: _Optional[_Union[_graphicsData_pb2.Graphics.Rect, _Mapping]] = ..., flip_mode: _Optional[_Union[_graphicsData_pb2.Graphics.Element.FlipMode, str]] = ..., rotation: _Optional[float] = ..., build_index: _Optional[int] = ..., build_out: _Optional[bool] = ..., build_out_index: _Optional[int] = ..., composite: _Optional[_Union[RenderLayer.Composite, _Mapping]] = ..., media: _Optional[_Union[_graphicsData_pb2.Media, _Mapping]] = ..., cut_out: _Optional[_Union[_graphicsData_pb2.Graphics.Text.CutOutFill, _Mapping]] = ..., background_effect: _Optional[_Union[_graphicsData_pb2.Graphics.BackgroundEffect, _Mapping]] = ..., output_screen: _Optional[_Union[_slide_pb2.Slide.Element.DataLink.OutputScreen, _Mapping]] = ..., scrolling: _Optional[_Union[RenderLayer.Scrolling, _Mapping]] = ..., slide_image: _Optional[_Union[_slide_pb2.Slide.Element.DataLink.SlideImage, _Mapping]] = ..., zone: _Optional[_Union[_slide_pb2.Slide.Element.DataLink.Zone, _Mapping]] = ...) -> None: ...

class SlideElement(_message.Message):
    __slots__ = ("element", "build_index", "base_key", "target_key", "cookies", "for_stage_layout")
    ELEMENT_FIELD_NUMBER: _ClassVar[int]
    BUILD_INDEX_FIELD_NUMBER: _ClassVar[int]
    BASE_KEY_FIELD_NUMBER: _ClassVar[int]
    TARGET_KEY_FIELD_NUMBER: _ClassVar[int]
    COOKIES_FIELD_NUMBER: _ClassVar[int]
    FOR_STAGE_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    element: _slide_pb2.Slide.Element
    build_index: int
    base_key: _musicKeyScale_pb2.MusicKeyScale
    target_key: _musicKeyScale_pb2.MusicKeyScale
    cookies: _containers.RepeatedCompositeFieldContainer[_proCore_pb2.WebFillTokenAndCookies.Cookie]
    for_stage_layout: bool
    def __init__(self, element: _Optional[_Union[_slide_pb2.Slide.Element, _Mapping]] = ..., build_index: _Optional[int] = ..., base_key: _Optional[_Union[_musicKeyScale_pb2.MusicKeyScale, _Mapping]] = ..., target_key: _Optional[_Union[_musicKeyScale_pb2.MusicKeyScale, _Mapping]] = ..., cookies: _Optional[_Iterable[_Union[_proCore_pb2.WebFillTokenAndCookies.Cookie, _Mapping]]] = ..., for_stage_layout: _Optional[bool] = ...) -> None: ...

class SlidePreview(_message.Message):
    __slots__ = ("cue", "element", "background")
    CUE_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    cue: _cue_pb2.Cue
    element: _slide_pb2.Slide.Element
    background: _color_pb2.Color
    def __init__(self, cue: _Optional[_Union[_cue_pb2.Cue, _Mapping]] = ..., element: _Optional[_Union[_slide_pb2.Slide.Element, _Mapping]] = ..., background: _Optional[_Union[_color_pb2.Color, _Mapping]] = ...) -> None: ...

class MediaPreview(_message.Message):
    __slots__ = ("action", "media")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    action: _action_pb2.Action
    media: _graphicsData_pb2.Media
    def __init__(self, action: _Optional[_Union[_action_pb2.Action, _Mapping]] = ..., media: _Optional[_Union[_graphicsData_pb2.Media, _Mapping]] = ...) -> None: ...
