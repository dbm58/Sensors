from types import SimpleNamespace

class DeviceData(SimpleNamespace):
    def __init__(self, mac = None):
        self.battery     = None
        self.humidity    = None
        self.mac         = mac
        self.name        = None
        self.temperature = None

    @property
    def valid(self):
        """is the structure fully initialized?"""
        return self.name is not None and self.temperature is not None
