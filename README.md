# GreenPAK / Renesas Forge FPGA [SLG47910 (Rev BB)] Bitstream Reverse Engineering  [Soon&trade; :)]


- Black-box analysis and hardware-verified patching of the fuse map used by Renesas' GoConfig Software Hub to program the SLG47910 (Shrike Lite board, 1K-LUT Forge FPGA)
- Hardware verified using Vicharak Shrike Lite dev board
- No datasheet register map was used. The LUT truth-table field was located purely by differential analysis across known bitstreams, then confirmed by manually patching a bitstream to implement a different logic function and verifying correct behavior on the FPGA.

# Result (TLDR ver.)

- Manually patched fuse bits in working bitstreams, zero usage of Go Configure software after the edit and the FPGA correctly implemented a different logic function each time. Verified via Shrike-Lite.
- Examples:
**AND -> OR** (set-only, 0->1)

| a | b | expected OR | measured |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 |
1. Manually edited a working `AND` gate bitstream file `FPGA_bitstream_MCU_AND.bin` to work as an `OR` gate, verified via 4 input combinations (`00,01,10,11`)

**NAND -> NOR** (clear-only, 1->0)

| a | b | expected NOR | measured |
|---|---|---|---|
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 |

**XOR -> AND** (mixed: clear at 2 addresses, set at 1)

| a | b | expected AND | measured |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |

All three matched exactly, confirms full bidirectional read/write control over the LUT fuse field


## Hardware / tools

| Item | Detail |
|---|---|
| FPGA | Renesas Forge FPGA SLG47910 (Rev BB), 1K LUTs |
| Board | Shrike Lite (RP2040-based MCU + FPGA) |
| Toolchain | Renesas GO Configure Software Hub (GoConfig), Thonny (MicroPython) |
## Hardware & Toolchain Specifications

| Component | Detail |
| :--- | :--- |
| **Target FPGA** | Renesas Forge FPGA SLG47910 (Rev BB), ~1K LUT architecture |
| **Development Board** | Vicharak Shrike Lite (Dual-core ARM Cortex-M0+ RP2040 MCU + FPGA)<br>👉 [Zephyr Project Shrike Lite Board Documentation](https://docs.zephyrproject.org/latest/boards/vicharak/shrike_lite/doc/index.html) |
| **Toolchain** | Renesas GoConfig Software Hub<br>👉 [Renesas GoConfig Software Hub Official Page](https://www.renesas.com/en/products/programmable-logic/forgefpga-low-density-fpgas) | 

## Key findings

- Bitstream is an **unencrypted NVM/SRAM fuse map** (no security fuse set in this project), straightforward for diff-based analysis.
- Each 2-input LUT's truth table is stored as **4 individual fuse bits**, one per input address, not a packed 4-bit nibble.
- **Fuse offset and bit position are not fixed globally** -- they shift based on IO pin assignment and PnR outcome.

## Limitations
- Only 2-input combinational functions were tested. Sequential elements (registers, counters) and larger LUTs are unexplored and part of future work.
 
### Note : im kinda a script kiddie :(
