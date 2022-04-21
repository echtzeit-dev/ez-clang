# ez-clang

ez-clang is an experimental Clang-based cross-compiler with a remote-JIT backend targeting very low-resource embedded devices. Compilation, linking and memory management all run on the host machine. Thus, the RPC endpoint on the device is very simple and only takes few kilobytes of flash memory. Right now, ez-clang supports 32-bit ARMv7-m Cortex devices (i.e. Arduino Due and QEMU LM3S811).

Public previews: https://echtzeit.dev/ez-clang

## Run ez-clang on your own hardware

A binary distribution of ez-clang will be published soon. Please check again in a few days.
