def b2s(num):
    """
    Returns a string with all bits in binary with the beginning 0b removed
    """
    return (bin(num))[2:]

''' unrolled simulation instructions = ["00000000000001010010001110000011", "00000000000000111010001100000011", 
                "00000000000100110000001100010011", "00000000011000111010000000100011",
                "00000000010000111010001100000011", "00000000000100110000001100010011",
                "00000000011000111010001000100011", "00000000100000111010001100000011",
                "00000000000100110000001100010011", "00000000011000111010010000100011"]
'''

'''
# branch simulation
offset = -10 & 0xFFF 

integer_instructions = [
    (0 << 20) | (10 << 15) | (2 << 12) | (7 << 7) | 3,      # lw x7, 0(x10)
    (3 << 20) | (0 << 15) | (0 << 12) | (5 << 7) | 19,     # addi x5, x0, 3
    (0 << 20) | (7 << 15) | (2 << 12) | (6 << 7) | 3,      # lw x6, 0(x7)
    (1 << 20) | (6 << 15) | (0 << 12) | (6 << 7) | 19,     # addi x6, x6, 1
    (0 << 25) | (6 << 20) | (7 << 15) | (2 << 12) | (0 << 7) | 35, # sw x6, 0(x7)
    (4 << 20) | (7 << 15) | (0 << 12) | (7 << 7) | 19,     # addi x7, x7, 4
    ((-1 & 0xFFF) << 20) | (5 << 15) | (0 << 12) | (5 << 7) | 19, # addi x5, x5, -1
    (                                                      # bne x5, x0, Loop
        99 | 
        (1 << 12) | 
        (5 << 15) | 
        (0 << 20) |
        ((offset & 0xF) << 8) | 
        (((offset >> 4) & 0x3F) << 25) | 
        (((offset >> 10) & 0x1) << 7) | 
        (((offset >> 11) & 0x1) << 31)
    )
]

instructions = [f"{instr:032b}" for instr in integer_instructions]
'''

#hazards instructions
'''
instructions = [
    "01000000001100001000000100110011",  # sub x2,  x1,  x3
    "00000000010100010111011000110011",  # and x12, x2,  x5
    "00000000001000110110011010110011",  # or  x13, x6,  x2
    "00000000110101100111000100110011",  # and x2,  x12, x13
    "00000000001000010000011100110011",  # add x14, x2,  x2
]'''

#dynamic instructions

instructions = [
    "00000000000000111010001100000011",  # lw   x6, 0(x7)
    "00000000010000111010010000000011",  # lw   x8, 4(x7)
    "00000000100000111010010010000011",  # lw   x9, 8(x7)
    "00000000000100110000001100010011",  # addi x6, x6, 1
    "00000000000101000000010000010011",  # addi x8, x8, 1
    "00000000000101001000010010010011",  # addi x9, x9, 1
    "00000000011000111010000000100011",  # sw   x6, 0(x7)
    "00000000100000111010001000100011",  # sw   x8, 4(x7)
    "00000000100100111010010000100011",  # sw   x9, 8(x7)
]
for idx, ii in enumerate(instructions):
    if not len(ii) == 32:
        raise ValueError("Not correct length at index %d: got %d bits (%s)" % (idx, len(ii), ii))
for ii in range(0, len(instructions)):
    instructions[ii] = int(instructions[ii], 2)

all_bytes = []
mask = 2**8 - 1
for ii in instructions:
    all_bytes.append(ii & mask)
    all_bytes.append((ii >> 8) & mask)
    all_bytes.append((ii >> 16) & mask)
    all_bytes.append((ii >> 24) & mask)
all_bytes_array = bytearray(all_bytes)
bin(all_bytes_array[0]), bin(all_bytes_array[-1])
with open("binaries/dynamic_instructions.bin", 'wb+') as rv_file:
    rv_file.write(all_bytes_array)