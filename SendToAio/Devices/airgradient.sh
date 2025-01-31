#!/usr/bin/env bash
#
#  curl:
#      https://curl.se/docs/manpage.html
#      https://curl.se/docs/tutorial.html
#      https://curl.se/docs/httpscripting.html
#
#  jq:
#      https://jqlang.github.io/jq/manual/
#      https://github.com/jqlang/jq
#      https://jqplay.org/
#
#  adafruit.io:
#      https://io.adafruit.com/api/docs/

#  ======================================================================
#  Main
#  ======================================================================
SN=$1
curl http://airgradient_$SN.local/measures/current \
