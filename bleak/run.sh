#!/bin/bash

macs=
macs=$macs aranet4:DC:44:81:C5:E7:73    # CO2 Monitor
#macs=$macs lywsd03:A4:C1:38:43:61:0E    # ATC_43610E - carol
#macs=$macs lywsd03:A4:C1:38:29:CA:D6    # ATC_29CAD6 - cold frame
#macs=$macs govee:A4:C1:38:E4:43:C9     # Govee

pushd `dirname $BASH_SOURCE`

[ -d ./venv ] && source ./venv/bin/activate

python ./bridge.py collect $macs --output send

popd

