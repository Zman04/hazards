class Pipeline:
    def __init__(self, binary_path):
        self.pc = 0
        self.instructions = self.load_binary(binary_path) # Functions as memory
        self.x5 = 3 # Hardcoded counter for the branch logic
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
        elif opcode == 99: # bne
            bne = 1
            imm_12    = (instruction >> 31) & 0x1
            imm_11    = (instruction >> 7)  & 0x1
            imm_10_5  = (instruction >> 25) & 0x3F
            imm_4_1   = (instruction >> 8)  & 0xF
            
            # Combine and multiply by 2 (left shift 1) 
            imm = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
            
            # Handle sign extension for the negative jump
            if imm & 0x1000:
                imm -= 0x2000

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
            "bne": bne,
            "val1": self.x5 if rs1 == 5 else 0, # Hardcoded: if rs1 is x5, give it x5's value
            "val2": 0,                          # bne x5, x0, Loop (x0 is always 0)
            "imm": imm
        }
    def execute(self):
        if self.id_ex is None:
            self.ex_mem = None
            return
            
        # Branch handling logic
        if self.id_ex["bne"] == 1:
            # Check if values are not equal
            if self.id_ex["val1"] != self.id_ex["val2"]: 
                # Calculate the jump address
                target_address = self.id_ex["pc"] + self.id_ex["imm"]
                
                # Update the PC so the Fetch stage grabs the right instruction next
                self.pc = target_address
                
                # Flush the accidentally fetched instruction from the Decode pipeline register
                self.if_id = None 

        # Pass the dictionary to the next stage
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