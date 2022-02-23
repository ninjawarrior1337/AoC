import days
from timeit import timeit
from utils import AoCDay

with open("input/d10.txt") as f:
    day: AoCDay = getattr(days, "Day10")(f.read())

    p1Time = timeit(day.part1, number=1)
    print(f"Part 1: {day.p1}; Time: {p1Time}")

    day.part2()
    print(f"Part 2: {day.p2}")