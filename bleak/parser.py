import argparse

#  device=aranet4:xx:xx:xx:xx
#  device should be an array
#  pass in a dictionary of devices
#  pass in a dictionary of outputs:w

class Parser:

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser("bridge")

        parser.add_argument("command", choices=['collect', 'scan'], action="store")
        parser.add_argument("devices", nargs="+", action="store")
        parser.add_argument("-o", "--output", choices=['line', 'print', 'raw', 'send'], action="store")

        args = parser.parse_args()

        if args.output == None:
            args.output = 'line'

        #print(args)

        return args
