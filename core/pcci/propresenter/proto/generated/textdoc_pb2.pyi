from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Document(_message.Message):
    __slots__ = ("document_settings", "document_attributes", "list_settings", "table_settings", "paragraphs", "width", "height")
    class ParagraphAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ParagraphAlignment_Left: _ClassVar[Document.ParagraphAlignment]
        ParagraphAlignment_Center: _ClassVar[Document.ParagraphAlignment]
        ParagraphAlignment_Right: _ClassVar[Document.ParagraphAlignment]
        ParagraphAlignment_Justified: _ClassVar[Document.ParagraphAlignment]
    ParagraphAlignment_Left: Document.ParagraphAlignment
    ParagraphAlignment_Center: Document.ParagraphAlignment
    ParagraphAlignment_Right: Document.ParagraphAlignment
    ParagraphAlignment_Justified: Document.ParagraphAlignment
    class LineSpacingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LineSpacingMode_Absolute: _ClassVar[Document.LineSpacingMode]
        LineSpacingMode_Relative: _ClassVar[Document.LineSpacingMode]
        LineSpacingMode_Multiple: _ClassVar[Document.LineSpacingMode]
    LineSpacingMode_Absolute: Document.LineSpacingMode
    LineSpacingMode_Relative: Document.LineSpacingMode
    LineSpacingMode_Multiple: Document.LineSpacingMode
    class RightIndentMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RightIndentMode_FromRight: _ClassVar[Document.RightIndentMode]
        RightIndentMode_FromLeft: _ClassVar[Document.RightIndentMode]
    RightIndentMode_FromRight: Document.RightIndentMode
    RightIndentMode_FromLeft: Document.RightIndentMode
    class TabStopType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TabStopType_Left: _ClassVar[Document.TabStopType]
        TabStopType_Right: _ClassVar[Document.TabStopType]
        TabStopType_Center: _ClassVar[Document.TabStopType]
        TabStopType_Decimal: _ClassVar[Document.TabStopType]
    TabStopType_Left: Document.TabStopType
    TabStopType_Right: Document.TabStopType
    TabStopType_Center: Document.TabStopType
    TabStopType_Decimal: Document.TabStopType
    class Color(_message.Message):
        __slots__ = ("red", "green", "blue", "alpha")
        RED_FIELD_NUMBER: _ClassVar[int]
        GREEN_FIELD_NUMBER: _ClassVar[int]
        BLUE_FIELD_NUMBER: _ClassVar[int]
        ALPHA_FIELD_NUMBER: _ClassVar[int]
        red: float
        green: float
        blue: float
        alpha: float
        def __init__(self, red: _Optional[float] = ..., green: _Optional[float] = ..., blue: _Optional[float] = ..., alpha: _Optional[float] = ...) -> None: ...
    class DocumentSettings(_message.Message):
        __slots__ = ("alignment", "transform", "delimiter", "scale_mode", "layout_width", "margins", "shadow", "has_explicit_margins")
        class DocumentAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            DocumentAlignment_Top: _ClassVar[Document.DocumentSettings.DocumentAlignment]
            DocumentAlignment_Middle: _ClassVar[Document.DocumentSettings.DocumentAlignment]
            DocumentAlignment_Bottom: _ClassVar[Document.DocumentSettings.DocumentAlignment]
        DocumentAlignment_Top: Document.DocumentSettings.DocumentAlignment
        DocumentAlignment_Middle: Document.DocumentSettings.DocumentAlignment
        DocumentAlignment_Bottom: Document.DocumentSettings.DocumentAlignment
        class TextTransform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            TextTransform_None: _ClassVar[Document.DocumentSettings.TextTransform]
            TextTransform_RemoveLineReturns: _ClassVar[Document.DocumentSettings.TextTransform]
            TextTransform_ReplaceLineReturns: _ClassVar[Document.DocumentSettings.TextTransform]
            TextTransform_SingleWordPerLine: _ClassVar[Document.DocumentSettings.TextTransform]
            TextTransform_SingleCharacterPerLine: _ClassVar[Document.DocumentSettings.TextTransform]
        TextTransform_None: Document.DocumentSettings.TextTransform
        TextTransform_RemoveLineReturns: Document.DocumentSettings.TextTransform
        TextTransform_ReplaceLineReturns: Document.DocumentSettings.TextTransform
        TextTransform_SingleWordPerLine: Document.DocumentSettings.TextTransform
        TextTransform_SingleCharacterPerLine: Document.DocumentSettings.TextTransform
        class ScaleMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            ScaleMode_None: _ClassVar[Document.DocumentSettings.ScaleMode]
            ScaleMode_AdjustContainerHeight: _ClassVar[Document.DocumentSettings.ScaleMode]
            ScaleMode_Up: _ClassVar[Document.DocumentSettings.ScaleMode]
            ScaleMode_Down: _ClassVar[Document.DocumentSettings.ScaleMode]
            ScaleMode_UpOrDown: _ClassVar[Document.DocumentSettings.ScaleMode]
        ScaleMode_None: Document.DocumentSettings.ScaleMode
        ScaleMode_AdjustContainerHeight: Document.DocumentSettings.ScaleMode
        ScaleMode_Up: Document.DocumentSettings.ScaleMode
        ScaleMode_Down: Document.DocumentSettings.ScaleMode
        ScaleMode_UpOrDown: Document.DocumentSettings.ScaleMode
        class Margins(_message.Message):
            __slots__ = ("left", "top", "right", "bottom")
            LEFT_FIELD_NUMBER: _ClassVar[int]
            TOP_FIELD_NUMBER: _ClassVar[int]
            RIGHT_FIELD_NUMBER: _ClassVar[int]
            BOTTOM_FIELD_NUMBER: _ClassVar[int]
            left: float
            top: float
            right: float
            bottom: float
            def __init__(self, left: _Optional[float] = ..., top: _Optional[float] = ..., right: _Optional[float] = ..., bottom: _Optional[float] = ...) -> None: ...
        class Shadow(_message.Message):
            __slots__ = ("enabled", "blur_radius", "opacity", "color", "angle", "offset")
            ENABLED_FIELD_NUMBER: _ClassVar[int]
            BLUR_RADIUS_FIELD_NUMBER: _ClassVar[int]
            OPACITY_FIELD_NUMBER: _ClassVar[int]
            COLOR_FIELD_NUMBER: _ClassVar[int]
            ANGLE_FIELD_NUMBER: _ClassVar[int]
            OFFSET_FIELD_NUMBER: _ClassVar[int]
            enabled: bool
            blur_radius: float
            opacity: float
            color: Document.Color
            angle: float
            offset: float
            def __init__(self, enabled: _Optional[bool] = ..., blur_radius: _Optional[float] = ..., opacity: _Optional[float] = ..., color: _Optional[_Union[Document.Color, _Mapping]] = ..., angle: _Optional[float] = ..., offset: _Optional[float] = ...) -> None: ...
        ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
        TRANSFORM_FIELD_NUMBER: _ClassVar[int]
        DELIMITER_FIELD_NUMBER: _ClassVar[int]
        SCALE_MODE_FIELD_NUMBER: _ClassVar[int]
        LAYOUT_WIDTH_FIELD_NUMBER: _ClassVar[int]
        MARGINS_FIELD_NUMBER: _ClassVar[int]
        SHADOW_FIELD_NUMBER: _ClassVar[int]
        HAS_EXPLICIT_MARGINS_FIELD_NUMBER: _ClassVar[int]
        alignment: Document.DocumentSettings.DocumentAlignment
        transform: Document.DocumentSettings.TextTransform
        delimiter: str
        scale_mode: Document.DocumentSettings.ScaleMode
        layout_width: float
        margins: Document.DocumentSettings.Margins
        shadow: Document.DocumentSettings.Shadow
        has_explicit_margins: bool
        def __init__(self, alignment: _Optional[_Union[Document.DocumentSettings.DocumentAlignment, str]] = ..., transform: _Optional[_Union[Document.DocumentSettings.TextTransform, str]] = ..., delimiter: _Optional[str] = ..., scale_mode: _Optional[_Union[Document.DocumentSettings.ScaleMode, str]] = ..., layout_width: _Optional[float] = ..., margins: _Optional[_Union[Document.DocumentSettings.Margins, _Mapping]] = ..., shadow: _Optional[_Union[Document.DocumentSettings.Shadow, _Mapping]] = ..., has_explicit_margins: _Optional[bool] = ...) -> None: ...
    class LevelSettings(_message.Message):
        __slots__ = ("follow_type", "numbering_scheme", "bullet_type", "is_bullet", "prefix", "suffix", "numbering_format", "start_number", "level_index")
        class FollowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            FollowType_Nothing: _ClassVar[Document.LevelSettings.FollowType]
            FollowType_Space: _ClassVar[Document.LevelSettings.FollowType]
            FollowType_Tab: _ClassVar[Document.LevelSettings.FollowType]
        FollowType_Nothing: Document.LevelSettings.FollowType
        FollowType_Space: Document.LevelSettings.FollowType
        FollowType_Tab: Document.LevelSettings.FollowType
        class NumberingScheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            NumberingScheme_Arabic: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_ArabicWithLeadingZero: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_OrdinalNumber: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_UppercaseRomanNumeral: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_LowercaseRomanNumeral: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_UppercaseLetter: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_LowercaseLetter: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_LowercaseRussianAlphabet: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_UppercaseRussianAlphabet: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_LowercaseGreekNumerals: _ClassVar[Document.LevelSettings.NumberingScheme]
            NumberingScheme_UppercaseGreekNumerals: _ClassVar[Document.LevelSettings.NumberingScheme]
        NumberingScheme_Arabic: Document.LevelSettings.NumberingScheme
        NumberingScheme_ArabicWithLeadingZero: Document.LevelSettings.NumberingScheme
        NumberingScheme_OrdinalNumber: Document.LevelSettings.NumberingScheme
        NumberingScheme_UppercaseRomanNumeral: Document.LevelSettings.NumberingScheme
        NumberingScheme_LowercaseRomanNumeral: Document.LevelSettings.NumberingScheme
        NumberingScheme_UppercaseLetter: Document.LevelSettings.NumberingScheme
        NumberingScheme_LowercaseLetter: Document.LevelSettings.NumberingScheme
        NumberingScheme_LowercaseRussianAlphabet: Document.LevelSettings.NumberingScheme
        NumberingScheme_UppercaseRussianAlphabet: Document.LevelSettings.NumberingScheme
        NumberingScheme_LowercaseGreekNumerals: Document.LevelSettings.NumberingScheme
        NumberingScheme_UppercaseGreekNumerals: Document.LevelSettings.NumberingScheme
        class BulletType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            BulletType_Dash: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_HyphenDash: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_SmallCircle: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_Circle: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_SmallOpenCircle: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_OpenCircle: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_SmallSquare: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_Square: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_SmallOpenSquare: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_OpenSquare: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_Checkmark: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_HeavyCheckmark: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_Diamond: _ClassVar[Document.LevelSettings.BulletType]
            BulletType_OpenDiamond: _ClassVar[Document.LevelSettings.BulletType]
        BulletType_Dash: Document.LevelSettings.BulletType
        BulletType_HyphenDash: Document.LevelSettings.BulletType
        BulletType_SmallCircle: Document.LevelSettings.BulletType
        BulletType_Circle: Document.LevelSettings.BulletType
        BulletType_SmallOpenCircle: Document.LevelSettings.BulletType
        BulletType_OpenCircle: Document.LevelSettings.BulletType
        BulletType_SmallSquare: Document.LevelSettings.BulletType
        BulletType_Square: Document.LevelSettings.BulletType
        BulletType_SmallOpenSquare: Document.LevelSettings.BulletType
        BulletType_OpenSquare: Document.LevelSettings.BulletType
        BulletType_Checkmark: Document.LevelSettings.BulletType
        BulletType_HeavyCheckmark: Document.LevelSettings.BulletType
        BulletType_Diamond: Document.LevelSettings.BulletType
        BulletType_OpenDiamond: Document.LevelSettings.BulletType
        FOLLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
        NUMBERING_SCHEME_FIELD_NUMBER: _ClassVar[int]
        BULLET_TYPE_FIELD_NUMBER: _ClassVar[int]
        IS_BULLET_FIELD_NUMBER: _ClassVar[int]
        PREFIX_FIELD_NUMBER: _ClassVar[int]
        SUFFIX_FIELD_NUMBER: _ClassVar[int]
        NUMBERING_FORMAT_FIELD_NUMBER: _ClassVar[int]
        START_NUMBER_FIELD_NUMBER: _ClassVar[int]
        LEVEL_INDEX_FIELD_NUMBER: _ClassVar[int]
        follow_type: Document.LevelSettings.FollowType
        numbering_scheme: Document.LevelSettings.NumberingScheme
        bullet_type: Document.LevelSettings.BulletType
        is_bullet: bool
        prefix: str
        suffix: str
        numbering_format: str
        start_number: int
        level_index: int
        def __init__(self, follow_type: _Optional[_Union[Document.LevelSettings.FollowType, str]] = ..., numbering_scheme: _Optional[_Union[Document.LevelSettings.NumberingScheme, str]] = ..., bullet_type: _Optional[_Union[Document.LevelSettings.BulletType, str]] = ..., is_bullet: _Optional[bool] = ..., prefix: _Optional[str] = ..., suffix: _Optional[str] = ..., numbering_format: _Optional[str] = ..., start_number: _Optional[int] = ..., level_index: _Optional[int] = ...) -> None: ...
    class ListSettings(_message.Message):
        __slots__ = ("level_settings",)
        LEVEL_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        level_settings: _containers.RepeatedCompositeFieldContainer[Document.LevelSettings]
        def __init__(self, level_settings: _Optional[_Iterable[_Union[Document.LevelSettings, _Mapping]]] = ...) -> None: ...
    class TableSettings(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class TabStop(_message.Message):
        __slots__ = ("position", "type")
        POSITION_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        position: float
        type: Document.TabStopType
        def __init__(self, position: _Optional[float] = ..., type: _Optional[_Union[Document.TabStopType, str]] = ...) -> None: ...
    class ParagraphSettings(_message.Message):
        __slots__ = ("alignment", "spacing_mode", "line_spacing", "additional_line_spacing", "before_paragraph", "after_paragraph", "left_indent", "right_indent", "right_indent_mode", "first_line_indent", "list_index", "level_index", "bullet_color", "bullet_scale", "tab_stops", "list_override_text", "default_tab_stop")
        ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
        SPACING_MODE_FIELD_NUMBER: _ClassVar[int]
        LINE_SPACING_FIELD_NUMBER: _ClassVar[int]
        ADDITIONAL_LINE_SPACING_FIELD_NUMBER: _ClassVar[int]
        BEFORE_PARAGRAPH_FIELD_NUMBER: _ClassVar[int]
        AFTER_PARAGRAPH_FIELD_NUMBER: _ClassVar[int]
        LEFT_INDENT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_INDENT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_INDENT_MODE_FIELD_NUMBER: _ClassVar[int]
        FIRST_LINE_INDENT_FIELD_NUMBER: _ClassVar[int]
        LIST_INDEX_FIELD_NUMBER: _ClassVar[int]
        LEVEL_INDEX_FIELD_NUMBER: _ClassVar[int]
        BULLET_COLOR_FIELD_NUMBER: _ClassVar[int]
        BULLET_SCALE_FIELD_NUMBER: _ClassVar[int]
        TAB_STOPS_FIELD_NUMBER: _ClassVar[int]
        LIST_OVERRIDE_TEXT_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_TAB_STOP_FIELD_NUMBER: _ClassVar[int]
        alignment: Document.ParagraphAlignment
        spacing_mode: Document.LineSpacingMode
        line_spacing: float
        additional_line_spacing: float
        before_paragraph: float
        after_paragraph: float
        left_indent: float
        right_indent: float
        right_indent_mode: Document.RightIndentMode
        first_line_indent: float
        list_index: int
        level_index: int
        bullet_color: Document.Color
        bullet_scale: float
        tab_stops: _containers.RepeatedCompositeFieldContainer[Document.TabStop]
        list_override_text: str
        default_tab_stop: float
        def __init__(self, alignment: _Optional[_Union[Document.ParagraphAlignment, str]] = ..., spacing_mode: _Optional[_Union[Document.LineSpacingMode, str]] = ..., line_spacing: _Optional[float] = ..., additional_line_spacing: _Optional[float] = ..., before_paragraph: _Optional[float] = ..., after_paragraph: _Optional[float] = ..., left_indent: _Optional[float] = ..., right_indent: _Optional[float] = ..., right_indent_mode: _Optional[_Union[Document.RightIndentMode, str]] = ..., first_line_indent: _Optional[float] = ..., list_index: _Optional[int] = ..., level_index: _Optional[int] = ..., bullet_color: _Optional[_Union[Document.Color, _Mapping]] = ..., bullet_scale: _Optional[float] = ..., tab_stops: _Optional[_Iterable[_Union[Document.TabStop, _Mapping]]] = ..., list_override_text: _Optional[str] = ..., default_tab_stop: _Optional[float] = ...) -> None: ...
    class FontInfo(_message.Message):
        __slots__ = ("system_family_name", "system_face_name", "display_family_name", "display_face_name", "full_name", "postscript_name", "alternate_postscript_names", "weight", "width", "is_italic", "variant_index", "other_properties")
        SYSTEM_FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
        SYSTEM_FACE_NAME_FIELD_NUMBER: _ClassVar[int]
        DISPLAY_FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
        DISPLAY_FACE_NAME_FIELD_NUMBER: _ClassVar[int]
        FULL_NAME_FIELD_NUMBER: _ClassVar[int]
        POSTSCRIPT_NAME_FIELD_NUMBER: _ClassVar[int]
        ALTERNATE_POSTSCRIPT_NAMES_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        IS_ITALIC_FIELD_NUMBER: _ClassVar[int]
        VARIANT_INDEX_FIELD_NUMBER: _ClassVar[int]
        OTHER_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        system_family_name: str
        system_face_name: str
        display_family_name: str
        display_face_name: str
        full_name: str
        postscript_name: str
        alternate_postscript_names: _containers.RepeatedScalarFieldContainer[str]
        weight: int
        width: int
        is_italic: bool
        variant_index: int
        other_properties: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, system_family_name: _Optional[str] = ..., system_face_name: _Optional[str] = ..., display_family_name: _Optional[str] = ..., display_face_name: _Optional[str] = ..., full_name: _Optional[str] = ..., postscript_name: _Optional[str] = ..., alternate_postscript_names: _Optional[_Iterable[str]] = ..., weight: _Optional[int] = ..., width: _Optional[int] = ..., is_italic: _Optional[bool] = ..., variant_index: _Optional[int] = ..., other_properties: _Optional[_Iterable[str]] = ...) -> None: ...
    class SolidFill(_message.Message):
        __slots__ = ("color",)
        COLOR_FIELD_NUMBER: _ClassVar[int]
        color: Document.Color
        def __init__(self, color: _Optional[_Union[Document.Color, _Mapping]] = ...) -> None: ...
    class GradientFill(_message.Message):
        __slots__ = ("angle", "stretch_to_document_bounds", "colors")
        ANGLE_FIELD_NUMBER: _ClassVar[int]
        STRETCH_TO_DOCUMENT_BOUNDS_FIELD_NUMBER: _ClassVar[int]
        COLORS_FIELD_NUMBER: _ClassVar[int]
        angle: float
        stretch_to_document_bounds: bool
        colors: _containers.RepeatedCompositeFieldContainer[Document.Color]
        def __init__(self, angle: _Optional[float] = ..., stretch_to_document_bounds: _Optional[bool] = ..., colors: _Optional[_Iterable[_Union[Document.Color, _Mapping]]] = ...) -> None: ...
    class CutOutFill(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Media(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class MediaFill(_message.Message):
        __slots__ = ("uuid", "stretch_to_document_bounds", "media")
        UUID_FIELD_NUMBER: _ClassVar[int]
        STRETCH_TO_DOCUMENT_BOUNDS_FIELD_NUMBER: _ClassVar[int]
        MEDIA_FIELD_NUMBER: _ClassVar[int]
        uuid: str
        stretch_to_document_bounds: bool
        media: Document.Media
        def __init__(self, uuid: _Optional[str] = ..., stretch_to_document_bounds: _Optional[bool] = ..., media: _Optional[_Union[Document.Media, _Mapping]] = ...) -> None: ...
    class BackgroundBlurFill(_message.Message):
        __slots__ = ("blur", "saturation")
        BLUR_FIELD_NUMBER: _ClassVar[int]
        SATURATION_FIELD_NUMBER: _ClassVar[int]
        blur: float
        saturation: float
        def __init__(self, blur: _Optional[float] = ..., saturation: _Optional[float] = ...) -> None: ...
    class BackgroundInvertFill(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class RunSettings(_message.Message):
        __slots__ = ("font", "character_size", "character_size_mode", "character_spacing", "script_level", "text_fill", "highlight_color", "stroke", "underline", "underline_color", "strike_through", "capitalization_type", "tabular_numbers", "preserve_fill_color", "kerning", "ligatures", "font_scale_factor")
        class CharacterSizeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            CharacterSizeMode_Normal: _ClassVar[Document.RunSettings.CharacterSizeMode]
            CharacterSizeMode_ScaledByDocumentHeight: _ClassVar[Document.RunSettings.CharacterSizeMode]
            CharacterSizeMode_ScaledByDocumentWidth: _ClassVar[Document.RunSettings.CharacterSizeMode]
        CharacterSizeMode_Normal: Document.RunSettings.CharacterSizeMode
        CharacterSizeMode_ScaledByDocumentHeight: Document.RunSettings.CharacterSizeMode
        CharacterSizeMode_ScaledByDocumentWidth: Document.RunSettings.CharacterSizeMode
        class CapitalizationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            CapitalizationType_None: _ClassVar[Document.RunSettings.CapitalizationType]
            CapitalizationType_AllCaps: _ClassVar[Document.RunSettings.CapitalizationType]
            CapitalizationType_LowerCase: _ClassVar[Document.RunSettings.CapitalizationType]
            CapitalizationType_SmallCaps: _ClassVar[Document.RunSettings.CapitalizationType]
            CapitalizationType_TitleCase: _ClassVar[Document.RunSettings.CapitalizationType]
            CapitalizationType_StartCase: _ClassVar[Document.RunSettings.CapitalizationType]
        CapitalizationType_None: Document.RunSettings.CapitalizationType
        CapitalizationType_AllCaps: Document.RunSettings.CapitalizationType
        CapitalizationType_LowerCase: Document.RunSettings.CapitalizationType
        CapitalizationType_SmallCaps: Document.RunSettings.CapitalizationType
        CapitalizationType_TitleCase: Document.RunSettings.CapitalizationType
        CapitalizationType_StartCase: Document.RunSettings.CapitalizationType
        class TextFill(_message.Message):
            __slots__ = ("solid_fill", "gradient_fill", "cut_out_fill", "media_fill", "background_blur_fill", "background_invert_fill")
            SOLID_FILL_FIELD_NUMBER: _ClassVar[int]
            GRADIENT_FILL_FIELD_NUMBER: _ClassVar[int]
            CUT_OUT_FILL_FIELD_NUMBER: _ClassVar[int]
            MEDIA_FILL_FIELD_NUMBER: _ClassVar[int]
            BACKGROUND_BLUR_FILL_FIELD_NUMBER: _ClassVar[int]
            BACKGROUND_INVERT_FILL_FIELD_NUMBER: _ClassVar[int]
            solid_fill: Document.SolidFill
            gradient_fill: Document.GradientFill
            cut_out_fill: Document.CutOutFill
            media_fill: Document.MediaFill
            background_blur_fill: Document.BackgroundBlurFill
            background_invert_fill: Document.BackgroundInvertFill
            def __init__(self, solid_fill: _Optional[_Union[Document.SolidFill, _Mapping]] = ..., gradient_fill: _Optional[_Union[Document.GradientFill, _Mapping]] = ..., cut_out_fill: _Optional[_Union[Document.CutOutFill, _Mapping]] = ..., media_fill: _Optional[_Union[Document.MediaFill, _Mapping]] = ..., background_blur_fill: _Optional[_Union[Document.BackgroundBlurFill, _Mapping]] = ..., background_invert_fill: _Optional[_Union[Document.BackgroundInvertFill, _Mapping]] = ...) -> None: ...
        class Stroke(_message.Message):
            __slots__ = ("thickness", "color")
            THICKNESS_FIELD_NUMBER: _ClassVar[int]
            COLOR_FIELD_NUMBER: _ClassVar[int]
            thickness: float
            color: Document.Color
            def __init__(self, thickness: _Optional[float] = ..., color: _Optional[_Union[Document.Color, _Mapping]] = ...) -> None: ...
        FONT_FIELD_NUMBER: _ClassVar[int]
        CHARACTER_SIZE_FIELD_NUMBER: _ClassVar[int]
        CHARACTER_SIZE_MODE_FIELD_NUMBER: _ClassVar[int]
        CHARACTER_SPACING_FIELD_NUMBER: _ClassVar[int]
        SCRIPT_LEVEL_FIELD_NUMBER: _ClassVar[int]
        TEXT_FILL_FIELD_NUMBER: _ClassVar[int]
        HIGHLIGHT_COLOR_FIELD_NUMBER: _ClassVar[int]
        STROKE_FIELD_NUMBER: _ClassVar[int]
        UNDERLINE_FIELD_NUMBER: _ClassVar[int]
        UNDERLINE_COLOR_FIELD_NUMBER: _ClassVar[int]
        STRIKE_THROUGH_FIELD_NUMBER: _ClassVar[int]
        CAPITALIZATION_TYPE_FIELD_NUMBER: _ClassVar[int]
        TABULAR_NUMBERS_FIELD_NUMBER: _ClassVar[int]
        PRESERVE_FILL_COLOR_FIELD_NUMBER: _ClassVar[int]
        KERNING_FIELD_NUMBER: _ClassVar[int]
        LIGATURES_FIELD_NUMBER: _ClassVar[int]
        FONT_SCALE_FACTOR_FIELD_NUMBER: _ClassVar[int]
        font: Document.FontInfo
        character_size: float
        character_size_mode: Document.RunSettings.CharacterSizeMode
        character_spacing: float
        script_level: int
        text_fill: Document.RunSettings.TextFill
        highlight_color: Document.Color
        stroke: Document.RunSettings.Stroke
        underline: bool
        underline_color: Document.Color
        strike_through: bool
        capitalization_type: Document.RunSettings.CapitalizationType
        tabular_numbers: bool
        preserve_fill_color: bool
        kerning: bool
        ligatures: bool
        font_scale_factor: float
        def __init__(self, font: _Optional[_Union[Document.FontInfo, _Mapping]] = ..., character_size: _Optional[float] = ..., character_size_mode: _Optional[_Union[Document.RunSettings.CharacterSizeMode, str]] = ..., character_spacing: _Optional[float] = ..., script_level: _Optional[int] = ..., text_fill: _Optional[_Union[Document.RunSettings.TextFill, _Mapping]] = ..., highlight_color: _Optional[_Union[Document.Color, _Mapping]] = ..., stroke: _Optional[_Union[Document.RunSettings.Stroke, _Mapping]] = ..., underline: _Optional[bool] = ..., underline_color: _Optional[_Union[Document.Color, _Mapping]] = ..., strike_through: _Optional[bool] = ..., capitalization_type: _Optional[_Union[Document.RunSettings.CapitalizationType, str]] = ..., tabular_numbers: _Optional[bool] = ..., preserve_fill_color: _Optional[bool] = ..., kerning: _Optional[bool] = ..., ligatures: _Optional[bool] = ..., font_scale_factor: _Optional[float] = ...) -> None: ...
    class Run(_message.Message):
        __slots__ = ("run_settings", "text")
        RUN_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        run_settings: Document.RunSettings
        text: str
        def __init__(self, run_settings: _Optional[_Union[Document.RunSettings, _Mapping]] = ..., text: _Optional[str] = ...) -> None: ...
    class Paragraph(_message.Message):
        __slots__ = ("paragraph_settings", "runs", "default_run_settings")
        PARAGRAPH_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        RUNS_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_RUN_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        paragraph_settings: Document.ParagraphSettings
        runs: _containers.RepeatedCompositeFieldContainer[Document.Run]
        default_run_settings: Document.RunSettings
        def __init__(self, paragraph_settings: _Optional[_Union[Document.ParagraphSettings, _Mapping]] = ..., runs: _Optional[_Iterable[_Union[Document.Run, _Mapping]]] = ..., default_run_settings: _Optional[_Union[Document.RunSettings, _Mapping]] = ...) -> None: ...
    class DocumentAttributes(_message.Message):
        __slots__ = ("paragraph_settings", "run_settings")
        PARAGRAPH_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        RUN_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        paragraph_settings: Document.ParagraphSettings
        run_settings: Document.RunSettings
        def __init__(self, paragraph_settings: _Optional[_Union[Document.ParagraphSettings, _Mapping]] = ..., run_settings: _Optional[_Union[Document.RunSettings, _Mapping]] = ...) -> None: ...
    DOCUMENT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    LIST_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TABLE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PARAGRAPHS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    document_settings: Document.DocumentSettings
    document_attributes: Document.DocumentAttributes
    list_settings: _containers.RepeatedCompositeFieldContainer[Document.ListSettings]
    table_settings: Document.TableSettings
    paragraphs: _containers.RepeatedCompositeFieldContainer[Document.Paragraph]
    width: float
    height: float
    def __init__(self, document_settings: _Optional[_Union[Document.DocumentSettings, _Mapping]] = ..., document_attributes: _Optional[_Union[Document.DocumentAttributes, _Mapping]] = ..., list_settings: _Optional[_Iterable[_Union[Document.ListSettings, _Mapping]]] = ..., table_settings: _Optional[_Union[Document.TableSettings, _Mapping]] = ..., paragraphs: _Optional[_Iterable[_Union[Document.Paragraph, _Mapping]]] = ..., width: _Optional[float] = ..., height: _Optional[float] = ...) -> None: ...
