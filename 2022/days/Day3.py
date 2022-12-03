from utils import AoCDay
from more_itertools import grouper, divide
from functools import reduce


class Day3(AoCDay):
    def score(self, s: str):
        return ord(s)-38 if s.isupper() else ord(s)-96

    def part1(self):
        self.p1 = sum(
            map(
                self.score,
                (
                    (set(divide(2, a)[0]) & set(divide(2, a)[1])).pop() for a in self.lines
                )
            )
        )
        self.p2 = sum(
            map(
                self.score,
                [
                    reduce(
                        lambda a, b: a & b,
                        [set(e) for e in g]
                    ).pop() for g in grouper(self.lines, 3)
                ]
            )
        )
