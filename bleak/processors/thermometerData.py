from dataclasses import dataclass
from typing import Optional

from .sensorDataBase import SensorDataBase

#  todo:  need a way to keep this out of the processor list
#  todo:  can `inspect` tell me if there is a dataclass decorator?

@dataclass
class ThermometerData(SensorDataBase):
    battery:      Optional[float] = None
    humidity:     Optional[float] = None
    temperature:  Optional[float] = None
    temperatureF: Optional[float] = None
    humidity:     Optional[float] = None
    millivolts:   Optional[int]   = None
    battery:      Optional[int]   = None
    counter:      Optional[int]   = None
    flags:        Optional[int]   = None

    @property
    def valid(self):
        """is the structure fully initialized?"""
        return self.name is not None and self.temperature is not None

    @staticmethod
    def toF(temp):
        if temp == None:
            return None
        fahrenheit = (temp * 9 / 5) + 32
        return fahrenheit
