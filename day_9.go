package main

import (
	"math"
	"strconv"
)

func checkArrayHasSum(arr []int, val int) bool {
	for o, oV := range arr {
		for m, mV := range arr {
			if o != m {
				if mV+oV == val {
					return true
				}
			}
		}
	}
	return false
}

func shiftIntSlice(arr []int, val int) []int {
	arr = arr[1:]
	arr = append(arr, val)
	return arr
}

func (d Day) Day9(in Input) (p1, p2 int) {
	checkArr := make([]int, 0)
	for i := 0; i < 25; i++ {
		// Load preamble
		val, _ := strconv.Atoi(in.Lines()[i])
		checkArr = append(checkArr, val)
	}
	// Part 1
	shortInput := in.Lines()[25:]
	for i := 0; i < len(shortInput); i++ {
		num, _ := strconv.Atoi(shortInput[i])

		if !checkArrayHasSum(checkArr, num) {
			p1 = num
			break
		}
		// fmt.Println(checkArr)
		checkArr = shiftIntSlice(checkArr, num)
	}
	// Part 2
	var solutionChan = make(chan int)
	for i := 0; i < len(in.Lines()); i++ {
		go func(startIdx int) {
			var tempSum = 0
			currLargest := 0
			currSmallest := math.MaxInt64
			for _, l := range in.Lines()[startIdx:] {
				lInt, _ := strconv.Atoi(l)
				if lInt > currLargest {
					currLargest = lInt
				}
				if lInt < currSmallest {
					currSmallest = lInt
				}
				tempSum += lInt
				if tempSum == p1 {
					solutionChan <- currLargest + currSmallest
				}
			}
		}(i)
	}
	p2 = <-solutionChan
	return
}
