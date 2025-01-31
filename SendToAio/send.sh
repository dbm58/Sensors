#!/usr/bin/env bash

FeedName=$1

read -r DataIn

ContentType="Content-Type: application/json"
Auth="X-AIO-Key: $AIOKey"
Url=https://io.adafruit.com/api/v2/$UserName/feeds/$FeedName/data
          
echo curl -H "$ContentType" -H "$Auth" -d "$DataIn" $Url
curl -H "$ContentType" -H "$Auth" -d "$DataIn" $Url
