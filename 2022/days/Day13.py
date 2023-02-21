from utils import AoCDay
from itertools import groupby
import json

class Day13(AoCDay):

    @staticmethod
    def compare(a: list | int, b: list | int):
        if type(a) == type(b):
            for idx in range(min(len(a), min(len(b)))):
                pass

    def part1(self):
        inputs = self.raw.split("\n\n")

        for c in inputs:
            left, right = c.split("\n")
            left, right = json.loads(left), json.loads(right)

            print(left, right)


