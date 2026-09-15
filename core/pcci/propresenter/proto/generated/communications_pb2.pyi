import customOptions_pb2 as _customOptions_pb2
import intRange_pb2 as _intRange_pb2
import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommunicationDevice(_message.Message):
    __slots__ = ("id", "name", "device_type", "behavior", "connected", "auto_reconnect", "options", "serial", "tcp_network", "udp_network", "artnet", "midi")
    class DeviceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEVICE_TYPE_DMX: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_MIDI: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_AMP: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_CITP: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_GLOBAL_CACHE: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_GVG100: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_ROSSTALK: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_SONY_BVS: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_SONY_BVW: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_VDCP: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_ALL_AMERICAN_8000: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_ALL_AMERICAN_9000: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_DAKTRONICS: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_DAKTRONICS_TV: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_ELECTRO_MECH: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_EVERSAN: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_FAIR_PLAY_MP70: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_HARRIS: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_JUGS: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_OES: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_SCOREBIRD: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_SCOREBOT: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_STALKER: _ClassVar[CommunicationDevice.DeviceType]
        DEVICE_TYPE_STAT_CREW: _ClassVar[CommunicationDevice.DeviceType]
    DEVICE_TYPE_DMX: CommunicationDevice.DeviceType
    DEVICE_TYPE_MIDI: CommunicationDevice.DeviceType
    DEVICE_TYPE_AMP: CommunicationDevice.DeviceType
    DEVICE_TYPE_CITP: CommunicationDevice.DeviceType
    DEVICE_TYPE_GLOBAL_CACHE: CommunicationDevice.DeviceType
    DEVICE_TYPE_GVG100: CommunicationDevice.DeviceType
    DEVICE_TYPE_ROSSTALK: CommunicationDevice.DeviceType
    DEVICE_TYPE_SONY_BVS: CommunicationDevice.DeviceType
    DEVICE_TYPE_SONY_BVW: CommunicationDevice.DeviceType
    DEVICE_TYPE_VDCP: CommunicationDevice.DeviceType
    DEVICE_TYPE_ALL_AMERICAN_8000: CommunicationDevice.DeviceType
    DEVICE_TYPE_ALL_AMERICAN_9000: CommunicationDevice.DeviceType
    DEVICE_TYPE_DAKTRONICS: CommunicationDevice.DeviceType
    DEVICE_TYPE_DAKTRONICS_TV: CommunicationDevice.DeviceType
    DEVICE_TYPE_ELECTRO_MECH: CommunicationDevice.DeviceType
    DEVICE_TYPE_EVERSAN: CommunicationDevice.DeviceType
    DEVICE_TYPE_FAIR_PLAY_MP70: CommunicationDevice.DeviceType
    DEVICE_TYPE_HARRIS: CommunicationDevice.DeviceType
    DEVICE_TYPE_JUGS: CommunicationDevice.DeviceType
    DEVICE_TYPE_OES: CommunicationDevice.DeviceType
    DEVICE_TYPE_SCOREBIRD: CommunicationDevice.DeviceType
    DEVICE_TYPE_SCOREBOT: CommunicationDevice.DeviceType
    DEVICE_TYPE_STALKER: CommunicationDevice.DeviceType
    DEVICE_TYPE_STAT_CREW: CommunicationDevice.DeviceType
    class Behavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BEHAVIOR_CONTROLLER: _ClassVar[CommunicationDevice.Behavior]
        BEHAVIOR_DEVICE: _ClassVar[CommunicationDevice.Behavior]
    BEHAVIOR_CONTROLLER: CommunicationDevice.Behavior
    BEHAVIOR_DEVICE: CommunicationDevice.Behavior
    class SerialHardware(_message.Message):
        __slots__ = ("interface_id", "name", "speed", "data_bits", "parity", "stop_bits", "hfci", "hfco")
        class Speed(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SPEED_1200: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_1800: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_2400: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_4800: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_7200: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_9600: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_14400: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_19200: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_28800: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_38400: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_57600: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_62500: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_76800: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_115200: _ClassVar[CommunicationDevice.SerialHardware.Speed]
            SPEED_230400: _ClassVar[CommunicationDevice.SerialHardware.Speed]
        SPEED_1200: CommunicationDevice.SerialHardware.Speed
        SPEED_1800: CommunicationDevice.SerialHardware.Speed
        SPEED_2400: CommunicationDevice.SerialHardware.Speed
        SPEED_4800: CommunicationDevice.SerialHardware.Speed
        SPEED_7200: CommunicationDevice.SerialHardware.Speed
        SPEED_9600: CommunicationDevice.SerialHardware.Speed
        SPEED_14400: CommunicationDevice.SerialHardware.Speed
        SPEED_19200: CommunicationDevice.SerialHardware.Speed
        SPEED_28800: CommunicationDevice.SerialHardware.Speed
        SPEED_38400: CommunicationDevice.SerialHardware.Speed
        SPEED_57600: CommunicationDevice.SerialHardware.Speed
        SPEED_62500: CommunicationDevice.SerialHardware.Speed
        SPEED_76800: CommunicationDevice.SerialHardware.Speed
        SPEED_115200: CommunicationDevice.SerialHardware.Speed
        SPEED_230400: CommunicationDevice.SerialHardware.Speed
        class DataBits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            DATA_BITS_5: _ClassVar[CommunicationDevice.SerialHardware.DataBits]
            DATA_BITS_6: _ClassVar[CommunicationDevice.SerialHardware.DataBits]
            DATA_BITS_7: _ClassVar[CommunicationDevice.SerialHardware.DataBits]
            DATA_BITS_8: _ClassVar[CommunicationDevice.SerialHardware.DataBits]
        DATA_BITS_5: CommunicationDevice.SerialHardware.DataBits
        DATA_BITS_6: CommunicationDevice.SerialHardware.DataBits
        DATA_BITS_7: CommunicationDevice.SerialHardware.DataBits
        DATA_BITS_8: CommunicationDevice.SerialHardware.DataBits
        class Parity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            PARITY_NONE: _ClassVar[CommunicationDevice.SerialHardware.Parity]
            PARITY_ODD: _ClassVar[CommunicationDevice.SerialHardware.Parity]
            PARITY_EVEN: _ClassVar[CommunicationDevice.SerialHardware.Parity]
        PARITY_NONE: CommunicationDevice.SerialHardware.Parity
        PARITY_ODD: CommunicationDevice.SerialHardware.Parity
        PARITY_EVEN: CommunicationDevice.SerialHardware.Parity
        class StopBits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            STOP_BITS_1: _ClassVar[CommunicationDevice.SerialHardware.StopBits]
            STOP_BITS_2: _ClassVar[CommunicationDevice.SerialHardware.StopBits]
        STOP_BITS_1: CommunicationDevice.SerialHardware.StopBits
        STOP_BITS_2: CommunicationDevice.SerialHardware.StopBits
        class HFCI(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            HFCI_NONE: _ClassVar[CommunicationDevice.SerialHardware.HFCI]
            HFCI_RTS: _ClassVar[CommunicationDevice.SerialHardware.HFCI]
            HFCI_DTR: _ClassVar[CommunicationDevice.SerialHardware.HFCI]
        HFCI_NONE: CommunicationDevice.SerialHardware.HFCI
        HFCI_RTS: CommunicationDevice.SerialHardware.HFCI
        HFCI_DTR: CommunicationDevice.SerialHardware.HFCI
        class HFCO(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            HFCO_NONE: _ClassVar[CommunicationDevice.SerialHardware.HFCO]
            HFCO_CTS: _ClassVar[CommunicationDevice.SerialHardware.HFCO]
            HFCO_DSR: _ClassVar[CommunicationDevice.SerialHardware.HFCO]
            HFCO_CAR: _ClassVar[CommunicationDevice.SerialHardware.HFCO]
        HFCO_NONE: CommunicationDevice.SerialHardware.HFCO
        HFCO_CTS: CommunicationDevice.SerialHardware.HFCO
        HFCO_DSR: CommunicationDevice.SerialHardware.HFCO
        HFCO_CAR: CommunicationDevice.SerialHardware.HFCO
        INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SPEED_FIELD_NUMBER: _ClassVar[int]
        DATA_BITS_FIELD_NUMBER: _ClassVar[int]
        PARITY_FIELD_NUMBER: _ClassVar[int]
        STOP_BITS_FIELD_NUMBER: _ClassVar[int]
        HFCI_FIELD_NUMBER: _ClassVar[int]
        HFCO_FIELD_NUMBER: _ClassVar[int]
        interface_id: str
        name: str
        speed: CommunicationDevice.SerialHardware.Speed
        data_bits: CommunicationDevice.SerialHardware.DataBits
        parity: CommunicationDevice.SerialHardware.Parity
        stop_bits: CommunicationDevice.SerialHardware.StopBits
        hfci: CommunicationDevice.SerialHardware.HFCI
        hfco: CommunicationDevice.SerialHardware.HFCO
        def __init__(self, interface_id: _Optional[str] = ..., name: _Optional[str] = ..., speed: _Optional[_Union[CommunicationDevice.SerialHardware.Speed, str]] = ..., data_bits: _Optional[_Union[CommunicationDevice.SerialHardware.DataBits, str]] = ..., parity: _Optional[_Union[CommunicationDevice.SerialHardware.Parity, str]] = ..., stop_bits: _Optional[_Union[CommunicationDevice.SerialHardware.StopBits, str]] = ..., hfci: _Optional[_Union[CommunicationDevice.SerialHardware.HFCI, str]] = ..., hfco: _Optional[_Union[CommunicationDevice.SerialHardware.HFCO, str]] = ...) -> None: ...
    class TCPHardware(_message.Message):
        __slots__ = ("interface_id", "name", "address", "port", "mode")
        class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            MODE_CONNECT_TO: _ClassVar[CommunicationDevice.TCPHardware.Mode]
            MODE_ACCEPT_ON: _ClassVar[CommunicationDevice.TCPHardware.Mode]
        MODE_CONNECT_TO: CommunicationDevice.TCPHardware.Mode
        MODE_ACCEPT_ON: CommunicationDevice.TCPHardware.Mode
        INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ADDRESS_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        MODE_FIELD_NUMBER: _ClassVar[int]
        interface_id: str
        name: str
        address: str
        port: int
        mode: CommunicationDevice.TCPHardware.Mode
        def __init__(self, interface_id: _Optional[str] = ..., name: _Optional[str] = ..., address: _Optional[str] = ..., port: _Optional[int] = ..., mode: _Optional[_Union[CommunicationDevice.TCPHardware.Mode, str]] = ...) -> None: ...
    class UDPHardware(_message.Message):
        __slots__ = ("interface_id", "name", "address", "port", "mode")
        class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            MODE_CONNECT: _ClassVar[CommunicationDevice.UDPHardware.Mode]
            MODE_LISTEN: _ClassVar[CommunicationDevice.UDPHardware.Mode]
            MODE_MULTICAST_LISTEN: _ClassVar[CommunicationDevice.UDPHardware.Mode]
            MODE_BROADCAST: _ClassVar[CommunicationDevice.UDPHardware.Mode]
        MODE_CONNECT: CommunicationDevice.UDPHardware.Mode
        MODE_LISTEN: CommunicationDevice.UDPHardware.Mode
        MODE_MULTICAST_LISTEN: CommunicationDevice.UDPHardware.Mode
        MODE_BROADCAST: CommunicationDevice.UDPHardware.Mode
        INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ADDRESS_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        MODE_FIELD_NUMBER: _ClassVar[int]
        interface_id: str
        name: str
        address: str
        port: int
        mode: CommunicationDevice.UDPHardware.Mode
        def __init__(self, interface_id: _Optional[str] = ..., name: _Optional[str] = ..., address: _Optional[str] = ..., port: _Optional[int] = ..., mode: _Optional[_Union[CommunicationDevice.UDPHardware.Mode, str]] = ...) -> None: ...
    class ArtnetHardware(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class MIDIHardware(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    AUTO_RECONNECT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    TCP_NETWORK_FIELD_NUMBER: _ClassVar[int]
    UDP_NETWORK_FIELD_NUMBER: _ClassVar[int]
    ARTNET_FIELD_NUMBER: _ClassVar[int]
    MIDI_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.UUID
    name: str
    device_type: CommunicationDevice.DeviceType
    behavior: CommunicationDevice.Behavior
    connected: bool
    auto_reconnect: bool
    options: _containers.RepeatedCompositeFieldContainer[CommunicationDeviceOption]
    serial: CommunicationDevice.SerialHardware
    tcp_network: CommunicationDevice.TCPHardware
    udp_network: CommunicationDevice.UDPHardware
    artnet: CommunicationDevice.ArtnetHardware
    midi: CommunicationDevice.MIDIHardware
    def __init__(self, id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., name: _Optional[str] = ..., device_type: _Optional[_Union[CommunicationDevice.DeviceType, str]] = ..., behavior: _Optional[_Union[CommunicationDevice.Behavior, str]] = ..., connected: _Optional[bool] = ..., auto_reconnect: _Optional[bool] = ..., options: _Optional[_Iterable[_Union[CommunicationDeviceOption, _Mapping]]] = ..., serial: _Optional[_Union[CommunicationDevice.SerialHardware, _Mapping]] = ..., tcp_network: _Optional[_Union[CommunicationDevice.TCPHardware, _Mapping]] = ..., udp_network: _Optional[_Union[CommunicationDevice.UDPHardware, _Mapping]] = ..., artnet: _Optional[_Union[CommunicationDevice.ArtnetHardware, _Mapping]] = ..., midi: _Optional[_Union[CommunicationDevice.MIDIHardware, _Mapping]] = ...) -> None: ...

class CommunicationDeviceCloud(_message.Message):
    __slots__ = ("id", "name", "device_type", "behavior")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.UUID
    name: str
    device_type: CommunicationDevice.DeviceType
    behavior: CommunicationDevice.Behavior
    def __init__(self, id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., name: _Optional[str] = ..., device_type: _Optional[_Union[CommunicationDevice.DeviceType, str]] = ..., behavior: _Optional[_Union[CommunicationDevice.Behavior, str]] = ...) -> None: ...

class CommunicationDeviceLocal(_message.Message):
    __slots__ = ("id", "connected", "auto_reconnect", "bundle_name", "bundle_identifier", "options", "serial", "tcp_network", "udp_network", "artnet", "midi")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    AUTO_RECONNECT_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_NAME_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    TCP_NETWORK_FIELD_NUMBER: _ClassVar[int]
    UDP_NETWORK_FIELD_NUMBER: _ClassVar[int]
    ARTNET_FIELD_NUMBER: _ClassVar[int]
    MIDI_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.UUID
    connected: bool
    auto_reconnect: bool
    bundle_name: str
    bundle_identifier: str
    options: _containers.RepeatedCompositeFieldContainer[CommunicationDeviceOption]
    serial: CommunicationDevice.SerialHardware
    tcp_network: CommunicationDevice.TCPHardware
    udp_network: CommunicationDevice.UDPHardware
    artnet: CommunicationDevice.ArtnetHardware
    midi: CommunicationDevice.MIDIHardware
    def __init__(self, id: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., connected: _Optional[bool] = ..., auto_reconnect: _Optional[bool] = ..., bundle_name: _Optional[str] = ..., bundle_identifier: _Optional[str] = ..., options: _Optional[_Iterable[_Union[CommunicationDeviceOption, _Mapping]]] = ..., serial: _Optional[_Union[CommunicationDevice.SerialHardware, _Mapping]] = ..., tcp_network: _Optional[_Union[CommunicationDevice.TCPHardware, _Mapping]] = ..., udp_network: _Optional[_Union[CommunicationDevice.UDPHardware, _Mapping]] = ..., artnet: _Optional[_Union[CommunicationDevice.ArtnetHardware, _Mapping]] = ..., midi: _Optional[_Union[CommunicationDevice.MIDIHardware, _Mapping]] = ...) -> None: ...

class ProPresenterCommunications(_message.Message):
    __slots__ = ("devices",)
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[CommunicationDeviceCloud]
    def __init__(self, devices: _Optional[_Iterable[_Union[CommunicationDeviceCloud, _Mapping]]] = ...) -> None: ...

class ProPresenterLocalCommunications(_message.Message):
    __slots__ = ("devices",)
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[CommunicationDeviceLocal]
    def __init__(self, devices: _Optional[_Iterable[_Union[CommunicationDeviceLocal, _Mapping]]] = ...) -> None: ...

class CommunicationCommand(_message.Message):
    __slots__ = ("name", "description", "format", "parameters")
    class Parameters(_message.Message):
        __slots__ = ("name", "replacement_range", "possible_values", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        REPLACEMENT_RANGE_FIELD_NUMBER: _ClassVar[int]
        POSSIBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        replacement_range: _intRange_pb2.IntRange
        possible_values: _containers.RepeatedScalarFieldContainer[str]
        value: str
        def __init__(self, name: _Optional[str] = ..., replacement_range: _Optional[_Union[_intRange_pb2.IntRange, _Mapping]] = ..., possible_values: _Optional[_Iterable[str]] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    format: str
    parameters: _containers.RepeatedCompositeFieldContainer[CommunicationCommand.Parameters]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., format: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[CommunicationCommand.Parameters, _Mapping]]] = ...) -> None: ...

class CommunicationDeviceOption(_message.Message):
    __slots__ = ("oes_pro_mode",)
    class OESProMode(_message.Message):
        __slots__ = ("enable",)
        ENABLE_FIELD_NUMBER: _ClassVar[int]
        enable: bool
        def __init__(self, enable: _Optional[bool] = ...) -> None: ...
    OES_PRO_MODE_FIELD_NUMBER: _ClassVar[int]
    oes_pro_mode: CommunicationDeviceOption.OESProMode
    def __init__(self, oes_pro_mode: _Optional[_Union[CommunicationDeviceOption.OESProMode, _Mapping]] = ...) -> None: ...
