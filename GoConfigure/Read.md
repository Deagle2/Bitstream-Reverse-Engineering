# Notes
- The current configuration implements a baseline example case (Gate ANDNOT_AB).
- Other logical gate primitives follow an identical pattern for compilation and bitstream generation.

## Quick Start (Pre-Built Bitstream)

1. Connect your board via USB
2. Upload `examples/bitstream/baseline/FPGA_MCU_bitstream_<NAME>.bin` using ShrikeFlash library
3. Expected result: Led goes HIGH/LOW depending on gate bitstream + python firmware stimulus (eg. AND gate bitstream:- LED HIGH when a=b=1)

## Build From Soure
1. Open the `.ffpga` in Go Configure Software Hub 
2. Click Synthesize → Generate Bitstream
3. Output will be in ffpga/build/

## Firmware

1. Open your preferred microcontroller IDE (e.g., Thonny IDE or Arduino IDE).
2. Load and flash the execution script located at firmware/micropython/main.py.

