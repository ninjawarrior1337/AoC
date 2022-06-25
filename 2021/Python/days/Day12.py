from utils import AoCDay
from collections import Counter, defaultdict

class Day12(AoCDay):
    graph: dict[str, list[str]] = defaultdict(lambda: [])
    smallCaveLimit = 1
    p1 = 0
    p2 = 0
    
    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        for l in self.lines:
            par, chi = l.split("-")
            if par == "start" or chi == "end":
                self.graph[par].append(chi)
                continue
            elif chi == "start" or par == "end":
                self.graph[chi].append(par)
                continue
            else:
                self.graph[chi].append(par)
                self.graph[par].append(chi)                

    def compute_paths(self, root: str, path: list[str]):
        caves = self.graph.get(root)
        counts = Counter(path[:-1])

        if root == "end":
            if self.smallCaveLimit == 1:
                self.p1+=1
            elif sum([c[1] >= 2 for c in counts.most_common() if c[0].lower() == c[0]]) <= 1:
                self.p2+=1
        
        elif (counts[root] >= self.smallCaveLimit and root.lower() == root):
            return None
        
        else:
            for c in caves: 
                self.compute_paths(c, [*path, c])
                    
                    
    def part1(self):
        print(dict(self.graph))
        self.compute_paths("start", ["start"])
        # self.p1 = len(self.validPaths)

    def part2(self):
        self.smallCaveLimit = 2
        self.compute_paths("start", ["start"])
        # print(self.validPaths)

        # self.p2 = len([p for p in self.validPaths if self.part2_validate(p)])


