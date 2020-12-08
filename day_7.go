package main

import (
	"fmt"
	"strconv"
	"strings"
)

type LuggageStore map[string][]string

var store = make(LuggageStore, 0)

func (l LuggageStore) CanContainShinyBag(n string) bool {
	if luggageContains, ok := l[n]; ok && strings.Contains(strings.Join(luggageContains, " "), "no other bags") {
		return false
	}
	if luggageContains, ok := l[n]; ok && strings.Contains(strings.Join(luggageContains, " "), "shiny gold") {
		return true
	} else {
		var tempCanContain = false
		for _, contains := range luggageContains {
			name := strings.Join(strings.Split(contains, " ")[1:3], " ")
			if l.CanContainShinyBag(name) {
				tempCanContain = true
				break
			}
		}
		return tempCanContain
	}
}

func (l LuggageStore) CountInsideBag(n string) int {
	var tempSum int
	for _, bag := range l[n] {
		data := strings.Split(bag, " ")
		name := strings.Join(data[1:3], " ")
		ct, _ := strconv.Atoi(data[0])
		if name != "other" {
			tempSum += ct + ct*l.CountInsideBag(name)
		}
	}
	return int(tempSum)
}

func (d Day) Day7(i Input) (p1, p2 int) {
	for _, line := range i.Lines() {
		data := strings.Split(line, " bags contain ")
		store[data[0]] = strings.Split(data[1], ", ")
	}

	fmt.Println(store)

	for k := range store {
		if store.CanContainShinyBag(k) {
			p1++
		}
	}

	p2 = store.CountInsideBag("shiny gold")

	return
}
