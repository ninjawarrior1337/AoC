from utils import AoCDay
from itertools import groupby

class Day4(AoCDay):
    def part1(self):
        self.p1 = 0
        self.p2 = 0
        for l in self.lines:
            o, t = l.split(",")
            lo, ro = o.split("-")
            lt, rt = t.split("-")

            As = set(range(int(lo), int(ro)+1))
            Bs = set(range(int(lt), int(rt)+1))

            if len(As-Bs) == len(As)-len(Bs) or len(Bs-As) == len(Bs)-len(As):
                self.p1 += 1

            if len(As & Bs) > 0:
                self.p2 += 1