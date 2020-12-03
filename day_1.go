package main

import (
	"strconv"
)

func (d Day) Day1(lines []string) (p1 int, p2 int) {
	report := make([]int, 0)

	for _, l := range lines {
		i, _ := strconv.Atoi(l)
		report = append(report, i)
	}

	for o, oV := range report {
		for m, mV := range report {
			if o != m {
				if mV+oV == 2020 {
					p1 = oV * mV
				}
			}
			for i, iV := range report {
				if o != i && i != m && o != m {
					if oV+iV+mV == 2020 {
						p2 = oV * iV * mV
					}
				}
			}
		}
	}
	return
}
