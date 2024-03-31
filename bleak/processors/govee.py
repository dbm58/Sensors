from struct import unpack_from

from .thermometerData import ThermometerData

class Govee:
    @staticmethod
    def decode(bluetoothDevice, advertisement):
        return bluetoothDevice

    @classmethod
    def twos_complement(cls, n: int, w: int = 16) -> int:
        """Two's complement integer conversion."""
        # Adapted from: https://stackoverflow.com/a/33716541.
        if n & (1 << (w - 1)):
            n = n - (1 << w)
        return n

    @classmethod
    def decodeimpl(cls, advertisement):
        if advertisement.mfg_data is None:
            return

        prefix = advertisement.mfg_data.hex()[0:4]
        if prefix != "88ec":
            return

        raw_temp, hum, batt = unpack_from("<HHB", advertisement.mfg_data, 3)

        data = ThermometerData()
        data.battery     = batt
        data.humidity    = hum / 100
        data.mac         = advertisement.address.address
        data.temperature = cls.twos_complement(raw_temp) / 100

        return data
