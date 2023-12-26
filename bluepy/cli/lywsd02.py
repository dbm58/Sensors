import argparse
from . import Commands
from . import Devices

import sys
sys.path.append('..')
from lib import Lywsd02

def parse(deviceParser):
    lywsd02 = deviceParser.add_parser("lywsd02", help="clock thermometer")
    lywsd02.set_defaults(device=Lywsd02)

    commandParser = lywsd02.add_subparsers(
        dest="command",
        help="command",
        required=True,
        title="command",
        )

    command = commandParser.add_parser("send", help="send data to adafruit.io")
    command.set_defaults(foo="bar")
    command = commandParser.add_parser("read", help="read data from the device")
    command = commandParser.add_parser("battery", help="show battery level")

    command = commandParser.add_parser("firmware", help="Display the firmware version")
    command.set_defaults(execute=lambda args : Commands.create()["firmware"](Lywsd02(args.mac)))

    command = commandParser.add_parser("setc", help="change temperture units to C")
    command = commandParser.add_parser("setf", help="change temperture units to F")
    command = commandParser.add_parser("sync", help="sync clock time to the time on the server")
    command = commandParser.add_parser("temperature", help="what does this do?")
