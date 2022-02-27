from utils import AoCDay
import numpy as np
from PIL import Image

class Day13(AoCDay):
    grid: np.ndarray
    points: list[tuple[int, int]] = []
    folds: list[tuple[str, int]] = []

    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        for i, l in enumerate(self.lines):
            if i < self.lines.index(""):
                x, y = l.split(",")
                self.points.append((int(x), int(y)))
            elif i > self.lines.index(""):
                direction, num = l[11:].split("=")
                self.folds.append((direction, int(num)))
        xMax = max(p[0] for p in self.points)
        yMax = max(p[1] for p in self.points)
        self.grid = np.zeros((yMax+1, xMax+1))
        self.grid = np.hstack([self.grid, np.zeros((yMax+1, 3))])
        for p in self.points:
            self.grid[p[1]][p[0]] = 1 

    def fold(self, dir: str, num: int):
        grid = self.grid[:]
        
        if dir == "x":
            grid = np.transpose(grid)

        upper = grid[0:num]
        lower = grid[num+1:]
        grid = upper + lower[::-1]
        
        if dir == "x":
            grid = np.transpose(grid)
        
        self.grid = np.where(grid >= 1, 1, 0)

    def part1(self):
        print(self.grid.shape)
        self.fold(*self.folds[0])
        print(self.grid)
        self.p1 = np.sum(self.grid)

    def part2(self):
        for f in self.folds[1:]:
            self.fold(*f)
        im = Image.fromarray(np.uint8(self.grid)*255)
        im.save("d13.png")