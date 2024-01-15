from time import sleep
import os
import sys

from bleson import get_provider
from bleson import Observer
from bleson.logger import set_level, ERROR

#  to give permission to run without sudo
#
#  sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)

class Scanner:
    @staticmethod
    def scan(args, collector):
        set_level(ERROR)

        adapter = get_provider().get_adapter()

        observer = Observer(adapter)
        observer.on_advertising_data = collector.collect

        try:
            while not collector.done:
                observer.start()
                sleep(2)
                observer.stop()
        except KeyboardInterrupt:
            try:
                observer.stop()
                sys.exit(0)
            except SystemExit:
                observer.stop()
                os._exit(0)
