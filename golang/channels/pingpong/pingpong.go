package main

import (
    "fmt"
    "time"
    "math/rand"
)

type Ball struct {hits int}

func main() {
    table := make(chan *Ball)
    go player("ping", table)
    go player("pong", table)

    table <- new(Ball)
    time.Sleep(15 * time.Second)
    ball := <-table
    fmt.Println("Main catches ball", ball.hits)
    panic("PANIC")
}

func player(name string, table chan *Ball) {
    for {
        ball := <-table
        ball.hits++
        fmt.Println("Caught by ", name, ball.hits)
        sleepTime := time.Duration(rand.Intn(1000)) * time.Millisecond
        fmt.Println("Sleeping for ", sleepTime)
        time.Sleep(sleepTime)
        table <- ball
    }
}
