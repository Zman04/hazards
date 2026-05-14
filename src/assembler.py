def b2s(num):
    """
    Returns a string with all bits in binary with the beginning 0b removed
    """
    return (bin(num))[2:]

instructions = ["00000000000001010010001110000011", "00000000000000111010001100000011", 
                "00000000000100110000001100010011", "00000000011000111010000000100011",
                "00000000010000111010001100000011", "00000000000100110000001100010011",
                "00000000011000111010001000100011", "00000000100000111010001100000011",
                "00000000000100110000001100010011", "00000000011000111010010000100011"]
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
with open("risc-v_instructions.bin", 'wb+') as rv_file:
    rv_file.write(all_bytes_array)