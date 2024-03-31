fmt = """
=======================================
  Name:           {data.name}
  Address:        {data.mac}
  RSSI:           {data.rssi} dBm
---------------------------------------
  Temperature:    {data.temperature:.01f} \u00b0C
                  {data.temperatureF:.01f} \u00b0F
  Humidity:       {data.humidity} %
  Battery:        {data.battery} %
                  {data.millivolts} mv
  Counter:        {data.counter}
  Flags:          {data.flags}
---------------------------------------
"""

class Lywsd03:
    @staticmethod
    def print(data):
        print(fmt.format(data=data))

    @staticmethod
    def line(data):
        line = f'{data.name:<15} {data.mac:<17}  Temp: {data.temperatureF:.2f} F'
        print(line)

