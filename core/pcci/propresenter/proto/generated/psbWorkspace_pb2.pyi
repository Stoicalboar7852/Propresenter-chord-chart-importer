import advertisementGroup_pb2 as _advertisementGroup_pb2
import digitalAudio_pb2 as _digitalAudio_pb2
import input_pb2 as _input_pb2
import proscreen_pb2 as _proscreen_pb2
import recording_pb2 as _recording_pb2
import zone_pb2 as _zone_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProScoreboardWorkspace(_message.Message):
    __slots__ = ("pro_screens", "videoInputs", "record_settings", "digital_audio_setup", "audio_inputs", "audio_input_transition_time", "zones", "advertisements")
    PRO_SCREENS_FIELD_NUMBER: _ClassVar[int]
    VIDEOINPUTS_FIELD_NUMBER: _ClassVar[int]
    RECORD_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_AUDIO_SETUP_FIELD_NUMBER: _ClassVar[int]
    AUDIO_INPUTS_FIELD_NUMBER: _ClassVar[int]
    AUDIO_INPUT_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    ADVERTISEMENTS_FIELD_NUMBER: _ClassVar[int]
    pro_screens: _containers.RepeatedCompositeFieldContainer[_proscreen_pb2.ProPresenterScreen]
    videoInputs: _containers.RepeatedCompositeFieldContainer[_input_pb2.VideoInput]
    record_settings: _recording_pb2.Recording.SettingsDocument
    digital_audio_setup: _digitalAudio_pb2.DigitalAudio.Setup
    audio_inputs: _containers.RepeatedCompositeFieldContainer[_input_pb2.AudioInput]
    audio_input_transition_time: float
    zones: _containers.RepeatedCompositeFieldContainer[_zone_pb2.Zone]
    advertisements: _containers.RepeatedCompositeFieldContainer[_advertisementGroup_pb2.AdvertisementGroup]
    def __init__(self, pro_screens: _Optional[_Iterable[_Union[_proscreen_pb2.ProPresenterScreen, _Mapping]]] = ..., videoInputs: _Optional[_Iterable[_Union[_input_pb2.VideoInput, _Mapping]]] = ..., record_settings: _Optional[_Union[_recording_pb2.Recording.SettingsDocument, _Mapping]] = ..., digital_audio_setup: _Optional[_Union[_digitalAudio_pb2.DigitalAudio.Setup, _Mapping]] = ..., audio_inputs: _Optional[_Iterable[_Union[_input_pb2.AudioInput, _Mapping]]] = ..., audio_input_transition_time: _Optional[float] = ..., zones: _Optional[_Iterable[_Union[_zone_pb2.Zone, _Mapping]]] = ..., advertisements: _Optional[_Iterable[_Union[_advertisementGroup_pb2.AdvertisementGroup, _Mapping]]] = ...) -> None: ...
