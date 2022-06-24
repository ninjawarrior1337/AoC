from utils import AoCDay
from collections import defaultdict
import networkx as nx


class Day6(AoCDay):
    adj_list: defaultdict[str, list[str]] = defaultdict(lambda: [])

    def construct_graph(self):
        for l in self.lines:
            c, o = l.split(")")
            self.adj_list[o].append(c)

    def part1(self):
        self.construct_graph()
        count = 0
        for p in self.adj_list.keys():
            curr_planet = p
            while curr_planet in list(self.adj_list.keys()):
                curr_planet = self.adj_list[curr_planet][0]
                count += 1
        self.p1 = count

    def part2(self):
        G = nx.Graph(self.adj_list)
        pa = nx.all_shortest_paths(G, self.adj_list["YOU"][0], self.adj_list["SAN"][0])
        found = pa.__next__()
        print(found)
        self.p2 = len(found) - 1
