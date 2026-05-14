class Pipeline:
    def __init__(self, binary_path):
        self.pc = 0
        self.instructions = self.load_binary(binary_path) # Functions as memory
        self.branch_counter = 0

        self.if_id = None # Pipeline Register
        self.id_ex = None
        self.ex_mem = None
        self.mem_wb = None

    def load_binary(self, binary_path):
        instructions = []
        try:
            with open(binary_path, 'rb') as f:
                # Read 4 bytes (32 bits) at a time
                while chunk := f.read(4):
                    if len(chunk) == 4:
                        # Convert the 4 raw bytes back into a single Python integer
                        instruction = int.from_bytes(chunk, byteorder='little')
                        instructions.append(instruction)
        except FileNotFoundError:
            print(f"Error: Could not find {binary_path}")
            
        return instructions

    def fetch(self):
        index = self.pc // 4

        if index < len(self.instructions):
            instruction = self.instructions[index]
            self.if_id = {"instruction": instruction, "pc": self.pc}
            self.pc += 4
        else:
            self.if_id = None

    def decode(self):
        instruction = self.if_id["instruction"]
        opcode = (instruction) & (2**7 - 1)
        rd = (instruction >> 7) & (2**5 - 1)
        funct3 = (instruction >> 12) & (2**3 - 1)
        rs1 = (instruction >> 15) & (2**5 - 1)
        rs2 = (instruction >> 20) & (2**5 - 1)

        self.id_ex = {
            "instruction": instruction,
            "pc": self.if_id["pc"],
            "opcode": opcode,
            "rd": rd,
            "funct3": funct3,
            "rs1": rs1,
            "rs2": rs2
        }
    def execute(self):
        pass
    def memory(self):
        pass
    def write_back(self):
        pass

    def run_simulation(self):
        i = 0
        done = False

        print("Cycle,Instr,Op,Fct3,Rd,Rs1,Rs2,RegWrite,ALUSrc,FwdA,FwdB,MemRd,MemWr,WBSel,bne")

        while (done != True):
            self.write_back()
            self.memory()
            self.execute()
            self.decode()
            self.fetch()

            i += 1

            if i > 10:
                done = True

if __name__ == "__main__":
    sim = Pipeline("risc-v_instrucitons.bin")
    sim.run()