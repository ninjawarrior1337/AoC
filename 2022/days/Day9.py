from utils import AoCDay
from itertools import groupby

class Day9(AoCDay):
    def trail(self, h: list[int], t: list[int]):
        neighbor = False
        for y in range(-1, 2):
            for x in range(-1, 2):
                neighbor |= [h[0]+x, h[1]+y] == t
        
        new_t = t[:]

        print(neighbor)

        if not neighbor:
            if t[0] == h[0]:
                if h[1] > t[1]:
                    new_t[1] += 1
                else:
                    new_t[1] -= 1
            elif t[1] == h[1]:
                if h[0] > t[0]:
                    new_t[0] += 1
                else:
                    new_t[0] -= 1
            else:
                if h[0] > t[0] and h[1] > t[1]:
                    new_t[0] += 1
                    new_t[1] += 1
                elif h[0] > t[0] and h[1] < t[1]:
                    new_t[0] += 1
                    new_t[1] -= 1
                elif h[0] < t[0] and h[1] > t[1]:
                    new_t[0] -= 1
                    new_t[1] += 1
                elif h[0] < t[0] and h[1] < t[1]:
                    new_t[0] -= 1
                    new_t[1] -= 1

        return new_t

    def part1(self):
        h_pos = [0, 0]
        t_pos = [0, 0]
        t_points = set()
        t_points.add((0, 0))
        for l in self.lines:
            d, q = l.split()[0], int(l.split()[1])
            # print(t_points)
            for _ in range(q):
                if d == "U":
                    h_pos[1] += 1
                elif d == "D":
                    h_pos[1] -= 1
                elif d == "L":
                    h_pos[0] -= 1
                elif d == "R":
                    h_pos[0] += 1

                # print(h_pos, t_pos)
                t_pos = self.trail(h_pos, t_pos)
                t_points.add(tuple(t_pos))

        self.p1 = len(t_points)
            
