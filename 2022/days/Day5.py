from utils import AoCDay
from itertools import groupby
from parse import parse
from collections import defaultdict
from queue import LifoQueue
from copy import deepcopy

class Day5(AoCDay):

    def build_stacks(self, iils: str) -> defaultdict[str, LifoQueue[str]]:
        stacks: defaultdict[str, LifoQueue[str]] = defaultdict(LifoQueue)

        for c, v in enumerate(iils[-1]):
            if v != " ":
                for r in range(len(iils)-1, -1, -1):
                    cha = iils[r][c]
                    if cha != " ":
                        stacks[v].put(iils[r][c])
        return stacks



    def part1(self):
        initial, moves = self.raw.split("\n\n")
        iils = initial.splitlines()

        stacks = self.build_stacks(iils)
        stacks_p2 = self.build_stacks(iils)
        
        for m in moves.split("\n"):
            ct, src, dest = parse("move {:d} from {:d} to {:d}", m).fixed

            popped = []

            for _ in range(ct):
                e = stacks[str(src)].get()
                stacks[str(dest)].put(e)

                popped.append(stacks_p2[str(src)].get())

            for e in reversed(popped):
                stacks_p2[str(dest)].put(e)

        self.p1 = ""

        for i in range(1, 10):
            self.p1 += (stacks[str(i)].get())

        self.p2 = ""

        for i in range(1, 10):
            self.p2 += (stacks_p2[str(i)].get())