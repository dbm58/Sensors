# ble-sensor

A mono-repo containing all of my BLE sensor projects.

| Name | Description |
| ---- | ----------- |
| bluepy | BLE CLI and MQTT bridge using the `bluepy` library.  `bluepy` is no longer being maintained, and this code will eventually be ported to `bleak` (or something similar). |
| bleson | BLE CLI and MQTT bridge using the `bleson` library. Uses advertising data.  More stable than the bluepy port.  |
| sendWeather | Get the current temperature from wttr.in, and send it up to adafruit.io |

Possible future projects:
| Name | Description |
| ---- | ----------- |
| bleak | The `bluepy`-based CLI/bridge ported to `bleak` |
| nodejs | ... |
| circuitpython | ... |

# Install

1.  `sudo cp push2aio.logrotate /etc/logrotate.d`
2.  ```
sudo touch /var/push2aio
sudo chgrp adm /var/push2aio
sudo chmod 660 /var/push2aio
```
3.  `crontab -e`
    */15 * * * * /home/pi/ble-sensor/run.sh >> /var/log/push2aio 2>&1
