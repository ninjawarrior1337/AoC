from curses import flash
from typing import Tuple
from utils import AoCDay
import numpy as np

class Day11(AoCDay):
    grid: np.ndarray
    num_flashes: int = 0
    all_flash_step: int = 0

    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.grid = np.array([[int(n) for n in l] for l in self.lines])

    def neighbors(self, r: int, c: int) -> list[Tuple[int, int]]:
        for ro in (-1, 0, 1):
            for co in (-1, 0, 1):
                if 0 <= ro+r < len(self.grid) and 0 <= co+c < len(self.grid[r]):
                    yield (ro+r,co+c)

    def step(self, step_num=0):
        self.grid += 1
        queue = []
        queue += zip(*np.where(self.grid > 9))
        flashes = set(queue)
        while queue:
            p = queue.pop()
            for n in self.neighbors(*p):
                self.grid[n] += 1
                if n not in flashes and self.grid[n] > 9:
                    queue.append(n)
                    flashes.add(n)

        for f in flashes:
            self.grid[f] = 0
            self.num_flashes+=1
        
        if len(flashes) == self.grid.size:
            self.all_flash_step = step_num+1
        

    def part1(self):
        print(self.grid)
        for i in range(100):
            self.step(i)
        print(self.grid)
        self.p1 = self.num_flashes

    def part2(self):
        for i in range(100, 10000):
            self.step(i)
            if self.all_flash_step > 0:
                break
        self.p2 = self.all_flash_step

    