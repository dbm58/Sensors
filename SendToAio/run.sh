#!/usr/bin/env bash

CarolsRoom=404cca6eb068
MainFloor=404cca6dcc38
Basement=744dbdbf1dc4

/usr/bin/echo Beginning data collection $(/usr/bin/date)

DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $DIR/secrets.sh

#  Usage:  collect <device> <id> <filter> <prop> <feed>
$DIR/collect.sh airgradient $Basement   ctof atmp ag-basement
$DIR/collect.sh airgradient $MainFloor  ctof atmp ag-main
$DIR/collect.sh airgradient $CarolsRoom ctof atmp ag-carols
