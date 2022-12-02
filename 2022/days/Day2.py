from utils import AoCDay
from itertools import groupby

m = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

ma = {
    "A": 1,
    "B": 2,
    "C": 3
}

tie = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}

win = {
    "X": "C",
    "Y": "A",
    "Z": "B"
}

win_o = {
    "A": "Y",
    "B": "Z",
    "C": "X"
}

lose = {
    "A": "Z",
    "B": "X",
    "C": "Y"
}

class Day2(AoCDay):
    def score1(self, s: str):
        sc = 0

        o, y = s.split(" ")

        sc += m[y]

        if win[y] == o:
            sc += 6
        elif tie[o] == y:
            sc += 3
        else:
            pass
        return sc

    def score2(self, s: str):
        sc = 0
        o, y = s.split(" ")

        dr = {
            "X": 0,
            "Y": 3,
            "Z": 6
        }

        sc += dr[y]
        
        if sc == 0:
            sc += m[lose[o]]
        elif sc == 3:
            sc += m[tie[o]]
        else:
            sc += m[win_o[o]]

        return sc
            
    def part1(self):
        tot = [self.score1(l) for l in self.lines]
        print(tot)
        self.p1 = sum(tot)

        tot = [self.score2(l) for l in self.lines]
        self.p2 = sum(tot)