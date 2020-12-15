package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/signal"
	"reflect"
	"runtime/pprof"
	"strings"
	"syscall"
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

var cpuprofile = flag.String("p", "", "write cpu profile to file")
var day = flag.String("d", "", "execute which day")

func main() {
	sigs := make(chan os.Signal, 1)
	answers := make(chan []reflect.Value)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	flag.Parse()

	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal(err)
		}
		defer f.Close()
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	var d Day
	var i Input

	fmt.Println("Running day " + *day)

	data, err := ioutil.ReadFile(fmt.Sprintf("data/%v.txt", *day))
	if err != nil {
		panic(err)
	}

	i.Raw = string(data)

	st := time.Now()
	go func() {
		answers <- reflect.ValueOf(d).MethodByName("Day" + *day).Call([]reflect.Value{
			reflect.ValueOf(i),
		})
	}()

	select {
	case <-sigs:
		fmt.Println("execution stopped")
	case a := <-answers:
		fmt.Printf("Part 1 Answer: %v\nPart 2 Answer %v\n", a[0], a[1])
		fmt.Printf("This calculation took: %vμs/%vms/%vs\n", time.Since(st).Microseconds(), time.Since(st).Milliseconds(), time.Since(st).Seconds())
	}
}
