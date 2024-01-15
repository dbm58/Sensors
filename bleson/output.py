#!/usr/bin/env python

from aio import Aio

class Output:
    @classmethod
    def toFahrenheit(cls, temp):
        fahrenheit = (temp * 9 / 5) + 32
        return fahrenheit

    @classmethod
    def write(cls, args, collector):
        for data in collector.data.values():
            if args.command == 'send':
                cls.writeAio(args, data)
            else:
                cls.writeConsole(args, data)

    @classmethod
    def writeConsole(cls, args, data):
        print('===============================')
        print('MAC:         ', data.mac)
        print('Name:        ', data.name)
        print('Temperature: ', f'{data.temperature} C')
        print('             ', f'{cls.toFahrenheit(data.temperature):.2f} F')
        print('Humidity:    ', f'{data.humidity}%')
        print('Battery:     ', f'{data.battery}%')
        print('Valid:       ', f'{data.valid}')

    @classmethod
    def writeAio(cls, args, data):
        if not data.valid:
            return

        if args.sendTempC:
            Aio.send(data.mac, data.temperature, 'temperature')
        if args.sendTempF:
            temp = cls.toFahrenheit(data.temperature)
            Aio.send(data.mac, temp, 'temperature')
        if args.sendHumidity:
            Aio.send(data.mac, data.humidity, 'humidity')
        if args.sendBattery:
            Aio.send(data.mac, data.battery, 'battery')
