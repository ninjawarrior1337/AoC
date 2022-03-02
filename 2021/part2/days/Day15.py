from collections import defaultdict
import numpy as np
from utils import AoCDay
from queue import PriorityQueue

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
    
    def dijkstra(self, src = (0,0), dest = (10, 10)):
        Q: PriorityQueue[tuple[int, tuple[int, int]]] = PriorityQueue()
        dist = {}
        prev = {}

        dist[src] = 0
        Q.put((dist[src], src))
        
        for v in self.graph.keys():
            if v != src:
                dist[v] = float("inf")
                prev[v] = None
        
        while Q.not_empty:
            _, u = Q.get()

            for n in self.graph[u]:
                alt = dist[u] + n[1]

                if alt < dist[n[0]]:
                    dist[n[0]] = alt
                    if dest and n[0] == dest:
                        return dist, prev
                    prev[n[0]] = u
                    Q.put((alt, n[0]))

        return dist, prev

    def larger_grid(self):
        stack = [self.grid[:]]
        for i in range(1, 5):
            g = stack[i-1]
            stack.append(np.where(g+1 >= 10, 1, g+1))

        self.grid = np.hstack(stack)

        stack = [self.grid[:]]
        for i in range(1, 5):
            g = stack[i-1]
            stack.append(np.where(g+1 >= 10, 1, g+1))

        self.grid = np.vstack(stack)

    def shape_idx(self):
        return (self.grid.shape[0]-1, self.grid.shape[1]-1)

    def part1(self):
        self.construct_graph()
        dist, _ = self.dijkstra(dest=self.shape_idx())
        self.p1 = dist[tuple([d-1 for d in self.grid.shape])]

    def part2(self):
        self.larger_grid()
        self.construct_graph()
        dist, _ = self.dijkstra(dest=self.shape_idx())
        self.p2 = dist[tuple([d-1 for d in self.grid.shape])]