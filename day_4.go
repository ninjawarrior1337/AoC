package main

import (
	"fmt"
	"log"
	"regexp"
	"strconv"
	"strings"
)

type Passport map[string]string

var passports = make([]Passport, 0)
var reqFeilds = []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

func ParsePassport(s string) {
	var p Passport = make(Passport)
	attrs := strings.Split(s, " ")

	p["ps"] = s

	for _, attrKV := range attrs {
		attrArr := strings.Split(attrKV, ":")
		key := attrArr[0]
		val := attrArr[1]
		p[key] = val
	}
	fmt.Println(p.IsValidP1())
	passports = append(passports, p)
}

func (p Passport) IsValidP1() bool {
	for _, f := range reqFeilds {
		if _, ok := p[f]; !ok {
			return false
		}
	}
	return true
}

func (p Passport) IsValidP2() bool {
	if !p.AreYrsValid() {
		log.Printf("Failed passport (years invalid): %v", p)
		return false
	}
	if !p.IsEyeColorValid() {
		log.Printf("Failed passport (eye invalid): %v", p["ps"])
		return false
	}
	if !p.IsHairColorValid() {
		log.Printf("Failed passport (hair invalid): %v", p["ps"])
		return false
	}
	if !p.IsIdValid() {
		log.Printf("Failed passport (pid invalid): %v", p["ps"])
		return false
	}
	if !p.IsHeightValid() {
		log.Printf("Failed passport (height invalid): %v", p["ps"])
		return false
	}
	return true
}

func (p Passport) AreYrsValid() bool {
	if p["byr"] == "" && p["iyr"] == "" && p["eyr"] == "" {
		return false
	}
	byr, _ := strconv.Atoi(p["byr"])
	iyr, _ := strconv.Atoi(p["iyr"])
	eyr, _ := strconv.Atoi(p["eyr"])
	return byr >= 1920 && byr <= 2002 && iyr >= 2010 && iyr <= 2020 && eyr >= 2020 && eyr <= 2030
}

func (p Passport) IsHeightValid() bool {
	if strings.Contains(p["hgt"], "in") {
		ht, _ := strconv.Atoi(strings.TrimSuffix(p["hgt"], "in"))
		if ht >= 59 && ht <= 76 {
			return true
		}
	} else if strings.Contains(p["hgt"], "cm") {
		ht, _ := strconv.Atoi(strings.TrimSuffix(p["hgt"], "cm"))
		if ht >= 150 && ht <= 193 {
			return true
		}
	}
	return false
}

func (p Passport) IsHairColorValid() bool {
	rp := regexp.MustCompile("^#[a-f0-9]{6}$")
	return rp.MatchString(p["hcl"])
}

func (p Passport) IsEyeColorValid() bool {
	rp := regexp.MustCompile("^(amb|blu|brn|gry|grn|hzl|oth)$")
	return rp.MatchString(p["ecl"])
}

func (p Passport) IsIdValid() bool {
	rp := regexp.MustCompile("^[0-9]{9}$")
	return rp.MatchString(p["pid"])
}

func (d Day) Day4(lines []string) (p1 int, p2 int) {
	currLines := make([]string, 0)
	for _, l := range lines {
		if len(l) > 0 {
			currLines = append(currLines, l)
		} else if len(currLines) > 0 {
			ParsePassport(strings.Join(currLines, " "))
			currLines = []string{}
		}
	}
	// Part 1
	for _, p := range passports {
		if p.IsValidP1() {
			p1++
		}
	}
	//Part 2
	for _, p := range passports {
		if p.IsValidP2() {
			p2++
		}
	}
	return
}
