#!/usr/bin/env python

import argparse

# scan [--timeout ###] <mac>[,<mac> ...] 
# scan [--timeout ###] <mac>[,<mac> ...] send key --temp --tempf --humid --batt

class Parser:
    @staticmethod
    def parse():
        parser = argparse.ArgumentParser("scan")

        parser.add_argument('--timeout', nargs='?', type=int, default=300)

        parser.add_argument('macs', action='store')

        commandParser = parser.add_subparsers(
            dest='command',
            help='command',
            title='command',
            )
        sendParser = commandParser.add_parser('send', help='read data from device and send to adafruit.io')
        sendParser.add_argument('-c', '--tempc', dest='sendTempC',    action='store_true', help='send temperature in C')
        sendParser.add_argument('-f', '--tempf', dest='sendTempF',    action='store_true', help='send temperature in F')
        sendParser.add_argument('-r', '--humid', dest='sendHumidity', action='store_true', help='send humidity')
        sendParser.add_argument('-b', '--batt',  dest='sendBattery',  action='store_true', help='send battery')

        args = parser.parse_args()

        return args
