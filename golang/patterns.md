# Basic concurrency patters in GO

## Generator Worker
Suppose you have generator function, which generates data, processes and returns
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
    w.data = rand.Intn(100)         // This could be a data generator or some task
                                    // which returns data from a service
}

func CreateWorker(name string) <-chan Workload {
    ch := make(chan Workload)
    go doer(name, ch)
    return ch
}

func doer(name string, ch chan<- Workload) {
    fmt.Println("Worker: ", name)
    for i := 0;; i++ {
        w := Workload{name, i}      // Create some workload
        w.do()                      // process the workload
        ch <- w                     // pass processed workload on channel
        time.Sleep(1 * time.Second)
    }
}

func main() {
    ch1 := CreateWorker("one")
    ch2 := CreateWorker("two")
    ch3 := CreateWorker("three")

    for {
        select {                    // which ever workload finishes first returns
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

This will start 3 workers, which will keep generating data and keep giving it to main.
Because of the `select case` statement, which ever channel has data return to main and nobody is waiting for another thread.

If you want the workers to be locked on each other, you can use:
```go
for {
    v1 := <-ch1
    fmt.Println(v1)

    v2 := <-ch2
    fmt.Println(v2)

    v3 := <-ch3:
    fmt.Println(v3)
}
```
Now, unless v1 returns, it will be blocked; After v1 returns, v2 will be blocked on receive and so on

#### Multiplexing - Joining multiple streams into one
We will continue with the `CreateWorker` method above.
Lets merge all the channels above into one.
```go
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

// Usage:
merged := Merge(ch1, ch2, ch3)
for {
    v := <-merged
    fmt.Println(v)
}
```



