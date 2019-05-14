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
                                    // pause for random time, goroutine can do the job at arbitary times
        time.Sleep(time.Duration(rand.Intn(1e3)) * time.Millisecond)
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
/*
Output: no sequence is maintained
Worker:  three
Worker:  one
Worker:  two
{three 81}
{two 59}
{one 47}
{one 25}
{two 56}
{two 94}
{one 62}
{one 28}
{three 11}
{one 37}
{one 95}
{two 28}
{three 47}
{two 87}
{one 90}
{one 41}
{one 87}
{two 29}
*/
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
/*Output: sequence is maintained
Worker:  three
Worker:  one
Worker:  two
{one 87}
{two 59}
{three 81}
{one 56}
{two 25}
{three 40}
{one 62}
{two 74}
{three 45}
{one 28}
{two 95}
{three 58}
{one 28}
{two 88}
{three 87}
{one 8}
{two 31}
{three 41}
*/
```
Now, unless v1 returns, it will be blocked; After v1 returns, v2 will be blocked on receive and so on

#### Joining multiple channels into one
We will continue with the `CreateWorker` method above.
Lets merge all the channels above into one.
```go
// There are 2 ways to do this. One uses select, but difficult to make it Variadic
func MergeUsingSelect(ch1, ch2 <-chan Workload) <-chan Workload {
    merged := make(chan Workload)
    go func() {
        for {
            select {
                case s := <-ch1: merged <- s
                case s := <-ch2: merged <- s
            }
        }
    }(ch)
    return merged
}

// This implementation is Variadic, though select one is cleaner
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

/* Output: No sequence is maintained
Worker:  two
Worker:  one
Worker:  three
{two 81}
{three 81}
{one 47}
{one 25}
{three 56}
{one 94}
{three 62}
{three 28}
{two 11}
{three 37}
{three 95}
{one 28}
{two 47}
{one 87}
{three 90}
{three 41}
*/
```
This is often called FAN-IN in queuing world

#### Round robin load balancing - Synchronize merged channels so that all return equally
Often you want all merged channels to be synchronized so that its load balanced in a round-robin manner.
This is tricky, since you want to merge channels and still use a way to block a channel till the others have yielded
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
    wait chan bool      // This is primary change, each worker will have a single wait channel
}
func (w *Workload) do() {
    w.data = rand.Intn(100)
}

func CreateWorker(name string) <-chan Workload {
    workerWait := make(chan bool)       // This is a single wait channel for this worker
    ch := make(chan Workload)
    go doer(name, workerWait, ch)
    return ch
}

func doer(name string, workerWait chan bool, ch chan<- Workload) {
    fmt.Println("Worker: ", name)
    for i := 0;; i++ {
        w := Workload{name, i, workerWait}
        w.do()
        ch <- w
        time.Sleep(time.Duration(rand.Intn(1e3)) * time.Millisecond) // processing for arbitary time
        workerWait <- true           // Wait to recv till someone external sends on wait[*]
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

        <-msg1.wait         // Send on wait so that the worker can recv and go ahead[*]
        <-msg2.wait
        <-msg3.wait
    }
}
/* Output: All 3 channels send round robin
Worker:  two
Worker:  one
Worker:  three
three  -  47
one  -  87
two  -  81
three  -  25
one  -  56
two  -  94
one  -  28
three  -  62
two  -  11
one  -  37
three  -  95
two  -  28
one  -  47
three  -  87
two  -  90
one  -  41
three  -  87
two  -  29
one  -  37
three  -  85
two  -  13
*/
```

#### Timeouts using Select
```go
func generator(msg string) <-chan string { // returns receive-only channel
    ch := make(chan string)
    go func() { // anonymous goroutine
        for i := 0; ; i++ {
            ch <- fmt.Sprintf("%s %d", msg, i)
            time.Sleep(time.Second)
        }
    }()
    return ch
}

func channelTimeout() {
    ch := generator("Hi!")
    for i := 0; i < 10; i++ {
        select {
        case s := <-ch:
            fmt.Println(s)
        case <-time.After(1 * time.Second): // time.After returns a channel that waits N time to send a message
            fmt.Println("Waited too long!")
            return
        }
    }
}
// Important to note is that every time select is executed, time.After resets to zero
// So, if there nothing to receive on ch, time.After will receive in 1 second and exit

func channelTimeEnd() {
    timeEnd := time.After(5 * time.Second)
    ch := generator("Hi!")
    for i := 0; i < 10; i++ {
        select {
        case s := <-ch:
            fmt.Println(s)
        case <-timeEnd:             // Will send in 5 seconds
            fmt.Println("Waited too long!")
            return
        }
    }
}
// Unlike the channelTimeout, this one ends the loop in 5 seconds since it doesn't reset
```

#### Quit channel
Quite a few cases, instead of timeout or timeEnd, you may want to close the loop deterministically.
For this, create a quit channel and select on it. Whenever you want to quit, just pass something.
The following quits as soon as you pass anything to the quit channel
```go
quit := make(chan bool)
ch := generator("Yo")

for i :=0; i< 10; i++ {
    ch <- fmt.Sprintf("msg : %s", i)
}
quit <- true

// in the loop, where ever you are listening
select {
    case v := <- ch:
        fmt.Println(v)
    case <- quit:
        return
}
```

If you want to do some clean ups before quiting, you can pass something back to the quit channel, like:
```go
quit := make(chan string)
ch := generator("Yo")

for i :=0; i< 10; i++ {
    ch <- fmt.Sprintf("msg : %s", i)
}
quit <- "cleanup"
<-quit
fmt.Println("Cleaned up, quiting now")

// in the loop, where ever you are listening
select {
    case v := <- ch:
        fmt.Println(v)
    case <- quit:
        cleanup()
        quit <- "cleaned"
        return
}
```

#### Collating results from a crawl
Consider a scenario where you are doing api calls to an external system. The external system may return with delays.
```go
struct Data {}
func Source1Crawl(s string) Data {
    // will take arbiraty time to crawl
    return Data{}
}
func Source2Crawl(s string) Data {
    // will take arbiraty time to crawl
    return Data{}
}
func Source3Crawl(s string) Data {
    // will take arbiraty time to crawl
    return Data{}
}
```
Slow and Synchronous
```go
results := []Data
results = append(results, Source1Crawl('term')
results = append(results, Source2Crawl('term')
results = append(results, Source3Crawl('term')
return results
```

Slow and Async
```go
results := []Data
c := make(chan Data)
go func { c <- Source1Crawl('term')}
go func { c <- Source1Crawl('term')}
go func { c <- Source1Crawl('term')}
for i := 0; i < 3; i++ {
    data := <- c
    results = results.append(results, data)
}
return results
```
Slow and Async with timeout
Get whatever returns under 60 milliseconds, ditch everything else and return
```go
// Start channels as above

timeout := time.After(60 * time.Millisecond)

for i := 0;i < 3; i++ {
    select {
        case data := <- c:
            results = results.append(results, data)
        case <- timeout:
            return results
    }
}
return results
```

Fast and Async and Robust
Make multiple requests for the same resource, get whichever is the fastest and return
```go
func GetFirst(s string, crawler func(string) Data) chan Data {
    ch := make(chan Data)
    go func() { ch <- crawler(s)}      // Launch multiple instances of crawler async
    go func() { ch <- crawler(s)}      // keep putting data to a single channel
    go func() { ch <- crawler(s)}
    return <- ch                       // Return which ever comes first
}

func FastRobustCrawl() {
    ch := make(chan Data)
    go func() { ch <- GetFirst('term', Source1Crawl)} // Crawl sources async with the input 'term'
    go func() { ch <- GetFirst('term', Source2Crawl)}
    go func() { ch <- GetFirst('term', Source3Crawl)}

    timeout := time.After(60 * time.Millisecond)

    for i := 0; i < 3; i++ {
        select {
        case result := <-c:                     // Get which ever source returns
            results = append(results, result)
        case <-timeout:                         // Timeout
            fmt.Println("timed out")
            return
        }
    }
    return results
}
```
