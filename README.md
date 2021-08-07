# Serial Bridge

This was written specifically to solve a problem I have but works just as well with anything else needing to bridge two serial ports on your machine

# Using USB based Insteon PLM with Universal Device's ISY994i

See this [guide](ISY994.md) on how to use a Raspberry Pi Zero Wireless and a USB based Insteon PLM of your choice to replace the unavailable Insteon serial based PLM. The end result can be pretty sweet 😉

![endresult](images/clean.jpg "ISY994 with integrated RPiZW and a wireless Insteon PLM")

## Installing the software

- Clone or unzip a copy of this project
- Install serial support `sudo apt install python3-serial`
- Optionally, run `sudo ./install.sh` which will install the tool in `/opt/serial-bridge` as well as installing and enabling the service so it runs on boot.

## Running the software

`bridge.py` is completely automated and follows the following logic:

- If 3 serial ports are detected, the two external ones will be bridged (RPi always has ONE serial port)
- If 2 serial ports are detected, these will be bridged (happens only when you use the UART on the RPi itself)
- _Less than 2 or more than 3 will result in error code_

Once running, it will show what ports it has detected
```
pi@raspberrypi:~/serial-bridge $ ./bridge.py 
Found ttyAMA0 port
Found ttyUSB1 port
Found ttyUSB0 port
```
Followed by which ones it's bridging (sidenote, `ttyAMA0` is the built-in UART on the RPi)
```
Bridging between ttyUSB1 and ttyUSB0
```
If you're using this to bridge to a ISY994, then you should either restart or power on your ISY994i.

If a serial port fails, `bridge.py` will close and reopen it with the hopes of that clearing up any issues.

# Support

If you find issues and are able to do bugfixes, please submit PRs for this project. If you're not able to fix, feel free to submit an issue on the project. No promises that I will fix it, especially if it's not related to the USB stick from Insteon (since I don't want to get the powerline USB one).

# Future

- Make SD card image for RPi allowing super easy setup (fire and forget essentially) with no network required
- Build and sell kits? Probably not
