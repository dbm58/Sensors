from .adafruit import send as aio_send
from .raw import raw_output

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

class Unknown:
#   send:  to adafruit
#   line:  compact; default
#   print: extended output
#   raw:   print device and advertisement

    @staticmethod
    def line(advert):
        line = f'{advert.device.name:<15} {advert.device.address:<17}  Co2:  {advert.readings.co2}'
        print(line)

    @staticmethod
    def print(advert):
        print(fmt.format(advertisement=advert))

    @staticmethod
    def raw(advert):
        print(raw_output(advert))

    @staticmethod
    def send(advert):
        print('send it')
        aio_send(aio, feed_base, sensor, value)

