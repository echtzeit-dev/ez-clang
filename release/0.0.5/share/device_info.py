#!/usr/bin/python3
import argparse
import os
import sys

from serial.tools.list_ports_linux import comports

parser = argparse.ArgumentParser()
parser.add_argument("ttyACM", help="Device serial port, e.g. /dev/ttyACM0", type=str)
args = parser.parse_args()

all_devices = comports()
#print(all_devices)
matches = [entry for entry in all_devices if entry.device == args.ttyACM]
if len(matches) == 0:
  sys.stderr.write("Error: no device on port " + args.ttyACM + "\n")
  exit(1)

def report(id_string):
  print(id_string)
  exit(0)

product = matches[0].product if matches[0].product != None else ""
vendor = matches[0].manufacturer if matches[0].manufacturer != None else ""
serial = matches[0].serial_number if matches[0].serial_number != None else ""
description = matches[0].description if matches[0].description != None else ""
hwid = matches[0].hwid if matches[0].hwid != None else ""

# For Teensy LC product is "USB Serial"
if vendor == 'Teensyduino':
  if serial == '10883420':
    report('teensylc')

# Since the trademark dispute some boards append the URL in brackets
if vendor.startswith('Arduino'):
  if product.startswith('Arduino Due') or serial == '7503130343135170D0E1':
    report('due')

# It appears as if the product string actually lacks a trailing 's'
if vendor.startswith('Adafruit'):
  if product.startswith('Metro M0') or serial == 'FC838D1450504335382E314AFF021816':
    report('metro_m0')

# Right now, qemu connects via socat virtual serial ports, like:
# > socat -d -d PTY,raw,b9600,echo=0,link=/dev/ttyS90 PTY,raw,b9600,echo=0,link=/dev/ttyS91
# > qemu-system-arm -machine lm3s811evb -nographic -m 16K -kernel bin/ez-clang-qemu.bin -serial /dev/ttyS90
if description == 'n/a' and "LINK=/dev" in hwid:
  report('qemu')

sys.stderr.write("Error: device not supported\n")
exit(1)
