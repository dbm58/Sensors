#!/bin/bash

function query()
{
    #  $1 = device type
    #  $2 = command
    #  $3 = mac
    ./sensor $1 $2 $3
}

function queryWithRetry()
{
    query $1 $2 $3
    if [ $? -gt 0 ]; then
        echo retry
        sleep 2
        query $1 $2 $3
    fi
    if [ $? -gt 0 ]; then
        echo retry 2
        sleep 2
        query $1 $2 $3
    fi
}

pushd `dirname $BASH_SOURCE`

[ -d ./venv ] && source ./venv/bin/activate

queryWithRetry lywsd02 send  E7:2E:00:51:C0:95 # LYWSD02
queryWithRetry lywsd02 sendh E7:2E:00:51:C0:95 # LYWSD02
#queryWithRetry lywsd02 read E7:2E:00:51:C0:95 # LYWSD02

popd

