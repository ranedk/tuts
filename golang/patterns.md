# Basic concurrency patters in GO

## Generator Worker
Suppose you want workers for a particular task, the easy way is to do is to make the worker create a channel and give it back to the main distributor.
```go
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
        time.Sleep(1 * time.Second)
    }
}

func main() {
    ch1 := CreateWorker("one")
    ch2 := CreateWorker("two")
    ch3 := CreateWorker("three")

    for {
        select {
            case v1 := <-ch1:
                fmt.Println(v1)
            case v2 := <-ch2:
                fmt.Println(v2)
            case v3 := <-ch3:
                fmt.Println(v3)
        }
    }
}

```
