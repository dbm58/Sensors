#!/bin/bash

macs=A4:C1:38:E4:43:C9     # Govee

pushd `dirname $BASH_SOURCE`

[ -d ./venv ] && source ./venv/bin/activate

./passive.py $macs send --tempf

popd

