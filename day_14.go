package main

import (
	"fmt"
	"strconv"
	"strings"
)

func applyMask(mask string, data string) string {
	var finalString = []rune{}
	for i, c := range mask {
		switch c {
		case 'X':
			finalString = append(finalString, rune(data[i]))
		case '1':
			finalString = append(finalString, '1')
		case '0':
			finalString = append(finalString, '0')
		}
	}
	return string(finalString)
}

func applyMaskP2(mask, data string) string {
	var finalString = []rune{}
	for i, c := range mask {
		switch c {
		case 'X':
			finalString = append(finalString, 'X')
		case '1':
			finalString = append(finalString, '1')
		case '0':
			finalString = append(finalString, rune(data[i]))
		}
	}
	return string(finalString)
}

func generateAllMaskPartials(maskedDataSlice []string) []string {
	temp := []string{}
	for _, maskedData := range maskedDataSlice {
		if strings.ContainsAny(maskedData, "X") {
			temp = append(temp, strings.Replace(maskedData, "X", "1", 1))
			temp = append(temp, strings.Replace(maskedData, "X", "0", 1))
		}
	}

	return temp
}

func generateAllMaskValues(maskedDataSlice string) []string {
	countXs := strings.Count(maskedDataSlice, "X")
	temp := []string{maskedDataSlice}
	for i := 0; i < countXs; i++ {
		temp = generateAllMaskPartials(temp)
	}
	return temp
}

func (d Day) Day14(i Input) (p1, p2 int) {
	var storage = make(map[string]int64)
	var storagep2 = make(map[string]int)
	currMask := ""
	for _, l := range i.Lines() {
		parts := strings.Split(l, " = ")
		switch parts[0] {
		case "mask":
			currMask = parts[1]
		default:
			addr := strings.TrimLeft(strings.TrimRight(parts[0], "]"), "mem[")
			data, _ := strconv.Atoi(parts[1])
			newValStr := applyMask(currMask, fmt.Sprintf("%036b", data))
			storage[addr], _ = strconv.ParseInt(newValStr, 2, 64)
		}
	}
	for _, v := range storage {
		p1 += int(v)
	}

	for _, l := range i.Lines() {
		parts := strings.Split(l, " = ")
		switch parts[0] {
		case "mask":
			currMask = parts[1]
		default:
			addr, _ := strconv.ParseInt(strings.TrimLeft(strings.TrimRight(parts[0], "]"), "mem["), 10, 64)
			data, _ := strconv.Atoi(parts[1])
			newAddrStr := applyMaskP2(currMask, fmt.Sprintf("%036b", addr))
			wAddrs := generateAllMaskValues(newAddrStr)
			for _, addr := range wAddrs {
				storagep2[addr] = data
			}
		}
	}

	for _, v := range storagep2 {
		p2 += int(v)
	}
	// fmt.Println(generateAllMaskValues("XX"))
	return
}
