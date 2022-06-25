from utils import AoCDay


class Day3(AoCDay):
    wire_1, wire_2 = [], []
    crosses = None

    @staticmethod
    def parse_wire(w: str):
        positions = []
        current_pos = [0, 0]

        moves = w.split(",")
        for m in moves:
            dir, dist = m[0], int(m[1:])
            for i in range(dist):
                if dir == "R":
                    current_pos[0] += 1
                if dir == "L":
                    current_pos[0] -= 1
                if dir == "U":
                    current_pos[1] += 1
                if dir == "D":
                    current_pos[1] -= 1
                positions.append(tuple(current_pos))
        return positions

    def part1(self):
        self.wire_1 = self.parse_wire(self.lines[0])
        self.wire_2 = self.parse_wire(self.lines[1])

        self.crosses = set(self.wire_1) & set(self.wire_2)
        self.p1 = min(abs(p[0]) + abs(p[1]) for p in self.crosses)

    def part2(self):
        self.p2 = min(sum((self.wire_1.index(c)+1, self.wire_2.index(c)+1)) for c in self.crosses)