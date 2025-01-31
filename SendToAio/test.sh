#!/usr/bin/env bash
#/usr/bin/env bash

CarolsRoom=404cca6eb068
MainFloor=404cca6dcc38
Basement=744dbdbf1dc4

/usr/bin/date
/usr/bin/echo 1: ${BASH_SOURCE[0]}
/usr/bin/echo 2: /usr/bin/dirname -- "${BASH_SOURCE[0]}"
/usr/bin/echo 3: cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )"
/usr/bin/echo 4: $(/usr/bin/pwd)

DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
/usr/bin/echo current directory is: $DIR

#  Usage:  collect <device> <id> <filter> <prop> <feed>
$DIR/collect.sh airgradient $Basement   ctof atmp ag-basement
$DIR/collect.sh airgradient $MainFloor  ctof atmp ag-main
$DIR/collect.sh airgradient $CarolsRoom ctof atmp ag-carols
