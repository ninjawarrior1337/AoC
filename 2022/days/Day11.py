from utils import AoCDay
from itertools import groupby
from typing import Callable, Self, Type
from parse import parse
from dataclasses import dataclass
from tqdm import tqdm
import math

@dataclass(init=False)
class Monkey():
    id: int
    items: list[int]
    op: Callable[[int], int]
    div: int
    t: int
    f: int

    ins_count = 0

    def construct_monkey(s: str) -> "Monkey":
        m = Monkey()
        l = s.split("\n")
        m.id = int(parse("Monkey {}:", l[0]).fixed[0])
        m.items = [int(x) for x in parse("  Starting items: {}", l[1]).fixed[0].split(", ")]

        # we dont talk about this
        def construct_op_lambda(l: str) -> Callable[[int], int]:
            if m.id == 0:
                return lambda x: x*2
            if m.id == 1:
                return lambda x: x*x
            if m.id == 2:
                return lambda x: x + 6
            if m.id == 3:
                return lambda x: x + 2
            if m.id == 4:
                return lambda x: x*11
            if m.id == 5:
                return lambda x: x+7
            if m.id == 6:
                return lambda x: x+1
            if m.id == 7:
                return lambda x: x+5
        
        m.op = construct_op_lambda(l[2])

        m.div = int(parse("  Test: divisible by {}", l[3]).fixed[0])

        m.t = int(parse("    If true: throw to monkey {}", l[4]).fixed[0])
        m.f = int(parse("    If false: throw to monkey {}", l[5]).fixed[0])

        return m

    def take_turn(self, m: list["Monkey"]):
        for idx, item in enumerate(self.items):
            new_worry = self.op(item)
            # new_worry //= 3

            # chinese remainder theorem
            new_worry %= math.prod((m.div for m in m))

            if new_worry % self.div == 0:
                m[self.t].items.append(new_worry)
            else:
                m[self.f].items.append(new_worry)

            self.ins_count += 1
            
        self.items.clear()

class Day11(AoCDay):
    def part1(self):
        info_parts = self.raw.split("\n\n")

        monkeys = [Monkey.construct_monkey(s) for s in info_parts]

        print(monkeys)

        for m in tqdm(range(10_000)):
            for m in monkeys:
                m.take_turn(monkeys)

        print()

        print(
            sorted(

                [m.ins_count for m in monkeys]
            )
        )
        
