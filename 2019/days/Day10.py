from utils import AoCDay
from functools import cache


class Day10(AoCDay):
    grid: list[list[bool]]

    def load(self):
        self.grid = [[c == "#" for c in line] for line in self.lines]

    def raycast_and_count(self, r: int, c: int):
        targets = [a for a in self.get_all_asteroids() if a is not (r, c)]
        lines = [
            lambda x: ((r - t[0])/(c - t[1]))*(x-t[1])
            for t in targets
        ]
        return lines

    @cache
    def get_all_asteroids(self) -> set[tuple[int, int]]:
        asteroids = set()
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c]:
                    asteroids.add((r, c))
        return asteroids


    def part1(self):
        self.load()

        print(self.get_all_asteroids())
        print([f(4) for f in self.raycast_and_count(4, 4)])
