import argparse


from .lywsd02 import parse as lywsd02Parse
from .lywsd03 import parse as lywsd03Parse

# ./sensor <type> <mac> send --temperature --humidity
#                       read
#                       battery
#                       firmware
#                       setc
#                       setf
#                       sync
#                       temperature

def parse():
    parser = argparse.ArgumentParser("sensor")
    parser.add_argument("mac", help="mac address", action="store")
    deviceParser = parser.add_subparsers(
        dest="device",
        help="devices",
        required=True,
        title="devices",
        )
    lywsd02Parse(deviceParser)
    lywsd03Parse(deviceParser)
    args = parser.parse_args()
    return args
    #args.execute()
