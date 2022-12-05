from utils import AoCDay
from itertools import groupby
from parse import parse
from collections import defaultdict
from queue import LifoQueue

class Day5(AoCDay):
    def part1(self):
        stacks: defaultdict[str, LifoQueue[str]] = defaultdict(LifoQueue)
        initial, moves = self.raw.split("\n\n")

        print(initial)

        iils = initial.splitlines()

        for c, v in enumerate(iils[-1]):
            if v != " ":
                for r in range(len(iils)-1, -1, -1):
                    cha = iils[r][c]
                    if cha != " ":
                        stacks[v].put(iils[r][c])
                        # print(iils[r][c])

        for m in moves.split("\n"):
            ct, src, dest = parse("move {:d} from {:d} to {:d}", m).fixed
            # print(ct, src, dest)

            popped = []
            for _ in range(ct):
                popped.append(stacks[str(src)].get())
            for e in reversed(popped):
                stacks[str(dest)].put(e)

        self.p1 = ""

        for i in range(1, 10):
            self.p1 += (stacks[str(i)].get())