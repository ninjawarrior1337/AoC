from utils import AoCDay
from more_itertools import windowed

class Day6(AoCDay):
    def part1(self):
        s = self.lines[0]
        for p, num in zip((1, 2), (4, 14)):
            w = windowed(s, num)

            for i, win in enumerate(w):
                if len(set(win)) == num:
                    if p == 1:
                        self.p1 = i+num
                    else:
                        self.p2 = i+num
                    break
                    
