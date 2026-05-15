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

        if self.if_id is None:
            self.id_ex = None
            return

        instruction = self.if_id["instruction"]
        opcode = (instruction) & (2**7 - 1)
        rd = (instruction >> 7) & (2**5 - 1)
        funct3 = (instruction >> 12) & (2**3 - 1)
        rs1 = (instruction >> 15) & (2**5 - 1)
        rs2 = (instruction >> 20) & (2**5 - 1)

        reg_write = mem_rd = mem_wr = wb_sel = bne = 0
        alu_src = 1

        if opcode == 3: # lw
            reg_write = 1
            mem_rd = 1
            wb_sel = 1
        elif opcode == 35: # sw
            mem_wr = 1
        elif opcode == 19: # addi
            reg_write = 1

        self.id_ex = {
            "instruction": instruction,
            "pc": self.if_id["pc"],
            "opcode": opcode,
            "rd": rd,
            "funct3": funct3,
            "rs1": rs1,
            "rs2": rs2,
            "RegWrite": reg_write,
            "ALUSrc": alu_src,
            "MemRd": mem_rd,
            "MemWr": mem_wr,
            "WBSel": wb_sel,
            "bne": bne
        }
    def execute(self):

        if self.id_ex is None:
            self.ex_mem = None
            return
        else:
            self.ex_mem = self.id_ex

    def memory(self):
        
        if self.ex_mem is None:
            self.mem_wb = None
            return
        else:
            self.mem_wb = self.ex_mem

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

            if self.mem_wb:
                print(f"{i},"
                    f"{self.mem_wb['instruction']},"
                    f"{self.mem_wb['opcode']},"
                    f"{self.mem_wb['funct3']},"
                    f"{self.mem_wb['rd']},"
                    f"{self.mem_wb['rs1']},"
                    f"{self.mem_wb['rs2']},"
                    f"{self.mem_wb['RegWrite']},"
                    f"{self.mem_wb['ALUSrc']},"
                    f"*,*,"  # Placeholders for FwdA and FwdB
                    f"{self.mem_wb['MemRd']},"
                    f"{self.mem_wb['MemWr']},"
                    f"{self.mem_wb['WBSel']},"
                    f"{self.mem_wb['bne']}")

            i += 1

            if (self.if_id is None and self.id_ex is None and
                    self.ex_mem is None and self.mem_wb is None):
                done = True

if __name__ == "__main__":
    sim = Pipeline("branch_instructions.bin")
    sim.run_simulation()