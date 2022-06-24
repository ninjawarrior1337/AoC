from utils import AoCDay


class Day1(AoCDay):

    def part1(self):
        s = 0
        for l in self.lines:
            li = int(l)
            s += (li // 3) - 2
        self.p1 = s

    @staticmethod
    def total_fuel(m: int):
        f = [(m // 3) - 2]
        while (nf := (f[-1] // 3) - 2) > 0:
            f.append(nf)
        return sum(f)

    def part2(self):
        components = [int(i) for i in self.lines]
        self.p2 = sum(self.total_fuel(c) for c in components)

