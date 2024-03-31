from struct import unpack_from

from bleak import uuids

from .thermometerData import ThermometerData

envSensor = uuids.normalize_uuid_str('181a')

class Lywsd03:
    @staticmethod
    def decode(bluetoothDevice, advertisement):

        if advertisement.service_data is None:
            return None
        if not envSensor in advertisement.service_data:
            return None

        sensorData = advertisement.service_data[envSensor]
                
        temperature, humidity, millivolts, battery, counter, flags = unpack_from("<xxxxxxhHHBBB", sensorData)

        ret = ThermometerData()
        ret.mac          = bluetoothDevice.address
        ret.name         = advertisement.local_name
        ret.rssi         = advertisement.rssi
        ret.temperature  = temperature / 100
        ret.temperatureF = ThermometerData.toF(ret.temperature)
        ret.humidity     = humidity  / 100
        ret.millivolts   = millivolts
        ret.battery      = battery
        ret.counter      = counter
        ret.flags        = flags
        return ret
