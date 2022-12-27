import inspect

class Commands(object):
    def __init__(self):
        pass

    def read(self, client):
        """read current values from device"""
        print('Fetching data from {}'.format(client.mac))
        batt = client.battery
        data = client.data
        time = client.time
        units = client.units
        temp = data.temperature if units == 'C' else (data.temperature * 9/5 + 32)
        print(f'Battery:     {batt}%')
        print(f'Humidity:    {data.humidity}%')
        print(f'Temperature: {temp:.1f}°{units}')
        print(f'Time:        {time[0]:%H:%M:%S}')
        print()
    
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
