class Pipeline:
    def __init__(self, binary_path):
        self.pc = 0
        self.instructions = self.load_binary(binary_path) # 
        self.branch_counter = 0

        self.if_id = None
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
        pass
    def decode(self):
        pass
    def execute(self):
        pass
    def memory(self):
        pass
    def write_back(self):
        pass