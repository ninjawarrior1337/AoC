from collections import defaultdict
from utils import AoCDay
import numpy as np

from collections import defaultdict
 
# Utility function to create dictionary
def multi_dict(K, type):
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K-1, type))

class Day13(AoCDay):
    grid: np.ndarray
    points: list[tuple[int, int]]
    folds = list[tuple[str, int]]

    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.grid = multi_dict(2, int)
        print(self.lines)
        self.points = [(p[0], p[1]) for l in self.lines if self.lines.index(l) < self.lines.index('') for p in l.split(",")]
        self.folds = [l[11:].split("=") for l in self.lines if self.lines.index(l) > self.lines.index('')]
        xMax = max(self.points, key=lambda p: p[0])
        yMax = max(self.points, key=lambda p: p[1])
        grid = np.zeros((yMax, xMax))
        for p in self.points:
            grid[p[1]][p[0]] = 1        

    def part1(self):
        print(self.points)
        print(self.folds)
        print(self.grid)