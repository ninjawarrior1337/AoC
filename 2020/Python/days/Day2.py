from utils import AoCDay


class Day2(AoCDay):

    @staticmethod
    def parse_pw(s: str) -> tuple[int, int, str, str]:
        r, p = s.split(": ")
        ra, l = r.split(" ")
        min, max = ra.split("-")
        return int(min), int(max), l, p

    def part1(self):
        pw = [self.parse_pw(p) for p in self.lines]

        self.p1 = len([p for p in pw if p[0] <= p[3].count(p[2]) <= p[1]])
        self.p2 = len([p for p in pw if (p[3][p[0]-1] == p[2]) != (p[3][p[1]-1] == p[2])])
