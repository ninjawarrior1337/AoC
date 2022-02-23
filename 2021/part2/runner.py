import sys
import days
from timeit import timeit
from utils import AoCDay

def run(num: str):
    with open(f"input/d{num}.txt") as f:
        day: AoCDay = getattr(days, f"Day{num}")(f.read())

        day.part1()
        print(f"Part 1: {day.p1}")

        day.part2()
        print(f"Part 2: {day.p2}")

try:
    dayNumber = sys.argv[1]
    run(dayNumber)
except:
    print("Please write the number day you wish to run")
    