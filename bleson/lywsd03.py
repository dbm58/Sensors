from struct import unpack_from

from deviceData import DeviceData

class Lywsd03:
    @staticmethod
    def decode(advertisement):
        # 1a180e614338c1a49406d412900b540a0f
        # xxxx                               uuid (0x181a)
        #     xxxxxxxxxxxx                   mac
        #                 xxxx               temp
        #                     xxxx           humidity
        #                         xxxx       battery mv
        #                             xx     battery %
        #                               xx   frame packet counter
        #                                 xx flags

        if advertisement.service_data is None:
            return

        #  should probably also check the service data length

        uuid, temp, hum, battmv, batt, counter, flags = unpack_from("<HxxxxxxhHHBBB", advertisement.service_data)

        if uuid != 0x181a:
            return None

        data = DeviceData()
        data.battery     = batt
        data.humidity    = hum / 100
        data.mac         = advertisement.address.address
        data.temperature = temp / 100

        # print(advertisement.address, 'service_data    ', advertisement.service_data.hex())
        # print(advertisement.address, 'uuid',        hex(uuid))
        # print(advertisement.address, 'temperature', temp / 100)
        # print(advertisement.address, 'humidity   ', hum / 100)
        # print(advertisement.address, 'battery mv ', battmv)
        # print(advertisement.address, 'battery    ', batt)
        # print(advertisement.address, 'counter    ', counter)
        # print(advertisement.address, 'flags      ', flags)

        return data
