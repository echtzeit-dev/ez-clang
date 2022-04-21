#!/usr/bin/python3
import argparse
import os
import serial as pyserial
import time

def filepath(arg):
  if os.path.exists(arg):
    return arg
  else:
    raise FileNotFoundError(arg)

parser = argparse.ArgumentParser()
parser.add_argument("port", help="Serial port of the target device",
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

reset_baudrate = 1200

print(f"Forcing reset using {reset_baudrate}bps open/close on port", args.port)
touchSerialPort(args.port, reset_baudrate)
