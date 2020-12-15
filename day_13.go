package main

import (
	"fmt"
	"math"
	"strconv"

	"github.com/cheggaaa/pb"
)

func (d Day) Day13(i Input) (p1, p2 int) {
	target, _ := strconv.Atoi(i.Lines()[0])
	// busses := strings.Split(i.Lines()[1], ",")
	bussesInt := []int{41, 37, 379, 23, 13, 17, 29, 557, 19}
	dt := math.MaxInt64
	selectedBus := 0
	for _, b := range bussesInt {
		for i := 0; true; i++ {
			if (i+target)%b == 0 {
				if i < dt {
					dt = i
					selectedBus = b
				}
				break
			}
		}
	}

	p1 = dt * selectedBus

	// busses := strings.Split(strings.ReplaceAll(i.Lines()[1], "x", "1"), ",")
	// p2 = <-Day13_P2_Dyn(busses)
	p2 = <-Day13_P2_Fixed()

	return
}

func Day13_P2_Dyn(busses []string) chan int {
	busOne, _ := strconv.Atoi(busses[0])
	solutionChan := make(chan int)
	timeChan := make(chan int, 1000)
	worker := func(timeChan chan int) {
		for time := range timeChan {
			if time < 0 {
				fmt.Println("what the fuck just happened", time)
			}
			// fmt.Println("checking timestamp", time)
			if isGood, ts := CheckBusLinear(time, len(busses), busses); isGood {
				solutionChan <- ts
			}
		}
	}

	for i := 0; i < 8; i++ {
		go worker(timeChan)
	}

	go func() {
		for i := busOne; ; i += busOne {
			timeChan <- i
		}
	}()
	return solutionChan
}

func Day13_P2_Fixed() chan int {
	var steps = 557
	bar := pb.New(41 * 37 * 379 * 23 * 13 * 17 * 29 * 19)
	solutionChan := make(chan int)
	timeChan := make(chan int, 100000)
	worker := func(timeChan chan int) {
		for time := range timeChan {
			if time%41 == 0 &&
				(time+35)%37 == 0 &&
				(time+41)%379 == 0 &&
				(time+49)%23 == 0 &&
				(time+54)%13 == 0 &&
				(time+58)%17 == 0 &&
				(time+70)%29 == 0 &&
				(time+72)%557 == 0 &&
				(time+91)%19 == 0 {
				solutionChan <- time
			}
		}
	}
	for i := 0; i < 100; i++ {
		go worker(timeChan)
	}
	go func() {
		for i := steps - 72; ; i += steps {
			bar.Increment()
			timeChan <- i
		}
	}()
	bar.Start()
	return solutionChan
}

func CheckBusLinear(time, origLen int, b []string) (bool, int) {
	if len(b) == 0 {
		return true, time - origLen
	}
	bint, _ := strconv.Atoi(b[0])
	if time%bint == 0 {
		return CheckBusLinear(time+1, origLen, b[1:])
	}
	return false, time
}
