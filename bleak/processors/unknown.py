from struct import unpack_from

class Unknown:
    @staticmethod
    def decode(bluetoothDevice, advertisement):
        return {
            'device': bluetoothDevice,
            'advertisement': advertisement
        }
