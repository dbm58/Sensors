import collections
import contextlib
import logging
import struct
import time
from datetime import datetime
from types import SimpleNamespace

from bluepy import btle

from .read_data import ReadData
from .temperature import Temperature

_LOGGER = logging.getLogger(__name__)

characteristics = {
                     'battery':       'EBE0CCC4-7A0A-4B0C-8A1A-6FF2997DA3A6',
                     'data':          'EBE0CCC1-7A0A-4B0C-8A1A-6FF2997DA3A6',
                     'firmware':      '00002a26-0000-1000-8000-00805f9b34fB',
                     'hardware':      '00002A27-0000-1000-8000-00805f9b34fB',
                     'history':       'EBE0CCBC-7A0A-4B0C-8A1A-6FF2997DA3A6',
                     'humidity':      None,
                     'model_number':  '00002A24-0000-1000-8000-00805f9b34fB',
                     'serial_number': '00002A25-0000-1000-8000-00805f9b34fB',
                     'software':      '00002A28-0000-1000-8000-00805f9b34fB',
                     'manufacturer':  '00002A29-0000-1000-8000-00805f9b34fB',
                     'num_records':   'EBE0CCB9-7A0A-4B0C-8A1A-6FF2997DA3A6',
                     'record_idx':    'EBE0CCBA-7A0A-4B0C-8A1A-6FF2997DA3A6',
                     'temperature':   None,
                     'time':          'EBE0CCB7-7A0A-4B0C-8A1A-6FF2997DA3A6',
                     'units':         'EBE0CCBE-7A0A-4B0C-8A1A-6FF2997DA3A6',
                  }
uuids = SimpleNamespace(**characteristics)

UNITS = {
    b'\x01': 'F',
    b'\xff': 'C',
}

UNITS_CODES = {
    'C': b'\xff',
    'F': b'\x01',
}

class Lywsd02:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, mac, notification_timeout=5.0):
        self._mac = mac
        self._peripheral = btle.Peripheral()
        self._notification_timeout = notification_timeout
        self._handles = {}
        self._history_data = collections.OrderedDict()
        self._context_depth = 0

        self._battery = None
        self._humidity = None
        self._temperature = None
        self._time = None
        self._tz_offset = None
        self._units = None

    @property
    def battery(self):
        if self._battery is not None:
            return self._battery

        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.battery)[0]
            self._battery = ord(char.read())
        return self._battery

    @property
    def data(self):
        self._get_sensor_data()
        res = ReadData(
            self.battery,
            self.humidity,
            self.temperature,
            self.time,
            self.tz_offset,
            self.units,
        )
        return res

    @property
    def history_data(self):
        self._get_history_data()
        return self._history_data

    @property
    def history_index(self):
        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.record_idx)[0]
            value = char.read()
        _idx = 0 if len(value) == 0 else struct.unpack_from('I', value)
        return _idx

    @history_index.setter
    def history_index(self, value):
        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.record_idx)[0]
            char.write(struct.pack('I', value), withResponse=True)

    @property
    def humidity(self):
        return self._humidity

    @property
    def mac(self):
        return self._mac

    @property
    def num_stored_entries(self):
        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.num_records)[0]
            value = char.read()
        total_records, current_records = struct.unpack_from('II', value)
        return total_records, current_records

    @property
    def temperature(self):
        return self._temperature

    @property
    def time(self):
        if self._time is not None:
            return self._time

        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.time)[0]
            value = char.read()
        if len(value) == 5:
            device_time, tz_offset = struct.unpack('Ib', value)
        else:
            device_time = struct.unpack('I', value)[0]
            tz_offset = 0
        self._time = datetime.fromtimestamp(device_time)
        self._tz_offset = tz_offset
        return self._time

    @time.setter
    def time(self, new_time: datetime):
        data = struct.pack('Ib', int(new_time.timestamp()), self.tz_offset)
        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.time)[0]
            char.write(data, withResponse=True)

    #  todo:  this should not be a property.  It should be an extension
    #         of datetime instance
    @property
    def tz_offset(self):
        if self._tz_offset is not None:
            return self._tz_offset
        if time.localtime().tm_isdst and time.daylight:
            return -time.altzone // 3600
        return -time.timezone // 3600

    #  todo:  I think that this is only needed because the getter was broken
    @tz_offset.setter
    def tz_offset(self, tz_offset: int):
        self._tz_offset = tz_offset

    @property
    def units(self):
        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.units)[0]
            value = char.read()
        return UNITS[value]

    @units.setter
    def units(self, value):
        if value.upper() not in UNITS_CODES:
            raise ValueError(
                f'Units value must be one of {list(UNITS_CODES.keys())}')

        with self.connect():
            char = self._peripheral.getCharacteristics(uuid=uuids.units)[0]
            char.write(UNITS_CODES[value.upper()], withResponse=True)

    def _get_sensor_data(self):
        if self._temperature is not None:
            return

        with self.connect():
            self._subscribe(uuids.data, self._process_sensor_data)

            if not self._peripheral.waitForNotifications(
                    self._notification_timeout):
                raise TimeoutError(f'No data from device for {self._notification_timeout} seconds')

    def _get_history_data(self):
        with self.connect():
            self._subscribe(uuids.history, self._process_history_data)

            while True:
                if not self._peripheral.waitForNotifications(
                        self._notification_timeout):
                    break

    # pylint: disable=invalid-name
    def handleNotification(self, handle, data):
        func = self._handles.get(handle)
        if func:
            func(data)

    def _subscribe(self, uuid, callback):
        self._peripheral.setDelegate(self)
        char = self._peripheral.getCharacteristics(uuid=uuid)[0]
        self._handles[char.getHandle()] = callback
        desc = char.getDescriptors(forUUID=0x2902)[0]

        desc.write(0x01.to_bytes(2, byteorder="little"), withResponse=True)

    def _process_sensor_data(self, data):
        if self._temperature is not None:
            return

        temperature, humidity = struct.unpack_from('hB', data)
        temperature /= 100

        self._temperature = Temperature(temperature)
        self._humidity    = humidity

    def _process_history_data(self, data):
        (idx, timestamp, max_temp, max_hum, min_temp, min_hum) = struct.unpack_from('<IIhBhB', data)

        date = datetime.fromtimestamp(timestamp)
        min_temp /= 100
        max_temp /= 100

        self._history_data[idx] = [date, min_temp, min_hum, max_temp, max_hum]

    @contextlib.contextmanager
    def connect(self):
        if self._context_depth == 0:
            _LOGGER.debug('Connecting to %s', self._mac)
            self._peripheral.connect(self._mac)
        self._context_depth += 1
        try:
            yield self
        finally:
            self._context_depth -= 1
            if self._context_depth == 0:
                _LOGGER.debug('Disconnecting from %s', self._mac)
                self._peripheral.disconnect()
