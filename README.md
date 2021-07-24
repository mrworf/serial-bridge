# Serial Bridge

This was written specifically to solve a problem I have but works just as well with anything else needing to bridge two serial ports on your machine

# Using USB based Insteon PLM with Universal Device's ISY994i

The ISY994i requires a serial connection to the Insteon PLM. However, a while back Smarthome decided to stop selling the serial port enabled PLM (2413S). While you can still get the USB based ones (either 2413U or 2448A7 which is wireless only) they don't work with the ISY994i.

Using this project on a Raspberry Pi (Zero in my case, but will work with any RPi) you can remedy this issue.

## Disclaimer

The author of these instructions and software cannot be held responsible for any issues or damages caused by it. Follow/use at your own peril.

## Requirements

- Raspberry Pi Zero/3
- RS232-to-USB (RS232-to-TTL instructions will be added once tested)
- Insteon 2448A7 (2413U not tested but should work)
- (Optional) USB Hub (to connect the two USB devices on the Zero)

## Special cable

To connect your RPi via the RS232 adapter, you must first created the required cable. 

The pins you must connect are
```
RJ45 PIN1 --> RS232 TX
RJ45 PIN8 --> RS232 RX
RJ45 PIN7 --> GND
```
This can either be done using RJ45 crimp tools or by getting a handy-dandy breakout box like https://www.amazon.com/gp/product/B07WKKVZRF 

## Installing the software

- Clone or unzip a copy of this project
- Install serial support `sudo apt install python3-serial`

## Running the software

`bridge.py` is completely automated and follows the following logic:

- If 3 serial ports are detected, the two external ones will be bridge (RPi always has ONE serial port)
- If 2 serial ports are detected, these will be bridged (happens only when you use the UART on the RPi itself)
- Less than 2 or more than 3 will result in error code

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

At this point, either restart or power on your ISY994i 

During the bootup, you'll start seeing messages similar to

```
SRC<-DST: b'\x02`'
SRC->DST: b'\x02`R\x18'
```
This is indicating that there is communication between the PLM and your ISY994.

SRC/DST may change place depending on which one `bridge.py` picked as source. In actuality it has no impact on the functionality.

If a serial port fails, `bridge.py` will close and reopen it with the hopes of that clearing up any issues.

## Performance

I see no difference in reaction times using wireless only. In fact, since switching to this, the comms between the ISY and my insteon network has never been more reliable. I'm also hopeful that by being offgrid (from a PLM standpoint) it will stay solid much longer since the main culprit (from my understanding) with the wired ones is all the extra components that connect to 110.

# Support

If you find issues and are able to do bugfixes, please submit PRs for this project. If you're not able to fix, feel free to submit an issue on the project. No promises that I will fix it, especially if it's not related to the USB stick from Insteon (since I don't want to get the powerline USB one).

# Future

- Test use of built-in UART and provide instructions
- Create `bridge.service` to simplify running this
- Make SD card image for RPi allowing super easy setup (fire and forget essentially) with no network required
- Build and sell kits? Probably not
