from utils import AoCDay
import multiprocessing as mp

class Particle():
    p: list[int, int]
    v: list[int, int]
    maxY: int = 0

    def __str__(self):
        return f"Pos: {self.p}; Vel: {self.v}"

    def __init__(self, vx, vy) -> None:
        self.p = [0, 0]
        self.v = [vx, vy]

    def step(self):
        self.p = [sum(z) for z in zip(self.p, self.v)]
        if self.v[0] > 0:
            self.v[0] -= 1
        elif self.v[0] < 0:
            self.v[0] += 1

        self.maxY = max(self.p[1], self.maxY)

        self.v[1] -= 1
        
def target_test(p: Particle, bl, tr):
    return bl[0] <= p.p[0] <= tr[0] and bl[1] <= p.p[1] <= tr[1] 

TARGET = (282, -80), (314, -45)

def do_sim(p: Particle) -> int:
    while True:
        p.step()
        if target_test(p, *TARGET):
            return p.maxY
        if p.p[0] > TARGET[1][0]:
            return -1
        elif p.p[1] < TARGET[0][1]:
            return -1

class Day17(AoCDay):
    def part1(self):
        initial: list[Particle] = []
        for y in range(-80, 314*3):
            for x in range(0, 314*3, 1):
                initial.append(Particle(x, y))
        
        with mp.Pool() as p:
            maxs = p.map(do_sim, initial)

            self.p1 = max(maxs)
            self.p2 = len([c for c in maxs if c != -1])