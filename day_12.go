package main

import (
	"fmt"
	"math"
	"strconv"
)

func IdealSin(num int) int {
	return int(math.Round(math.Sin(float64(num) * math.Pi / 180)))
}

func IdealCos(num int) int {
	return int(math.Round(math.Cos(float64(num) * math.Pi / 180)))
}

func (d Day) Day12(i Input) (p1, p2 float64) {
	var ship = make(map[string]int)
	var ship2 = make(map[string]int)
	var waypoint = make(map[string]int)
	ship["x"], ship["y"], ship["d"] = 0, 0, 0
	ship2["x"], ship2["y"], ship2["d"] = 0, 0, 0
	waypoint["x"], waypoint["y"] = 10, 1
	for _, l := range i.Lines() {
		movement := l[0]
		numberSlice := l[1:]
		number, _ := strconv.Atoi(numberSlice)
		switch movement {
		case 'N':
			ship["y"] += number
			waypoint["y"] += number
		case 'S':
			ship["y"] -= number
			waypoint["y"] -= number
		case 'E':
			ship["x"] += number
			waypoint["x"] += number
		case 'W':
			ship["x"] -= number
			waypoint["x"] -= number
		case 'L':
			ship["d"] += number
			waypoint["x"], waypoint["y"] = waypoint["x"]*IdealCos(number)-waypoint["y"]*IdealSin(number), waypoint["x"]*IdealSin(number)+waypoint["y"]*IdealCos(number)
		case 'R':
			ship["d"] -= number
			waypoint["x"], waypoint["y"] = waypoint["x"]*IdealCos(-number)-waypoint["y"]*IdealSin(-number), waypoint["x"]*IdealSin(-number)+waypoint["y"]*IdealCos(-number)
		case 'F':
			if cos := IdealCos(ship["d"]); cos != 0 {
				ship["x"] += int(cos) * number
			}
			if sin := IdealSin(ship["d"]); sin != 0 {
				ship["y"] += int(sin) * number
			}

			ship2["x"] += waypoint["x"] * number
			ship2["y"] += waypoint["y"] * number
		}
		fmt.Println("Instruction", string(movement), number, "Ship", ship2, "WP", waypoint)
	}
	p1 = math.Abs(float64(ship["x"])) + math.Abs(float64(ship["y"]))
	p2 = math.Abs(float64(ship2["x"])) + math.Abs(float64(ship2["y"]))
	return
}
