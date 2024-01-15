#!/usr/bin/env python

from time import sleep
import os
import sys
from struct import unpack_from

from bleson import get_provider
from bleson import Observer
from bleson import UUID16
from bleson.logger import log, set_level, ERROR, DEBUG

set_level(ERROR)

# https://macaddresschanger.com/bluetooth-mac-lookup/A4%3AC1%3A38
# OUI Prefix	Company
# A4:C1:38	Telink Semiconductor (Taipei) Co. Ltd.
GOVEE_BT_mac_OUI_PREFIX = "A4:C1:38"

H5075_UPDATE_UUID16 = UUID16(0xEC88)


# ###########################################################################

def xiaomi(advertisement):
    #if advertisement.address.address.startswith(GOVEE_BT_mac_OUI_PREFIX):
        #print('======================================================================')
        #print(advertisement.address, advertisement)
        #if advertisement.name is not None:
            #print(advertisement.address, 'name:', advertisement.name)
        #if advertisement.service_data is not None:
            #print(advertisement.address, 'service_data:', advertisement.service_data)
        #if advertisement.mfg_data is not None:
            #print(advertisement.address, 'mfg_data:', advertisement.mfg_data)

    if advertisement.address.address == 'E7:2E:00:51:C0:95':
        print('======================================================================')
        print(dir(advertisement))
        print(advertisement.address, advertisement)
        if advertisement.name is not None:
            print(advertisement.address, 'name:', advertisement.name)
        if advertisement.service_data is not None:
            print(advertisement.address, 'service_data:', advertisement.service_data)
        if advertisement.mfg_data is not None:
            print(advertisement.address, 'mfg_data:', advertisement.mfg_data)
        print(advertisement.address, 'svc_data_uuid16:', advertisement.svc_data_uuid16)

def handleBleAdvertisement(advertisement):
    if advertisement.address.address.startswith(GOVEE_BT_mac_OUI_PREFIX):
        mac = advertisement.address.address

        if H5075_UPDATE_UUID16 in advertisement.uuid16s:
            print(mac, ' ', advertisement.name)

def dumpAdvert(advertisement):
    if advertisement.address.address == 'A4:C1:38:43:61:0E':
        #print(dir(advertisement))
        print('======================================================================')
        print(advertisement.address, advertisement)
        print(advertisement.address, 'service_data    ', advertisement.service_data)
        if advertisement.service_data is not None:
            print(advertisement.address, 'service_data    ', advertisement.service_data.hex())
            temp, hum, battmv, batt, counter, flags = unpack_from("<hHHBBB", advertisement.service_data, 8)
            print(advertisement.address, 'temperature', temp / 100)
            print(advertisement.address, 'humidity   ', hum / 100)
            print(advertisement.address, 'battery    ', batt)
            print(advertisement.address, 'battery mv ', battmv)
            print(advertisement.address, 'counter    ', counter)
            print(advertisement.address, 'flags      ', flags)
        print(advertisement.address, 'svc_data_uuid16 ', advertisement.svc_data_uuid16)
        print(advertisement.address, 'svc_data_uuid32 ', advertisement.svc_data_uuid32)
        print(advertisement.address, 'svc_data_uuid128', advertisement.svc_data_uuid128)
        # 1a180e614338c1a49406d412900b540a0f
        # xxxx                               uuid (0x181a)
        #     xxxxxxxxxxxx                   mac
        #                 xxxx               temp
        #                     xx             humidity
        #                       xx           battery %
        #                         xxxx       battery mv
        #                             xx     frame packet counter

# ###########################################################################


adapter = get_provider().get_adapter()

observer = Observer(adapter)
#observer.on_advertising_data = handleBleAdvertisement
observer.on_advertising_data = dumpAdvert
#observer.on_advertising_data = xiaomi

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
