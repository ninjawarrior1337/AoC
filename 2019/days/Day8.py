from utils import AoCDay
from collections import defaultdict
from PIL import Image


class Day8(AoCDay):
    layers: defaultdict[int, list[int]] = defaultdict(lambda: [])
    w, h = (25, 6)

    def load(self):
        curr_layer = 0
        while curr_layer * (self.w * self.h) + (self.w * self.h) < len(self.lines[0]):
            num_arr = [int(c) for c in self.lines[0]]
            self.layers[curr_layer] = num_arr[
                                      curr_layer * (self.w * self.h): curr_layer * (self.w * self.h) + (
                                                  self.w * self.h)]
            curr_layer += 1

    def part1(self):
        self.load()

        target_layer = min(self.layers.values(), key=lambda l: l.count(0))
        self.p1 = target_layer.count(1) * target_layer.count(2)

    def part2(self):
        im = Image.new("1", self.dim)
        print(self.layers.keys())
        for y in range(self.dim[1]):
            for x in range(self.dim[0]):
                for l in range(max(self.layers.keys()), -1, -1):
                    d = self.layers[l][x+(self.dim[0]*y)]
                    if d == 1:
                        im.putpixel((x, y), 1)
                    if d == 0:
                        im.putpixel((x, y), 0)

        # im.show()

