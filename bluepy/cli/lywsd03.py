import argparse
from . import Commands
from . import Devices

import sys
sys.path.append('..')
from lib import Lywsd03

def parse(deviceParser):
    lywsd03 = deviceParser.add_parser("lywsd03", help="puck thermometer")
    lywsd03.set_defaults(device=Lywsd03)

    commandParser = lywsd03.add_subparsers(
        dest="command",
        required=True,
        title="command",
        help="command"
        )

    command = commandParser.add_parser(
        "send",
        help="send data to adafruit.io"
        )
    command.add_argument(
        "-t",
        "--temperature",
        dest="sendTemperature",
        action="store_true",
        help="send temperature"
        )
    command.add_argument(
        "-r",
        "--humidity",
        dest="sendHumidity",
        action="store_true",
        help="send humidity"
        )

    command = commandParser.add_parser("read", help="read data from the device")
    command.set_defaults(
       execute=lambda args : Commands.create()["read"](Lywsd03(args.mac))
       )

    command = commandParser.add_parser("battery", help="show battery level")
    command.set_defaults(
       execute=lambda args : Commands.create()["battery"](Lywsd03(args.mac))
       )

    command = commandParser.add_parser("firmware", help="show firmware version")
    command.set_defaults(execute=lambda args : Commands.create()["firmware"](Lywsd03(args.mac)))

    command = commandParser.add_parser("setc", help="change temperture units to C")
    command = commandParser.add_parser("setf", help="change temperture units to F")
    command = commandParser.add_parser("temperature", help="what does this do?")
