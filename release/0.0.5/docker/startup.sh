#!/bin/bash

if [ $(find /dev -name ttyACM0 | wc -c) -gt 0 ]; then
    echo "Connecting to device at /dev/ttyACM0"
    /usr/bin/ez-clang --connect=/dev/ttyACM0
else
    echo "No device at /dev/ttyACM0, starting QEMU session"
    socat -d -d pty,raw,b9600,echo=0,mode=777,link=/dev/ttyS90 pty,raw,b9600,echo=0,mode=777,link=/dev/ttyS91 2> /dev/null &
    sleep 1
    qemu-system-arm -machine lm3s811evb -nographic -m 16K -kernel /usr/lib/ez-clang/0.0.5/qemu/ez-clang-qemu.bin -serial /dev/ttyS90 > /dev/null &
    sleep 1
    /usr/bin/ez-clang --connect=/dev/ttyS91
fi

