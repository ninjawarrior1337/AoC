from typing import List, Tuple, Any

from utils import AoCDay
from itertools import groupby


class Day4(AoCDay):
    bottom: int
    top: int

    def __init__(self, li):
        super().__init__(li)
        line = self.lines[0]
        self.bottom, self.top = (int(i) for i in line.split("-"))

    @staticmethod
    def convert_to_tuple(i: int) -> list[tuple[str, int]]:
        return [(k, len(list(g))) for k, g in groupby(str(i))]

    def part1(self):
        count = 0
        for i in range(self.bottom, self.top + 1):
            i_arr = [int(c) for c in str(i)]
            has_two_adj = False
            increases = True
            for j in range(len(i_arr) - 1):
                if i_arr[j + 1] < i_arr[j]:
                    increases = False
                if i_arr[j + 1] == i_arr[j]:
                    has_two_adj = True
            if increases and has_two_adj:
                count += 1

        self.p1 = count

    def part2(self):
        count = 0
        for i in range(self.bottom, self.top + 1):
            i_arr = [int(c) for c in str(i)]
            has_two_adj = False
            increases = True
            for j in range(len(i_arr) - 1):
                if i_arr[j + 1] < i_arr[j]:
                    increases = False

            if any(e[1] == 2 for e in self.convert_to_tuple(i)):
                has_two_adj = True

            if increases and has_two_adj:
                count += 1

        self.p2 = count
