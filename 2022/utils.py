from abc import ABC
from typing import Any

class AoCDay(ABC):
    p1: Any = None
    p2: Any = None
    lines: list[str]
    raw: str

    def __init__(self, linesRaw: str) -> None:
        self.lines = linesRaw.splitlines()
        self.raw = linesRaw

    def part1(self):
        print("TODO: Solve part 1")

    def part2(self):
        print("TODO: Solve part 2")