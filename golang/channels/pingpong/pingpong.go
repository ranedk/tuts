package main

import (
    "fmt"
    "time"
)

type Ball struct {hits int}

func main() {
    table := make(chan *Ball)
    go player("ping", table)
    go player("pong", table)

    table <- new(Ball)
    time.Sleep(5 * time.Second)
    ball := <-table
    fmt.Println("Main catches ball", ball.hits)
    panic("PANIC")
}

func player(name string, table chan *Ball) {
    for {
        ball := <-table
        ball.hits++
        fmt.Println("Caught by ", name, ball.hits)
        sleepTime := 1 * time.Second
        fmt.Println("Sleeping for ", sleepTime)
        time.Sleep(sleepTime)
        table <- ball
    }
}
