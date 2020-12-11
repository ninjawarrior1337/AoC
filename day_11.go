package main

import (
	"fmt"
)

type SeatGrid [][]string

type Mutation struct {
	X   int
	Y   int
	End string
}

func (g SeatGrid) RunDidChange(filledLimit int, countFunc func(x, y int) []string) bool {
	var m = make([]Mutation, 0)
	for y, r := range g {
		for x := range r {
			m = append(m, g.CheckAtLoc(x, y, filledLimit, countFunc))
		}
	}
	noChanges := true
	for _, mut := range m {
		if mut != (Mutation{}) {
			noChanges = false
		}
	}
	if noChanges {
		return false
	}
	for _, mut := range m {
		if mut != (Mutation{}) {
			g[mut.Y][mut.X] = mut.End
		}
	}
	return true
}

func (g SeatGrid) CheckAtLoc(x, y, filledLimit int, countFunc func(x, y int) []string) Mutation {
	currValue := g[y][x]
	posStatus := countFunc(x, y)
	if currValue == "L" {
		counts := CountString(posStatus)
		if counts["#"] == 0 {
			return Mutation{
				X:   x,
				Y:   y,
				End: "#",
			}
		}

	}
	if currValue == "#" {
		counts := CountString(posStatus)
		// fmt.Println(x, y, counts)
		if counts["#"] >= filledLimit {
			return Mutation{
				X:   x,
				Y:   y,
				End: "L",
			}
		}
	}
	return Mutation{}
}

func CountString(arr []string) map[string]int {
	out := make(map[string]int)
	for _, str := range arr {
		out[str] = out[str] + 1
	}
	return out
}

func (g SeatGrid) GetPositionsArround(x, y int) []string {
	var s = make([]string, 0)
	for yOff := -1; yOff <= 1; yOff++ {
		for xOff := -1; xOff <= 1; xOff++ {
			if !(xOff == 0 && yOff == 0) {
				s = append(s, g.GetCoordSafe(x+xOff, y+yOff))
			}

		}
	}
	return s
}

func (g SeatGrid) GetPositionsSeen(x, y int) []string {
	var directions = [][]int{{0, 1}, {1, 0}, {1, 1}, {0, -1}, {-1, 0}, {-1, -1}, {-1, 1}, {1, -1}}
	var finalList = []string{}
	for _, d := range directions {
		inc := 1
		for {
			val := g.GetCoordSafe(x+d[0]*inc, y+d[1]*inc)
			if val == "" || val == "L" || val == "#" {
				finalList = append(finalList, val)
				break
			}
			inc++
		}
	}
	return finalList
}

func (g SeatGrid) GetCoordSafe(x, y int) string {
	if y < 0 || y > len(g)-1 || x < 0 || x > len(g[y])-1 {
		return ""
	}
	return g[y][x]
}

func (g SeatGrid) CountOccupied() int {
	var c int
	for y, r := range g {
		for x := range r {
			if g[y][x] == "#" {
				c++
			}
		}
	}
	return c
}

func (g SeatGrid) String() string {
	var out = ""
	for _, y := range g {
		out += fmt.Sprintf("%v\n", y)
	}
	return out
}

func (g SeatGrid) LoadInput(i Input) {
	for y, l := range i.Lines() {
		g[y] = make([]string, len(l))
		for x, c := range l {
			g[y][x] = string(c)
		}
	}
}

func (d Day) Day11(i Input) (p1, p2 int) {
	var g = make(SeatGrid, len(i.Lines()))
	g.LoadInput(i)
	fmt.Println(g)
	//Part 1
	for g.RunDidChange(4, g.GetPositionsArround) {
		fmt.Println(g)
	}
	p1 = g.CountOccupied()

	//Part 2
	g.LoadInput(i)
	for g.RunDidChange(5, g.GetPositionsSeen) {
		fmt.Println(g)
	}
	p2 = g.CountOccupied()

	// fmt.Println(g.GetPositionsSeen(3, 3))

	return
}
