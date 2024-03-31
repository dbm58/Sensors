import asyncio
import inspect
import itertools
import json
import sys

from bleak import BleakScanner
from parser import Parser

import processors
import output

async def collect(args):
    try:
        async with BleakScanner() as scanner:
            print("Collecting...")

            async for bd, ad in scanner.advertisement_data():
                if not bd.address in args.devices:
                    continue

                data = args.devices[bd.address]['decoder'](bd, ad)
                if data == None:
                    continue
                args.devices[bd.address]['data'] = data

                #  todo:  we need a timeout
                if all(map(lambda d: not d.get('data',None) == None, args.devices.values())):
                    break

            for dev in args.devices.values():
                dev['outputer'](dev['data'])

    except KeyboardInterrupt:
        print("Shutting down...")
    except asyncio.exceptions.CancelledError:
        print("Shutting down...")

async def scan(args):
    try:
        async with BleakScanner() as scanner:
            print("Scanning...")

            async for bd, ad in scanner.advertisement_data():
                if not bd.address in args.devices:
                    continue

                data = args.devices[bd.address]['decoder'](bd, ad)
                if data == None:
                    continue

                args.devices[bd.address]['outputer'](data)

    except KeyboardInterrupt:
        print("Shutting down...")
    except asyncio.exceptions.CancelledError:
        print("Shutting down...")

def main(args):
    if args.command == 'collect':
        asyncio.run(collect(args))
    else:
        asyncio.run(scan(args))

if __name__ == "__main__":
    args = Parser.parse()
    args.devices = dict(
             map(
                 lambda m: (
                     m[0],
                     {
                         'addr': m[0],
                         'type': m[1],
                         'decoder': processors.members[m[1]].decode,
                         'outputer': getattr(output.members[m[1]], args.output)
                     }
                 ),
                 map(
                     lambda m: ( m.split(':',1)[1], m.split(':',1)[0], ),
                     args.devices
                 )
             )
         )
    #print(processors.members)
    #print(output.members)
    #print(args)
    #sys.exit()

    main(args)
