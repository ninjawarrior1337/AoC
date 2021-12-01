package main

import (
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

func (d Day) Day3(i Input) (p1 int, p2 int) {
	tMap := make(TobagganMap)
	for i, l := range i.Lines() {
		tMap.LoadRow(i, l)
	}

	// Part 1
	for x, y := 0, 0; y < len(tMap); y++ {
		log.Printf("checking row %v", y)
		if tMap.IsTreeAtCoord(x, y) {
			p1++
		}
		x += 3
	}

	// Part 2
	p2 = 1
	var p2Waiter sync.WaitGroup
	var mutex = &sync.Mutex{}
	var p2Offsets = [][]int{
		{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2},
	}
	for _, offset := range p2Offsets {
		p2Waiter.Add(1)
		go func(offset []int) {
			var treeCounter = 0
			for x, y := 0, 0; y < len(tMap); y += offset[1] {
				if tMap.IsTreeAtCoord(x, y) {
					treeCounter++
				}
				x += offset[0]
			}
			mutex.Lock()
			p2 *= treeCounter
			mutex.Unlock()
			p2Waiter.Done()
		}(offset)
	}
	p2Waiter.Wait()

	return
}
