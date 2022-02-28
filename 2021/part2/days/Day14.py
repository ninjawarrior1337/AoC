from audioop import reverse
from typing import Counter
from utils import AoCDay

class Day14(AoCDay):
    base: list[str]
    insertions: dict[str, str]

    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.base = [c for c in self.lines[0]]
        self.insertions = {r.split(" -> ")[0]: r.split(" -> ")[1] for r in self.lines[2:] }

    def compute_insertions(self):
        insertions = []
        for i in self.insertions.items():
            left, right = [c for c in i[0]]
            for idx in range(len(self.base)-1, 0, -1):
                if self.base[idx-1] == left and self.base[idx] == right:
                    # self.base.insert(idx, "")
                    insertions.append((idx, i[1]))
        return insertions


    def apply_insertions(self, ins: list[tuple[int, str]]):
        ins_sorted = sorted(ins, key=lambda i: i[0], reverse=True)
        for i in ins_sorted:
            self.base.insert(i[0], i[1])

    def part1(self):
        print(self.base)
        print(self.insertions)
        for _ in range(10):
            ins = self.compute_insertions()
            self.apply_insertions(ins)
        c = Counter(self.base)
        common = c.most_common()
        self.p1 = common[0][1] - common[-1][1]

    def part2(self):
        print(self.base)
        print(self.insertions)
        for _ in range(30):
            ins = self.compute_insertions()
            self.apply_insertions(ins)
        c = Counter(self.base)
        common = c.most_common()
        self.p2 = common[0][1] - common[-1][1]
        
        