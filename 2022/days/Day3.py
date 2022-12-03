from utils import AoCDay
from itertools import groupby
from more_itertools import grouper
from functools import reduce

class Day3(AoCDay):
    def score(self, s: str):
        if s.isupper():
            return ord(s)-38
        else:
            return ord(s)-96

    def part1(self):
        total = 0
        for l in self.lines:
            a = set(l[:len(l)//2])
            b = set(l[len(l)//2:])

            print(a & b)
            s = (a&b).pop()
            total += self.score(s)

        self.p1 = total

        self.p2 = 0
        for g in grouper(self.lines, 3):
            sets = [set(v) for v in g]
            s = reduce(lambda a, b: a&b, sets)
            
            self.p2 += sum(self.score(a) for a in s) 