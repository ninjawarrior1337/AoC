from utils import AoCDay


class Day6(AoCDay):

    def group_gen(self):
        self.lines.append("")
        s = set()
        for i in self.lines:
            if i:
                for c in i:
                    s.add(c)
            else:
                yield s
                s.clear()

    def part1(self):
        self.p1 = sum(len(s) for s in self.group_gen())
