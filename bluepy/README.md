# ble-sensor

## Description 

Library and CLI to read Xiami LYWSD02 and LYWSD03 temperature/humidity sensors.  Originally based on https://github.com/h4/lywsd02, but pretty heavily modified.

## Installation

```
> github clone https://github.com/dbm58/ble-sensor.git
> cd ble-sensor/bluepy
> python3 -m venv venv
> source venv/bin/activate
> python3 -m ensurepip --upgrade
> pip3 install -r requirements.txt 
```

##  Operation

```
> ./sensor -h
```