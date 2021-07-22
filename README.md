Bridges two serial devices on a raspberry pi.

Very simple, if it finds 3 ttys on boot, it will assume that the two which aren't the built-in serial port shall be bridged.
If it only finds two ttys, it assumes those should be bridged.
Any other amount (more or less) will cause the software to exit

To install, you need python3-serial (ie, sudo apt install python3-serial)

# TODO

- Fix readme
- Add service

