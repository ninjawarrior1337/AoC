from utils import AoCDay
from itertools import groupby

class Day10(AoCDay):
    def part1(self):
        clock = 1
        x = 1

        grid = [[]]

        mem = []

        for l in self.lines:
            if l == "noop":
                clock += 1
                mem.append(x)

            else:
                _, arg = l.split(" ")
                arg_n = int(arg)

                clock += 1
                mem.append(x)
                clock += 1
                mem.append(x)
                x += arg_n

        mem.append(x)

        print(mem)

        base = 20
        self.p1 = 0
        while base < len(mem):
            print(mem[base-1], base)
            self.p1 += mem[base-1] * (base)
            base += 40


        # render
        for i, c in enumerate(mem):
            sprite_pos = range(c-1, c+2)
            if i%40 in sprite_pos:
                print("#", end="")
            else:
                print(".", end="")
            # print(i, c)

            if (i+1) % 40 == 0:
                print()