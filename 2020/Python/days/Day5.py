from utils import AoCDay


class Day5(AoCDay):

    @staticmethod
    def parse_seat(seat: str):
        i_s = seat.replace("F", "0").replace("B", "1").replace("R", "1").replace("L", "0")

        return int(i_s, 2)

    def part1(self):
        seats = [self.parse_seat(s) for s in self.lines]
        self.p1 = max(seats)
        m = min(seats)
        for i in range(m, self.p1):
            if i + 1 not in seats:
                self.p2 = i+1
                break
        