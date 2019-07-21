# Returns 32 for 32-bit and 64 for 64-bit
import struct
print(struct.calcsize("P") * 8)