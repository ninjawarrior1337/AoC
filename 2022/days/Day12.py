from utils import AoCDay
from itertools import groupby

import networkx as nx
from matplotlib import pyplot as plt
import sys

class Day12(AoCDay):
    def part1(self):
        points = {(x, y): ord(v) for y, l in enumerate(self.lines) for x, v in enumerate(l)}

        s = (0, 0)
        e = (0, 0)

        for (x, y), v in points.items():
            if v == ord("S"):
                points[(x, y)] = ord('a')
                s = (x, y)
            if v == ord("E"):
                points[(x, y)] = ord('z')
                e = (x, y)
            points[(x, y)] = points[(x, y)] - ord('a')

        print(points)

        graph = nx.DiGraph()

        graph.add_nodes_from(points)

        print(graph)

        w, h = len(self.lines[0]), len(self.lines)

        def check_points(src: int, dest: int) -> bool:
            return dest <= (src+1)

        # edges
        for (x, y), v in points.items():
            # L
            if 0 <= x-1 < w and check_points(v, points[(x-1, y)]):
                graph.add_edge((x, y), (x-1, y), weight=v-points[(x-1, y)])
            # R 
            if 0 <= x+1 < w and check_points(v, points[(x+1, y)]):
                graph.add_edge((x, y), (x+1, y), weight=v-points[(x+1, y)])
            # U
            if 0 <= y+1 < h and check_points(v, points[(x, y+1)]):
                graph.add_edge((x, y), (x, y+1), weight=v-points[(x, y+1)])
            # D
            if 0 <= y-1 < h and check_points(v, points[(x, y-1)]):
                graph.add_edge((x, y), (x, y-1), weight=v-points[(x, y-1)])

        print(graph)

        sp = nx.shortest_path(graph, s, e)

        self.p1 = len(sp)-1

        all_a = [(x, y) for (x, y), v in points.items() if v == 0]

        def safe_shortest(graph, start, e):
            try:
                return len(nx.shortest_path(graph, start, e))-1
            except Exception:
                return sys.maxsize

        self.p2 = (min(
            [
                safe_shortest(graph, start, e)
                for start in all_a
            ]
        ))
