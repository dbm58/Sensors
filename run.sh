#!/bin/bash

pushd `dirname $BASH_SOURCE`

./bleson/run.sh
./bluepy/run.sh
./sendWeather/run.sh

popd

