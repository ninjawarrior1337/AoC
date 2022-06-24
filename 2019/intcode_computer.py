class IntcodeCPU:
    ptr: int = 0
    program: list[int]
    mem: list[int]

    OPCODES = {
        1: lambda x, y: x + y,
        2: lambda x, y: x * y
    }

    def output(self):
        return self.mem[0]

    def load_program(self, p: str):
        self.program = [int(i) for i in p.split(",")]
        self.reset()

    def reset(self):
        self.ptr = 0
        self.mem = self.program[:]

    def run(self, n: int, v: int):
        self.mem[1] = n
        self.mem[2] = v
        while 1:
            ins = self.mem[self.ptr]

            if ins == 99:
                return
            ptr1, ptr2, dest = self.mem[self.ptr+1: self.ptr+4]

            self.mem[dest] = self.OPCODES[ins](self.mem[ptr1], self.mem[ptr2])

            self.ptr += 4
