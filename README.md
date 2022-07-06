# ez-clang

ez-clang is an experimental Clang-based cross-compiler with a remote-JIT backend targeting very low-resource embedded devices. Compilation, linking and memory management all run on the host machine. Thus, the RPC endpoint on the device is very simple and only takes few kilobytes of flash memory. Right now, ez-clang supports 32-bit ARMv7-m Cortex devices (i.e. Arduino Due and QEMU LM3S811).

Public previews: https://echtzeit.dev/ez-clang

## Run ez-clang on your own hardware

Docker: https://hub.docker.com/r/echtzeit/ez-clang

Artifacts: https://github.com/echtzeit-dev/ez-clang/releases/tag/v0.0.5

## [Release 0.0.5](release/0.0.5)

Interface Documentation:
* [RPC Interface spec](release/0.0.5/docs/rpc.md)
* [Runtime spec](release/0.0.5/docs/runtime.md)

**Disclaimer:** ez-clang is in a very experimental stage. Please consider any code and documentation a subject to change.
