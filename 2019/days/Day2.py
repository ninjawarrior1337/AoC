from utils import AoCDay
from intcode_computer import IntcodeCPU


class Day2(AoCDay):

    def part1(self):
        cpu = IntcodeCPU()
        cpu.load_program(self.lines[0])

        cpu.run(12, 2)
        self.p1 = cpu.output()

    def part2(self):
        target = 19690720
        cpu = IntcodeCPU()
        cpu.load_program(self.lines[0])

        for i in range(100):
            for j in range(100):
                cpu.run(i, j)
                if cpu.output() == target:
                    self.p2 = 100*i + j
                    return
                cpu.reset()
