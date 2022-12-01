from utils import AoCDay

class Day1(AoCDay):
    def part1(self):
        totals = []
        self.lines.append("")
        t = 0
        for v in self.lines:
            if v != "":
                i = int(v)
                t += i
            else:
                totals.append(t)
                t = 0
        print(totals)
        self.p1 = max(totals)

        self.p2 = 0
        for i in range(3):
            self.p1 = max(totals)
            self.p2 += self.p1
            totals.remove(self.p1)
