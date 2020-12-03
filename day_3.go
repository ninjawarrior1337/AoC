package main

import (
	"bufio"
	"fmt"
	"log"
	"sync"
)

type TobagganMap map[int][]bool

func (t TobagganMap) IsTreeAtCoord(x int, y int) bool {
	log.Printf("checking %v, %v", x, len(t[y]))
	return t[y][x%len(t[y])]
}

func (t TobagganMap) LoadRow(idx int, r string) {
	row := make([]bool, 0)
	for _, c := range r {
		if c == '#' {
			row = append(row, true)
		} else {
			row = append(row, false)
		}
	}
	fmt.Println(idx, row)
	t[idx] = row
}

func (d Day) Day3(s *bufio.Scanner) (p1 int, p2 int) {
	var c int
	tMap := make(TobagganMap)
	for s.Scan() {
		t := s.Text()
		tMap.LoadRow(c, t)
		c++ // hehehehheheehhehhehheheeheh
	}

	var x = 0
	for y := 0; y < len(tMap); y++ {
		log.Printf("checking row %v", y)
		if tMap.IsTreeAtCoord(x, y) {
			p1++
		}
		x += 3
	}

	p2 = 1
	var p2Waiter sync.WaitGroup
	var p2Offsets = [][]int{
		{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2},
	}
	for _, offset := range p2Offsets {
		p2Waiter.Add(1)
		go func(offset []int) {
			var treeCounter = 0
			var x = 0
			for y := 0; y < len(tMap); y += offset[1] {
				if tMap.IsTreeAtCoord(x, y) {
					treeCounter++
				}
				x += offset[0]
			}
			p2 *= treeCounter
			p2Waiter.Done()
		}(offset)
	}
	p2Waiter.Wait()

	return
}
