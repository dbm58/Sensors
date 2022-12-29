from typing import NamedTuple
from datetime import datetime

class ReadData(NamedTuple):
    battery:     int
    humidity:    int
    temperature: int
    time:        datetime
    tzoffset:    int
    units:       str

