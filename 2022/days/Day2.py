from utils import AoCDay

rps = {
    "X": 0,
    "Y": 1,
    "Z": 2,
    "A": 0,
    "B": 1,
    "C": 2
}

win = {
    2: 0,
    1: 2,
    0: 1
}

class Day2(AoCDay):
    def score1(self, s: str):
        sc = 0
        o, y = (rps[x] for x in s.split(" "))
        sc += y+1
        if win[o] == y:
            sc += 6
        elif y == o:
            sc += 3
        else:
            pass
        return sc

    def score2(self, s: str):
        sc = 0
        o, y = (rps[x] for x in s.split(" "))

        if y == 0:
            pass
        elif y == 1:
            sc += 3
        else:
            sc += 6
        
        if sc == 6:
            sc += win[o]+1
        elif sc == 3:
            sc += o+1
        else:
            sc = {y: x for x, y in win.items()}[o]+1

        return sc
            
    def part1(self):
        tot = [self.score1(l) for l in self.lines]
        print(tot)
        self.p1 = sum(tot)

        tot = [self.score2(l) for l in self.lines]
        self.p2 = sum(tot)