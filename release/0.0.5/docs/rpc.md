# ez-clang RPC Interface for ARM Cortex Devices

Summary of RPC endpoints to be implemented by compatible device firmwares. Please find more details in the paragraph for the respective request.

| Endpoint     | Required | Input | Output |
|--------------|-------|---------|----------------|
| `__ez_clang_rpc_lookup` | mandatory, bootstrap | `array<string>` | `expected<array<addr>>` |
| `__ez_clang_rpc_commit` | mandatory | `array<addr, size, size, data>` | `error` |
| `__ez_clang_rpc_execute` | mandatory | `addr` | `error` |
| `__ez_clang_rpc_mem_read_cstring` | optional | `addr` | `string` |

## Message Header Encoding

RPC messages in both directions are prefixed with a message header. Device firmware must be able to handle opcodes: `0` Setup, `1` Hangup, and `3` Call. In general, RPC traffic is synchronous: when the host sends `3` Call, it must wait for the `2` Result message. Exceptions are `1` Hangup and `5` ReportString, which might be sent to the host at any time.

| Field        | Bytes | Example | Interpretation |
|--------------|-------|---------|----------------|
| Total size   | 8     | `24 00 00 00 00 00 00 00` | 32 bytes header + 4 bytes payload |
| Opcode       | 8     | `03 00 00 00 00 00 00 00` | `0` Setup, `1` Hangup, `2` Result, `3` Call, `4` ReportValue, `5` ReportString |
| Message ID   | 8     | `09 00 00 00 00 00 00 00` | Response ID will be `9` |
| Handler      | 8     | `01 19 00 00 00 00 00 00` | Address of the RPC handler (only for Opcode `3` Call) |

## Setup Message

Sent from device to host notifying that the device is ready for a REPL session.

| Field            | Bytes | Example | Interpretation |
|------------------|-------|---------|----------------|
| Magic Number     | 8     | `01 23 57 BD BD 57 23 01` | Start of serial stream |
| Version String   | 8 + N | `05 00 00 00 00 00 00 00` `30 2E 30 2E 35` | "0.0.5" with size prefix |
| Code Buffer Base | 8     | `00 04 00 20 00 00 00 00` | Address of code buffer in SRAM is `0x20000400` |
| Code Buffer Size | 8     | `00 10 00 00 00 00 00 00` | Size of code buffer in SRAM is 4KB |
| Bootstrap Symbols | 8    | `02 00 00 00 00 00 00 00` | 2 symbols given for bootstrapping |
| Symbol 1 | (8 + N) + 8   | `15 00 00 00 00 00 00 00` `5f 5f 65 7a 5f 63 6c 61 6e 67 5f 72 70 63 5f 6c 6f 6f 6b 75 70` `01 18 00 00 00 00 00 00` | __ez_clang_rpc_lookup @ `0x00001801` |
| Symbol 2 | (8 + N) + 8   | `15 00 00 00 00 00 00 00` `5f 5f 65 7a 5f 63 6c 61 6e 67 5f 72 70 63 5f 63 6f 6d 6d 69 74` `01 19 00 00 00 00 00 00` | __ez_clang_rpc_commit @ `0x00001901` |

## Hangup Message

Sent in any direction and confirmed from the other side, notifying that the current REPL session is ending. On failure, output encoding follows the [error response encoding](#error-encoding).

| Field            | Bytes | Example | Interpretation |
|------------------|-------|---------|----------------|
| Success Code     | 1     | `00`    | Hangup with **no error** |

## Error Encoding

Some functions that return an error status, encoded in a single leading byte. A zero value indicates success. Other values indicate an error. The leading byte encodes the failure code and is followed by an error message.

| Field            | Bytes | Example | Interpretation |
|------------------|-------|---------|----------------|
| Failure Code     | 1     | `01`    | Result **has an error** |
| Description Size | 8     | `04 00 00 00 00 00 00 00` | 4 bytes string |
| Description      | N     | `49 6e 66 6f` | "Info" |

## Lookup Request

Resolve device addresses for a number of symbols. Takes an array of symbol names. Returns same-sized array of addresses. For symbols that are not found, the respective index holds a NULL value.

`__ez_clang_rpc_lookup(array<string>) -> expected<array<addr>>`

### Input

| Field  | Bytes | Example                   | Interpretation |
|--------|-------|---------------------------|----------------|
| Count  | 8     | `02 00 00 00 00 00 00 00` | Request for two symbols |
| Name 1 | 8 + N | `16 00 00 00 00 00 00 00` `5f 5f 65 7a 5f 63 6c 61 6e 67 5f 72 70 63 5f 65 78 65 63 75 74 65` | First symbol: __ez_clang_rpc_execute |
| Name 2 | 8 + N | `17 00 00 00 00 00 00 00` `5f 5f 65 7a 5f 63 6c 61 6e 67 5f 72 65 70 6f 72 74 5f 76 61 6c 75 65` | Second symbol: __ez_clang_report_value |

### Output

| Field        | Bytes | Example                   | Interpretation |
|--------------|-------|---------------------------|----------------|
| Success Code | 1     | `00`                      | No errors during lookup |
| Count        | 8     | `02 00 00 00 00 00 00 00` | Result with two addresses |
| Address 1    | 8     | `01 1A 00 00 00 00 00 00` | First symbol @ `0x00001A01` |
| Address 2    | 8     | `01 1B 00 00 00 00 00 00` | Second symbol @ `0x00001B01` |

## Commit Request

Copy linked code and data segments into device memory. On failure, output encoding follows the [error response encoding](#error-encoding).

`__ez_clang_rpc_commit(array<addr, size, size, data>) -> error`

### Input

| Field          | Bytes | Example                   | Interpretation |
|----------------|-------|---------------------------|----------------|
| Segments       | 8     | `01 00 00 00 00 00 00 00` | Request for one segment |
| Target address | 8     | `00 04 00 20 00 00 00 00` | Segment base @ `0x20000400` |
| Segment size   | 8     | `20 00 00 00 00 00 00 00` | Total size is 32 byte |
| Content size   | 8     | `10 00 00 00 00 00 00 00` | Content size is 16 byte (remaining space is zeroed) |
| Content        | N     | `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00` (TODO) | Binary content |

### Output

| Field        | Bytes | Example | Interpretation |
|--------------|-------|---------|----------------|
| Success Code | 1     | `00`    | All segments committed successfully |

## Execute Request

Invoke the function on the given address. The address is expected to point to a 16-bit aligned Thumb-function (least-significant byte is `0x01`) in the code buffer. On failure, output encoding follows the [error response encoding](#error-encoding).

`__ez_clang_rpc_execute(addr) -> error`

### Input

| Field   | Bytes | Example                   | Interpretation |
|---------|-------|---------------------------|----------------|
| Address | 8     | `01 22 00 00 00 00 00 00` | Invoke JITed function at `0x00002201` |

### Output

| Field        | Bytes | Example | Interpretation |
|--------------|-------|---------|----------------|
| Success Code | 1     | `00`    | Function executed successfully |

## Read C-String Request

Read a null-terminated string from the given address and send it back.

`__ez_clang_rpc_mem_read_cstring(addr) -> string`

### Input

| Field   | Bytes | Example                   | Interpretation |
|---------|-------|---------------------------|----------------|
| Address | 8     | `10 04 00 20 00 00 00 00` | Read C-String from `0x20000410` |

### Output

| Field        | Bytes | Example | Interpretation |
|--------------|-------|---------|----------------|
| String       | 8 + N | `03 00 00 00 00 00 00 00` `61 62 63` | "abc" |
