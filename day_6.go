package main

import (
	"fmt"
	"strings"
)

type Questionaire []string

var questionsAnswered = 0
var questionsEveryoneAnswered = 0

func contains_rune(s []rune, e rune) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}

func ParseQuestionareP1(s string) {
	var seenLetters = []rune{}
	for _, r := range s {
		if !contains_rune(seenLetters, r) && r != ' ' && r != '\n' {
			seenLetters = append(seenLetters, r)
		}
	}
	questionsAnswered += len(seenLetters)
}

func ParseQuestionareP2(s []string) {
	var qea = 0
	var yesMap = make(map[rune]int, 0)
	for _, ans := range s {
		for _, q := range ans {
			yesMap[q]++
		}
	}
	fmt.Println(yesMap, len(s))
	for _, ct := range yesMap {
		if ct == len(s) {
			qea++
		}
	}
	questionsEveryoneAnswered += qea
}

func (d Day) Day6(i Input) (p1 int, p2 int) {
	for _, g := range i.Groups() {
		ParseQuestionareP1(g)
		ParseQuestionareP2(strings.Split(g, "\n"))
	}

	p1 = questionsAnswered
	p2 = questionsEveryoneAnswered

	return
}
