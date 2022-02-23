from abc import ABC
from typing import Any

class AoCDay(ABC):
    p1: Any = None
    p2: Any = None
    lines: list[str]

    def __init__(self, lines: str) -> None:
        self.lines = lines.splitlines()

    def part1(self):
        print("TODO: Solve part 1")

    def part2(self):
        print("TODO: Solve part 2")