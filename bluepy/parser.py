#!/usr/bin/env python

import argparse

# ./sensor <type> <mac> send --temperature --humidity
#                       read
#                       battery
#                       firmware
#                       setc
#                       setf
#                       sync
#                       temperature

def clck():
    return "clck"

def puck():
    return "puck"

parser = argparse.ArgumentParser("sensor")

parser.add_argument("mac", help="mac address", action="store")

deviceParser = parser.add_subparsers(dest="device", title="devices", help="devices")
lywsd02 = deviceParser.add_parser("lywsd02", help="clock thermometer")
lywsd02.set_defaults(func=clck)
commandParser = lywsd02.add_subparsers(dest="command", title="command", help="command")
command = commandParser.add_parser("send", help="send data to adafruit.io")
command = commandParser.add_parser("read", help="read data from the device")
command = commandParser.add_parser("battery", help="show battery level")
command = commandParser.add_parser("firmware", help="what does this do?")
command = commandParser.add_parser("setc", help="change temperture units to C")
command = commandParser.add_parser("setf", help="change temperture units to F")
command = commandParser.add_parser("sync", help="sync clock time to the time on the server")
command = commandParser.add_parser("temperature", help="what does this do?")

lywsd03 = deviceParser.add_parser("lywsd03", help="puck thermometer")
lywsd03.set_defaults(func=puck)
commandParser = lywsd03.add_subparsers(dest="command", title="command", help="command")
command = commandParser.add_parser("send", help="send data to adafruit.io")
destParser = command.add_subparsers(dest="destination", title="destination", help="destination")
destParser.add_parser("adafruit", help="send to adafruit.io")
destParser.add_parser("console", help="send to the console (default)")
command = commandParser.add_parser("read", help="read data from the device")
command = commandParser.add_parser("battery", help="show battery level")
command = commandParser.add_parser("firmware", help="what does this do?")
command = commandParser.add_parser("setc", help="change temperture units to C")
command = commandParser.add_parser("setf", help="change temperture units to F")
command = commandParser.add_parser("temperature", help="what does this do?")



# parser.add_argument("mac", action="store")  # Equivalent to parser.add_argument("--name")
# parser.add_argument("--send", action="store_const", const=3.14)
# parser.add_argument("--is-valid", action="store_true")
# parser.add_argument("--is-invalid", action="store_false")
# parser.add_argument("--item", action="append")
# parser.add_argument("--repeated", action="append_const", const=42)
# parser.add_argument("--add-one", action="count")
# parser.add_argument(
# "--version", action="version", version="%(prog)s 0.1.0"
#)

args = parser.parse_args()

print(args)
#print(args.func())
