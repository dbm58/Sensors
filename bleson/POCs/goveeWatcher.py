from time import sleep
import os
import sys
from struct import unpack_from

from bleson import get_provider
from bleson import Observer
from bleson import UUID16
from bleson.logger import log, set_level, ERROR, DEBUG

# Disable warnings
set_level(ERROR)

# # Uncomment for debug log level
# set_level(DEBUG)

# https://macaddresschanger.com/bluetooth-mac-lookup/A4%3AC1%3A38
# OUI Prefix	Company
# A4:C1:38	Telink Semiconductor (Taipei) Co. Ltd.
GOVEE_BT_mac_OUI_PREFIX = "A4:C1:38"

H5075_UPDATE_UUID16 = UUID16(0xEC88)

govee_devices = {}

# ###########################################################################
FORMAT_PRECISION = ".2f"

def twos_complement(n: int, w: int = 16) -> int:
    """Two's complement integer conversion."""
    # Adapted from: https://stackoverflow.com/a/33716541.
    if n & (1 << (w - 1)):
        n = n - (1 << w)
    return n

def toFahrenheit(temp):
    fahrenheit = (temp * 9 / 5) + 32
    return fahrenheit

def print_values(mac):
    govee_device = govee_devices[mac]
    print(govee_device)

def handleBleAdvertisement(advertisement):
    log.debug(advertisement)

    if advertisement.address.address.startswith(GOVEE_BT_mac_OUI_PREFIX):
        mac = advertisement.address.address

        if mac not in govee_devices:
            govee_devices[mac] = {}

        if H5075_UPDATE_UUID16 in advertisement.uuid16s:
            govee_devices[mac]["address"] = mac
            govee_devices[mac]["name"] = advertisement.name

        if advertisement.rssi is not None and advertisement.rssi != 0:
            govee_devices[mac]["rssi"] = advertisement.rssi

        if advertisement.mfg_data is not None:
            prefix = advertisement.mfg_data.hex()[0:4]
            if prefix == "88ec":
                govee_devices[mac]["address"] = mac
                govee_devices[mac]["mfg_data"] = advertisement.mfg_data.hex()

                raw_temp, hum, batt = unpack_from("<HHB", advertisement.mfg_data, 3)
                govee_devices[mac]["temperature"] = float(twos_complement(raw_temp) / 100.0)
                govee_devices[mac]["humidity"] = float(hum / 100.0)
                govee_devices[mac]["battery"] = int(batt)
                #https://github.com/dacarson/Govee-exporter/blob/main/goveelog.py

                print_values(mac)

        log.debug(govee_devices[mac])


# ###########################################################################


adapter = get_provider().get_adapter()

observer = Observer(adapter)
observer.on_advertising_data = handleBleAdvertisement

try:
    while True:
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
