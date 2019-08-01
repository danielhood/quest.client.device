# Accepts output of mode2 -m 
# Parses pulse durations and converts to bytes
# This outputs the first 5 bytes which is good enough
# to uniquely idenity majiquest wands.
# Requires LIRC installed to get mode2 and an exposed /dev/lirc0 device
#
# To run:
#    mode2 -m | python std.py
#

import sys
import fileinput

def getByte(bits, offset):
    byte = 0
    for i in range(0, 8):
        if bits[i+offset]:
            byte |= 1 << i
    return byte

try:
    hasStart1 = False
    hasStart2 = False
    hasStart3 = False
    bits = [0]*54
    bitCount = 0
    for line in fileinput.input():
        vals = line.split()
        if len(vals) == 6 and str.isdigit(vals[0]):
            print(vals)
            bits[bitCount] = int(vals[0]) > 400
            bits[bitCount+1] = int(vals[2]) > 400
            bits[bitCount+2] = int(vals[4]) > 400

            if hasStart3:
                if bitCount == 51:
                    bitCount = 0
                    hasStart1 = False
                    hasStart2 = False
                    hasStart3 = False
                    print (getByte(bits, 31),getByte(bits, 23),getByte(bits, 15),getByte(bits, 7),getByte(bits, 0))
                else:
                    bitCount += 3
            elif hasStart2:
                if bits[6] or bits[7] or bits[8]:
                    hasStart1 = False
                    hasStart2 = False
                    bitCount = 0
                else:
                    hasStart3 = True
                    bitCount += 3
            elif hasStart1:
                if bits[3] or bits[4] or bits[5]:
                    hasStart1 = False
                    bitCount = 0
                else:
                    hasStart2 = True
                    bitCount += 3
            else:
                if bits[0] or bits[1] or bits[2]:
                    hasStart1 = False
                    bitCount = 0
                else:
                    hasStart1 = True
                    bitCount += 3
except KeyboardInterrupt:
    exit()
