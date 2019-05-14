package main

import (
    "fmt"
    "time"
    "math/rand"
)

type Workload struct {
    name string
    data int
    wait chan bool
}
func (w *Workload) do() {
    w.data = rand.Intn(100)
}

func CreateWorker(name string) <-chan Workload {
    channelWait := make(chan bool)
    ch := make(chan Workload)
    go doer(name, channelWait, ch)
    return ch
}

func doer(name string, channelWait chan bool, ch chan<- Workload) {
    fmt.Println("Worker: ", name)
    for i := 0;; i++ {
        w := Workload{name, i, channelWait}
        w.do()
        ch <- w
        time.Sleep(time.Duration(rand.Intn(1e3)) * time.Millisecond)
        channelWait <- true
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
    time.Sleep(1 * time.Second)

    ch := Merge(ch1, ch2, ch3)
    for i := 0; i < 10; i++ {
        msg1 := <-ch
        fmt.Println(msg1.name, " - ", msg1.data)

        msg2 := <-ch
        fmt.Println(msg2.name, " - ", msg2.data)

        msg3 := <-ch
        fmt.Println(msg3.name, " - ", msg3.data)

        <-msg1.wait
        <-msg2.wait
        <-msg3.wait
    }
}

