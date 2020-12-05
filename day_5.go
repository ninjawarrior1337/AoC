package main

import (
	"fmt"
	"sort"
)

type Seat struct {
	Part string
	Id   int
	Row  int
	Col  int
}

var seats = []Seat{}

func ParsePass(line string) {
	var s Seat

	var rowString = string(line[0:7])
	var colString = string(line[7:])
	s.Part = line

	// Compute Row
	var rowArray = []int{}
	for i := 0; i <= 127; i++ {
		rowArray = append(rowArray, i)
	}
	for _, r := range rowString {
		switch r {
		case 'F':
			rowArray = rowArray[0 : len(rowArray)/2]
		case 'B':
			rowArray = rowArray[len(rowArray)/2:]
		}
	}
	s.Row = rowArray[0]

	// Compute Col
	var colArray = []int{}
	for i := 0; i <= 7; i++ {
		colArray = append(colArray, i)
	}
	for _, r := range colString {
		switch r {
		case 'L':
			colArray = colArray[0 : len(colArray)/2]
		case 'R':
			colArray = colArray[len(colArray)/2:]
		}
	}

	s.Col = colArray[0]

	s.Id = s.Row*8 + s.Col

	seats = append(seats, s)
}

func contains(s []int, e int) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}

func (d Day) Day5(lines []string) (p1 int, p2 int) {
	for _, line := range lines {
		ParsePass(line)
	}

	//We'll need this for both parts.
	ids := []int{}
	for _, p := range seats {
		ids = append(ids, p.Id)
	}
	sort.Ints(ids)
	fmt.Println(ids)

	//Part 1
	p1 = ids[len(ids)-1]

	//Part 2
	for i := ids[0]; i <= ids[len(ids)-1]; i++ {
		if contains(ids, i+1) && contains(ids, i-1) && !contains(ids, i) {
			p2 = i
		}
	}

	return
}
