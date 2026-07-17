# GreenPAK / Renesas Forge FPGA [SLG47910 (Rev BB)] Bitstream Reverse Engineering 


- Black-box analysis and hardware-verified patching of the fuse map used by Renesas' GoConfig Software Hub to program the SLG47910 (Shrike Lite board, 1K-LUT Forge FPGA)
- Hardware verified using Vicharak Shrike Lite dev board
- No datasheet register map was used. The LUT truth-table field was located purely by differential analysis across known bitstreams, then confirmed by manually patching a bitstream to implement a different logic function and verifying correct behavior on the FPGA.
- Only 2-input combinational functions were tested. Sequential elements (registers, counters) and larger LUTs are unexplored and part of future work.

## TL;DR Results

Manually flipped fuse bits inside compiled bitstream files — zero use of GoConfig after the initial build — and the FPGA correctly implemented a different logic function each time. Verified on hardware via LED output across all 4 input combinations.
<details>
<summary>Full input/output tables [Click Here]</summary>

**AND → OR** (set-only)
| a | b | expected OR | measured |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 |

**NAND → NOR** (clear-only)
| a | b | expected NOR | measured |
|---|---|---|---|
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 |

**XOR → AND** (mixed: clear at 2 addresses, set at 1)
| a | b | expected AND | measured |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |

</details>

| Patch | Bit direction | Result |
|---|---|---|
| AND → OR | set-only (0→1) | exact OR truth table |
| NAND → NOR | clear-only (1→0) | exact NOR truth table |
| XOR → AND | mixed (set + clear) | exact AND truth table |

All three patches matched their target truth table exactly across all 4 input combinations, confirming full bidirectional read/write control over the LUT fuse field — not just observation of GoConfig's output, but arbitrary rewriting of it.



---

## Hardware / Toolchain

| Component | Detail |
|---|---|
| Target FPGA | Renesas Forge FPGA SLG47910 (Rev BB), 1120 LUTs |
| Dev board | Vicharak Shrike Lite (dual-core RP2040 MCU + FPGA) — [board docs](https://docs.zephyrproject.org) |
| Toolchain | Renesas GoConfig Software Hub (bitstream generation) | 
| Scripting | Python, Micropython, bash|

## Methodology (Short Ver.)

- The core technique is **differential analysis**, across known functions, built on several tiny combinational modules that are pin-for-pin identical and differ only in
actual function, compile each to a bitstream via Go Configure Software Hub, then diff the binaries. Bits that change consistently across many such pairs encode the actual logic; 
everything else is noise (such as routing artifacts or unrelated PnR states).  

### Full writeup  Soon&trade; ;)

## Key findings

- Bitstream was an **unencrypted NVM/SRAM fuse map** (no security fuse set in this project), straightforward for differtial-based analysis.
- Each 2-input LUT's truth table is stored as **4 individual fuse bits**, one per input address, not a packed 4-bit nibble.
- **Fuse offset and bit position are not fixed globally** -- they shift based on IO pin assignment and PnR outcome.
- Demonstrated **arbitrary write access**: hand-patched fuse bits directly in the compiled `.bin`, **bypassing GoConfig entirely post-generation**, and the chip executed the new logic correctly on the first flash, every time.

# FloorPlan
<img width="1312" height="642" alt="image" src="https://github.com/user-attachments/assets/2793686c-0a71-4621-8e9f-b7a20b7d3284" />

  **IO Planning**
* **Inputs:**
    * `a`  $\rightarrow$ `GPIO4_IN` --(1)
    * `b` $\rightarrow$ `GPIO5_IN` --(2)
* **Outputs:**
    * `led`  $\rightarrow$ `GPIO16_OUT` (Data) --(3)
    * `led_oe`  $\rightarrow$ `GPIO16_OE` (Output Enable) --(3)

## License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
 
### Author: A script kiddie :D
