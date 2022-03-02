from collections import defaultdict
import numpy as np
from utils import AoCDay

class Day15(AoCDay):
    grid: np.ndarray
    graph: dict[tuple[int, int], list[tuple[tuple[int, int], int]]]

    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.grid = np.array([int(c) for c in self.lines[0]])
        for l in self.lines[1:]:
            ints = [int(c) for c in l]
            self.grid = np.vstack([self.grid, ints])
        self.graph = defaultdict(list)

    def neighbors(self, point: tuple[int, int]):
        for ro in [-1, 1]:
            r = point[0]+ro
            if 0 <= r < self.grid.shape[0]:
                yield (point[0]+ro, point[1])
        for co in [-1, 1]:
            c = point[1]+co
            if 0 <= c < self.grid.shape[1]:
                yield (point[0], point[1]+co)

    def construct_graph(self):
        shape = self.grid.shape
        for r in range(shape[0]):
            for c in range(shape[1]):
                pos = (r, c)
                for n in self.neighbors(pos):
                    self.graph[pos].append((n, self.grid[n]))
    
    def dijkstra(self, src = (0,0)):
        Q: set[tuple[int, int]] = set()
        dist = {}
        prev = {}
        for v in self.graph.keys():
            dist[v] = float("inf")
            prev[v] = None
            Q.add(v)
        dist[src] = 0

        print(Q)

        while Q:
            u = min(Q, key=lambda v: dist[v])
            print(u)
            for n in self.graph[u]:
                if n[0] in Q:
                    alt = dist[u] + n[1]
                    print(dist[n[0]], alt, alt < dist[n[0]])
                    if alt < dist[n[0]]:
                        dist[n] = alt
                        prev[n] = u
                        print(dist[n])
            Q.remove(u)
            print(len(Q))
        return dist, prev

    def part1(self):
        print(self.grid)
        self.construct_graph()
        print(self.graph)
        print(self.dijkstra())