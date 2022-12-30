import inspect
import string
import sys

from Adafruit_IO import Client, RequestError, Feed, Data

sys.path.append('..')
import app_secrets

def _send(aio, feed_base, sensor, value):
    #  This shouldn't be a separate command
    #  This is an alternate output type
    #  sensor lywsd03 read ##:##:##:##:## --console
    #  sensor lywsd03 read ##:##:##:##:## --aio
    if value is None:
        return

    feed_name = feed_base.substitute({'sensor': sensor}).lower()
    print(feed_name)
    try:
        feed = aio.feeds(feed_name)
        print('feed exists')
        print(feed)
    except RequestError:
        #  The feed doesn't exist.  Create it!
        print('feed doesn\'t exist')
        new_feed = Feed(name=feed_name)
        feed = aio.create_feed(new_feed)
    aio.send_data(feed.key, value)

class Commands:
    def __init__(self):
        pass

    def battery(self, device):
        """Get the battery value"""
        print(f'Fetching battery level from {device.mac}')
        battery = device.battery
        print(f'Battery: {battery}%')
        print()

    def firmware(self, device):
        """Get the firmware version string"""
        print(f'Fetching firmware version from {device.mac}')
        fw_ver = device.firmware_version
        print(f'Firmware Version: {fw_ver}')
        print()

    def read(self, device):
        """read current values from device"""
        print(f'Fetching data from {device.mac}')
        data = device.data
        print(f'Battery:     {data.battery}%')
        print(f'Humidity:    {data.humidity}%')
        print(f'Temperature: {data.temperature:.1C} {data.temperature:.1F}')
        if data.time is not None:
            print(f'Time:        {data.time:%H:%M:%S}')
        print()

    def send(self, device):
        """read data and send it to adafruit.io"""
        data = device.data
        mac  = device.mac.replace(':', '')
        aio = Client(app_secrets.AIO_USER_NAME, app_secrets.AIO_KEY)
        feed = string.Template(f'{mac}-$sensor')
        # _send(aio, feed, 'battery',     data.battery)
        # _send(aio, feed, 'humidity',    data.humidity)
        _send(aio, feed, 'temperature', data.temperature.degrees_f)

    def setc(self, device):
        """set temperature unit on display to Celsius"""
        print(f'Setting temperature units to C for {device.mac}')
        device.units = 'C'

    def setf(self, device):
        """set temperature unit on display to Fahrenheit"""
        print(f'Setting temperature units to F for {device.mac}')
        device.units = 'F'

    def sync(self, device):
        """synchronize time with this machine"""
        print(f'Synchronizing time of {device.mac}')

    def temperature(self, device):
        """current temperature reading"""
        print(f'Reading temperature from {device.mac}')
        print(f'Temperature: {device.temperature:1C} {device.temperature:1F}')

    @classmethod
    def _members(cls):
        members = inspect.getmembers(
                cls(),
                predicate=lambda m:
                    inspect.isroutine(m)
                    and (not m.__name__.startswith('_'))
                    and (not m.__self__ == cls)
                )
        return dict(members)

    @classmethod
    def create(cls):
        return cls._members()

    @classmethod
    def add_parser(cls, parser):
        members = cls._members()
        choices = list(members.keys())

        helptext = ['Command to execute.  One of: ']
        helptext.extend([f'{a} - {members[a].__doc__}' for a in choices])
        helptext = '\n'.join(helptext)

        parser.add_argument('command', help=helptext, choices=choices)

        return choices
