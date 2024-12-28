
passive bluetooth sensor reading

# Install

python3 -m venv venv
pip install -r requirements.txt

Note:  Current using a fork of bleson to get around a bug.  See the requirements.txt file for details.  Because of this fork, I had trouble running `pip install -r requirements.txt`.  Maybe this will just work in the future.

To give permission to run without sudo:

    sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)

# Notes:

To rebuild requirements.txt:

    pip freeze > requirements.txt

To fix the "Set scan parameters failed: Input/output error" from hcitool:

    hciconfig hci0 down
    hciconfig hci0 up

This won't always work.  Then try:

    service bluetooth restart
    service dbus restart

If that doesn't work, then red-switch.
