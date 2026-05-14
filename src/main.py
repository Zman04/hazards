class Pipeline:
    def __init__(self, binary_path):
        self.pc = 0
        self.instructions = self.load_binary(binary_path) # 
        self.branch_counter = 0

        self.if_id = None
        self.id_ex = None
        self.ex_mem = None
        self.mem_wb = None

    