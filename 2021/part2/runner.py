import sys
import days
from timeit import timeit
from utils import AoCDay

def run(num: str):
    with open(f"input/d{num}.txt") as f:
        dayClass: AoCDay.__class__
        try:
            dayClass = getattr(days, f"Day{num}")
        except:
            return print(f"Day {num} not found")

        day: AoCDay = dayClass(f.read())

        day.part1()
        print(f"Part 1: {day.p1}")

        day.part2()
        print(f"Part 2: {day.p2}")

try:
    dayNumber = sys.argv[1]
except:
    print("Please write the number day you wish to run")

run(dayNumber)
    