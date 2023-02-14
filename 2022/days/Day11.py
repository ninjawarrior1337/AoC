from utils import AoCDay
from itertools import groupby
from typing import Callable

class Monkey():
    id: int
    items: list[int]
    op: Callable[[int], int]
    test: Callable[[int], bool]
    t: int
    f: int

    def take_turn(self, m: list["Monkey"]):
        for idx, item in enumerate(self.items):
            new_worry = self.op(item)
            new_worry //= 3

            if self.test(new_worry):
                m[t].items.append(new_worry)
            else:
                m[f].items.append(new_worry)
            
        self.items.clear()

class Day11(AoCDay):
    def part1(self):
        info_parts = self.raw.split("\n\n")

        print(info_parts)

