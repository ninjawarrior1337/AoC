from utils import AoCDay
from itertools import groupby

class Day4(AoCDay):
    def part1(self):
        res = []
        self.p2 = 0
        for l in self.lines:
            o, t = l.split(",")
            ar = range(int(o.split("-")[0]), int(o.split("-")[1])+1)
            br = range(int(t.split("-")[0]), int(t.split("-")[1])+1)
            
            a = (int(o.split("-")[0]), int(o.split("-")[1]))
            b = (int(t.split("-")[0]), int(t.split("-")[1]))

            insidea = True
            insideb = True
            for v in ar:
                if not b[0] <= v <= b[1]:
                    insidea = False
            for v in br:
                if not a[0] <= v <= a[1]:
                    insideb = False
            if insidea or insideb:
                print(l, insidea, insideb)
            res.append(insidea or insideb)

            if len(set(ar) & set(br)) > 0:
                self.p2 += 1
        
        self.p1 = sum(1 for v in res if v)