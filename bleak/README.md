# bridge

A bridge between bluetooth sensors and external systems.

```
python bridge.py {collect | scan} <macs> [<output-options>]
```
where `collect` gets one reading from each mac

`scan` continually reads all the macs

`<macs>` is a space-delimited list of type/mac pairs.  E.g. 
```
aranet4:DC:44:81:C5:E7:73 lywsd03:A4:C1:38:43:61:0E
```

`<output-options>` = `--output {line, print, raw, send}`

where `line` prints a single line with some of the values for the sensor

`print` displays a large amount of data for the reading

`raw` displays the ble device structure, and the raw advertisement data

`send` sends selected values to adafruit.io

## To install:
```
> python3.11 -m venv venv
> pip install adafruit-io
> pip install bleak
```

## References

https://github.com/adafruit/Adafruit_IO_Python

https://github.com/hbldh/bleak

Aranet4 support influenced by https://github.com/Anrijs/Aranet4-Python

## Other Links

BLE Scan:
https://raspberrypi.stackexchange.com/q/137823

BLEAK code examples:
https://nabeelvalley.co.za/docs/iot/bluetooth-intro/

Another BLEAK example:
https://github.com/gopro/OpenGoPro/blob/main/demos/python/tutorial/tutorial_modules/tutorial_1_connect_ble/ble_connect.py

Example code in BLEAK docs:
https://bleak.readthedocs.io/en/latest/api/scanner.html

BLEAK examples directory:
https://github.com/hbldh/bleak/tree/develop/examples

AdaFruit I/O Python Library:
https://github.com/adafruit/Adafruit_IO_Python

Original alternative firmware:
https://github.com/pvvx/ATC_MiThermometer

BtHome Issue (pointers):
https://github.com/Bluetooth-Devices/bthome-ble/issues/36

