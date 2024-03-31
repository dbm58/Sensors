fmt = """
=======================================
  Name:     {advertisement.device.name}
  Address:  {advertisement.device.address}
  RSSI:     {advertisement.rssi} dBm
--------------------------------------
  CO2:            {advertisement.readings.co2} pm
  Temperature:    {advertisement.readings.temperature:.01f} \u00b0C
  Humidity:       {advertisement.readings.humidity} %
  Pressure:       {advertisement.readings.pressure:.01f} hPa
  Battery:        {advertisement.readings.battery} %
  Status Disp.:   {advertisement.readings.status.name}
  Age:            {advertisement.readings.ago}/{advertisement.readings.interval}
  Counter:        {advertisement.readings.counter}
--------------------------------------
"""
#  Put these back in some day.  If there is no alarm on the temp and/or humidity,
#  then these are -1 (normal state).  Which means that there is no name property
#  Status Temp.:   {advertisement.readings.status_t.name}
#  Status Humid.:  {advertisement.readings.status_h.name}

class Govee:
    @staticmethod
    def print(data):
        print(data)

