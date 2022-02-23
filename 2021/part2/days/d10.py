from binascii import Incomplete
from typing import Tuple
from utils import AoCDay

class Day10(AoCDay):
    char_map = {"[": "]", "<": ">", "{": "}", "(": ")"}
    errorScores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    autoScores = { ")": 1, "]": 2, "}": 3, ">": 4}

    def compute_autocomplete_score(self, stack: list[str]) -> int:
        score = 0
        for c in stack:
            score *= 5
            score += self.autoScores[self.char_map[c]]
        return score

    def compute_stack(self, s: str) -> Tuple[bool, str, list[str]]:
        stack = []
        for c in s:
            if c in self.char_map.keys():
                stack.append(c)
            else:
                if c is not self.char_map[stack[-1]]:
                    return (True, c)
                else:
                    stack.pop()
        return (False, None, stack)

    def part1(self):
        self.p1 = sum(self.errorScores[self.compute_stack(s)[1]] for s in self.lines if self.compute_stack(s)[0])
        pass

    def part2(self):
        stacks = [self.compute_stack(s)[2] for s in self.lines if not self.compute_stack(s)[0]]
        stacks = [s[::-1] for s in stacks]
        scores = [self.compute_autocomplete_score(s) for s in stacks]
        self.p2 = sorted(scores)[len(scores)//2]
        pass