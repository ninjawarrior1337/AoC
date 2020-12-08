package main

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

type OpCode string

const (
	Acc OpCode = "acc"
	Jmp OpCode = "jmp"
	Nop OpCode = "nop"
)

type Instruction struct {
	OpCode OpCode
	Value  int
}

type Program []Instruction

func (p Program) FlipOp(idx int) {
	if p[idx].OpCode == Jmp {
		p[idx].OpCode = Nop
	} else {
		p[idx].OpCode = Jmp
	}
}

func (p Program) Run() (ret int) {
	var accumVar int
	for i := 0; i < len(p); i++ {
		ins := p[i]
		switch ins.OpCode {
		case Acc:
			accumVar += ins.Value
		case Nop:
			continue
		case Jmp:
			i += (ins.Value - 1)
		}
	}
	ret = accumVar
	return
}

func (p Program) RunWithLoopDetection() (ret int) {
	var accumVar int
	var seenIdx = make([]int, 0)
	for i := 0; i < len(p); i++ {
		ins := p[i]
		if contains_int(seenIdx, i) {
			return accumVar
		} else {
			seenIdx = append(seenIdx, i)
		}
		switch ins.OpCode {
		case Acc:
			accumVar += ins.Value
		case Nop:
			continue
		case Jmp:
			i += (ins.Value - 1)
		}
	}
	ret = accumVar
	return
}

func ParseInstruction(is string) Instruction {
	var i Instruction
	data := strings.Split(is, " ")
	valTmp, _ := strconv.Atoi(data[1])
	code, val := OpCode(data[0]), valTmp
	i.Value = val
	i.OpCode = code
	fmt.Println(i)
	return i
}

func (p Program) FindJmpOrNop() (locList []int) {
	for idx, i := range p {
		if i.OpCode == Jmp || i.OpCode == Nop {
			locList = append(locList, idx)
		}
	}
	return
}

func (d Day) Day8(i Input) (p1, p2 int) {
	program := make(Program, 0)

	for _, l := range i.Lines() {
		fmt.Printf("parsing %v\n", l)
		program = append(program, ParseInstruction(l))
	}

	//Part 1
	p1 = program.RunWithLoopDetection()

	// Get ready for some brute forcing
	var foundChan = make(chan int)
	fmt.Println(program.FindJmpOrNop())
	for _, i := range program.FindJmpOrNop() {
		go func(replaceIdx int) {
			var tempProgram Program
			var retChan = make(chan int)
			tempProgram = append(tempProgram, program[:]...)
			tempProgram.FlipOp(replaceIdx)
			go func() {
				retChan <- tempProgram.Run()
			}()
			select {
			case <-time.After(1 * time.Second):
			case ret := <-retChan:
				foundChan <- ret
			}
		}(i)
	}
	p2 = <-foundChan
	return
}
