#!/usr/bin/env python

import cli

# ./sensor <type> <mac> send --temperature --humidity
#                       read
#                       battery
#                       firmware
#                       setc
#                       setf
#                       sync
#                       temperature

args = cli.parse()
args.execute(args)
print(args)
