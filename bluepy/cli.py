#!/usr/bin/env python

import cli

# ./sensor [opts] <mac> <type> <command>
#
# where [opts] is:
#       -v --verbose - additional (debugging) output
#
# where <type> is:
#       lywsd02 - clock
#       lywsd03 - puck
#
# where <command> is:
#       send --temperature --humidity
#       read
#       battery
#       firmware
#       setc
#       setf
#       sync
#       temperature

args = cli.parse()
if args.verbose:
    print(args)
#args.execute(args)
