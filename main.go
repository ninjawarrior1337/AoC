package main

import (
	"bufio"
	"fmt"
	"os"
	"reflect"
	"time"
)

type Day struct{}

func main() {
	var d Day

	day := os.Args[len(os.Args)-1]
	fmt.Println("Running day " + day)

	f, _ := os.Open(fmt.Sprintf("data/%v.txt", day))
	defer f.Close()
	s := bufio.NewScanner(f)

	lines := make([]string, 0)
	for s.Scan() {
		lines = append(lines, s.Text())
	}

	st := time.Now()
	values := reflect.ValueOf(d).MethodByName("Day" + day).Call([]reflect.Value{
		reflect.ValueOf(lines),
	})
	fmt.Printf("Part 1 Answer: %v\nPart 2 Answer %v\n", values[0], values[1])
	fmt.Printf("This calculation took: %vμs\n", time.Since(st).Microseconds())
}
