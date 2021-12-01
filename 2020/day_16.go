package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

type TicketField struct {
	Field string
	Min1  int
	Max1  int
	Min2  int
	Max2  int
}

type Ticket []int

func parseRestriction(i string) {
	var r TicketField

	regex := regexp.MustCompile(`(.+): (\d+)-(\d+) or (\d+)-(\d+)`)
	match := regex.FindAllStringSubmatch(i, -1)[0]
	r.Field = match[1]
	r.Min1, _ = strconv.Atoi(match[2])
	r.Max1, _ = strconv.Atoi(match[3])
	r.Min2, _ = strconv.Atoi(match[4])
	r.Max2, _ = strconv.Atoi(match[5])
	ticketFields = append(ticketFields, r)
}

func parseTicket(i string) Ticket {
	var t Ticket
	for _, num := range strings.Split(i, ",") {
		numInt, _ := strconv.Atoi(num)
		t = append(t, numInt)
	}
	return t
}

func (t Ticket) VerifyAllFields(tfs []TicketField) (bool, int) {
	for _, tn := range t {
		passedOne := false
		for _, tf := range tfs {
			if (tf.Min1 <= tn && tn <= tf.Max1) || (tf.Min2 <= tn && tn <= tf.Max2) {
				passedOne = true
				break
			}
		}
		if !passedOne {
			return false, tn
		}
	}
	return true, 0
}

func (t Ticket) VerifySpecificField(fIdx int, tf TicketField) bool {
	tn := t[fIdx]
	if (tf.Min1 <= tn && tn <= tf.Max1) || (tf.Min2 <= tn && tn <= tf.Max2) {
		return true
	}
	return false
}

func FilterTickets(tl []Ticket) (f []Ticket) {
	for _, t := range tl {
		if ok, _ := t.VerifyAllFields(ticketFields); ok {
			f = append(f, t)
		}
	}
	return
}

func RemoveElementInt(arr []int, num int) []int {
	idx := -1
	for i, v := range arr {
		if v == num {
			idx = i
			break
		}
	}

	if idx == -1 {
		return arr
	}

	arr[idx] = arr[len(arr)-1]

	return arr[:len(arr)-1]
}

var ticketFields = []TicketField{}
var nearbyTickets = []Ticket{}

func (d Day) Day16(i Input) (p1, p2 int) {
	g := i.Groups()
	for _, restrict := range strings.Split(g[0], "\n") {
		parseRestriction(restrict)
	}
	for _, nearby := range strings.Split(g[2], "\n")[1:] {
		nearbyTickets = append(nearbyTickets, parseTicket(nearby))
	}

	failedNumbers := []int{}

	for _, t := range nearbyTickets {
		if ok, num := t.VerifyAllFields(ticketFields); !ok {
			failedNumbers = append(failedNumbers, num)
		}
	}

	for _, num := range failedNumbers {
		p1 += num
	}

	filteredTickets := FilterTickets(nearbyTickets)

	myticket := Ticket([]int{53, 101, 83, 151, 127, 131, 103, 61, 73, 71, 97, 89, 113, 67, 149, 163, 139, 59, 79, 137})
	fieldMap := map[string][]int{}

	for i := range ticketFields {
		for _, tf := range ticketFields {
			passed := true
			for _, t := range filteredTickets {
				if !t.VerifySpecificField(i, tf) {
					passed = false
					break
				}
			}
			if passed {
				fieldMap[tf.Field] = append(fieldMap[tf.Field], i)
			}
		}
	}

	for k, v := range fieldMap {
		fmt.Println(k, v)
	}

	fmt.Println()

	for i := 0; i < 100; i++ {
		for currField, v := range fieldMap {
			if len(v) == 1 {
				// fmt.Println(currField, v)
				valueToRemove := v[0]
				for k := range fieldMap {
					if k != currField {
						fieldMap[k] = RemoveElementInt(fieldMap[k], valueToRemove)
					}
				}
			}
		}
	}

	fmt.Println()

	for k, v := range fieldMap {
		fmt.Println(k, v)
	}

	p2 = 1
	for k, v := range fieldMap {
		if strings.Contains(k, "departure") {
			p2 *= myticket[v[0]]
		}
	}

	return
}
