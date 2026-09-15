import action_pb2 as _action_pb2
import alphaType_pb2 as _alphaType_pb2
import ccli_pb2 as _ccli_pb2
import color_pb2 as _color_pb2
import cue_pb2 as _cue_pb2
import effects_pb2 as _effects_pb2
import graphicsData_pb2 as _graphicsData_pb2
import input_pb2 as _input_pb2
import macros_pb2 as _macros_pb2
import messages_pb2 as _messages_pb2
import playlist_pb2 as _playlist_pb2
import preferences_pb2 as _preferences_pb2
import presentation_pb2 as _presentation_pb2
import proCoreTestPatterns_pb2 as _proCoreTestPatterns_pb2
import propDocument_pb2 as _propDocument_pb2
import propresenter_pb2 as _propresenter_pb2
import slide_pb2 as _slide_pb2
import recording_pb2 as _recording_pb2
import stage_pb2 as _stage_pb2
import timers_pb2 as _timers_pb2
import url_pb2 as _url_pb2
import uuid_pb2 as _uuid_pb2
import proworkspace_pb2 as _proworkspace_pb2
import psbWorkspace_pb2 as _psbWorkspace_pb2
import digitalAudio_pb2 as _digitalAudio_pb2
import proAudienceLook_pb2 as _proAudienceLook_pb2
import proMask_pb2 as _proMask_pb2
import timedPlayback_pb2 as _timedPlayback_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NetworkIdentifier(_message.Message):
    __slots__ = ("identifiers",)
    class IndexOrName(_message.Message):
        __slots__ = ("index", "name")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        index: int
        name: str
        def __init__(self, index: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    identifiers: _containers.RepeatedCompositeFieldContainer[NetworkIdentifier.IndexOrName]
    def __init__(self, identifiers: _Optional[_Iterable[_Union[NetworkIdentifier.IndexOrName, _Mapping]]] = ...) -> None: ...

class TriggerOptions(_message.Message):
    __slots__ = ("content_destination", "suppress_auto_start_video", "suppress_media_background", "force_retrigger", "reset_chord_chart", "from_playlist_library", "from_timeline", "ignore_analytics", "start_position", "trigger_source", "network_identifier", "request_client_context", "follow_timecode", "timecode_offset")
    CONTENT_DESTINATION_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_AUTO_START_VIDEO_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_MEDIA_BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    FORCE_RETRIGGER_FIELD_NUMBER: _ClassVar[int]
    RESET_CHORD_CHART_FIELD_NUMBER: _ClassVar[int]
    FROM_PLAYLIST_LIBRARY_FIELD_NUMBER: _ClassVar[int]
    FROM_TIMELINE_FIELD_NUMBER: _ClassVar[int]
    IGNORE_ANALYTICS_FIELD_NUMBER: _ClassVar[int]
    START_POSITION_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CLIENT_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    FOLLOW_TIMECODE_FIELD_NUMBER: _ClassVar[int]
    TIMECODE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    content_destination: _action_pb2.Action.ContentDestination
    suppress_auto_start_video: bool
    suppress_media_background: bool
    force_retrigger: bool
    reset_chord_chart: bool
    from_playlist_library: bool
    from_timeline: bool
    ignore_analytics: bool
    start_position: float
    trigger_source: _timedPlayback_pb2.TriggerSource
    network_identifier: NetworkIdentifier
    request_client_context: bool
    follow_timecode: bool
    timecode_offset: float
    def __init__(self, content_destination: _Optional[_Union[_action_pb2.Action.ContentDestination, str]] = ..., suppress_auto_start_video: _Optional[bool] = ..., suppress_media_background: _Optional[bool] = ..., force_retrigger: _Optional[bool] = ..., reset_chord_chart: _Optional[bool] = ..., from_playlist_library: _Optional[bool] = ..., from_timeline: _Optional[bool] = ..., ignore_analytics: _Optional[bool] = ..., start_position: _Optional[float] = ..., trigger_source: _Optional[_Union[_timedPlayback_pb2.TriggerSource, _Mapping]] = ..., network_identifier: _Optional[_Union[NetworkIdentifier, _Mapping]] = ..., request_client_context: _Optional[bool] = ..., follow_timecode: _Optional[bool] = ..., timecode_offset: _Optional[float] = ...) -> None: ...

class ControlTransport(_message.Message):
    __slots__ = ("play", "pause", "rewind", "fastforward", "skip_back", "skip_forward", "step_back", "step_forward", "go_to_start", "go_to_end", "jump_to_time", "jump_to_percent", "mark_in", "mark_out", "set_scale_mode", "set_flipped_mode", "set_play_rate", "set_rotation", "toggle_playback", "set_effects", "update_effect", "begin_scrub", "end_scrub", "scrub_to_time", "scrub_to_percent", "set_audio_fade", "set_audio_properties", "set_alpha_type")
    class PlayControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class PauseControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class RewindControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class FastForwardControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class SkipBackControlType(_message.Message):
        __slots__ = ("offset",)
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        offset: float
        def __init__(self, offset: _Optional[float] = ...) -> None: ...
    class SkipForwardControlType(_message.Message):
        __slots__ = ("offset",)
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        offset: float
        def __init__(self, offset: _Optional[float] = ...) -> None: ...
    class StepBackControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class StepForwardControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class GoToStartControlType(_message.Message):
        __slots__ = ("offset",)
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        offset: float
        def __init__(self, offset: _Optional[float] = ...) -> None: ...
    class GoToEndControlType(_message.Message):
        __slots__ = ("offset",)
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        offset: float
        def __init__(self, offset: _Optional[float] = ...) -> None: ...
    class JumpToTimeControlType(_message.Message):
        __slots__ = ("time",)
        TIME_FIELD_NUMBER: _ClassVar[int]
        time: float
        def __init__(self, time: _Optional[float] = ...) -> None: ...
    class JumpToPercentControlType(_message.Message):
        __slots__ = ("percent",)
        PERCENT_FIELD_NUMBER: _ClassVar[int]
        percent: float
        def __init__(self, percent: _Optional[float] = ...) -> None: ...
    class MarkInPointControlType(_message.Message):
        __slots__ = ("time",)
        TIME_FIELD_NUMBER: _ClassVar[int]
        time: float
        def __init__(self, time: _Optional[float] = ...) -> None: ...
    class MarkOutPointControlType(_message.Message):
        __slots__ = ("time",)
        TIME_FIELD_NUMBER: _ClassVar[int]
        time: float
        def __init__(self, time: _Optional[float] = ...) -> None: ...
    class SetScaleModeControlType(_message.Message):
        __slots__ = ("mode", "is_blurred", "alignment")
        MODE_FIELD_NUMBER: _ClassVar[int]
        IS_BLURRED_FIELD_NUMBER: _ClassVar[int]
        ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
        mode: _graphicsData_pb2.Media.ScaleBehavior
        is_blurred: bool
        alignment: _graphicsData_pb2.Media.ScaleAlignment
        def __init__(self, mode: _Optional[_Union[_graphicsData_pb2.Media.ScaleBehavior, str]] = ..., is_blurred: _Optional[bool] = ..., alignment: _Optional[_Union[_graphicsData_pb2.Media.ScaleAlignment, str]] = ...) -> None: ...
    class SetFlippedModeControlType(_message.Message):
        __slots__ = ("horizontal", "vertical")
        HORIZONTAL_FIELD_NUMBER: _ClassVar[int]
        VERTICAL_FIELD_NUMBER: _ClassVar[int]
        horizontal: bool
        vertical: bool
        def __init__(self, horizontal: _Optional[bool] = ..., vertical: _Optional[bool] = ...) -> None: ...
    class SetPlayRateControlType(_message.Message):
        __slots__ = ("play_rate",)
        PLAY_RATE_FIELD_NUMBER: _ClassVar[int]
        play_rate: float
        def __init__(self, play_rate: _Optional[float] = ...) -> None: ...
    class SetNativeRotationControlType(_message.Message):
        __slots__ = ("rotation",)
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        rotation: _graphicsData_pb2.Media.DrawingProperties.NativeRotationType
        def __init__(self, rotation: _Optional[_Union[_graphicsData_pb2.Media.DrawingProperties.NativeRotationType, str]] = ...) -> None: ...
    class SetAlphaTypeControlType(_message.Message):
        __slots__ = ("alpha_type",)
        ALPHA_TYPE_FIELD_NUMBER: _ClassVar[int]
        alpha_type: _alphaType_pb2.AlphaType
        def __init__(self, alpha_type: _Optional[_Union[_alphaType_pb2.AlphaType, str]] = ...) -> None: ...
    class TogglePlaybackControlType(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class SetEffectsControlType(_message.Message):
        __slots__ = ("effects",)
        EFFECTS_FIELD_NUMBER: _ClassVar[int]
        effects: _containers.RepeatedCompositeFieldContainer[_effects_pb2.Effect]
        def __init__(self, effects: _Optional[_Iterable[_Union[_effects_pb2.Effect, _Mapping]]] = ...) -> None: ...
    class UpdateEffectControlType(_message.Message):
        __slots__ = ("effect",)
        EFFECT_FIELD_NUMBER: _ClassVar[int]
        effect: _effects_pb2.Effect
        def __init__(self, effect: _Optional[_Union[_effects_pb2.Effect, _Mapping]] = ...) -> None: ...
    class BeginScrubControlType(_message.Message):
        __slots__ = ("time",)
        TIME_FIELD_NUMBER: _ClassVar[int]
        time: float
        def __init__(self, time: _Optional[float] = ...) -> None: ...
    class EndScrubControlType(_message.Message):
        __slots__ = ("time",)
        TIME_FIELD_NUMBER: _ClassVar[int]
        time: float
        def __init__(self, time: _Optional[float] = ...) -> None: ...
    class ScrubToTimeControlType(_message.Message):
        __slots__ = ("time",)
        TIME_FIELD_NUMBER: _ClassVar[int]
        time: float
        def __init__(self, time: _Optional[float] = ...) -> None: ...
    class ScrubToPercentControlType(_message.Message):
        __slots__ = ("percent",)
        PERCENT_FIELD_NUMBER: _ClassVar[int]
        percent: float
        def __init__(self, percent: _Optional[float] = ...) -> None: ...
    class SetAudioFadeType(_message.Message):
        __slots__ = ("fade_in_duration", "fade_out_duration", "should_fade_in", "should_fade_out")
        FADE_IN_DURATION_FIELD_NUMBER: _ClassVar[int]
        FADE_OUT_DURATION_FIELD_NUMBER: _ClassVar[int]
        SHOULD_FADE_IN_FIELD_NUMBER: _ClassVar[int]
        SHOULD_FADE_OUT_FIELD_NUMBER: _ClassVar[int]
        fade_in_duration: float
        fade_out_duration: float
        should_fade_in: bool
        should_fade_out: bool
        def __init__(self, fade_in_duration: _Optional[float] = ..., fade_out_duration: _Optional[float] = ..., should_fade_in: _Optional[bool] = ..., should_fade_out: _Optional[bool] = ...) -> None: ...
    class SetAudioPropertiesType(_message.Message):
        __slots__ = ("audio_properties", "solo")
        AUDIO_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        SOLO_FIELD_NUMBER: _ClassVar[int]
        audio_properties: _graphicsData_pb2.Media.AudioProperties
        solo: _containers.RepeatedScalarFieldContainer[bool]
        def __init__(self, audio_properties: _Optional[_Union[_graphicsData_pb2.Media.AudioProperties, _Mapping]] = ..., solo: _Optional[_Iterable[bool]] = ...) -> None: ...
    PLAY_FIELD_NUMBER: _ClassVar[int]
    PAUSE_FIELD_NUMBER: _ClassVar[int]
    REWIND_FIELD_NUMBER: _ClassVar[int]
    FASTFORWARD_FIELD_NUMBER: _ClassVar[int]
    SKIP_BACK_FIELD_NUMBER: _ClassVar[int]
    SKIP_FORWARD_FIELD_NUMBER: _ClassVar[int]
    STEP_BACK_FIELD_NUMBER: _ClassVar[int]
    STEP_FORWARD_FIELD_NUMBER: _ClassVar[int]
    GO_TO_START_FIELD_NUMBER: _ClassVar[int]
    GO_TO_END_FIELD_NUMBER: _ClassVar[int]
    JUMP_TO_TIME_FIELD_NUMBER: _ClassVar[int]
    JUMP_TO_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MARK_IN_FIELD_NUMBER: _ClassVar[int]
    MARK_OUT_FIELD_NUMBER: _ClassVar[int]
    SET_SCALE_MODE_FIELD_NUMBER: _ClassVar[int]
    SET_FLIPPED_MODE_FIELD_NUMBER: _ClassVar[int]
    SET_PLAY_RATE_FIELD_NUMBER: _ClassVar[int]
    SET_ROTATION_FIELD_NUMBER: _ClassVar[int]
    TOGGLE_PLAYBACK_FIELD_NUMBER: _ClassVar[int]
    SET_EFFECTS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_EFFECT_FIELD_NUMBER: _ClassVar[int]
    BEGIN_SCRUB_FIELD_NUMBER: _ClassVar[int]
    END_SCRUB_FIELD_NUMBER: _ClassVar[int]
    SCRUB_TO_TIME_FIELD_NUMBER: _ClassVar[int]
    SCRUB_TO_PERCENT_FIELD_NUMBER: _ClassVar[int]
    SET_AUDIO_FADE_FIELD_NUMBER: _ClassVar[int]
    SET_AUDIO_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SET_ALPHA_TYPE_FIELD_NUMBER: _ClassVar[int]
    play: ControlTransport.PlayControlType
    pause: ControlTransport.PauseControlType
    rewind: ControlTransport.RewindControlType
    fastforward: ControlTransport.FastForwardControlType
    skip_back: ControlTransport.SkipBackControlType
    skip_forward: ControlTransport.SkipForwardControlType
    step_back: ControlTransport.StepBackControlType
    step_forward: ControlTransport.StepForwardControlType
    go_to_start: ControlTransport.GoToStartControlType
    go_to_end: ControlTransport.GoToEndControlType
    jump_to_time: ControlTransport.JumpToTimeControlType
    jump_to_percent: ControlTransport.JumpToPercentControlType
    mark_in: ControlTransport.MarkInPointControlType
    mark_out: ControlTransport.MarkOutPointControlType
    set_scale_mode: ControlTransport.SetScaleModeControlType
    set_flipped_mode: ControlTransport.SetFlippedModeControlType
    set_play_rate: ControlTransport.SetPlayRateControlType
    set_rotation: ControlTransport.SetNativeRotationControlType
    toggle_playback: ControlTransport.TogglePlaybackControlType
    set_effects: ControlTransport.SetEffectsControlType
    update_effect: ControlTransport.UpdateEffectControlType
    begin_scrub: ControlTransport.BeginScrubControlType
    end_scrub: ControlTransport.EndScrubControlType
    scrub_to_time: ControlTransport.ScrubToTimeControlType
    scrub_to_percent: ControlTransport.ScrubToPercentControlType
    set_audio_fade: ControlTransport.SetAudioFadeType
    set_audio_properties: ControlTransport.SetAudioPropertiesType
    set_alpha_type: ControlTransport.SetAlphaTypeControlType
    def __init__(self, play: _Optional[_Union[ControlTransport.PlayControlType, _Mapping]] = ..., pause: _Optional[_Union[ControlTransport.PauseControlType, _Mapping]] = ..., rewind: _Optional[_Union[ControlTransport.RewindControlType, _Mapping]] = ..., fastforward: _Optional[_Union[ControlTransport.FastForwardControlType, _Mapping]] = ..., skip_back: _Optional[_Union[ControlTransport.SkipBackControlType, _Mapping]] = ..., skip_forward: _Optional[_Union[ControlTransport.SkipForwardControlType, _Mapping]] = ..., step_back: _Optional[_Union[ControlTransport.StepBackControlType, _Mapping]] = ..., step_forward: _Optional[_Union[ControlTransport.StepForwardControlType, _Mapping]] = ..., go_to_start: _Optional[_Union[ControlTransport.GoToStartControlType, _Mapping]] = ..., go_to_end: _Optional[_Union[ControlTransport.GoToEndControlType, _Mapping]] = ..., jump_to_time: _Optional[_Union[ControlTransport.JumpToTimeControlType, _Mapping]] = ..., jump_to_percent: _Optional[_Union[ControlTransport.JumpToPercentControlType, _Mapping]] = ..., mark_in: _Optional[_Union[ControlTransport.MarkInPointControlType, _Mapping]] = ..., mark_out: _Optional[_Union[ControlTransport.MarkOutPointControlType, _Mapping]] = ..., set_scale_mode: _Optional[_Union[ControlTransport.SetScaleModeControlType, _Mapping]] = ..., set_flipped_mode: _Optional[_Union[ControlTransport.SetFlippedModeControlType, _Mapping]] = ..., set_play_rate: _Optional[_Union[ControlTransport.SetPlayRateControlType, _Mapping]] = ..., set_rotation: _Optional[_Union[ControlTransport.SetNativeRotationControlType, _Mapping]] = ..., toggle_playback: _Optional[_Union[ControlTransport.TogglePlaybackControlType, _Mapping]] = ..., set_effects: _Optional[_Union[ControlTransport.SetEffectsControlType, _Mapping]] = ..., update_effect: _Optional[_Union[ControlTransport.UpdateEffectControlType, _Mapping]] = ..., begin_scrub: _Optional[_Union[ControlTransport.BeginScrubControlType, _Mapping]] = ..., end_scrub: _Optional[_Union[ControlTransport.EndScrubControlType, _Mapping]] = ..., scrub_to_time: _Optional[_Union[ControlTransport.ScrubToTimeControlType, _Mapping]] = ..., scrub_to_percent: _Optional[_Union[ControlTransport.ScrubToPercentControlType, _Mapping]] = ..., set_audio_fade: _Optional[_Union[ControlTransport.SetAudioFadeType, _Mapping]] = ..., set_audio_properties: _Optional[_Union[ControlTransport.SetAudioPropertiesType, _Mapping]] = ..., set_alpha_type: _Optional[_Union[ControlTransport.SetAlphaTypeControlType, _Mapping]] = ...) -> None: ...

class AudioInputSettings(_message.Message):
    __slots__ = ("inputs", "transitionTime")
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONTIME_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[_input_pb2.AudioInput]
    transitionTime: float
    def __init__(self, inputs: _Optional[_Iterable[_Union[_input_pb2.AudioInput, _Mapping]]] = ..., transitionTime: _Optional[float] = ...) -> None: ...

class VideoInputSettings(_message.Message):
    __slots__ = ("inputs",)
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[_input_pb2.VideoInput]
    def __init__(self, inputs: _Optional[_Iterable[_Union[_input_pb2.VideoInput, _Mapping]]] = ...) -> None: ...

class RecordRequest(_message.Message):
    __slots__ = ("stream", "working_directory", "resi")
    class Resi(_message.Message):
        __slots__ = ("gop", "segmentSize", "destinationGroupId", "bufSize", "minRate", "maxRate", "eventName", "social_description")
        GOP_FIELD_NUMBER: _ClassVar[int]
        SEGMENTSIZE_FIELD_NUMBER: _ClassVar[int]
        DESTINATIONGROUPID_FIELD_NUMBER: _ClassVar[int]
        BUFSIZE_FIELD_NUMBER: _ClassVar[int]
        MINRATE_FIELD_NUMBER: _ClassVar[int]
        MAXRATE_FIELD_NUMBER: _ClassVar[int]
        EVENTNAME_FIELD_NUMBER: _ClassVar[int]
        SOCIAL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        gop: int
        segmentSize: float
        destinationGroupId: str
        bufSize: int
        minRate: int
        maxRate: int
        eventName: str
        social_description: str
        def __init__(self, gop: _Optional[int] = ..., segmentSize: _Optional[float] = ..., destinationGroupId: _Optional[str] = ..., bufSize: _Optional[int] = ..., minRate: _Optional[int] = ..., maxRate: _Optional[int] = ..., eventName: _Optional[str] = ..., social_description: _Optional[str] = ...) -> None: ...
    STREAM_FIELD_NUMBER: _ClassVar[int]
    WORKING_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    RESI_FIELD_NUMBER: _ClassVar[int]
    stream: _recording_pb2.Recording.Stream
    working_directory: _url_pb2.URL
    resi: RecordRequest.Resi
    def __init__(self, stream: _Optional[_Union[_recording_pb2.Recording.Stream, _Mapping]] = ..., working_directory: _Optional[_Union[_url_pb2.URL, _Mapping]] = ..., resi: _Optional[_Union[RecordRequest.Resi, _Mapping]] = ...) -> None: ...

class TextSegmentRequest(_message.Message):
    __slots__ = ("segments", "start_position")
    class Segment(_message.Message):
        __slots__ = ("index", "size")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        index: int
        size: float
        def __init__(self, index: _Optional[int] = ..., size: _Optional[float] = ...) -> None: ...
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    START_POSITION_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[TextSegmentRequest.Segment]
    start_position: float
    def __init__(self, segments: _Optional[_Iterable[_Union[TextSegmentRequest.Segment, _Mapping]]] = ..., start_position: _Optional[float] = ...) -> None: ...

class TriggerCue(_message.Message):
    __slots__ = ("trigger_handle", "trigger_options", "cue", "presentation", "playlist", "client_data")
    class PresentationCue(_message.Message):
        __slots__ = ("presentation", "arrangement_id", "cue_index")
        PRESENTATION_FIELD_NUMBER: _ClassVar[int]
        ARRANGEMENT_ID_FIELD_NUMBER: _ClassVar[int]
        CUE_INDEX_FIELD_NUMBER: _ClassVar[int]
        presentation: _presentation_pb2.Presentation
        arrangement_id: _uuid_pb2.UUID
        cue_index: int
        def __init__(self, presentation: _Optional[_Union[_presentation_pb2.Presentation, _Mapping]] = ..., arrangement_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., cue_index: _Optional[int] = ...) -> None: ...
    TRIGGER_HANDLE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CUE_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DATA_FIELD_NUMBER: _ClassVar[int]
    trigger_handle: int
    trigger_options: TriggerOptions
    cue: _cue_pb2.Cue
    presentation: TriggerCue.PresentationCue
    playlist: _playlist_pb2.Playlist
    client_data: int
    def __init__(self, trigger_handle: _Optional[int] = ..., trigger_options: _Optional[_Union[TriggerOptions, _Mapping]] = ..., cue: _Optional[_Union[_cue_pb2.Cue, _Mapping]] = ..., presentation: _Optional[_Union[TriggerCue.PresentationCue, _Mapping]] = ..., playlist: _Optional[_Union[_playlist_pb2.Playlist, _Mapping]] = ..., client_data: _Optional[int] = ...) -> None: ...

class NetworkTriggerDataItem(_message.Message):
    __slots__ = ("trigger_options", "trigger_cue", "action", "cue")
    TRIGGER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_CUE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CUE_FIELD_NUMBER: _ClassVar[int]
    trigger_options: TriggerOptions
    trigger_cue: TriggerCue
    action: _action_pb2.Action
    cue: _cue_pb2.Cue
    def __init__(self, trigger_options: _Optional[_Union[TriggerOptions, _Mapping]] = ..., trigger_cue: _Optional[_Union[TriggerCue, _Mapping]] = ..., action: _Optional[_Union[_action_pb2.Action, _Mapping]] = ..., cue: _Optional[_Union[_cue_pb2.Cue, _Mapping]] = ...) -> None: ...

class SlideElementTextRenderInfo(_message.Message):
    __slots__ = ("layers",)
    class LayerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LAYER_TYPE_COMPOSITE: _ClassVar[SlideElementTextRenderInfo.LayerType]
        LAYER_TYPE_MASK: _ClassVar[SlideElementTextRenderInfo.LayerType]
        LAYER_TYPE_OVER: _ClassVar[SlideElementTextRenderInfo.LayerType]
        LAYER_TYPE_UNDER: _ClassVar[SlideElementTextRenderInfo.LayerType]
    LAYER_TYPE_COMPOSITE: SlideElementTextRenderInfo.LayerType
    LAYER_TYPE_MASK: SlideElementTextRenderInfo.LayerType
    LAYER_TYPE_OVER: SlideElementTextRenderInfo.LayerType
    LAYER_TYPE_UNDER: SlideElementTextRenderInfo.LayerType
    class Layer(_message.Message):
        __slots__ = ("layer_type", "text_build_index", "cut_out_fill", "media_fill", "background_effect")
        LAYER_TYPE_FIELD_NUMBER: _ClassVar[int]
        TEXT_BUILD_INDEX_FIELD_NUMBER: _ClassVar[int]
        CUT_OUT_FILL_FIELD_NUMBER: _ClassVar[int]
        MEDIA_FILL_FIELD_NUMBER: _ClassVar[int]
        BACKGROUND_EFFECT_FIELD_NUMBER: _ClassVar[int]
        layer_type: SlideElementTextRenderInfo.LayerType
        text_build_index: int
        cut_out_fill: _graphicsData_pb2.Graphics.Text.CutOutFill
        media_fill: _graphicsData_pb2.Graphics.Text.MediaFill
        background_effect: _graphicsData_pb2.Graphics.BackgroundEffect
        def __init__(self, layer_type: _Optional[_Union[SlideElementTextRenderInfo.LayerType, str]] = ..., text_build_index: _Optional[int] = ..., cut_out_fill: _Optional[_Union[_graphicsData_pb2.Graphics.Text.CutOutFill, _Mapping]] = ..., media_fill: _Optional[_Union[_graphicsData_pb2.Graphics.Text.MediaFill, _Mapping]] = ..., background_effect: _Optional[_Union[_graphicsData_pb2.Graphics.BackgroundEffect, _Mapping]] = ...) -> None: ...
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedCompositeFieldContainer[SlideElementTextRenderInfo.Layer]
    def __init__(self, layers: _Optional[_Iterable[_Union[SlideElementTextRenderInfo.Layer, _Mapping]]] = ...) -> None: ...

class ValidateEncoderRequest(_message.Message):
    __slots__ = ("encoder",)
    ENCODER_FIELD_NUMBER: _ClassVar[int]
    encoder: _recording_pb2.Recording.Stream.Encoder
    def __init__(self, encoder: _Optional[_Union[_recording_pb2.Recording.Stream.Encoder, _Mapping]] = ...) -> None: ...

class ValidateEncoderResponse(_message.Message):
    __slots__ = ("is_valid",)
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    def __init__(self, is_valid: _Optional[bool] = ...) -> None: ...

class CaptureActionRequest(_message.Message):
    __slots__ = ("start_resi", "stop_capture", "error")
    class StartResi(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class StopCapture(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Error(_message.Message):
        __slots__ = ("error_code", "capture_action")
        ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
        CAPTURE_ACTION_FIELD_NUMBER: _ClassVar[int]
        error_code: int
        capture_action: _action_pb2.Action.CaptureType
        def __init__(self, error_code: _Optional[int] = ..., capture_action: _Optional[_Union[_action_pb2.Action.CaptureType, _Mapping]] = ...) -> None: ...
    START_RESI_FIELD_NUMBER: _ClassVar[int]
    STOP_CAPTURE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    start_resi: CaptureActionRequest.StartResi
    stop_capture: CaptureActionRequest.StopCapture
    error: CaptureActionRequest.Error
    def __init__(self, start_resi: _Optional[_Union[CaptureActionRequest.StartResi, _Mapping]] = ..., stop_capture: _Optional[_Union[CaptureActionRequest.StopCapture, _Mapping]] = ..., error: _Optional[_Union[CaptureActionRequest.Error, _Mapping]] = ...) -> None: ...

class CaptureActionResponse(_message.Message):
    __slots__ = ("start_resi", "stop_capture", "cancel_capture_action")
    class CancelCaptureAction(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class StartResi(_message.Message):
        __slots__ = ("event_name", "event_description")
        EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
        EVENT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        event_name: str
        event_description: str
        def __init__(self, event_name: _Optional[str] = ..., event_description: _Optional[str] = ...) -> None: ...
    class StopCapture(_message.Message):
        __slots__ = ("stop_capture",)
        STOP_CAPTURE_FIELD_NUMBER: _ClassVar[int]
        stop_capture: bool
        def __init__(self, stop_capture: _Optional[bool] = ...) -> None: ...
    START_RESI_FIELD_NUMBER: _ClassVar[int]
    STOP_CAPTURE_FIELD_NUMBER: _ClassVar[int]
    CANCEL_CAPTURE_ACTION_FIELD_NUMBER: _ClassVar[int]
    start_resi: CaptureActionResponse.StartResi
    stop_capture: CaptureActionResponse.StopCapture
    cancel_capture_action: CaptureActionResponse.CancelCaptureAction
    def __init__(self, start_resi: _Optional[_Union[CaptureActionResponse.StartResi, _Mapping]] = ..., stop_capture: _Optional[_Union[CaptureActionResponse.StopCapture, _Mapping]] = ..., cancel_capture_action: _Optional[_Union[CaptureActionResponse.CancelCaptureAction, _Mapping]] = ...) -> None: ...

class MacroIcons(_message.Message):
    __slots__ = ("icons",)
    class MacroIcon(_message.Message):
        __slots__ = ("image_type", "image_data", "content_type")
        IMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
        IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
        CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        image_type: _macros_pb2.MacrosDocument.Macro.ImageType
        image_data: bytes
        content_type: str
        def __init__(self, image_type: _Optional[_Union[_macros_pb2.MacrosDocument.Macro.ImageType, str]] = ..., image_data: _Optional[bytes] = ..., content_type: _Optional[str] = ...) -> None: ...
    ICONS_FIELD_NUMBER: _ClassVar[int]
    icons: _containers.RepeatedCompositeFieldContainer[MacroIcons.MacroIcon]
    def __init__(self, icons: _Optional[_Iterable[_Union[MacroIcons.MacroIcon, _Mapping]]] = ...) -> None: ...

class PropPauseRequest(_message.Message):
    __slots__ = ("prop_id", "pause", "resume", "status")
    class Pause(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Resume(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Status(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    PROP_ID_FIELD_NUMBER: _ClassVar[int]
    PAUSE_FIELD_NUMBER: _ClassVar[int]
    RESUME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    prop_id: _uuid_pb2.UUID
    pause: PropPauseRequest.Pause
    resume: PropPauseRequest.Resume
    status: PropPauseRequest.Status
    def __init__(self, prop_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., pause: _Optional[_Union[PropPauseRequest.Pause, _Mapping]] = ..., resume: _Optional[_Union[PropPauseRequest.Resume, _Mapping]] = ..., status: _Optional[_Union[PropPauseRequest.Status, _Mapping]] = ...) -> None: ...

class GenericEvent(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MediaThumbnail(_message.Message):
    __slots__ = ("width", "height", "data", "stride")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    STRIDE_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    data: bytes
    stride: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., data: _Optional[bytes] = ..., stride: _Optional[int] = ...) -> None: ...

class PCOData(_message.Message):
    __slots__ = ("service_type_id", "plan_id")
    SERVICE_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    service_type_id: str
    plan_id: str
    def __init__(self, service_type_id: _Optional[str] = ..., plan_id: _Optional[str] = ...) -> None: ...

class WebFillTokenAndCookies(_message.Message):
    __slots__ = ("cookies", "token")
    class Cookie(_message.Message):
        __slots__ = ("name", "value", "domain", "expiry")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        DOMAIN_FIELD_NUMBER: _ClassVar[int]
        EXPIRY_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        domain: str
        expiry: int
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ..., domain: _Optional[str] = ..., expiry: _Optional[int] = ...) -> None: ...
    COOKIES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    cookies: _containers.RepeatedCompositeFieldContainer[WebFillTokenAndCookies.Cookie]
    token: str
    def __init__(self, cookies: _Optional[_Iterable[_Union[WebFillTokenAndCookies.Cookie, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...

class InputStatusCallback(_message.Message):
    __slots__ = ("enable",)
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    enable: bool
    def __init__(self, enable: _Optional[bool] = ...) -> None: ...

class SlideThumbnailRequest(_message.Message):
    __slots__ = ("cue", "background", "width", "height")
    CUE_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    cue: _cue_pb2.Cue
    background: _color_pb2.Color
    width: int
    height: int
    def __init__(self, cue: _Optional[_Union[_cue_pb2.Cue, _Mapping]] = ..., background: _Optional[_Union[_color_pb2.Color, _Mapping]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class SendData(_message.Message):
    __slots__ = ("message_id", "workspace", "stage_document", "timers_document", "validate_encoder_request", "trigger_cue", "digital_audio_setup", "macros_document", "message_document", "prop_document", "ccli_document", "audience_looks", "live_audience_look", "masks", "recording_settings_document", "capture_action_response", "copyright_layout", "global_background_transition", "global_messages_transition", "global_foreground_transition", "global_props_transition", "global_audio_transition", "preferences", "test_pattern", "startup_complete", "visual_playlist_doc", "audio_playlist_doc", "kill_watchdog", "macro_icons", "debug_trigger_data_dump", "library_playlist_doc", "audio_playlist_focus_uuid", "media_playlist_focus_uuid", "library_playlist_focus_uuid", "library_playlist_item_focus_uuid", "prop_pause", "media_thumbnail", "pco_data", "webfill_token_and_cookies", "psb_workspace", "input_status_callback", "slide_thumbnail")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    STAGE_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TIMERS_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ENCODER_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_CUE_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_AUDIO_SETUP_FIELD_NUMBER: _ClassVar[int]
    MACROS_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    PROP_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    CCLI_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_LOOKS_FIELD_NUMBER: _ClassVar[int]
    LIVE_AUDIENCE_LOOK_FIELD_NUMBER: _ClassVar[int]
    MASKS_FIELD_NUMBER: _ClassVar[int]
    RECORDING_SETTINGS_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ACTION_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_BACKGROUND_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_MESSAGES_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_FOREGROUND_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_PROPS_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_AUDIO_TRANSITION_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    TEST_PATTERN_FIELD_NUMBER: _ClassVar[int]
    STARTUP_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    VISUAL_PLAYLIST_DOC_FIELD_NUMBER: _ClassVar[int]
    AUDIO_PLAYLIST_DOC_FIELD_NUMBER: _ClassVar[int]
    KILL_WATCHDOG_FIELD_NUMBER: _ClassVar[int]
    MACRO_ICONS_FIELD_NUMBER: _ClassVar[int]
    DEBUG_TRIGGER_DATA_DUMP_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_DOC_FIELD_NUMBER: _ClassVar[int]
    AUDIO_PLAYLIST_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    MEDIA_PLAYLIST_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_ITEM_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    PROP_PAUSE_FIELD_NUMBER: _ClassVar[int]
    MEDIA_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    PCO_DATA_FIELD_NUMBER: _ClassVar[int]
    WEBFILL_TOKEN_AND_COOKIES_FIELD_NUMBER: _ClassVar[int]
    PSB_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    INPUT_STATUS_CALLBACK_FIELD_NUMBER: _ClassVar[int]
    SLIDE_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    workspace: _proworkspace_pb2.ProPresenterWorkspace
    stage_document: _stage_pb2.Stage.Document
    timers_document: _timers_pb2.TimersDocument
    validate_encoder_request: ValidateEncoderRequest
    trigger_cue: TriggerCue
    digital_audio_setup: _digitalAudio_pb2.DigitalAudio.Setup
    macros_document: _macros_pb2.MacrosDocument
    message_document: _messages_pb2.MessageDocument
    prop_document: _propDocument_pb2.PropDocument
    ccli_document: _ccli_pb2.CCLIDocument
    audience_looks: _proAudienceLook_pb2.AudienceLookCollection
    live_audience_look: _proAudienceLook_pb2.ProAudienceLook
    masks: _proMask_pb2.MaskCollection
    recording_settings_document: _recording_pb2.Recording.SettingsDocument
    capture_action_response: CaptureActionResponse
    copyright_layout: _ccli_pb2.CopyrightLayout
    global_background_transition: _effects_pb2.Transition
    global_messages_transition: _effects_pb2.Transition
    global_foreground_transition: _effects_pb2.Transition
    global_props_transition: _effects_pb2.Transition
    global_audio_transition: _effects_pb2.Transition
    preferences: _preferences_pb2.Preferences
    test_pattern: _proCoreTestPatterns_pb2.TestPatternRequest
    startup_complete: GenericEvent
    visual_playlist_doc: _propresenter_pb2.PlaylistDocument
    audio_playlist_doc: _propresenter_pb2.PlaylistDocument
    kill_watchdog: GenericEvent
    macro_icons: MacroIcons
    debug_trigger_data_dump: GenericEvent
    library_playlist_doc: _propresenter_pb2.PlaylistDocument
    audio_playlist_focus_uuid: _uuid_pb2.UUID
    media_playlist_focus_uuid: _uuid_pb2.UUID
    library_playlist_focus_uuid: _uuid_pb2.UUID
    library_playlist_item_focus_uuid: _uuid_pb2.UUID
    prop_pause: PropPauseRequest
    media_thumbnail: MediaThumbnail
    pco_data: PCOData
    webfill_token_and_cookies: WebFillTokenAndCookies
    psb_workspace: _psbWorkspace_pb2.ProScoreboardWorkspace
    input_status_callback: InputStatusCallback
    slide_thumbnail: SlideThumbnailRequest
    def __init__(self, message_id: _Optional[int] = ..., workspace: _Optional[_Union[_proworkspace_pb2.ProPresenterWorkspace, _Mapping]] = ..., stage_document: _Optional[_Union[_stage_pb2.Stage.Document, _Mapping]] = ..., timers_document: _Optional[_Union[_timers_pb2.TimersDocument, _Mapping]] = ..., validate_encoder_request: _Optional[_Union[ValidateEncoderRequest, _Mapping]] = ..., trigger_cue: _Optional[_Union[TriggerCue, _Mapping]] = ..., digital_audio_setup: _Optional[_Union[_digitalAudio_pb2.DigitalAudio.Setup, _Mapping]] = ..., macros_document: _Optional[_Union[_macros_pb2.MacrosDocument, _Mapping]] = ..., message_document: _Optional[_Union[_messages_pb2.MessageDocument, _Mapping]] = ..., prop_document: _Optional[_Union[_propDocument_pb2.PropDocument, _Mapping]] = ..., ccli_document: _Optional[_Union[_ccli_pb2.CCLIDocument, _Mapping]] = ..., audience_looks: _Optional[_Union[_proAudienceLook_pb2.AudienceLookCollection, _Mapping]] = ..., live_audience_look: _Optional[_Union[_proAudienceLook_pb2.ProAudienceLook, _Mapping]] = ..., masks: _Optional[_Union[_proMask_pb2.MaskCollection, _Mapping]] = ..., recording_settings_document: _Optional[_Union[_recording_pb2.Recording.SettingsDocument, _Mapping]] = ..., capture_action_response: _Optional[_Union[CaptureActionResponse, _Mapping]] = ..., copyright_layout: _Optional[_Union[_ccli_pb2.CopyrightLayout, _Mapping]] = ..., global_background_transition: _Optional[_Union[_effects_pb2.Transition, _Mapping]] = ..., global_messages_transition: _Optional[_Union[_effects_pb2.Transition, _Mapping]] = ..., global_foreground_transition: _Optional[_Union[_effects_pb2.Transition, _Mapping]] = ..., global_props_transition: _Optional[_Union[_effects_pb2.Transition, _Mapping]] = ..., global_audio_transition: _Optional[_Union[_effects_pb2.Transition, _Mapping]] = ..., preferences: _Optional[_Union[_preferences_pb2.Preferences, _Mapping]] = ..., test_pattern: _Optional[_Union[_proCoreTestPatterns_pb2.TestPatternRequest, _Mapping]] = ..., startup_complete: _Optional[_Union[GenericEvent, _Mapping]] = ..., visual_playlist_doc: _Optional[_Union[_propresenter_pb2.PlaylistDocument, _Mapping]] = ..., audio_playlist_doc: _Optional[_Union[_propresenter_pb2.PlaylistDocument, _Mapping]] = ..., kill_watchdog: _Optional[_Union[GenericEvent, _Mapping]] = ..., macro_icons: _Optional[_Union[MacroIcons, _Mapping]] = ..., debug_trigger_data_dump: _Optional[_Union[GenericEvent, _Mapping]] = ..., library_playlist_doc: _Optional[_Union[_propresenter_pb2.PlaylistDocument, _Mapping]] = ..., audio_playlist_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., media_playlist_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., library_playlist_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., library_playlist_item_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., prop_pause: _Optional[_Union[PropPauseRequest, _Mapping]] = ..., media_thumbnail: _Optional[_Union[MediaThumbnail, _Mapping]] = ..., pco_data: _Optional[_Union[PCOData, _Mapping]] = ..., webfill_token_and_cookies: _Optional[_Union[WebFillTokenAndCookies, _Mapping]] = ..., psb_workspace: _Optional[_Union[_psbWorkspace_pb2.ProScoreboardWorkspace, _Mapping]] = ..., input_status_callback: _Optional[_Union[InputStatusCallback, _Mapping]] = ..., slide_thumbnail: _Optional[_Union[SlideThumbnailRequest, _Mapping]] = ...) -> None: ...

class TimerRuntimeState(_message.Message):
    __slots__ = ("timer_uuid", "timer_name", "action_type", "is_running", "has_overrun", "state", "current_time", "has_started")
    class ResourceState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PREROLLING: _ClassVar[TimerRuntimeState.ResourceState]
        ACTIVATED: _ClassVar[TimerRuntimeState.ResourceState]
        UPDATED: _ClassVar[TimerRuntimeState.ResourceState]
        DEACTIVATED: _ClassVar[TimerRuntimeState.ResourceState]
        RELEASED: _ClassVar[TimerRuntimeState.ResourceState]
    PREROLLING: TimerRuntimeState.ResourceState
    ACTIVATED: TimerRuntimeState.ResourceState
    UPDATED: TimerRuntimeState.ResourceState
    DEACTIVATED: TimerRuntimeState.ResourceState
    RELEASED: TimerRuntimeState.ResourceState
    TIMER_UUID_FIELD_NUMBER: _ClassVar[int]
    TIMER_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
    HAS_OVERRUN_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
    HAS_STARTED_FIELD_NUMBER: _ClassVar[int]
    timer_uuid: _uuid_pb2.UUID
    timer_name: str
    action_type: _action_pb2.Action.TimerType
    is_running: bool
    has_overrun: bool
    state: TimerRuntimeState.ResourceState
    current_time: float
    has_started: bool
    def __init__(self, timer_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., timer_name: _Optional[str] = ..., action_type: _Optional[_Union[_action_pb2.Action.TimerType, _Mapping]] = ..., is_running: _Optional[bool] = ..., has_overrun: _Optional[bool] = ..., state: _Optional[_Union[TimerRuntimeState.ResourceState, str]] = ..., current_time: _Optional[float] = ..., has_started: _Optional[bool] = ...) -> None: ...

class TimerStateUpdate(_message.Message):
    __slots__ = ("timer", "state")
    TIMER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    timer: _timers_pb2.Timer
    state: TimerRuntimeState
    def __init__(self, timer: _Optional[_Union[_timers_pb2.Timer, _Mapping]] = ..., state: _Optional[_Union[TimerRuntimeState, _Mapping]] = ...) -> None: ...

class HandledException(_message.Message):
    __slots__ = ("description",)
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: str
    def __init__(self, description: _Optional[str] = ...) -> None: ...

class LeaveBreadcrumb(_message.Message):
    __slots__ = ("type", "description", "metadata")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Navigation: _ClassVar[LeaveBreadcrumb.Type]
        Request: _ClassVar[LeaveBreadcrumb.Type]
        Process: _ClassVar[LeaveBreadcrumb.Type]
        Log: _ClassVar[LeaveBreadcrumb.Type]
        User: _ClassVar[LeaveBreadcrumb.Type]
        State: _ClassVar[LeaveBreadcrumb.Type]
        Error: _ClassVar[LeaveBreadcrumb.Type]
        Manual: _ClassVar[LeaveBreadcrumb.Type]
    Navigation: LeaveBreadcrumb.Type
    Request: LeaveBreadcrumb.Type
    Process: LeaveBreadcrumb.Type
    Log: LeaveBreadcrumb.Type
    User: LeaveBreadcrumb.Type
    State: LeaveBreadcrumb.Type
    Error: LeaveBreadcrumb.Type
    Manual: LeaveBreadcrumb.Type
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    type: LeaveBreadcrumb.Type
    description: str
    metadata: _containers.RepeatedCompositeFieldContainer[LeaveBreadcrumb.MetadataEntry]
    def __init__(self, type: _Optional[_Union[LeaveBreadcrumb.Type, str]] = ..., description: _Optional[str] = ..., metadata: _Optional[_Iterable[_Union[LeaveBreadcrumb.MetadataEntry, _Mapping]]] = ...) -> None: ...

class PropPauseResponse(_message.Message):
    __slots__ = ("prop_id", "status")
    class Status(_message.Message):
        __slots__ = ("paused", "time_remaining", "percentage_complete", "total_time")
        PAUSED_FIELD_NUMBER: _ClassVar[int]
        TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        PERCENTAGE_COMPLETE_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TIME_FIELD_NUMBER: _ClassVar[int]
        paused: bool
        time_remaining: float
        percentage_complete: float
        total_time: float
        def __init__(self, paused: _Optional[bool] = ..., time_remaining: _Optional[float] = ..., percentage_complete: _Optional[float] = ..., total_time: _Optional[float] = ...) -> None: ...
    PROP_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    prop_id: _uuid_pb2.UUID
    status: PropPauseResponse.Status
    def __init__(self, prop_id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., status: _Optional[_Union[PropPauseResponse.Status, _Mapping]] = ...) -> None: ...

class ShowMessage(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class GetMediaThumbnail(_message.Message):
    __slots__ = ("width_hint", "height_hint", "media", "action")
    WIDTH_HINT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_HINT_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    width_hint: int
    height_hint: int
    media: _graphicsData_pb2.Media
    action: _action_pb2.Action
    def __init__(self, width_hint: _Optional[int] = ..., height_hint: _Optional[int] = ..., media: _Optional[_Union[_graphicsData_pb2.Media, _Mapping]] = ..., action: _Optional[_Union[_action_pb2.Action, _Mapping]] = ...) -> None: ...

class RequestWebFillTokenAndCookies(_message.Message):
    __slots__ = ("refresh_first", "link")
    REFRESH_FIRST_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    refresh_first: bool
    link: str
    def __init__(self, refresh_first: _Optional[bool] = ..., link: _Optional[str] = ...) -> None: ...

class MediaAssetTriggered(_message.Message):
    __slots__ = ("media_uuid", "container_id")
    MEDIA_UUID_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
    media_uuid: _uuid_pb2.UUID
    container_id: str
    def __init__(self, media_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., container_id: _Optional[str] = ...) -> None: ...

class SlideThumbnailResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class SendDataResponse(_message.Message):
    __slots__ = ("message_id", "validate_encoder_response", "timer_state", "capture_action_request", "test_pattern", "handled_exception", "audio_playlist_focus_uuid", "media_playlist_focus_uuid", "library_playlist_focus_uuid", "library_playlist_item_focus_uuid", "prop_pause", "show_message", "hide_message", "get_media_thumbnail", "request_webfill_token_and_cookies", "media_asset_triggered", "leave_breadcrumb", "slide_thumbnail")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ENCODER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TIMER_STATE_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_ACTION_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TEST_PATTERN_FIELD_NUMBER: _ClassVar[int]
    HANDLED_EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    AUDIO_PLAYLIST_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    MEDIA_PLAYLIST_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_PLAYLIST_ITEM_FOCUS_UUID_FIELD_NUMBER: _ClassVar[int]
    PROP_PAUSE_FIELD_NUMBER: _ClassVar[int]
    SHOW_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    HIDE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GET_MEDIA_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_WEBFILL_TOKEN_AND_COOKIES_FIELD_NUMBER: _ClassVar[int]
    MEDIA_ASSET_TRIGGERED_FIELD_NUMBER: _ClassVar[int]
    LEAVE_BREADCRUMB_FIELD_NUMBER: _ClassVar[int]
    SLIDE_THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    validate_encoder_response: ValidateEncoderResponse
    timer_state: TimerStateUpdate
    capture_action_request: CaptureActionRequest
    test_pattern: _proCoreTestPatterns_pb2.TestPatternResponse
    handled_exception: HandledException
    audio_playlist_focus_uuid: _uuid_pb2.UUID
    media_playlist_focus_uuid: _uuid_pb2.UUID
    library_playlist_focus_uuid: _uuid_pb2.UUID
    library_playlist_item_focus_uuid: _uuid_pb2.UUID
    prop_pause: PropPauseResponse
    show_message: ShowMessage
    hide_message: GenericEvent
    get_media_thumbnail: GetMediaThumbnail
    request_webfill_token_and_cookies: RequestWebFillTokenAndCookies
    media_asset_triggered: MediaAssetTriggered
    leave_breadcrumb: LeaveBreadcrumb
    slide_thumbnail: SlideThumbnailResponse
    def __init__(self, message_id: _Optional[int] = ..., validate_encoder_response: _Optional[_Union[ValidateEncoderResponse, _Mapping]] = ..., timer_state: _Optional[_Union[TimerStateUpdate, _Mapping]] = ..., capture_action_request: _Optional[_Union[CaptureActionRequest, _Mapping]] = ..., test_pattern: _Optional[_Union[_proCoreTestPatterns_pb2.TestPatternResponse, _Mapping]] = ..., handled_exception: _Optional[_Union[HandledException, _Mapping]] = ..., audio_playlist_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., media_playlist_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., library_playlist_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., library_playlist_item_focus_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., prop_pause: _Optional[_Union[PropPauseResponse, _Mapping]] = ..., show_message: _Optional[_Union[ShowMessage, _Mapping]] = ..., hide_message: _Optional[_Union[GenericEvent, _Mapping]] = ..., get_media_thumbnail: _Optional[_Union[GetMediaThumbnail, _Mapping]] = ..., request_webfill_token_and_cookies: _Optional[_Union[RequestWebFillTokenAndCookies, _Mapping]] = ..., media_asset_triggered: _Optional[_Union[MediaAssetTriggered, _Mapping]] = ..., leave_breadcrumb: _Optional[_Union[LeaveBreadcrumb, _Mapping]] = ..., slide_thumbnail: _Optional[_Union[SlideThumbnailResponse, _Mapping]] = ...) -> None: ...

class TriggerTransferRenderState(_message.Message):
    __slots__ = ("slide", "stage_message", "presentation_media", "announcement_media", "audio_media", "live_video_media", "presentation", "announcement", "timers", "capture", "timecode", "system_time")
    class TimerState(_message.Message):
        __slots__ = ("timer", "is_running", "has_overrun", "value")
        TIMER_FIELD_NUMBER: _ClassVar[int]
        IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
        HAS_OVERRUN_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        timer: _timers_pb2.Timer
        is_running: bool
        has_overrun: bool
        value: float
        def __init__(self, timer: _Optional[_Union[_timers_pb2.Timer, _Mapping]] = ..., is_running: _Optional[bool] = ..., has_overrun: _Optional[bool] = ..., value: _Optional[float] = ...) -> None: ...
    class MediaState(_message.Message):
        __slots__ = ("current_media", "is_playing", "is_looping", "current_time", "time_remaining", "playlist_uuid", "playlist_name", "markers")
        CURRENT_MEDIA_FIELD_NUMBER: _ClassVar[int]
        IS_PLAYING_FIELD_NUMBER: _ClassVar[int]
        IS_LOOPING_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        PLAYLIST_UUID_FIELD_NUMBER: _ClassVar[int]
        PLAYLIST_NAME_FIELD_NUMBER: _ClassVar[int]
        MARKERS_FIELD_NUMBER: _ClassVar[int]
        current_media: _graphicsData_pb2.Media
        is_playing: bool
        is_looping: bool
        current_time: float
        time_remaining: float
        playlist_uuid: _uuid_pb2.UUID
        playlist_name: str
        markers: _containers.RepeatedCompositeFieldContainer[_action_pb2.Action.MediaType.PlaybackMarker]
        def __init__(self, current_media: _Optional[_Union[_graphicsData_pb2.Media, _Mapping]] = ..., is_playing: _Optional[bool] = ..., is_looping: _Optional[bool] = ..., current_time: _Optional[float] = ..., time_remaining: _Optional[float] = ..., playlist_uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., playlist_name: _Optional[str] = ..., markers: _Optional[_Iterable[_Union[_action_pb2.Action.MediaType.PlaybackMarker, _Mapping]]] = ...) -> None: ...
    class CaptureState(_message.Message):
        __slots__ = ("status", "time")
        class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            Stopped: _ClassVar[TriggerTransferRenderState.CaptureState.Status]
            Active: _ClassVar[TriggerTransferRenderState.CaptureState.Status]
            Caution: _ClassVar[TriggerTransferRenderState.CaptureState.Status]
            Error: _ClassVar[TriggerTransferRenderState.CaptureState.Status]
        Stopped: TriggerTransferRenderState.CaptureState.Status
        Active: TriggerTransferRenderState.CaptureState.Status
        Caution: TriggerTransferRenderState.CaptureState.Status
        Error: TriggerTransferRenderState.CaptureState.Status
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        status: TriggerTransferRenderState.CaptureState.Status
        time: float
        def __init__(self, status: _Optional[_Union[TriggerTransferRenderState.CaptureState.Status, str]] = ..., time: _Optional[float] = ...) -> None: ...
    class AutoAdvanceState(_message.Message):
        __slots__ = ("active", "remaining_time")
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        REMAINING_TIME_FIELD_NUMBER: _ClassVar[int]
        active: bool
        remaining_time: float
        def __init__(self, active: _Optional[bool] = ..., remaining_time: _Optional[float] = ...) -> None: ...
    class TimelineState(_message.Message):
        __slots__ = ("active", "current_time", "last_slide_index")
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        LAST_SLIDE_INDEX_FIELD_NUMBER: _ClassVar[int]
        active: bool
        current_time: float
        last_slide_index: int
        def __init__(self, active: _Optional[bool] = ..., current_time: _Optional[float] = ..., last_slide_index: _Optional[int] = ...) -> None: ...
    class SlideState(_message.Message):
        __slots__ = ("presentation", "playlist", "current_cue", "next_cue", "auto_advance", "timeline_state", "current_cue_index", "current_playlist_index", "is_current_position", "trigger_source")
        class TriggerSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            Normal: _ClassVar[TriggerTransferRenderState.SlideState.TriggerSource]
            Timeline: _ClassVar[TriggerTransferRenderState.SlideState.TriggerSource]
            Editor: _ClassVar[TriggerTransferRenderState.SlideState.TriggerSource]
        Normal: TriggerTransferRenderState.SlideState.TriggerSource
        Timeline: TriggerTransferRenderState.SlideState.TriggerSource
        Editor: TriggerTransferRenderState.SlideState.TriggerSource
        PRESENTATION_FIELD_NUMBER: _ClassVar[int]
        PLAYLIST_FIELD_NUMBER: _ClassVar[int]
        CURRENT_CUE_FIELD_NUMBER: _ClassVar[int]
        NEXT_CUE_FIELD_NUMBER: _ClassVar[int]
        AUTO_ADVANCE_FIELD_NUMBER: _ClassVar[int]
        TIMELINE_STATE_FIELD_NUMBER: _ClassVar[int]
        CURRENT_CUE_INDEX_FIELD_NUMBER: _ClassVar[int]
        CURRENT_PLAYLIST_INDEX_FIELD_NUMBER: _ClassVar[int]
        IS_CURRENT_POSITION_FIELD_NUMBER: _ClassVar[int]
        TRIGGER_SOURCE_FIELD_NUMBER: _ClassVar[int]
        presentation: _presentation_pb2.Presentation
        playlist: _playlist_pb2.Playlist
        current_cue: _uuid_pb2.UUID
        next_cue: _uuid_pb2.UUID
        auto_advance: TriggerTransferRenderState.AutoAdvanceState
        timeline_state: TriggerTransferRenderState.TimelineState
        current_cue_index: int
        current_playlist_index: int
        is_current_position: bool
        trigger_source: TriggerTransferRenderState.SlideState.TriggerSource
        def __init__(self, presentation: _Optional[_Union[_presentation_pb2.Presentation, _Mapping]] = ..., playlist: _Optional[_Union[_playlist_pb2.Playlist, _Mapping]] = ..., current_cue: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., next_cue: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., auto_advance: _Optional[_Union[TriggerTransferRenderState.AutoAdvanceState, _Mapping]] = ..., timeline_state: _Optional[_Union[TriggerTransferRenderState.TimelineState, _Mapping]] = ..., current_cue_index: _Optional[int] = ..., current_playlist_index: _Optional[int] = ..., is_current_position: _Optional[bool] = ..., trigger_source: _Optional[_Union[TriggerTransferRenderState.SlideState.TriggerSource, str]] = ...) -> None: ...
    class TimecodeState(_message.Message):
        __slots__ = ("status", "time", "fps")
        class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            Stopped: _ClassVar[TriggerTransferRenderState.TimecodeState.Status]
            Playing: _ClassVar[TriggerTransferRenderState.TimecodeState.Status]
            Error: _ClassVar[TriggerTransferRenderState.TimecodeState.Status]
            Discontinuity: _ClassVar[TriggerTransferRenderState.TimecodeState.Status]
        Stopped: TriggerTransferRenderState.TimecodeState.Status
        Playing: TriggerTransferRenderState.TimecodeState.Status
        Error: TriggerTransferRenderState.TimecodeState.Status
        Discontinuity: TriggerTransferRenderState.TimecodeState.Status
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        FPS_FIELD_NUMBER: _ClassVar[int]
        status: TriggerTransferRenderState.TimecodeState.Status
        time: float
        fps: float
        def __init__(self, status: _Optional[_Union[TriggerTransferRenderState.TimecodeState.Status, str]] = ..., time: _Optional[float] = ..., fps: _Optional[float] = ...) -> None: ...
    SLIDE_FIELD_NUMBER: _ClassVar[int]
    STAGE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_MEDIA_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_MEDIA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_MEDIA_FIELD_NUMBER: _ClassVar[int]
    LIVE_VIDEO_MEDIA_FIELD_NUMBER: _ClassVar[int]
    PRESENTATION_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    TIMERS_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_FIELD_NUMBER: _ClassVar[int]
    TIMECODE_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_TIME_FIELD_NUMBER: _ClassVar[int]
    slide: _slide_pb2.Slide
    stage_message: str
    presentation_media: TriggerTransferRenderState.MediaState
    announcement_media: TriggerTransferRenderState.MediaState
    audio_media: TriggerTransferRenderState.MediaState
    live_video_media: _graphicsData_pb2.Media
    presentation: TriggerTransferRenderState.SlideState
    announcement: TriggerTransferRenderState.SlideState
    timers: _containers.RepeatedCompositeFieldContainer[TriggerTransferRenderState.TimerState]
    capture: TriggerTransferRenderState.CaptureState
    timecode: TriggerTransferRenderState.TimecodeState
    system_time: int
    def __init__(self, slide: _Optional[_Union[_slide_pb2.Slide, _Mapping]] = ..., stage_message: _Optional[str] = ..., presentation_media: _Optional[_Union[TriggerTransferRenderState.MediaState, _Mapping]] = ..., announcement_media: _Optional[_Union[TriggerTransferRenderState.MediaState, _Mapping]] = ..., audio_media: _Optional[_Union[TriggerTransferRenderState.MediaState, _Mapping]] = ..., live_video_media: _Optional[_Union[_graphicsData_pb2.Media, _Mapping]] = ..., presentation: _Optional[_Union[TriggerTransferRenderState.SlideState, _Mapping]] = ..., announcement: _Optional[_Union[TriggerTransferRenderState.SlideState, _Mapping]] = ..., timers: _Optional[_Iterable[_Union[TriggerTransferRenderState.TimerState, _Mapping]]] = ..., capture: _Optional[_Union[TriggerTransferRenderState.CaptureState, _Mapping]] = ..., timecode: _Optional[_Union[TriggerTransferRenderState.TimecodeState, _Mapping]] = ..., system_time: _Optional[int] = ...) -> None: ...
