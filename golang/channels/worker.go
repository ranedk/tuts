package main

import (
    "fmt"
    "time"
    "math/rand"
)

type Workload struct {
    name string
    data int
}
func (w *Workload) do() {
    w.data = rand.Intn(100)
}

func CreateWorker(name string) <-chan Workload {
    ch := make(chan Workload)
    go doer(name, ch)
    return ch
}

func doer(name string, ch chan<- Workload) {
    fmt.Println("Worker: ", name)
    for i := 0;; i++ {
        w := Workload{name, i}
        w.do()
        ch <- w
        time.Sleep(time.Duration(rand.Intn(1e3)) * time.Millisecond)
    }
}

func Merge(chs ...<-chan Workload) <-chan Workload {
    merged := make(chan Workload)
    for _, ch := range chs {
        go func(c <-chan Workload) {
            for {
                merged <- <-c
            }
        }(ch)
    }
    return merged
}

func main() {
    ch1 := CreateWorker("one")
    ch2 := CreateWorker("two")
    ch3 := CreateWorker("three")

    // Get data as its available
    /*for {
        select {
            case v1 := <-ch1:
                fmt.Println(v1)
            case v2 := <-ch2:
                fmt.Println(v2)
            case v3 := <-ch3:
                fmt.Println(v3)
        }
    }*/

    // Locked: Data is processed one after the other
    /*for {
        v1 := <-ch1
        fmt.Println(v1)

        v2 := <-ch2
        fmt.Println(v2)

        v3 := <-ch3
        fmt.Println(v3)
    }*/

    merged := Merge(ch1, ch2, ch3)
    for {
        v := <-merged
        fmt.Println(v)
    }
}

