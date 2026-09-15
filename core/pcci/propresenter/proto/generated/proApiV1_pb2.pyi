import proApiV1Announcement_pb2 as _proApiV1Announcement_pb2
import proApiV1Audio_pb2 as _proApiV1Audio_pb2
import proApiV1Capture_pb2 as _proApiV1Capture_pb2
import proApiV1Clear_pb2 as _proApiV1Clear_pb2
import proApiV1ErrorResponse_pb2 as _proApiV1ErrorResponse_pb2
import proApiV1Groups_pb2 as _proApiV1Groups_pb2
import proApiV1Link_pb2 as _proApiV1Link_pb2
import proApiV1Library_pb2 as _proApiV1Library_pb2
import proApiV1Looks_pb2 as _proApiV1Looks_pb2
import proApiV1Macro_pb2 as _proApiV1Macro_pb2
import proApiV1Masks_pb2 as _proApiV1Masks_pb2
import proApiV1Media_pb2 as _proApiV1Media_pb2
import proApiV1Message_pb2 as _proApiV1Message_pb2
import proApiV1Miscellaneous_pb2 as _proApiV1Miscellaneous_pb2
import proApiV1Playlist_pb2 as _proApiV1Playlist_pb2
import proApiV1Preroll_pb2 as _proApiV1Preroll_pb2
import proApiV1Presentation_pb2 as _proApiV1Presentation_pb2
import proApiV1Prop_pb2 as _proApiV1Prop_pb2
import proApiV1Stage_pb2 as _proApiV1Stage_pb2
import proApiV1Status_pb2 as _proApiV1Status_pb2
import proApiV1Theme_pb2 as _proApiV1Theme_pb2
import proApiV1Timer_pb2 as _proApiV1Timer_pb2
import proApiV1Transport_pb2 as _proApiV1Transport_pb2
import proApiV1Trigger_pb2 as _proApiV1Trigger_pb2
import proApiV1VideoInputs_pb2 as _proApiV1VideoInputs_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NetworkAPI_v1(_message.Message):
    __slots__ = ("action",)
    class Action(_message.Message):
        __slots__ = ("audio_request", "capture_request", "clearing_request", "groups_request", "link_request", "library_request", "looks_request", "macro_request", "masks_request", "media_request", "message_request", "miscellaneous_request", "playlist_request", "preroll_request", "presentation_request", "prop_request", "stage_request", "status_request", "theme_request", "timer_request", "transport_request", "trigger_request", "video_inputs_request", "announcement_request", "audio_response", "capture_response", "clearing_response", "groups_response", "link_response", "library_response", "looks_response", "macro_response", "masks_response", "media_response", "message_response", "miscellaneous_response", "playlist_response", "preroll_response", "presentation_response", "prop_response", "stage_response", "status_response", "theme_response", "timer_response", "transport_response", "trigger_response", "video_inputs_response", "announcement_response", "error_response", "update_identifier")
        AUDIO_REQUEST_FIELD_NUMBER: _ClassVar[int]
        CAPTURE_REQUEST_FIELD_NUMBER: _ClassVar[int]
        CLEARING_REQUEST_FIELD_NUMBER: _ClassVar[int]
        GROUPS_REQUEST_FIELD_NUMBER: _ClassVar[int]
        LINK_REQUEST_FIELD_NUMBER: _ClassVar[int]
        LIBRARY_REQUEST_FIELD_NUMBER: _ClassVar[int]
        LOOKS_REQUEST_FIELD_NUMBER: _ClassVar[int]
        MACRO_REQUEST_FIELD_NUMBER: _ClassVar[int]
        MASKS_REQUEST_FIELD_NUMBER: _ClassVar[int]
        MEDIA_REQUEST_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_REQUEST_FIELD_NUMBER: _ClassVar[int]
        MISCELLANEOUS_REQUEST_FIELD_NUMBER: _ClassVar[int]
        PLAYLIST_REQUEST_FIELD_NUMBER: _ClassVar[int]
        PREROLL_REQUEST_FIELD_NUMBER: _ClassVar[int]
        PRESENTATION_REQUEST_FIELD_NUMBER: _ClassVar[int]
        PROP_REQUEST_FIELD_NUMBER: _ClassVar[int]
        STAGE_REQUEST_FIELD_NUMBER: _ClassVar[int]
        STATUS_REQUEST_FIELD_NUMBER: _ClassVar[int]
        THEME_REQUEST_FIELD_NUMBER: _ClassVar[int]
        TIMER_REQUEST_FIELD_NUMBER: _ClassVar[int]
        TRANSPORT_REQUEST_FIELD_NUMBER: _ClassVar[int]
        TRIGGER_REQUEST_FIELD_NUMBER: _ClassVar[int]
        VIDEO_INPUTS_REQUEST_FIELD_NUMBER: _ClassVar[int]
        ANNOUNCEMENT_REQUEST_FIELD_NUMBER: _ClassVar[int]
        AUDIO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        CAPTURE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        CLEARING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        GROUPS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        LINK_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        LIBRARY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        LOOKS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        MACRO_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        MASKS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        MEDIA_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        MISCELLANEOUS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        PLAYLIST_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        PREROLL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        PRESENTATION_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        PROP_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        STAGE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        STATUS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        THEME_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        TIMER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        TRANSPORT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        TRIGGER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        VIDEO_INPUTS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        ANNOUNCEMENT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        ERROR_RESPONSE_FIELD_NUMBER: _ClassVar[int]
        UPDATE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        audio_request: _proApiV1Audio_pb2.API_v1_Audio_Request
        capture_request: _proApiV1Capture_pb2.API_v1_Capture_Request
        clearing_request: _proApiV1Clear_pb2.API_v1_Clear_Request
        groups_request: _proApiV1Groups_pb2.API_v1_Groups_Request
        link_request: _proApiV1Link_pb2.API_v1_Link_Request
        library_request: _proApiV1Library_pb2.API_v1_Library_Request
        looks_request: _proApiV1Looks_pb2.API_v1_Looks_Request
        macro_request: _proApiV1Macro_pb2.API_v1_Macro_Request
        masks_request: _proApiV1Masks_pb2.API_v1_Masks_Request
        media_request: _proApiV1Media_pb2.API_v1_Media_Request
        message_request: _proApiV1Message_pb2.API_v1_Message_Request
        miscellaneous_request: _proApiV1Miscellaneous_pb2.API_v1_Miscellaneous_Request
        playlist_request: _proApiV1Playlist_pb2.API_v1_Playlist_Request
        preroll_request: _proApiV1Preroll_pb2.API_v1_Preroll_Request
        presentation_request: _proApiV1Presentation_pb2.API_v1_Presentation_Request
        prop_request: _proApiV1Prop_pb2.API_v1_Prop_Request
        stage_request: _proApiV1Stage_pb2.API_v1_Stage_Request
        status_request: _proApiV1Status_pb2.API_v1_Status_Request
        theme_request: _proApiV1Theme_pb2.API_v1_Theme_Request
        timer_request: _proApiV1Timer_pb2.API_v1_Timer_Request
        transport_request: _proApiV1Transport_pb2.API_v1_Transport_Request
        trigger_request: _proApiV1Trigger_pb2.API_v1_Trigger_Request
        video_inputs_request: _proApiV1VideoInputs_pb2.API_v1_Video_Inputs_Request
        announcement_request: _proApiV1Announcement_pb2.API_v1_Announcement_Request
        audio_response: _proApiV1Audio_pb2.API_v1_Audio_Response
        capture_response: _proApiV1Capture_pb2.API_v1_Capture_Response
        clearing_response: _proApiV1Clear_pb2.API_v1_Clear_Response
        groups_response: _proApiV1Groups_pb2.API_v1_Groups_Response
        link_response: _proApiV1Link_pb2.API_v1_Link_Response
        library_response: _proApiV1Library_pb2.API_v1_Library_Response
        looks_response: _proApiV1Looks_pb2.API_v1_Looks_Response
        macro_response: _proApiV1Macro_pb2.API_v1_Macro_Response
        masks_response: _proApiV1Masks_pb2.API_v1_Masks_Response
        media_response: _proApiV1Media_pb2.API_v1_Media_Response
        message_response: _proApiV1Message_pb2.API_v1_Message_Response
        miscellaneous_response: _proApiV1Miscellaneous_pb2.API_v1_Miscellaneous_Response
        playlist_response: _proApiV1Playlist_pb2.API_v1_Playlist_Response
        preroll_response: _proApiV1Preroll_pb2.API_v1_Preroll_Response
        presentation_response: _proApiV1Presentation_pb2.API_v1_Presentation_Response
        prop_response: _proApiV1Prop_pb2.API_v1_Prop_Response
        stage_response: _proApiV1Stage_pb2.API_v1_Stage_Response
        status_response: _proApiV1Status_pb2.API_v1_Status_Response
        theme_response: _proApiV1Theme_pb2.API_v1_Theme_Response
        timer_response: _proApiV1Timer_pb2.API_v1_Timer_Response
        transport_response: _proApiV1Transport_pb2.API_v1_Transport_Response
        trigger_response: _proApiV1Trigger_pb2.API_v1_Trigger_Response
        video_inputs_response: _proApiV1VideoInputs_pb2.API_v1_Video_Inputs_Response
        announcement_response: _proApiV1Announcement_pb2.API_v1_Announcement_Response
        error_response: _proApiV1ErrorResponse_pb2.API_v1_Error_Response
        update_identifier: str
        def __init__(self, audio_request: _Optional[_Union[_proApiV1Audio_pb2.API_v1_Audio_Request, _Mapping]] = ..., capture_request: _Optional[_Union[_proApiV1Capture_pb2.API_v1_Capture_Request, _Mapping]] = ..., clearing_request: _Optional[_Union[_proApiV1Clear_pb2.API_v1_Clear_Request, _Mapping]] = ..., groups_request: _Optional[_Union[_proApiV1Groups_pb2.API_v1_Groups_Request, _Mapping]] = ..., link_request: _Optional[_Union[_proApiV1Link_pb2.API_v1_Link_Request, _Mapping]] = ..., library_request: _Optional[_Union[_proApiV1Library_pb2.API_v1_Library_Request, _Mapping]] = ..., looks_request: _Optional[_Union[_proApiV1Looks_pb2.API_v1_Looks_Request, _Mapping]] = ..., macro_request: _Optional[_Union[_proApiV1Macro_pb2.API_v1_Macro_Request, _Mapping]] = ..., masks_request: _Optional[_Union[_proApiV1Masks_pb2.API_v1_Masks_Request, _Mapping]] = ..., media_request: _Optional[_Union[_proApiV1Media_pb2.API_v1_Media_Request, _Mapping]] = ..., message_request: _Optional[_Union[_proApiV1Message_pb2.API_v1_Message_Request, _Mapping]] = ..., miscellaneous_request: _Optional[_Union[_proApiV1Miscellaneous_pb2.API_v1_Miscellaneous_Request, _Mapping]] = ..., playlist_request: _Optional[_Union[_proApiV1Playlist_pb2.API_v1_Playlist_Request, _Mapping]] = ..., preroll_request: _Optional[_Union[_proApiV1Preroll_pb2.API_v1_Preroll_Request, _Mapping]] = ..., presentation_request: _Optional[_Union[_proApiV1Presentation_pb2.API_v1_Presentation_Request, _Mapping]] = ..., prop_request: _Optional[_Union[_proApiV1Prop_pb2.API_v1_Prop_Request, _Mapping]] = ..., stage_request: _Optional[_Union[_proApiV1Stage_pb2.API_v1_Stage_Request, _Mapping]] = ..., status_request: _Optional[_Union[_proApiV1Status_pb2.API_v1_Status_Request, _Mapping]] = ..., theme_request: _Optional[_Union[_proApiV1Theme_pb2.API_v1_Theme_Request, _Mapping]] = ..., timer_request: _Optional[_Union[_proApiV1Timer_pb2.API_v1_Timer_Request, _Mapping]] = ..., transport_request: _Optional[_Union[_proApiV1Transport_pb2.API_v1_Transport_Request, _Mapping]] = ..., trigger_request: _Optional[_Union[_proApiV1Trigger_pb2.API_v1_Trigger_Request, _Mapping]] = ..., video_inputs_request: _Optional[_Union[_proApiV1VideoInputs_pb2.API_v1_Video_Inputs_Request, _Mapping]] = ..., announcement_request: _Optional[_Union[_proApiV1Announcement_pb2.API_v1_Announcement_Request, _Mapping]] = ..., audio_response: _Optional[_Union[_proApiV1Audio_pb2.API_v1_Audio_Response, _Mapping]] = ..., capture_response: _Optional[_Union[_proApiV1Capture_pb2.API_v1_Capture_Response, _Mapping]] = ..., clearing_response: _Optional[_Union[_proApiV1Clear_pb2.API_v1_Clear_Response, _Mapping]] = ..., groups_response: _Optional[_Union[_proApiV1Groups_pb2.API_v1_Groups_Response, _Mapping]] = ..., link_response: _Optional[_Union[_proApiV1Link_pb2.API_v1_Link_Response, _Mapping]] = ..., library_response: _Optional[_Union[_proApiV1Library_pb2.API_v1_Library_Response, _Mapping]] = ..., looks_response: _Optional[_Union[_proApiV1Looks_pb2.API_v1_Looks_Response, _Mapping]] = ..., macro_response: _Optional[_Union[_proApiV1Macro_pb2.API_v1_Macro_Response, _Mapping]] = ..., masks_response: _Optional[_Union[_proApiV1Masks_pb2.API_v1_Masks_Response, _Mapping]] = ..., media_response: _Optional[_Union[_proApiV1Media_pb2.API_v1_Media_Response, _Mapping]] = ..., message_response: _Optional[_Union[_proApiV1Message_pb2.API_v1_Message_Response, _Mapping]] = ..., miscellaneous_response: _Optional[_Union[_proApiV1Miscellaneous_pb2.API_v1_Miscellaneous_Response, _Mapping]] = ..., playlist_response: _Optional[_Union[_proApiV1Playlist_pb2.API_v1_Playlist_Response, _Mapping]] = ..., preroll_response: _Optional[_Union[_proApiV1Preroll_pb2.API_v1_Preroll_Response, _Mapping]] = ..., presentation_response: _Optional[_Union[_proApiV1Presentation_pb2.API_v1_Presentation_Response, _Mapping]] = ..., prop_response: _Optional[_Union[_proApiV1Prop_pb2.API_v1_Prop_Response, _Mapping]] = ..., stage_response: _Optional[_Union[_proApiV1Stage_pb2.API_v1_Stage_Response, _Mapping]] = ..., status_response: _Optional[_Union[_proApiV1Status_pb2.API_v1_Status_Response, _Mapping]] = ..., theme_response: _Optional[_Union[_proApiV1Theme_pb2.API_v1_Theme_Response, _Mapping]] = ..., timer_response: _Optional[_Union[_proApiV1Timer_pb2.API_v1_Timer_Response, _Mapping]] = ..., transport_response: _Optional[_Union[_proApiV1Transport_pb2.API_v1_Transport_Response, _Mapping]] = ..., trigger_response: _Optional[_Union[_proApiV1Trigger_pb2.API_v1_Trigger_Response, _Mapping]] = ..., video_inputs_response: _Optional[_Union[_proApiV1VideoInputs_pb2.API_v1_Video_Inputs_Response, _Mapping]] = ..., announcement_response: _Optional[_Union[_proApiV1Announcement_pb2.API_v1_Announcement_Response, _Mapping]] = ..., error_response: _Optional[_Union[_proApiV1ErrorResponse_pb2.API_v1_Error_Response, _Mapping]] = ..., update_identifier: _Optional[str] = ...) -> None: ...
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: NetworkAPI_v1.Action
    def __init__(self, action: _Optional[_Union[NetworkAPI_v1.Action, _Mapping]] = ...) -> None: ...
