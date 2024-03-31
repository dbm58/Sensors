import asyncio
from dataclasses import dataclass
from enum import IntEnum
import struct

from bleak.backends.device import BLEDevice

class Param(IntEnum):
    """Enums for the different log_size available"""
    TEMPERATURE = 1
    HUMIDITY = 2
    PRESSURE = 3
    CO2 = 4
    HUMIDITY2 = 5


class Status(IntEnum):
    """Enum for the different status colors"""
    NONE = 0
    GREEN = 1
    AMBER = 2
    RED = 3
    BLUE = 4

@dataclass
class CurrentReading:
    """dataclass to store the information when querying the devices current settings"""
    name: str = ""
    version: str = ""
    temperature: float = -1
    humidity: float = -1
    pressure: float = -1
    co2: int = -1
    battery: int = -1
    status: int = -1
    status_t: int = -1
    status_h: int = -1
    interval: int = -1
    ago: int = -1
    stored: int = -1
    counter: int = -1

    def decode(self, value: tuple):
        """Process data from current log_size and process before storing"""
        self.co2 = self._set(Param.CO2, value[0])
        self.temperature = self._set(Param.TEMPERATURE, value[1])
        self.pressure = self._set(Param.PRESSURE, value[2])
        self.humidity = self._set(Param.HUMIDITY, value[3])
        self.battery = value[4]
        self.status = Status(value[5])
        # If extended data list
        if len(value) > 6:
            self.interval = value[6]
            self.ago = value[7]

    def decode2(self, value: tuple, gatt=False):
        """Process data from current log_size and process before storing"""

        # order from gatt and advertisements are different
        if gatt:
            self.temperature = self._set(Param.TEMPERATURE, value[4])
            self.humidity = self._set(Param.HUMIDITY2, value[5])
            self.battery = value[3]
            self.status_h, self.status_t = self._decode_status_flags(value[6])
            self.interval = value[1]
            self.ago = value[2]
        else:
            self.temperature = self._set(Param.TEMPERATURE, value[1])
            self.humidity = self._set(Param.HUMIDITY2, value[3])
            self.battery = value[5]
            self.status_h, self.status_t = self._decode_status_flags(value[6])
            self.interval = value[7]
            self.ago = value[8]
            self.counter = value[9]

    @staticmethod
    def _decode_status_flags(status):
        status_t = Status.GREEN
        status_h = Status.GREEN

        if status & 0b0001:
            status_h = Status.BLUE
        elif status & 0b0010:
            status_h = Status.RED

        if status & 0b0100:
            status_t = Status.BLUE
        elif status & 0b1000:
            status_t = Status.RED

        return (status_h, status_t)

    @staticmethod
    def _set(param: Param, value: int):
        """
        While in CO2 calibration mode Aranet4 did not take new measurements and
        stores Magic numbers in measurement history.
        Here data is converted with checking for Magic numbers.
        """
        invalid_reading_flag = True
        multiplier = 1
        if param == Param.CO2:
            invalid_reading_flag = value >> 15 == 1
            multiplier = 1
        elif param == Param.PRESSURE:
            invalid_reading_flag = value >> 15 == 1
            multiplier = 0.1
        elif param == Param.TEMPERATURE:
            invalid_reading_flag = value >> 14 & 1 == 1
            multiplier = 0.05
        elif param == Param.HUMIDITY:
            invalid_reading_flag = value >> 8
            multiplier = 1
        elif param == Param.HUMIDITY2:
            invalid_reading_flag = value >> 15 == 1
            multiplier = 0.1

        if invalid_reading_flag:
            return -1
        if isinstance(multiplier, float):
            return round(value * multiplier, 1)
        return value * multiplier


@dataclass(order=True)
class Version:
    major: int = -1
    minor: int = -1
    patch: int = -1

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"


class CalibrationState(IntEnum):
    """Enum for calibration state"""
    NOT_ACTIVE = 0
    END_REQUEST = 1
    IN_PROGRESS = 2
    ERROR = 3

@dataclass
class ManufacturerData:
    """dataclass to store manufacturer data"""

    disconnected: bool = False
    calibration_state: CalibrationState  = -1
    dfu_active: bool = False
    integrations: bool = False
    version: Version = None

    def decode(self, value: tuple):
        self.disconnected = self._get_b(value[0], 0)
        self.calibration_state = CalibrationState(self._get_uint2(value[0], 2))
        self.dfu_active = self._get_b(value[0], 4)
        self.integrations = self._get_b(value[0], 5)
        self.version = Version(value[3], value[2], value[1])

    def _get_b(self, value, pos):
        return True if value & (1 << pos) else False

    def _get_uint2(self, value, pos):
        return (value >> pos) & 0x03

@dataclass
class Aranet4Advertisement:
    """dataclass to store the information aboud scanned aranet4 device"""

    device: BLEDevice = None
    readings: CurrentReading = None
    manufacturer_data: ManufacturerData = None
    rssi: int = None

    def __init__(self, device = None, ad_data = None):
        self.device = device

        if device and ad_data:
            has_manufacurer_data = Aranet4.MANUFACTURER_ID in ad_data.manufacturer_data
            self.rssi = ad_data.rssi

            if has_manufacurer_data:
                mf_data = ManufacturerData()
                raw_bytes = ad_data.manufacturer_data[Aranet4.MANUFACTURER_ID]

                packing = None
                if len(raw_bytes) > 7:
                    packing = raw_bytes[7]

                # Basic info
                value_fmt = "<BBBB"
                if packing == 0:
                   value = struct.unpack(value_fmt, raw_bytes[1:5])
                else:
                   value = struct.unpack(value_fmt, raw_bytes[0:4])
                mf_data.decode(value)
                self.manufacturer_data = mf_data

                # Extended info / measurements
                if packing == 0 and len(raw_bytes) >= 24: # Aranet2
                    value_fmt = "<HHHHBBBHHB"
                    value = struct.unpack(value_fmt, raw_bytes[8:24])
                    self.readings = CurrentReading()
                    self.readings.decode2(value)
                    self.readings.name = device.name
                elif packing == 1 and len(raw_bytes) >= 20: # Aranet4
                    value_fmt = "<HHHBBBHH"
                    value = struct.unpack(value_fmt, raw_bytes[8:21])
                    self.readings = CurrentReading()
                    self.readings.decode(value)
                    self.readings.name = device.name
                else:
                    mf_data.integrations = False

class Aranet4:
    MANUFACTURER_ID = 0x0702

    @staticmethod
    def decode(bd, ad):
        advertisement = Aranet4Advertisement(bd,ad)
        return advertisement
