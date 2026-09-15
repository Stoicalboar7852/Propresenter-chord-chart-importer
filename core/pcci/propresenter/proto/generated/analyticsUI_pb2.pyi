from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Location(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOCATION_UNKNOWN: _ClassVar[Location]
    PRESENTATION: _ClassVar[Location]
    BIBLE_MODULE: _ClassVar[Location]

class SelectionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SELECTION_MODE_UNKNOWN: _ClassVar[SelectionMode]
    OBJECT: _ClassVar[SelectionMode]
    RANGE: _ClassVar[SelectionMode]
LOCATION_UNKNOWN: Location
PRESENTATION: Location
BIBLE_MODULE: Location
SELECTION_MODE_UNKNOWN: SelectionMode
OBJECT: SelectionMode
RANGE: SelectionMode

class QuickSearchShown(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[QuickSearchShown.Source]
        APPLICATION_MENU: _ClassVar[QuickSearchShown.Source]
        TOOLBAR: _ClassVar[QuickSearchShown.Source]
        UNLINKED_HEADER: _ClassVar[QuickSearchShown.Source]
    SOURCE_UNKNOWN: QuickSearchShown.Source
    APPLICATION_MENU: QuickSearchShown.Source
    TOOLBAR: QuickSearchShown.Source
    UNLINKED_HEADER: QuickSearchShown.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: QuickSearchShown.Source
    def __init__(self, source: _Optional[_Union[QuickSearchShown.Source, str]] = ...) -> None: ...

class QuickSearchSearch(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[QuickSearchSearch.Source]
        LIBRARY: _ClassVar[QuickSearchSearch.Source]
        SONG_SELECT: _ClassVar[QuickSearchSearch.Source]
        MULTI_TRACKS: _ClassVar[QuickSearchSearch.Source]
    SOURCE_UNKNOWN: QuickSearchSearch.Source
    LIBRARY: QuickSearchSearch.Source
    SONG_SELECT: QuickSearchSearch.Source
    MULTI_TRACKS: QuickSearchSearch.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: QuickSearchSearch.Source
    def __init__(self, source: _Optional[_Union[QuickSearchSearch.Source, str]] = ...) -> None: ...

class QuickSearchOpenItems(_message.Message):
    __slots__ = ("source", "style", "count")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[QuickSearchOpenItems.Source]
        LIBRARY: _ClassVar[QuickSearchOpenItems.Source]
        SONG_SELECT: _ClassVar[QuickSearchOpenItems.Source]
        MULTI_TRACKS: _ClassVar[QuickSearchOpenItems.Source]
    SOURCE_UNKNOWN: QuickSearchOpenItems.Source
    LIBRARY: QuickSearchOpenItems.Source
    SONG_SELECT: QuickSearchOpenItems.Source
    MULTI_TRACKS: QuickSearchOpenItems.Source
    class Style(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STYLE_UNKNOWN: _ClassVar[QuickSearchOpenItems.Style]
        STYLE_RETURN_KEY: _ClassVar[QuickSearchOpenItems.Style]
        COMMAND_RETURN_KEY: _ClassVar[QuickSearchOpenItems.Style]
        DRAG_DROP: _ClassVar[QuickSearchOpenItems.Style]
    STYLE_UNKNOWN: QuickSearchOpenItems.Style
    STYLE_RETURN_KEY: QuickSearchOpenItems.Style
    COMMAND_RETURN_KEY: QuickSearchOpenItems.Style
    DRAG_DROP: QuickSearchOpenItems.Style
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    source: QuickSearchOpenItems.Source
    style: QuickSearchOpenItems.Style
    count: int
    def __init__(self, source: _Optional[_Union[QuickSearchOpenItems.Source, str]] = ..., style: _Optional[_Union[QuickSearchOpenItems.Style, str]] = ..., count: _Optional[int] = ...) -> None: ...

class ToolbarThemeShown(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ToolbarThemeApplication(_message.Message):
    __slots__ = ("target",)
    class Target(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TARGET_UNKNOWN: _ClassVar[ToolbarThemeApplication.Target]
        SLIDE_SELECTION: _ClassVar[ToolbarThemeApplication.Target]
        PRESENTATION_SELECTION: _ClassVar[ToolbarThemeApplication.Target]
    TARGET_UNKNOWN: ToolbarThemeApplication.Target
    SLIDE_SELECTION: ToolbarThemeApplication.Target
    PRESENTATION_SELECTION: ToolbarThemeApplication.Target
    TARGET_FIELD_NUMBER: _ClassVar[int]
    target: ToolbarThemeApplication.Target
    def __init__(self, target: _Optional[_Union[ToolbarThemeApplication.Target, str]] = ...) -> None: ...

class MainViewShow(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[MainViewShow.Source]
        TOOLBAR: _ClassVar[MainViewShow.Source]
        APPLICATION_MENU: _ClassVar[MainViewShow.Source]
    SOURCE_UNKNOWN: MainViewShow.Source
    TOOLBAR: MainViewShow.Source
    APPLICATION_MENU: MainViewShow.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewShow.Source
    def __init__(self, source: _Optional[_Union[MainViewShow.Source, str]] = ...) -> None: ...

class MainViewPresentationEditor(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[MainViewPresentationEditor.Source]
        TOOLBAR: _ClassVar[MainViewPresentationEditor.Source]
        APPLICATION_MENU: _ClassVar[MainViewPresentationEditor.Source]
        CONTEXT_MENU: _ClassVar[MainViewPresentationEditor.Source]
    SOURCE_UNKNOWN: MainViewPresentationEditor.Source
    TOOLBAR: MainViewPresentationEditor.Source
    APPLICATION_MENU: MainViewPresentationEditor.Source
    CONTEXT_MENU: MainViewPresentationEditor.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewPresentationEditor.Source
    def __init__(self, source: _Optional[_Union[MainViewPresentationEditor.Source, str]] = ...) -> None: ...

class MainViewReflowEditor(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[MainViewReflowEditor.Source]
        TOOLBAR: _ClassVar[MainViewReflowEditor.Source]
        APPLICATION_MENU: _ClassVar[MainViewReflowEditor.Source]
        LIBRARY_CONTEXT_MENU: _ClassVar[MainViewReflowEditor.Source]
    SOURCE_UNKNOWN: MainViewReflowEditor.Source
    TOOLBAR: MainViewReflowEditor.Source
    APPLICATION_MENU: MainViewReflowEditor.Source
    LIBRARY_CONTEXT_MENU: MainViewReflowEditor.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewReflowEditor.Source
    def __init__(self, source: _Optional[_Union[MainViewReflowEditor.Source, str]] = ...) -> None: ...

class MainViewBible(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[MainViewBible.Source]
        TOOLBAR: _ClassVar[MainViewBible.Source]
        APPLICATION_MENU: _ClassVar[MainViewBible.Source]
    SOURCE_UNKNOWN: MainViewBible.Source
    TOOLBAR: MainViewBible.Source
    APPLICATION_MENU: MainViewBible.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewBible.Source
    def __init__(self, source: _Optional[_Union[MainViewBible.Source, str]] = ...) -> None: ...

class BibleTrigger(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: Location
    def __init__(self, location: _Optional[_Union[Location, str]] = ...) -> None: ...

class BibleGenerateSlides(_message.Message):
    __slots__ = ("translation_count", "slide_count", "verse_location", "reference_location", "show_verse_numbers", "break_new_verse", "display_translation", "preserve_font_color", "reference_style")
    class TextBoxLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TEXT_BOX_LOCATION_UNKNOWN: _ClassVar[BibleGenerateSlides.TextBoxLocation]
        LOCATION_NONE: _ClassVar[BibleGenerateSlides.TextBoxLocation]
        LOCATION_TEXT_BOX: _ClassVar[BibleGenerateSlides.TextBoxLocation]
        LOCATION_WITH_VERSE: _ClassVar[BibleGenerateSlides.TextBoxLocation]
    TEXT_BOX_LOCATION_UNKNOWN: BibleGenerateSlides.TextBoxLocation
    LOCATION_NONE: BibleGenerateSlides.TextBoxLocation
    LOCATION_TEXT_BOX: BibleGenerateSlides.TextBoxLocation
    LOCATION_WITH_VERSE: BibleGenerateSlides.TextBoxLocation
    class ReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REFERENCE_TYPE_UNKNOWN: _ClassVar[BibleGenerateSlides.ReferenceType]
        PASSAGE_NONE: _ClassVar[BibleGenerateSlides.ReferenceType]
        PASSAGE_EACH: _ClassVar[BibleGenerateSlides.ReferenceType]
        PASSAGE_LAST: _ClassVar[BibleGenerateSlides.ReferenceType]
        VERSE: _ClassVar[BibleGenerateSlides.ReferenceType]
    REFERENCE_TYPE_UNKNOWN: BibleGenerateSlides.ReferenceType
    PASSAGE_NONE: BibleGenerateSlides.ReferenceType
    PASSAGE_EACH: BibleGenerateSlides.ReferenceType
    PASSAGE_LAST: BibleGenerateSlides.ReferenceType
    VERSE: BibleGenerateSlides.ReferenceType
    TRANSLATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    SLIDE_COUNT_FIELD_NUMBER: _ClassVar[int]
    VERSE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SHOW_VERSE_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    BREAK_NEW_VERSE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    PRESERVE_FONT_COLOR_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_STYLE_FIELD_NUMBER: _ClassVar[int]
    translation_count: int
    slide_count: int
    verse_location: BibleGenerateSlides.TextBoxLocation
    reference_location: BibleGenerateSlides.TextBoxLocation
    show_verse_numbers: bool
    break_new_verse: bool
    display_translation: bool
    preserve_font_color: bool
    reference_style: BibleGenerateSlides.ReferenceType
    def __init__(self, translation_count: _Optional[int] = ..., slide_count: _Optional[int] = ..., verse_location: _Optional[_Union[BibleGenerateSlides.TextBoxLocation, str]] = ..., reference_location: _Optional[_Union[BibleGenerateSlides.TextBoxLocation, str]] = ..., show_verse_numbers: _Optional[bool] = ..., break_new_verse: _Optional[bool] = ..., display_translation: _Optional[bool] = ..., preserve_font_color: _Optional[bool] = ..., reference_style: _Optional[_Union[BibleGenerateSlides.ReferenceType, str]] = ...) -> None: ...

class BibleGenerateNext(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: Location
    def __init__(self, location: _Optional[_Union[Location, str]] = ...) -> None: ...

class BibleGeneratePrevious(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: Location
    def __init__(self, location: _Optional[_Union[Location, str]] = ...) -> None: ...

class BibleSaveSlides(_message.Message):
    __slots__ = ("destination",)
    class SlideDestination(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SLIDE_DESTINATION_UNKNOWN: _ClassVar[BibleSaveSlides.SlideDestination]
        SAVE_TO_LIBRARY: _ClassVar[BibleSaveSlides.SlideDestination]
        SAVE_TO_PLAYLIST: _ClassVar[BibleSaveSlides.SlideDestination]
        COPY_TO_PRESENTATION: _ClassVar[BibleSaveSlides.SlideDestination]
    SLIDE_DESTINATION_UNKNOWN: BibleSaveSlides.SlideDestination
    SAVE_TO_LIBRARY: BibleSaveSlides.SlideDestination
    SAVE_TO_PLAYLIST: BibleSaveSlides.SlideDestination
    COPY_TO_PRESENTATION: BibleSaveSlides.SlideDestination
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: BibleSaveSlides.SlideDestination
    def __init__(self, destination: _Optional[_Union[BibleSaveSlides.SlideDestination, str]] = ...) -> None: ...

class BibleLookup(_message.Message):
    __slots__ = ("location",)
    class Location(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOCATION_UNKNOWN: _ClassVar[BibleLookup.Location]
        TEXT_REFERENCE: _ClassVar[BibleLookup.Location]
        MENU_BOOK: _ClassVar[BibleLookup.Location]
        MENU_CHAPTER: _ClassVar[BibleLookup.Location]
        MENU_VERSE: _ClassVar[BibleLookup.Location]
        TEXT_SEARCH_CHAPTER: _ClassVar[BibleLookup.Location]
        TEXT_SEARCH_VERSE: _ClassVar[BibleLookup.Location]
    LOCATION_UNKNOWN: BibleLookup.Location
    TEXT_REFERENCE: BibleLookup.Location
    MENU_BOOK: BibleLookup.Location
    MENU_CHAPTER: BibleLookup.Location
    MENU_VERSE: BibleLookup.Location
    TEXT_SEARCH_CHAPTER: BibleLookup.Location
    TEXT_SEARCH_VERSE: BibleLookup.Location
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: BibleLookup.Location
    def __init__(self, location: _Optional[_Union[BibleLookup.Location, str]] = ...) -> None: ...

class BibleInstall(_message.Message):
    __slots__ = ("free_installed_count", "purchased_installed_count")
    FREE_INSTALLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    PURCHASED_INSTALLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    free_installed_count: int
    purchased_installed_count: int
    def __init__(self, free_installed_count: _Optional[int] = ..., purchased_installed_count: _Optional[int] = ...) -> None: ...

class BibleRemove(_message.Message):
    __slots__ = ("free_installed_count", "purchased_installed_count")
    FREE_INSTALLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    PURCHASED_INSTALLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    free_installed_count: int
    purchased_installed_count: int
    def __init__(self, free_installed_count: _Optional[int] = ..., purchased_installed_count: _Optional[int] = ...) -> None: ...

class BibleStartup(_message.Message):
    __slots__ = ("free_installed_count", "purchased_installed_count")
    FREE_INSTALLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    PURCHASED_INSTALLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    free_installed_count: int
    purchased_installed_count: int
    def __init__(self, free_installed_count: _Optional[int] = ..., purchased_installed_count: _Optional[int] = ...) -> None: ...

class MainViewMaskEditor(_message.Message):
    __slots__ = ("source",)
    class MaskSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MASK_SOURCE_UNKNOWN: _ClassVar[MainViewMaskEditor.MaskSource]
        TOOLBAR: _ClassVar[MainViewMaskEditor.MaskSource]
        LOOKS_WINDOW: _ClassVar[MainViewMaskEditor.MaskSource]
    MASK_SOURCE_UNKNOWN: MainViewMaskEditor.MaskSource
    TOOLBAR: MainViewMaskEditor.MaskSource
    LOOKS_WINDOW: MainViewMaskEditor.MaskSource
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewMaskEditor.MaskSource
    def __init__(self, source: _Optional[_Union[MainViewMaskEditor.MaskSource, str]] = ...) -> None: ...

class MainViewStageEditor(_message.Message):
    __slots__ = ("source",)
    class StageSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STAGE_SOURCE_UNKNOWN: _ClassVar[MainViewStageEditor.StageSource]
        TOOLBAR: _ClassVar[MainViewStageEditor.StageSource]
        APPLICATION_MENU: _ClassVar[MainViewStageEditor.StageSource]
        LOWER_RIGHT: _ClassVar[MainViewStageEditor.StageSource]
    STAGE_SOURCE_UNKNOWN: MainViewStageEditor.StageSource
    TOOLBAR: MainViewStageEditor.StageSource
    APPLICATION_MENU: MainViewStageEditor.StageSource
    LOWER_RIGHT: MainViewStageEditor.StageSource
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewStageEditor.StageSource
    def __init__(self, source: _Optional[_Union[MainViewStageEditor.StageSource, str]] = ...) -> None: ...

class MainViewThemeEditor(_message.Message):
    __slots__ = ("source",)
    class ThemeSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STAGE_SOURCE_UNKNOWN: _ClassVar[MainViewThemeEditor.ThemeSource]
        TOOLBAR: _ClassVar[MainViewThemeEditor.ThemeSource]
        THEME_CONTEXT_MENU: _ClassVar[MainViewThemeEditor.ThemeSource]
    STAGE_SOURCE_UNKNOWN: MainViewThemeEditor.ThemeSource
    TOOLBAR: MainViewThemeEditor.ThemeSource
    THEME_CONTEXT_MENU: MainViewThemeEditor.ThemeSource
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewThemeEditor.ThemeSource
    def __init__(self, source: _Optional[_Union[MainViewThemeEditor.ThemeSource, str]] = ...) -> None: ...

class MainViewCopyrightEditor(_message.Message):
    __slots__ = ("source",)
    class CopyrightSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COPYRIGHT_SOURCE_UNKNOWN: _ClassVar[MainViewCopyrightEditor.CopyrightSource]
        TOOLBAR: _ClassVar[MainViewCopyrightEditor.CopyrightSource]
        PREFERENCE: _ClassVar[MainViewCopyrightEditor.CopyrightSource]
    COPYRIGHT_SOURCE_UNKNOWN: MainViewCopyrightEditor.CopyrightSource
    TOOLBAR: MainViewCopyrightEditor.CopyrightSource
    PREFERENCE: MainViewCopyrightEditor.CopyrightSource
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewCopyrightEditor.CopyrightSource
    def __init__(self, source: _Optional[_Union[MainViewCopyrightEditor.CopyrightSource, str]] = ...) -> None: ...

class MainViewPropsEditor(_message.Message):
    __slots__ = ("source",)
    class PropsSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PROPS_SOURCE_UNKNOWN: _ClassVar[MainViewPropsEditor.PropsSource]
        TOOLBAR: _ClassVar[MainViewPropsEditor.PropsSource]
        LOWER_RIGHT: _ClassVar[MainViewPropsEditor.PropsSource]
    PROPS_SOURCE_UNKNOWN: MainViewPropsEditor.PropsSource
    TOOLBAR: MainViewPropsEditor.PropsSource
    LOWER_RIGHT: MainViewPropsEditor.PropsSource
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: MainViewPropsEditor.PropsSource
    def __init__(self, source: _Optional[_Union[MainViewPropsEditor.PropsSource, str]] = ...) -> None: ...

class LowerRightTimers(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightTimersCollapse(_message.Message):
    __slots__ = ("state",)
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNKNOWN: _ClassVar[LowerRightTimersCollapse.State]
        COLLAPSED: _ClassVar[LowerRightTimersCollapse.State]
        EXPANDED: _ClassVar[LowerRightTimersCollapse.State]
    STATE_UNKNOWN: LowerRightTimersCollapse.State
    COLLAPSED: LowerRightTimersCollapse.State
    EXPANDED: LowerRightTimersCollapse.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: LowerRightTimersCollapse.State
    def __init__(self, state: _Optional[_Union[LowerRightTimersCollapse.State, str]] = ...) -> None: ...

class LowerRightTimersEdit(_message.Message):
    __slots__ = ("field",)
    class Field(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FIELD_UNKNOWN: _ClassVar[LowerRightTimersEdit.Field]
        TYPE: _ClassVar[LowerRightTimersEdit.Field]
        VALUE: _ClassVar[LowerRightTimersEdit.Field]
        OVERRUN: _ClassVar[LowerRightTimersEdit.Field]
        NAME: _ClassVar[LowerRightTimersEdit.Field]
    FIELD_UNKNOWN: LowerRightTimersEdit.Field
    TYPE: LowerRightTimersEdit.Field
    VALUE: LowerRightTimersEdit.Field
    OVERRUN: LowerRightTimersEdit.Field
    NAME: LowerRightTimersEdit.Field
    FIELD_FIELD_NUMBER: _ClassVar[int]
    field: LowerRightTimersEdit.Field
    def __init__(self, field: _Optional[_Union[LowerRightTimersEdit.Field, str]] = ...) -> None: ...

class LowerRightTimersState(_message.Message):
    __slots__ = ("state",)
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNKNOWN: _ClassVar[LowerRightTimersState.State]
        START: _ClassVar[LowerRightTimersState.State]
        STOP: _ClassVar[LowerRightTimersState.State]
        RESET: _ClassVar[LowerRightTimersState.State]
    STATE_UNKNOWN: LowerRightTimersState.State
    START: LowerRightTimersState.State
    STOP: LowerRightTimersState.State
    RESET: LowerRightTimersState.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: LowerRightTimersState.State
    def __init__(self, state: _Optional[_Union[LowerRightTimersState.State, str]] = ...) -> None: ...

class LowerRightTimersCreate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightTimersDelete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightMessages(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightMessagesEdit(_message.Message):
    __slots__ = ("action",)
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACTION_UNKNOWN: _ClassVar[LowerRightMessagesEdit.Action]
        ADD_TEXT_TOKEN: _ClassVar[LowerRightMessagesEdit.Action]
        ADD_TIMER_TOKEN: _ClassVar[LowerRightMessagesEdit.Action]
        ADD_CUSTOM_TOKEN: _ClassVar[LowerRightMessagesEdit.Action]
        SET_THEME: _ClassVar[LowerRightMessagesEdit.Action]
        SET_TEXT: _ClassVar[LowerRightMessagesEdit.Action]
        SET_WEB_NOTIFICATION: _ClassVar[LowerRightMessagesEdit.Action]
        SET_DISMISS_BEHAVIOR: _ClassVar[LowerRightMessagesEdit.Action]
    ACTION_UNKNOWN: LowerRightMessagesEdit.Action
    ADD_TEXT_TOKEN: LowerRightMessagesEdit.Action
    ADD_TIMER_TOKEN: LowerRightMessagesEdit.Action
    ADD_CUSTOM_TOKEN: LowerRightMessagesEdit.Action
    SET_THEME: LowerRightMessagesEdit.Action
    SET_TEXT: LowerRightMessagesEdit.Action
    SET_WEB_NOTIFICATION: LowerRightMessagesEdit.Action
    SET_DISMISS_BEHAVIOR: LowerRightMessagesEdit.Action
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: LowerRightMessagesEdit.Action
    def __init__(self, action: _Optional[_Union[LowerRightMessagesEdit.Action, str]] = ...) -> None: ...

class LowerRightMessagesState(_message.Message):
    __slots__ = ("state",)
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNKNOWN: _ClassVar[LowerRightMessagesState.State]
        SHOW: _ClassVar[LowerRightMessagesState.State]
        CLEAR: _ClassVar[LowerRightMessagesState.State]
    STATE_UNKNOWN: LowerRightMessagesState.State
    SHOW: LowerRightMessagesState.State
    CLEAR: LowerRightMessagesState.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: LowerRightMessagesState.State
    def __init__(self, state: _Optional[_Union[LowerRightMessagesState.State, str]] = ...) -> None: ...

class LowerRightMessagesCreate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightMessagesDelete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightProps(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightPropsTransition(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightPropsCreate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightPropsDelete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightPropsState(_message.Message):
    __slots__ = ("state",)
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNKNOWN: _ClassVar[LowerRightPropsState.State]
        SHOW: _ClassVar[LowerRightPropsState.State]
        CLEAR: _ClassVar[LowerRightPropsState.State]
    STATE_UNKNOWN: LowerRightPropsState.State
    SHOW: LowerRightPropsState.State
    CLEAR: LowerRightPropsState.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: LowerRightPropsState.State
    def __init__(self, state: _Optional[_Union[LowerRightPropsState.State, str]] = ...) -> None: ...

class LowerRightStage(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightStageChangeLayout(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightStageConfigureScreens(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightStageEditLayouts(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightStageMessageState(_message.Message):
    __slots__ = ("state",)
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNKNOWN: _ClassVar[LowerRightStageMessageState.State]
        SHOW: _ClassVar[LowerRightStageMessageState.State]
        CLEAR: _ClassVar[LowerRightStageMessageState.State]
    STATE_UNKNOWN: LowerRightStageMessageState.State
    SHOW: LowerRightStageMessageState.State
    CLEAR: LowerRightStageMessageState.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: LowerRightStageMessageState.State
    def __init__(self, state: _Optional[_Union[LowerRightStageMessageState.State, str]] = ...) -> None: ...

class LowerRightMacros(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightMacrosTrigger(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightMacrosCreate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LowerRightMacrosDelete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TextInspector(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TextInspectorScrollingText(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: _Optional[bool] = ...) -> None: ...

class TextInspectorForeground(_message.Message):
    __slots__ = ("fill_type", "selection_mode")
    class FillType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FILL_TYPE_UNKNOWN: _ClassVar[TextInspectorForeground.FillType]
        SOLID: _ClassVar[TextInspectorForeground.FillType]
        GRADIENT: _ClassVar[TextInspectorForeground.FillType]
    FILL_TYPE_UNKNOWN: TextInspectorForeground.FillType
    SOLID: TextInspectorForeground.FillType
    GRADIENT: TextInspectorForeground.FillType
    FILL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SELECTION_MODE_FIELD_NUMBER: _ClassVar[int]
    fill_type: TextInspectorForeground.FillType
    selection_mode: SelectionMode
    def __init__(self, fill_type: _Optional[_Union[TextInspectorForeground.FillType, str]] = ..., selection_mode: _Optional[_Union[SelectionMode, str]] = ...) -> None: ...

class TextInspectorUnderlineColor(_message.Message):
    __slots__ = ("is_enabled", "selection_mode")
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SELECTION_MODE_FIELD_NUMBER: _ClassVar[int]
    is_enabled: bool
    selection_mode: SelectionMode
    def __init__(self, is_enabled: _Optional[bool] = ..., selection_mode: _Optional[_Union[SelectionMode, str]] = ...) -> None: ...

class TextInspectorBackgroundColor(_message.Message):
    __slots__ = ("color_type", "selection_mode")
    class ColorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COLOR_TYPE_UNKNOWN: _ClassVar[TextInspectorBackgroundColor.ColorType]
        CLEAR: _ClassVar[TextInspectorBackgroundColor.ColorType]
        OTHER: _ClassVar[TextInspectorBackgroundColor.ColorType]
    COLOR_TYPE_UNKNOWN: TextInspectorBackgroundColor.ColorType
    CLEAR: TextInspectorBackgroundColor.ColorType
    OTHER: TextInspectorBackgroundColor.ColorType
    COLOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    SELECTION_MODE_FIELD_NUMBER: _ClassVar[int]
    color_type: TextInspectorBackgroundColor.ColorType
    selection_mode: SelectionMode
    def __init__(self, color_type: _Optional[_Union[TextInspectorBackgroundColor.ColorType, str]] = ..., selection_mode: _Optional[_Union[SelectionMode, str]] = ...) -> None: ...

class TextInspectorLineTransform(_message.Message):
    __slots__ = ("transform_type",)
    class TransformType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TRANSFORM_TYPE_UNKNOWN: _ClassVar[TextInspectorLineTransform.TransformType]
        NONE: _ClassVar[TextInspectorLineTransform.TransformType]
        REMOVE_LINE_RETURNS: _ClassVar[TextInspectorLineTransform.TransformType]
        REPLACE_LINE_RETURNS: _ClassVar[TextInspectorLineTransform.TransformType]
        ONE_WORD_PER_LINE: _ClassVar[TextInspectorLineTransform.TransformType]
        ONE_CHARACTER_PER_LINE: _ClassVar[TextInspectorLineTransform.TransformType]
    TRANSFORM_TYPE_UNKNOWN: TextInspectorLineTransform.TransformType
    NONE: TextInspectorLineTransform.TransformType
    REMOVE_LINE_RETURNS: TextInspectorLineTransform.TransformType
    REPLACE_LINE_RETURNS: TextInspectorLineTransform.TransformType
    ONE_WORD_PER_LINE: TextInspectorLineTransform.TransformType
    ONE_CHARACTER_PER_LINE: TextInspectorLineTransform.TransformType
    TRANSFORM_TYPE_FIELD_NUMBER: _ClassVar[int]
    transform_type: TextInspectorLineTransform.TransformType
    def __init__(self, transform_type: _Optional[_Union[TextInspectorLineTransform.TransformType, str]] = ...) -> None: ...

class ShowSlideLabel(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ShowSlideLabelChange(_message.Message):
    __slots__ = ("number_of_slides", "source")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[ShowSlideLabelChange.Source]
        CONTEXT_MENU: _ClassVar[ShowSlideLabelChange.Source]
        POPOVER: _ClassVar[ShowSlideLabelChange.Source]
    SOURCE_UNKNOWN: ShowSlideLabelChange.Source
    CONTEXT_MENU: ShowSlideLabelChange.Source
    POPOVER: ShowSlideLabelChange.Source
    NUMBER_OF_SLIDES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    number_of_slides: int
    source: ShowSlideLabelChange.Source
    def __init__(self, number_of_slides: _Optional[int] = ..., source: _Optional[_Union[ShowSlideLabelChange.Source, str]] = ...) -> None: ...

class EditorOverlayShown(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[EditorOverlayShown.Source]
        DOUBLE_CLICK: _ClassVar[EditorOverlayShown.Source]
        CONTEXTUAL_MENU: _ClassVar[EditorOverlayShown.Source]
        PLUS_BUTTON_MENU: _ClassVar[EditorOverlayShown.Source]
    SOURCE_UNKNOWN: EditorOverlayShown.Source
    DOUBLE_CLICK: EditorOverlayShown.Source
    CONTEXTUAL_MENU: EditorOverlayShown.Source
    PLUS_BUTTON_MENU: EditorOverlayShown.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: EditorOverlayShown.Source
    def __init__(self, source: _Optional[_Union[EditorOverlayShown.Source, str]] = ...) -> None: ...

class EditorOverlayClosed(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[EditorOverlayClosed.Source]
        CLICK_OFF_ELEMENT: _ClassVar[EditorOverlayClosed.Source]
        ESCAPE_KEY: _ClassVar[EditorOverlayClosed.Source]
        CLOSE_BUTTON: _ClassVar[EditorOverlayClosed.Source]
    SOURCE_UNKNOWN: EditorOverlayClosed.Source
    CLICK_OFF_ELEMENT: EditorOverlayClosed.Source
    ESCAPE_KEY: EditorOverlayClosed.Source
    CLOSE_BUTTON: EditorOverlayClosed.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: EditorOverlayClosed.Source
    def __init__(self, source: _Optional[_Union[EditorOverlayClosed.Source, str]] = ...) -> None: ...

class WhatsNewViewed(_message.Message):
    __slots__ = ("version", "view_time")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    VIEW_TIME_FIELD_NUMBER: _ClassVar[int]
    version: str
    view_time: int
    def __init__(self, version: _Optional[str] = ..., view_time: _Optional[int] = ...) -> None: ...

class ClearGroups(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[ClearGroups.Source]
        APPLICATION_MENU: _ClassVar[ClearGroups.Source]
        PREVIEW_MENU: _ClassVar[ClearGroups.Source]
        ACTION_MENU: _ClassVar[ClearGroups.Source]
    SOURCE_UNKNOWN: ClearGroups.Source
    APPLICATION_MENU: ClearGroups.Source
    PREVIEW_MENU: ClearGroups.Source
    ACTION_MENU: ClearGroups.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: ClearGroups.Source
    def __init__(self, source: _Optional[_Union[ClearGroups.Source, str]] = ...) -> None: ...

class ClearGroupsCreate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClearGroupsDelete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClearGroupsChangeVisibility(_message.Message):
    __slots__ = ("visibility",)
    class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        VISIBILITY_UNKNOWN: _ClassVar[ClearGroupsChangeVisibility.Visibility]
        SHOWN: _ClassVar[ClearGroupsChangeVisibility.Visibility]
        HIDDEN: _ClassVar[ClearGroupsChangeVisibility.Visibility]
    VISIBILITY_UNKNOWN: ClearGroupsChangeVisibility.Visibility
    SHOWN: ClearGroupsChangeVisibility.Visibility
    HIDDEN: ClearGroupsChangeVisibility.Visibility
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    visibility: ClearGroupsChangeVisibility.Visibility
    def __init__(self, visibility: _Optional[_Union[ClearGroupsChangeVisibility.Visibility, str]] = ...) -> None: ...

class ClearGroupsChangeIcon(_message.Message):
    __slots__ = ("icon_type", "is_tinted")
    class IconType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ICON_TYPE_UNKNOWN: _ClassVar[ClearGroupsChangeIcon.IconType]
        DEFAULT: _ClassVar[ClearGroupsChangeIcon.IconType]
        CUSTOM: _ClassVar[ClearGroupsChangeIcon.IconType]
    ICON_TYPE_UNKNOWN: ClearGroupsChangeIcon.IconType
    DEFAULT: ClearGroupsChangeIcon.IconType
    CUSTOM: ClearGroupsChangeIcon.IconType
    ICON_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_TINTED_FIELD_NUMBER: _ClassVar[int]
    icon_type: ClearGroupsChangeIcon.IconType
    is_tinted: bool
    def __init__(self, icon_type: _Optional[_Union[ClearGroupsChangeIcon.IconType, str]] = ..., is_tinted: _Optional[bool] = ...) -> None: ...

class PreviewAreaClearGroupsTrigger(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PreviewAreaClearGroupsChanged(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class PlaceholderLink(_message.Message):
    __slots__ = ("link_type", "link_source")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[PlaceholderLink.Type]
        PRESENTATION: _ClassVar[PlaceholderLink.Type]
        MEDIA: _ClassVar[PlaceholderLink.Type]
        EXTERNAL_PRESENTATION: _ClassVar[PlaceholderLink.Type]
    TYPE_UNKNOWN: PlaceholderLink.Type
    PRESENTATION: PlaceholderLink.Type
    MEDIA: PlaceholderLink.Type
    EXTERNAL_PRESENTATION: PlaceholderLink.Type
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[PlaceholderLink.Source]
        QUICK_SEARCH: _ClassVar[PlaceholderLink.Source]
        IMPORT_BUTTON: _ClassVar[PlaceholderLink.Source]
        CREATE_BUTTON: _ClassVar[PlaceholderLink.Source]
        DRAG_DROP: _ClassVar[PlaceholderLink.Source]
        AUTOMATIC: _ClassVar[PlaceholderLink.Source]
    SOURCE_UNKNOWN: PlaceholderLink.Source
    QUICK_SEARCH: PlaceholderLink.Source
    IMPORT_BUTTON: PlaceholderLink.Source
    CREATE_BUTTON: PlaceholderLink.Source
    DRAG_DROP: PlaceholderLink.Source
    AUTOMATIC: PlaceholderLink.Source
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    LINK_SOURCE_FIELD_NUMBER: _ClassVar[int]
    link_type: PlaceholderLink.Type
    link_source: PlaceholderLink.Source
    def __init__(self, link_type: _Optional[_Union[PlaceholderLink.Type, str]] = ..., link_source: _Optional[_Union[PlaceholderLink.Source, str]] = ...) -> None: ...

class PlaceholderUnlink(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PlanningCenterLive(_message.Message):
    __slots__ = ("window_type",)
    class WindowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        WINDOW_TYPE_UNKNOWN: _ClassVar[PlanningCenterLive.WindowType]
        DOCKED: _ClassVar[PlanningCenterLive.WindowType]
        FLOATING: _ClassVar[PlanningCenterLive.WindowType]
    WINDOW_TYPE_UNKNOWN: PlanningCenterLive.WindowType
    DOCKED: PlanningCenterLive.WindowType
    FLOATING: PlanningCenterLive.WindowType
    WINDOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    window_type: PlanningCenterLive.WindowType
    def __init__(self, window_type: _Optional[_Union[PlanningCenterLive.WindowType, str]] = ...) -> None: ...

class NetworkGroupAdd(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NetworkGroupRemove(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NetworkGroupLeave(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CcliReportReset(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CcliReportShown(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Capture(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[Capture.Source]
        TOOLBAR: _ClassVar[Capture.Source]
        ACTION_POPOVER: _ClassVar[Capture.Source]
        ACTION_CONTEXTUAL_MENU: _ClassVar[Capture.Source]
        CALENDAR: _ClassVar[Capture.Source]
        PREFERENCES_RESI: _ClassVar[Capture.Source]
        MAIN_MENU: _ClassVar[Capture.Source]
    SOURCE_UNKNOWN: Capture.Source
    TOOLBAR: Capture.Source
    ACTION_POPOVER: Capture.Source
    ACTION_CONTEXTUAL_MENU: Capture.Source
    CALENDAR: Capture.Source
    PREFERENCES_RESI: Capture.Source
    MAIN_MENU: Capture.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: Capture.Source
    def __init__(self, source: _Optional[_Union[Capture.Source, str]] = ...) -> None: ...

class Welcome(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FIRST_LAUNCH: _ClassVar[Welcome.Source]
        APPLICATION_MENU: _ClassVar[Welcome.Source]
    FIRST_LAUNCH: Welcome.Source
    APPLICATION_MENU: Welcome.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: Welcome.Source
    def __init__(self, source: _Optional[_Union[Welcome.Source, str]] = ...) -> None: ...

class WelcomeScreenConfigurationHelp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeDownloadSampleContent(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeUserGroup(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeTutorials(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeKnowledgeBase(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeBlog(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeInstagram(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeFacebook(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WelcomeMigration(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestPatterns(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        APPLICATION_MENU: _ClassVar[TestPatterns.Source]
        SCREEN_CONFIGURATION: _ClassVar[TestPatterns.Source]
    APPLICATION_MENU: TestPatterns.Source
    SCREEN_CONFIGURATION: TestPatterns.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: TestPatterns.Source
    def __init__(self, source: _Optional[_Union[TestPatterns.Source, str]] = ...) -> None: ...

class SettingsCustomLogo(_message.Message):
    __slots__ = ("has_logo",)
    HAS_LOGO_FIELD_NUMBER: _ClassVar[int]
    has_logo: bool
    def __init__(self, has_logo: _Optional[bool] = ...) -> None: ...

class WindowedOutputCreated(_message.Message):
    __slots__ = ("screen_type", "num_active_windowed_outputs")
    class ScreenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AUDIENCE: _ClassVar[WindowedOutputCreated.ScreenType]
        STAGE: _ClassVar[WindowedOutputCreated.ScreenType]
    AUDIENCE: WindowedOutputCreated.ScreenType
    STAGE: WindowedOutputCreated.ScreenType
    SCREEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_ACTIVE_WINDOWED_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    screen_type: WindowedOutputCreated.ScreenType
    num_active_windowed_outputs: int
    def __init__(self, screen_type: _Optional[_Union[WindowedOutputCreated.ScreenType, str]] = ..., num_active_windowed_outputs: _Optional[int] = ...) -> None: ...

class ActivationFlowOpened(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOURCE_UNKNOWN: _ClassVar[ActivationFlowOpened.Source]
        LAUNCH_ALERT: _ClassVar[ActivationFlowOpened.Source]
        STATUS_TOOLBAR_POPOVER: _ClassVar[ActivationFlowOpened.Source]
        PREFERENCES: _ClassVar[ActivationFlowOpened.Source]
        CLOUD_ONBOARDING: _ClassVar[ActivationFlowOpened.Source]
    SOURCE_UNKNOWN: ActivationFlowOpened.Source
    LAUNCH_ALERT: ActivationFlowOpened.Source
    STATUS_TOOLBAR_POPOVER: ActivationFlowOpened.Source
    PREFERENCES: ActivationFlowOpened.Source
    CLOUD_ONBOARDING: ActivationFlowOpened.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: ActivationFlowOpened.Source
    def __init__(self, source: _Optional[_Union[ActivationFlowOpened.Source, str]] = ...) -> None: ...
