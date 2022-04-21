# ez-clang Runtime for ARM Cortex Devices

Summary of runtime functions to be exposed by compatible device firmwares. Where not stated otherwise, these functions can be called from both, engine and user code. Please find more details in the paragraph for the respective function.

| Function     | Required | Parameters | Return Value |
|--------------|----------|------------|--------------|
| `__ez_clang_report_value` | mandatory | `uint32_t ID, const char *Blob, uint32_t Size` | `void` |
| `__ez_clang_report_string` | optional | `const char *Blob, uint32_t Size` | `void` |
| `__ez_clang_inline_heap_acquire` | optional | `uint32_t Size` | `char *` |

## __ez_clang_report_value

The host uses this function implicitly to print expression results. The repsonse handler for the ID knows the type of the raw data in the transmitted blob. The implementation is expected to send a `ReportValue` RPC message to the host.

| Parameter          | Description |
|--------------------|-------------|
| `uint32_t ID`      | ID of the respective RPC execute request |
| `const char *Blob` | Memory address of the return value |
| `uint32_t Size`    | Size of the return value in bytes |

Notes:
* For each RPC execute request, the host synthsizes one implicit call to this function.
* If called manually from user code, the behavior is undefined.

## __ez_clang_report_string

Send an asynchronous `ReportString` RPC message to the host. The payload will be interpreted as a string and get dumped to `stdout` immediately. Typically used for status messages from user code.

| Parameter          | Description |
|--------------------|-------------|
| `const char *Blob` | Memory address of the string value |
| `uint32_t Size`    | Size of the string in bytes |

## __ez_clang_inline_heap_acquire

Allocate heap-like memory for temporary buffers in user-code. The returned buffer is only valid while the originating RPC call is in-flight. If there is not enough free memory, this function is expected to return `NULL`. Typically used for target buffers in `printf` implementations.

| Parameter          | Description |
|--------------------|-------------|
| `uint32_t Size`    | Buffer size in bytes |
