#!/bin/bash

pushd `dirname $BASH_SOURCE`

[ -d ./venv ] && source ./venv/bin/activate

TMP_FILE=/tmp/weather.json
rm -f $TMP_FILE
curl wttr.in/43.05,-87.98?format=j1 > $TMP_FILE
./sendWeather.py < $TMP_FILE
rm -f $TMP_FILE

popd

