# ble-sensor/bluepy

## Description 

Library and CLI to read Xiami LYWSD02 and LYWSD03 temperature/humidity sensors.  Originally based on https://github.com/h4/lywsd02, but pretty heavily modified.

This project uses the `bluepy` package, which is no longer under active development.

## Installation

```
> git clone https://github.com/dbm58/ble-sensor.git
> cd ble-sensor/bluepy
> python3 -m venv venv
> source venv/bin/activate
> python3 -m ensurepip --upgrade
> pip3 install -r requirements.txt 
```

Create `app_secrets.py`.  Note that you must do this step, even if you do not plan to use the `send` command.
```
> cp app_secrets.template.py app_secrets.py
```

If you are going to be using the `send` command, then edit `app-secrets.py` and set up your `adafruit.io` credentials.

##  Operation

Find MAC addresses for BLE devices in your area:
```
> sudo hcitool lescan
```

```
> ./sensor -h
```

If you get a "failed to connect" error, try again.  If it persists, you may need to be closed to the BLE device.