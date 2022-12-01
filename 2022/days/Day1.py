from utils import AoCDay
from itertools import groupby
class Day1(AoCDay):
    def part1(self):
        totals = [sum(int(v) for v in a) for k, a in groupby(self.lines, lambda l: l != "") if k]
        self.p1 = max(totals)
        self.p2 = sum(sorted(totals, reverse=True)[:3])
