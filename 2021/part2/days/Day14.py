from collections import defaultdict
from typing import Counter
from utils import AoCDay

class Day14(AoCDay):
    base: list[str]
    pairs: dict[tuple[str, str], int]
    counts: dict[str, int]
    insertions: dict[str, str]

    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.base = [c for c in self.lines[0]]
        self.counts = defaultdict(Counter(self.base))
        self.insertions = {r.split(" -> ")[0]: r.split(" -> ")[1] for r in self.lines[2:] }
        self.pairs = defaultdict(int)
        self.compute_pairs()

    def compute_pairs(self):
        for i in range(1, len(self.base)):
            left, right = self.base[i-1], self.base[i]
            self.pairs[(left, right)] += 1


    def apply_insertions(self):
        for p, v in list(self.pairs.items()):
            for tmpl, val in self.insertions.items():
                left, right = list(tmpl)
                if p == (left, right):
                    self.pairs[(left, val)] += 1 * v
                    self.pairs[(val, right)] += 1 * v
                    self.pairs[(left, right)] -= 1 * v
                    self.counts[val] += 1

    def part1(self):
        print(self.pairs)
        print(self.insertions)
        for i in range(5):
            self.apply_insertions()
        print(self.counts)
        print(self.pairs)
        print(sum(self.pairs.values()))

    def part2(self):
        pass
        
        