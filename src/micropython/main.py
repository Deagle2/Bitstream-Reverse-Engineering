import shrike
import machine 
shrike.flash("FPGA_bitstream_MCU.bin") # Change according to bitstream file name
# Current version requires these specific IO Ports for proper function
# Check README.md and methodology section
# Fuse offset and bit position are not fixed globally, they will shift acc to IO Planning
a = machine.Pin(1, machine.Pin.OUT) 
b = machine.Pin(3, machine.Pin.OUT)  

# Iterate over (ab - 1 bit inputs) -> 00,01,10,11 
# Example if a.value(0) and b.value(1) and flashed with an OR gate bitstream LED will go HIGH
# Example if a.value(0) and b.value(1) and flashed with an AND gate bitstream LED will go LOW
a.value(0)  
b.value(0)  
