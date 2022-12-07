from utils import AoCDay
from parse import parse
from collections import defaultdict

class Day7(AoCDay):
    def part1(self):
        curr_dir = ["/"]
        dirs: set[tuple] = set(("/"))
        f_size: dict[tuple, int] = {}
        
        for l in self.lines[2:]:
            if l[0].isdigit():
                s, n = parse("{:d} {}", l).fixed
                f_size[tuple([*curr_dir, n])] = s
            elif l.startswith("$ cd .."):
                curr_dir.pop()
            elif l.startswith("$ cd"):
                dir = parse("$ cd {}", l).fixed
                curr_dir.append(dir[0])
            elif l.startswith("dir"):
                _, cd = l.split()
                dirs.add(tuple([*curr_dir, cd]))
        
        dir_sizes: defaultdict[tuple, int] = defaultdict(lambda: 0)
        for d in dirs:
            for f_loc, size in f_size.items():
                if all(f_loc[i] == d[i] for i in range(len(d))):
                    dir_sizes[d] += size
                            
        self.p1 = sum(s for s in dir_sizes.values() if s <= 100000)

        fs_target = 70000000-30000000

        total = dir_sizes[("/")]
        for s in sorted(dir_sizes.values()):
            if total-s <= fs_target:
                self.p2 = s
                break