#!/usr/bin/env python3

import subprocess
import re
import logging
import serial
import select
import sys

def find_ports():
  dmesg = subprocess.run(['dmesg'], stdout=subprocess.PIPE)

  s = dmesg.stdout.decode('utf-8')
  r = re.findall(r'tty[A-Z]{3}[0-9]', s)

  r = list(set(r))

  for serial in r:
    print(f'Found {serial} port')

  if len(r) < 2:
    logging.error('Too few ports, cannot bridge')
    sys.exit(255)
  if len(r) > 3:
    logging.error('Too many ports, do not know what to bridge')
    sys.exit(255)
  if len(r) == 2 and 'ttyAMA0' not in r:
    logging.error('Native UART not found (looking for ttyAMA0)')
    sys.exit(255)

  if len(r) == 3: # Standard bridging
    r.remove('ttyAMA0')

  return r

def open_port(port):
  p = serial.Serial(f'/dev/{port}', baudrate=19200)
  p.reset_input_buffer()
  p.reset_output_buffer()
  return p

def transfer_data(a, b):
  data = a.read(a.in_waiting)
  b.write(data)
  return data

r = find_ports()

srcport = r[0]
dstport = r[1]

print(f'Bridging between {srcport} and {dstport}')

src = open_port(srcport)
dst = open_port(dstport)

ports = [src, dst]

while True:
  readable, writeable, exceptional = select.select(ports, [], ports)
  if len(exceptional):
    print('Error detected on serial communication')
    if src in exceptional:
      logging.info(f'Reopening {srcport}')
      try:
        src.close()
      except:
        logging.exception('Unable to close src')
      src = open_port(srcport)
    if dst in exceptional:
      logging.info(f'Reopening {dstport}')
      try:
        dst.close()
      except:
        logging.exception('Unable to close dst')
      dst = open_port(dstport)
    ports = [src, dst]
    logging.info('Resuming bridging')
    continue
  if src in readable:
    c = transfer_data(src, dst)
    print('SRC->DST: ' + repr(c))
  if dst in readable:
    c = transfer_data(dst, src)
    print('SRC<-DST: ' + repr(c))
