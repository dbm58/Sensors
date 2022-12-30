import collections
import contextlib
from datetime import datetime
import logging
from types import SimpleNamespace

from bluepy import btle

from .read_data import ReadData
from .temperature import Temperature

# todo:  need a Temperature class

_LOGGER = logging.getLogger(__name__)

characteristics = {
                     'battery':       '00002A19-0000-1000-8000-00805F9B34FB',
                     'firmware':      '00002a26-0000-1000-8000-00805f9b34fB',
                     'hardware':      '00002A27-0000-1000-8000-00805f9b34fB',
                     'humidity':      '00002A6F-0000-1000-8000-00805f9b34fB',
                     'model_number':  '00002A24-0000-1000-8000-00805f9b34fB',
                     'serial_number': '00002A25-0000-1000-8000-00805f9b34fB',
                     'software':      '00002A28-0000-1000-8000-00805f9b34fB',
                     'manufacturer':  '00002A29-0000-1000-8000-00805f9b34fB',
                     'temperature':   '00002A6E-0000-1000-8000-00805f9b34fB',
                  }
uuids = SimpleNamespace(**characteristics)

class Lywsd03:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, mac, notification_timeout=5.0):
        self._mac = mac
        self._peripheral = btle.Peripheral()
        self._notification_timeout = notification_timeout
        self._handles = {}
        self._history_data = collections.OrderedDict()
        self._context_depth = 0

        self._battery = None
        self._firmware_version = None
        self._humidity = None
        self._temperature = None
        self._time = None
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
        res = ReadData(
            self.battery,
            self.humidity,
            self.temperature,
            self.time,
            None, # tz
            None, # units
        )
        return res

    @property
    def firmware_version(self):
        if self._firmware_version is None:
            with self.connect():
                char = self._peripheral.getCharacteristics(uuid=uuids.firmware)[0]
                self._firmware_version = str(char.read(), 'utf-8')
        return self._firmware_version

    @property
    def humidity(self):
        if self._humidity is None:
            with self.connect():
                char = self._peripheral.getCharacteristics(uuid=uuids.humidity)[0]
                data_bytes = char.read()
                self._humidity = int.from_bytes(data_bytes, byteorder='little') / 100

        return self._humidity

    @property
    def mac(self):
        return self._mac

    @property
    def temperature(self):
        if self._temperature is None:
            with self.connect():
                char = self._peripheral.getCharacteristics(uuid=uuids.temperature)[0]
                data_bytes = char.read()
                self._temperature = Temperature.from_bytes(data_bytes, 100)

        return self._temperature

    @property
    def time(self):
        return None

    @time.setter
    def time(self, value: datetime):
        pass

    @property
    def units(self):
        return None

    @units.setter
    def units(self, value):
        raise NotImplementedError()

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
