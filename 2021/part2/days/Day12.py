from utils import AoCDay
from collections import Counter, defaultdict

class Day12(AoCDay):
    graph: dict[str, list[str]] = defaultdict(lambda: [])
    smallCaveLimit = 1
    validPaths = []
    
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
        paths = []
        caves = self.graph.get(root)
        counts = Counter(path[:-1])

        if root == "end":
            self.validPaths.append(path[1:-1])
        
        elif (counts[root] >= self.smallCaveLimit and root.lower() == root) or root == "end":
            return path
        
        else:
            for c in caves: 
                paths.append(self.compute_paths(c, [*path, c]))
        
        return paths

    def part2_validate(self, p: list[str]) -> bool:
        counts = Counter(p)
        # print(counts.most_common(), p)
        return sum([c[1] >= 2 for c in counts.most_common() if c[0].lower() == c[0]]) <= 1
        pass

    def part1(self):
        print(dict(self.graph))
        self.compute_paths("start", ["start"])
        self.p1 = len(self.validPaths)

    def part2(self):
        self.validPaths = []
        self.smallCaveLimit = 2
        self.compute_paths("start", ["start"])
        # print(self.validPaths)

        self.p2 = len([p for p in self.validPaths if self.part2_validate(p)])


