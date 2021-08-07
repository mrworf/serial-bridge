# Optimizing the boot

When you're powering the RPi from the ISY994, you are under a time crunch to have the serial bridge up and running in time for when the ISY994 expects to be able to talk to it.

This guide tries to help you on your way to get the speed up.

Note, this guide ALSO assumes you're using the built-in UART for talking to the ISY994i.

# Step 1: Free up the serial port

We need to disable the use of the serial port by linux itself.

First, turn of the serial console:
```
systemctl stop serial-getty@ttyS0.service
systemctl disable serial-getty@ttyS0.service
systemctl stop serial-getty@ttyS1.service
systemctl disable serial-getty@ttyS1.service
```
Next, let's edit the `/boot/cmdline.txt` and remove the item called `console=serial0,115200`

This should now allow you to use the UART on the board, also known as `/dev/ttyAMA0`

# Step 2: Speeding things up

This will disable bluetooth among other things (not wifi or network though)

## First, optimize the /boot/config.txt

Add the following lines under the `[all]` section (found at the end of the file)

```
dtoverlay=disable-bt
disable_splash=1
boot_delay=0
```

## Next, disable all the services

```
sudo systemctl disable hciuart.service
sudo systemctl disable bluealsa.service
sudo systemctl disable dphys-swapfile.service
sudo systemctl disable keyboard-setup.service
sudo systemctl disable apt-daily.service
sudo systemctl disable raspi-config.service
sudo systemctl disable avahi-daemon.service
sudo systemctl disable triggerhappy.service
```
(some of these may not exist on your system, that's fine)

## Remove plymouth (if in use)

```
sudo apt-get purge --remove plymouth
```

## Finally, tweak /boot/cmdline.txt

Make sure to add the following to the SINGLE line you have in this file, `quiet` since it will stop the kernel from wasting cycles on printing stuff you can't see anyway

# Done

Once you install the bridge service, it will position itself to launch as soon as technically possible, which on my Raspberry Pi Zero Wireless means in about 21s
```
pi@raspberrypi:~ $ systemd-analyze critical-chain bridge.service
The time after the unit is active or started is printed after the "@" character.
The time the unit takes to start is printed after the "+" character.

bridge.service @20.356s
└─basic.target @20.320s
  └─sockets.target @20.320s
    └─triggerhappy.socket @20.319s
      └─sysinit.target @20.298s
        └─systemd-timesyncd.service @18.210s +2.083s
          └─systemd-tmpfiles-setup.service @17.087s +928ms
            └─local-fs.target @16.806s
              └─boot.mount @16.590s +207ms
                └─systemd-fsck@dev-disk-by\x2dpartuuid-8bb7d6de\x2d01.service @14.730s +1.819s
                  └─dev-disk-by\x2dpartuuid-8bb7d6de\x2d01.device @12.371s
```
