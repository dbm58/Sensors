import inspect
import string
from types import SimpleNamespace

from Adafruit_IO import Client, RequestError, Feed, Data

import secrets

def _read(client):
    data = client.data
    units = client.units
    res  = SimpleNamespace(
           **{
                 'battery':     client.battery,
                 'humidity':    data.humidity,
                 'temperature': data.temperature if units == 'C' else (data.temperature * 9/5 + 32),
                 'time':        client.time[0],
                 'tzoffset':    client.time[1],
                 'units':       units,
             })
    return res

def _send(aio, feedBase, sensor, value):
    feedName = feedBase.substitute({'sensor': sensor}).lower()
    print(feedName)
    try:
        feed = aio.feeds(feedName)
        print('feed exists')
        print(feed)
    except RequestError:
        #  The feed doesn't exist.  Create it!
        print('feed doesn''t exist')
        newFeed = Feed(name=feedName)
        feed = aio.create_feed(newFeed)
    aio.send_data(feed.key, value)
    
class Commands(object):
    def __init__(self):
        pass

    def read(self, client):
        """read current values from device"""
        print('Fetching data from {}'.format(client.mac))
        data = _read(client)
        print(f'Battery:     {data.battery}%')
        print(f'Humidity:    {data.humidity}%')
        print(f'Temperature: {data.temperature:.1f}°{data.units}')
        print(f'Time:        {data.time:%H:%M:%S}')
        print()
    
    def send(self, client):
        """read data and send it to adafruit.io"""
        data = _read(client)
        aio = Client(secrets.userName, secrets.key)
        feed = string.Template(f'{client.macNum}-$sensor')
        _send(aio, feed, 'battery',     data.battery)
        _send(aio, feed, 'humidity',    data.humidity)
        _send(aio, feed, 'temperature', data.temperature)
    
    def setc(self, client):
        """set temperature unit on display to Celsius"""
        print('Setting temperature units to C for {}'.format(client.mac))
        client.units = 'C'
    
    def setf(self, client):
        """set temperature unit on display to Fahrenheit"""
        print('Setting temperature units to F for {}'.format(client.mac))
        client.units = 'F'
    
    def sync(self, client):
        """synchronize time with this machine"""
        print('Synchronizing time of {}'.format(client.mac))
        client.time = datetime.now()

    @classmethod
    def create(cls, parser):
        members = inspect.getmembers(cls())
        actions = [y for y in members if (not y[0].startswith('__')) and y[0] != 'create']

        dispatch = {k:v for k,v in actions}
        choices = list(dispatch.keys())
        helptext = ['Action to perform, either: ']
        helptext.extend([f'{a} - {dispatch[a].__doc__}' for a in choices])
        helptext = '\n'.join(helptext)

        return (dispatch, choices, helptext)
