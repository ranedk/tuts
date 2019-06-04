# Google I/O 2013 - Advanced Go Concurrency Patterns
https://www.youtube.com/watch?v=QDDwwePbDtw

## Key take aways

### Interfaces
- Use interfaces for the same reason you use in other language - Polymorphism
    - Figure out parts of code that have similar behaviour
    - Create an interface for that behaviour
    - Write hard implementations of all those parts which share the interface
    - Glue together

    - In terms of structuring it, Interfaces and methods which are implemented on the interface must be in one file, while concrete implementations should use those interfaces.

### Race conditions
- When there is a pointer of a struct inside a function that is being run in multiple go routines
    - Multiple go routines are changing the same pointer struct
- When one pointer of a struct is being passed to multiple go routines and each may change it.
- When multiple pointers of the same instance of the struct are accessed in multiple goroutines

NOTE: In Go, copying small structs is very fast and doesn't involve a lot of overhead. So its better
to make things immutable by always copying structs. Only when the structs are very large, one should
try to pass pointers, or you are sure a struct is only managed within a single goroutine.

NOTE: Make functions synchronous, so that you can call it as a goroutine. If you implement a function
with inbuilt asychronousity, it will be difficult to manage.

NOTE: Do not copy a value of type `T` if its methods are associated with the pointer type `*T`

NOTE: Communication is better than trying to change struct states.. meaning... if there is a struct
which maintains a state based on which an action needs to be performed, its always better to instead
create a channel for this communication. So instead of changing the state, send into a channel, which
can be received and acted upon. This minimised race conditions

NOTE: Interestingly, select doesn't block a channel if the channel is nil `v := <-ch` will not block
is `ch` is `nil`. To way to use this is to make the channel nil if you don't want to block it.

#### Power of Select loop
For a particular task there should be one and only one `for select case` loop. The `for select case`
loop can manage all kinds of state management of the task:
- When to start the app
- When to stop the app
- When to receive the app
- When to start cleaning up
- What to do when there is an error

```go
func (s *stateStruct) loop() {      // Main loop should have access to the pointer of the state struct
    for {
        select {
            case <- start:
                s.StartApp()
            case err := <- errors:
                s.HandleError()
            case c := <-quit:
                if c == "cleanup" {
                    s.cleanUp()
                    quit <- "quit"
                }
                if c == "quit" {
                    s.Quit()
                }
        }
    }
}
```

Its a good practice to NOT make anything blocking(for a long time) inside the `for select case` loop,
in case something is blocking, put it in a go routine and communicate with channels.

## Race detection

Go has tooling to figure if there is a race condition or a deadlock
```bash
$ go build -race mycmd
```

- Do not use `PANIC` for error handling
- Do not have goroutines running for ever (generally), there will be exceptions
