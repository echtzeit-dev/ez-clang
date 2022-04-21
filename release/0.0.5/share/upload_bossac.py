#!/usr/bin/python3
import argparse
import os
import subprocess
import serial as pyserial
import time

def filepath(arg):
  if os.path.exists(arg):
    return arg
  else:
    raise FileNotFoundError(arg)

def platformio_bossac():
  return "/".join([os.environ['HOME'], ".platformio/packages/tool-bossac/bossac"])

parser = argparse.ArgumentParser()
parser.add_argument("--bossac", help="Path to the bossa cli tool",
                                type=filepath, default=platformio_bossac())
parser.add_argument("--port",   help="Serial port of the target device",
                                type=filepath)
parser.add_argument("--id",     help="Internal ID of the target device",
                                type=str)
parser.add_argument("firmware", help="Path to the firmware image to upload",
                                type=filepath)
args = parser.parse_args()

def touchSerialPort(port, baudrate):
    conn = pyserial.Serial()
    conn.port = port
    conn.baudrate = baudrate
    conn.bytesize = pyserial.EIGHTBITS
    conn.stopbits = pyserial.STOPBITS_ONE
    conn.parity = pyserial.PARITY_NONE
    conn.open()
    conn.setDTR(True) 
    time.sleep(0.022)    
    conn.setDTR(False)  
    conn.close()
    time.sleep(3)

bossac_cmd = {
  "due": [
    args.bossac, "--info", "--port", args.port, "--write", "--reset", "--erase",
    "-U", "false", "--boot", args.firmware
  ],
  "metro_m0": [
    args.bossac, "--info", "--port", args.port, "--write", "--reset", "--erase",
    "-U", "true", args.firmware
  ]
}

if not args.id in bossac_cmd:
  print("Unsupported ID for bossac upload. Supported IDs are:", bossac_cmd.keys())
  exit(1)

reset_baudrate = 1200
print(f"Forcing reset using {reset_baudrate}bps open/close on port", args.port)
touchSerialPort(args.port, reset_baudrate)

print("Uploading", args.firmware)
bossac = subprocess.Popen(bossac_cmd[args.id])
if bossac.wait() != 0:
  print("Upload failed in bossac")
  exit(1)

print("Upload successful")
