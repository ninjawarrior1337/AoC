package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"reflect"
	"strings"
	"time"
)

type Day struct{}
type Input struct {
	Raw string
}

func (i Input) Lines() []string {
	return strings.Split(i.Raw, "\n")
}

func (i Input) Groups() []string {
	return strings.Split(i.Raw, "\n\n")
}

func main() {
	var d Day
	var i Input

	day := os.Args[len(os.Args)-1]
	fmt.Println("Running day " + day)

	data, err := ioutil.ReadFile(fmt.Sprintf("data/%v.txt", day))
	if err != nil {
		panic(err)
	}

	i.Raw = string(data)

	st := time.Now()
	values := reflect.ValueOf(d).MethodByName("Day" + day).Call([]reflect.Value{
		reflect.ValueOf(i),
	})
	fmt.Printf("Part 1 Answer: %v\nPart 2 Answer %v\n", values[0], values[1])
	fmt.Printf("This calculation took: %vμs/%vms/%vs\n", time.Since(st).Microseconds(), time.Since(st).Milliseconds(), time.Since(st).Seconds())
}
