from utils import AoCDay
from collections import defaultdict
from PIL import Image


class Day8(AoCDay):
    layers: list[list[int]]
    w, h = (25, 6)

    def load(self):
        pixels = [int(x) for x in self.lines[0]]
        self.layers = [pixels[i: i+self.w*self.h] for i in range(0, len(self.lines[0]), self.w*self.h)]

    def part1(self):
        self.load()

        target_layer = min(self.layers, key=lambda l: l.count(0))
        self.p1 = target_layer.count(1) * target_layer.count(2)

    def part2(self):
        im = Image.new("1", (self.w, self.h))
        print(self.layers)
        for y in range(self.h):
            for x in range(self.w):
                for l in range(len(self.layers)-1, -1, -1):
                    d = self.layers[l][x+(self.w*y)]
                    if d == 1:
                        im.putpixel((x, y), 1)
                    if d == 0:
                        im.putpixel((x, y), 0)

        im.show()

