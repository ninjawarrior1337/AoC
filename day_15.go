package main

import (
	"github.com/cheggaaa/pb"
)

func (d Day) Day15(i Input) (p1, p2 int) {
	starting := []int{9, 12, 1, 4, 17, 0, 18}
	seen := map[int]int{}
	bar := pb.StartNew(30000000)
	bar.Start()
	//Load values into seen map
	for i, v := range starting {
		seen[v] = i
	}
	for i := len(starting); i < 30000000; i++ {
		bar.Increment()
		lastValue := starting[i-1]
		if v, ok := seen[lastValue]; ok {
			starting = append(starting, (i)-(v+1))
		} else {
			starting = append(starting, 0)
		}

		seen[lastValue] = i - 1
	}
	bar.Finish()

	p1 = starting[2020-1]
	p2 = starting[len(starting)-1]

	return
}
