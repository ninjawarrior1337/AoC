package main

import (
	"fmt"
	"sort"
	"strconv"
)

type JoltageList []int

func (d Day) Day10(i Input) (p1, p2 int) {
	var jl JoltageList = make(JoltageList, 0)
	for _, l := range i.Lines() {
		joltage, _ := strconv.Atoi(l)
		jl = append(jl, joltage)
	}
	sort.Ints(jl)
	fmt.Println(jl)
	//Part 1
	var onejt = 1
	var threejt = 1
	for i, j := range jl {
		if i+1 < len(jl) {
			if jl[i+1] == j+1 {
				onejt++
			}
			if jl[i+1] == j+3 {
				threejt++
			}
		}
	}
	fmt.Println(onejt)
	fmt.Println(threejt)
	p1 = onejt * threejt
	//Part 2
	wayMap := map[int]int{0: 1}
	for _, j := range jl {
		for i := 1; i <= 3; i++ {
			wayMap[j] += wayMap[j-i]
		}
	}
	fmt.Println(wayMap)
	p2 = wayMap[jl[len(jl)-1]]
	return
}
