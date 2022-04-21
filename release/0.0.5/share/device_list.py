#!/usr/bin/python3
from serial.tools.list_ports_linux import comports

ports = []
for (port, desc, hwid) in sorted(comports()):
  print("{:16} {!r:28} {}".format(port, desc, hwid))
  ports.append(port)

