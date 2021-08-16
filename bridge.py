#!/usr/bin/env python3

import subprocess
import re
import serial
import select
import sys
import logging

def find_ports():
  dmesg = subprocess.run(['dmesg'], stdout=subprocess.PIPE)

  s = dmesg.stdout.decode('utf-8')
  r = re.findall(r'tty[A-Z]{3}[0-9]', s)

  r = list(set(r))

  logging.debug('Found a total of %d serial ports', len(r))

  for serial in r:
    logging.info(f'Found {serial} port')

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

  r.sort() # So we're consistent

  return r

def to_hex(data):
  return ' '.join('{:02x}'.format(x) for x in data)

def to_str(data):
  return ''.join('%c' % (x if x > 31 and x < 127 else '.') for x in data)

def splitdata(data):
  return [data[i:i + 8] for i in range(0, len(data), 8)]

def open_port(port):
  p = serial.Serial(f'/dev/{port}', baudrate=19200)
  p.reset_input_buffer()
  p.reset_output_buffer()
  return p

def transfer_data(a, b):
  data = a.read(a.in_waiting)
  b.write(data)
  return data

if len(sys.argv) > 1 and sys.argv[1].lower() == '--debug':
  level = logging.DEBUG
  print('Debug logging enabled')
else:
  level = logging.INFO

logging.basicConfig(format='%(levelname)s: %(message)s', level=level)

r = find_ports()

srcport = r[0]
dstport = r[1]

logging.info(f'Bridging between {srcport} and {dstport}')

src = open_port(srcport)
dst = open_port(dstport)

ports = [src, dst]

logging.debug(' %-33s | %-33s' % ('/dev/' + srcport, '/dev/' + dstport))
logging.debug('-' * 71)

while True:
  readable, writeable, exceptional = select.select(ports, [], ports)
  if len(exceptional):
    logging.warning('Error detected on serial communication')
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

  srcdata = ''
  dstdata = ''

  if src in readable:
    srcdata = splitdata(transfer_data(src, dst))
  if dst in readable:
    dstdata = splitdata(transfer_data(dst, src))

  for row in range(0,max(len(srcdata), len(dstdata))):
     adata = srcdata[row] if row < len(srcdata) else b''
     bdata = dstdata[row] if row < len(dstdata) else b''

     str = '%-23s ; %-8s | %-23s ; %-8s' % (to_hex(adata), to_str(adata), to_hex(bdata), to_str(bdata))
     logging.debug(str)
