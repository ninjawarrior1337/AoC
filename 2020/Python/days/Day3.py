from utils import AoCDay


class Day3(AoCDay):

    def coord_generator(self, rr: int, d: int):
        r, c = 0, 0
        while r < len(self.lines):
            yield r, c % len(self.lines[0])
            r += d
            c += rr


    def part1(self):
        slope = [[c == "#" for c in l] for l in self.lines]

        trees = 0
        for r, c in self.coord_generator(3, 1):
            if slope[r][c]:
                trees += 1
        self.p1 = trees

        self.p2 = 1
        for a in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
            trees = 0
            for r, c in self.coord_generator(*a):
                if slope[r][c]:
                    trees += 1
            self.p2 *= trees
