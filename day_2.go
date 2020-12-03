package main

import (
	"bufio"
	"strconv"
	"strings"
)

type Requirement struct {
	Lower int
	Upper int
	Char  string
}

var passwords = make([]string, 0)
var requirements = make([]Requirement, 0)

func parseRequirement(req string) Requirement {
	var r Requirement
	var l = strings.Split(req, " ")

	lower := strings.Split(l[0], "-")[0]
	upper := strings.Split(l[0], "-")[1]
	r.Upper, _ = strconv.Atoi(upper)
	r.Lower, _ = strconv.Atoi(lower)
	r.Char = l[1]
	return r
}

func passwordDoesPassPt1(r Requirement, p string) bool {
	ct := strings.Count(p, r.Char)
	if ct >= r.Lower && ct <= r.Upper {
		return true
	}
	return false
}

func passwordDoesPassPt2(r Requirement, p string) bool {
	isSlotOneValid := string(p[r.Lower-1]) == r.Char
	isSlowTwoValid := string(p[r.Upper-1]) == r.Char
	return (isSlotOneValid || isSlowTwoValid) && !(isSlotOneValid && isSlowTwoValid)
}

func (d Day) Day2(s *bufio.Scanner) (p1 int, p2 int) {
	for s.Scan() {
		t := s.Text()
		req := strings.Split(t, ": ")[0]
		pass := strings.Split(t, ": ")[1]
		passwords = append(passwords, pass)
		requirements = append(requirements, parseRequirement(req))
	}
	for i, p := range passwords {
		if passwordDoesPassPt1(requirements[i], p) {
			p1++
		}
		if passwordDoesPassPt2(requirements[i], p) {
			p2++
		}
	}
	return
}
