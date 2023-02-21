from utils import AoCDay
from more_itertools import windowed
from PIL import Image

class Day14(AoCDay):

    @staticmethod
    def construct_cave(lines: list[str], floor=False):
        grid: dict[tuple[int, int], str] = {}
        for line in lines:
            pts = line.split(" -> ")
            pts = [(int(p.split(",")[0]), int(p.split(",")[1])) for p in pts]
            print(pts)

            for s, e in windowed(pts, 2):
                if s[0] == e[0]:
                    for y in range(min(s[1], e[1]), max(s[1], e[1])+1):
                        grid[(s[0], y)] = "rock"
                else:
                    for x in range(min(s[0], e[0]), max(s[0], e[0])+1):
                        grid[(x, s[1])] = "rock"


        maxX, maxY = max(p[0] for p in grid.keys()), max(p[1] for p in grid.keys())

        if floor:
                for x in range(maxX):
                    grid[x, maxY+2] = "rock"

        return grid

    @staticmethod
    def tick(grid: dict[tuple[int, int], str], floor = False) -> bool:
        at_rest = False
        maxX, maxY = max(p[0] for p in grid.keys()), max(p[1] for p in grid.keys())

        curr = (500, 0)
        while not at_rest:
            if curr[1] > maxY and not floor:
                return True
                
            # move down first
            down_dest = (curr[0], curr[1]+1)
            if not grid.get(down_dest):
                curr = down_dest
                continue
            
            # check down-left
            dl_dest = (curr[0]-1, curr[1]+1)
            if not grid.get(dl_dest):
                curr = dl_dest
                continue

            # check down-right
            dr_dest = (curr[0]+1, curr[1]+1)
            if not grid.get(dr_dest):
                curr = dr_dest
                continue

            at_rest = True

        grid[curr] = "sand"

    @staticmethod
    def render(grid: dict[tuple[int, int], str], frames: list[Image.Image]):
        maxX, maxY = max(p[0] for p in grid.keys()), max(p[1] for p in grid.keys())

        img = Image.new("1", (maxX+1, maxY+1))

        for x, y in grid.keys():
            img.putpixel((x, y), 1)

        
        frames.append(img)

    def part1(self):
        c = self.construct_cave(self.lines)

        frames: list[Image.Image] = []

        self.render(c, frames)

        while not self.tick(c):
            self.render(c, frames)


        print(len(frames)-1)

        # part 2
        c = self.construct_cave(self.lines, True)

        frames: list[Image.Image] = []

        self.render(c, frames)

        while not self.tick(c):
            self.render(c, frames)


        print(len(frames)-1)

        frames[-1].show()
