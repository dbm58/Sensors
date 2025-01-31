#!/usr/bin/env bash

#  Usage:  collect <device> <id> <filter> <prop> <feed>

Device=$1
Id=$2
Filter=$3
Prop=$4
Feed=$5

DIR=$( cd -- "$( /usr/bin/dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

$DIR/Devices/$Device.sh $Id \
    | jq -c --arg prop $Prop -f $DIR/Filters/$Filter.jq \
    | $DIR/send.sh $Feed
