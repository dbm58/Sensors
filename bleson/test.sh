#!/bin/bash

macs=A4:C1:38:43:61:0E           # ATC_43610E - carol
#macs=$macs,A4:C1:38:29:CA:D6     # ATC_29CAD6 - cold frame
#macs=$macs,A4:C1:38:E4:43:C9     # Govee

source venv/bin/activate
./passive.py $macs

