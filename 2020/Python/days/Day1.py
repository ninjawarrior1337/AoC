from utils import AoCDay


class Day1(AoCDay):

    def part1(self):
        ns = [int(x) for x in self.lines]

        for i in ns:
            for j in ns:
                if i+j == 2020:
                    self.p1 = i*j
                for k in ns:
                    if i+j+k == 2020:
                        self.p2 = i*j*k