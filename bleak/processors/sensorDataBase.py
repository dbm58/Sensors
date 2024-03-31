from dataclasses import dataclass
from typing import Optional

@dataclass
class SensorDataBase():
    mac:    Optional[str] = ""
    name:   Optional[str] = ""
    rssi:   Optional[int] = None
    
