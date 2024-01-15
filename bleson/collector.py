from deviceData import DeviceData
from govee      import Govee
from lywsd03    import Lywsd03

class Collector:
    def __init__(self, args):
        self.macsToScan = args.macs.split(',')
        self.data = {mac: DeviceData(mac) for mac in self.macsToScan}

    def collect(self, advertisement):
        mac = advertisement.address.address

        if mac not in self.macsToScan:
            return

        if advertisement.name is not None:
            self.data[mac].name = advertisement.name

        newData = Govee.decode(advertisement) \
               or Lywsd03.decode(advertisement)

        if newData is None:
            return

        oldData = self.data[mac]

        newData.battery     = oldData.battery     if newData.battery is None     else newData.battery
        newData.humidity    = oldData.humidity    if newData.humidity is None    else newData.humidity
        newData.mac         = oldData.mac         if newData.mac is None         else newData.mac
        newData.name        = oldData.name        if newData.name is None        else newData.name
        newData.temperature = oldData.temperature if newData.temperature is None else newData.temperature

        self.data[mac] = newData

    @property
    def done(self):
        done = self.data.values() and  all(d.valid for d in self.data.values())
        return done
