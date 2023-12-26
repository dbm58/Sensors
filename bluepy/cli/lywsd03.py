import argparse
from . import Commands
from . import Devices

import sys
sys.path.append('..')
from lib import Lywsd03

def parse(deviceParser):
    lywsd03 = deviceParser.add_parser("lywsd03", help="puck thermometer")
    lywsd03.set_defaults(device=Lywsd03)

    commandParser = lywsd03.add_subparsers(dest="command", title="command", help="command")

    command = commandParser.add_parser("send", help="send data to adafruit.io")
    destParser = command.add_subparsers(dest="destination", title="destination", help="destination")
    destParser.add_parser("adafruit", help="send to adafruit.io")
    destParser.add_parser("console", help="send to the console (default)")

    command = commandParser.add_parser("read", help="read data from the device")
    command = commandParser.add_parser("battery", help="show battery level")

    command = commandParser.add_parser("firmware", help="what does this do?")
    command.set_defaults(execute=lambda args : Commands.create()["firmware"](Lywsd03(args.mac)))

    command = commandParser.add_parser("setc", help="change temperture units to C")
    command = commandParser.add_parser("setf", help="change temperture units to F")
    command = commandParser.add_parser("temperature", help="what does this do?")
