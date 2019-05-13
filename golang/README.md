# Golang

## Why and where use Go?
Brilliant for I/O related tasks, websockets, http-crawlers etc. Very few keywords (you can learn the basics in a day). Concurrency with channels is a breeze and easy to setup. Compiler helps in finding deadlocks and concurency issues. (not as good as Rust, but the overhead to learn this is not very high). Very efficient for data transformations. So if you are writing a data pipeline with transformations and I/O, this is the language. Great fit for your first statically typed language.

Basic visual code setup is good enough for efficient coding. No need to anything Jetbrains.

## The Bad
Best practices and some corners are difficult to get right and will require experience.

## Lets begin

### Installation:
```bash
$ sudo tar -xvf go1.12.2.linux-amd64.tar.gz
# (get the latest version from https://golang.org/dl/)

$ sudo mv go /usr/local

$ export GOROOT=/usr/local/go
# this is where all go binaries and compiler go

$ export GOPATH=$HOME/Projects/Go
# this is where go libraries and dependencies go

# put this in your zshrc (or bashrc)

$ go version  // verify installation
$ go env  // verify installation
```

### Starting a project
```bash
$ cd /home/user/my-working-directory
$ mkdir hello

$ go mod init github.com/ranedk/hello
# initialize a go package, creates a file go.mod

# installing go dependencies
$  go get github.com/SlyMarbo/rss
# Will install the package in $GOPATH and make an entry in go.mod
```

### Basics
Create a file names hello.go
```go
package main

import (
    "fmt"
    "time"
    "math/rand"  // math is the folder name, rand is the package name
)

func main() {
    fmt.Println("Hello, 世界")
    fmt.Println("The time is", time.Now())
}
```
```shell
$ go build

$ ./hello
Hello, 世界
The time is 2019-05-09 19:01:55.717598856 +0530 IST m=+0.000505962
```

- All public functions, which can be used outside the module start with CAPITAL letters

#### Functions
```go
func add(x int, y int) int {    // can be shortened to func add(x, y int): int {
    return x + y
}

// function can return more than one value
func swap(x, y string) (string, string) {
    return y, x
}

a, b := swap("hello", "world")  // since a and b have not been defined yet,
                                // use :=, this infers types automatically

x := 10
y := 20

x = x + y      // := not required since x is already defined

// Named returned values (this is confusing, don't use)
func split(sum int) (x, y int) {    // find x and y in the function definition
                                    //and returns them without explicit call
    x = sum * 4 / 9
    y = sum - x
    return
}

// Declaring, before using (rarely used)
var i int
i = 10      // := not required since i is already declared

var i, j, k int = 1, 2 3    // nice to have, not impressive


var i int       // by default, value of i is 0
var s string    // by default, value of s is ""
var b bool      // by default, value of b is false
```
Variadic functions - functions which take any number of parameters:
```go
func sum(nums ...int) {         // like python *args
    fmt.Print(nums, " ")
    total := 0
    for _, num := range nums {
        total += num
    }
    fmt.Println(total)
}

sum(1, 2)
sum(1, 2, 3)
sum(1, 2, 3, 4, 5)

nums := []int{1, 2, 3, 4}
sum(nums...)                   // like python *arr
```
#### Types
bool: true/false

string: "Hello world", `hello world` (backticks allow multi-line strings)
character: 'a'

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // alias for uint8

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128    (e.g. -5 + 12i)

- Constants
const Pi = 3.147    // constants dont need :=

#### Controls
```go

// For loops

func sumloop1() {
    sum := 0
    for i := 0; i < 10; i++ {
        sum += i
    }
    fmt.Println(sum)
}

// for loop like while

func sumloop2() {
    sum := 1
    for sum < 1000 {
        sum += sum
    }
    fmt.Println(sum)
}

// for loop like while(true)

func infiniteLoop() {
    for {
        // till we find a break
    }
}


// If conditions

func cond1(x) {
    if x < 0 {
        return sqrt(-x) + "i"
    }
}

func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {   // v is scoped only inside
                                        // if and else statement
        return v
    } else {
        fmt.Printf("%g >= %g\n", v, lim)
    }
    return lim
}

// Idiomatic usage
// if <expression>; condition {
//     code
// } e.g.
if t, ok := number.IsPositive(); ok {
    fmt.Println("Found positive: ", number)
}

// switch case (break is implicit as soon as one case matches)

func PrintOS() {
    fmt.Print("Go runs on ")
    switch os := runtime.GOOS; os {
    case "darwin":
        fmt.Println("OS X.")
    case "linux":
        fmt.Println("Linux.")
    default:
        // freebsd, openbsd,
        // plan9, windows...
        fmt.Printf("%s.\n", os)
    }
}

// switch without condition is better if-else-elseif

func main() {
    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("Good morning!")
    case t.Hour() < 17:
        fmt.Println("Good afternoon.")
    default:
        fmt.Println("Good evening.")
    }
}

// Defer statement (run a statement when the function exits)

func helloWorld() {
    defer fmt.Println("world")

    fmt.Println("hello")
}
```

#### Struct & Pointers
```go

// Like C
var p *int      // integer pointer
i = 10
p = &i
q := &i     // implicit, infered pointer


type Vertex struct {
    X int
    Y int
}
v1 := Vertex{1, 2}
v2 := Vertex{X:1, Y:2}

fmt.Println(v1, v2)
// prints complete v1 and v2 nicely (beautiful for debugging)

v1.X = 100      // Access struct params

p1 := &v1       // pointer to struct

Xvalue := (*p1).X   // The old and painful C like way to access

Xvalue := p1.X
// Go is awesome, access works in the same way with values or pointers
```

#### Arrays
```go
func basicUsage() {
    var a [2]string
    a[0] = "Hello"
    a[1] = "World"
    fmt.Println(a[0], a[1])
    fmt.Println(a)

    primes := [6]int{2, 3, 5, 7, 11, 13}
    fmt.Println(primes)
}

// Slices

primes := [6]int{2, 3, 5, 7, 11, 13}
var s []int = primes[1:4]       // this refers to the original array, changing
                                // values in s, will change value in primes

// Like python, slice has lower_bound:upper_bound,
// which default to 0:length_of_array

var MySlice = []int{1, 2, 3, 4, 5}  // This is a slice since length
                                    // is not mentioned, but is also an array

// Array of structs
s := []struct {
    i int
    b bool
}{
    {2, true},
    {3, false},
    {5, true},
    {7, true},
    {11, false},
    {13, true},
}

// Complicated Slice operations

package main

import "fmt"

func main() {
    s := []int{2, 3, 5, 7, 11, 13}
    printSlice(s)       // len=6 cap=6 [2 3 5 7 11 13]

    // Slice the slice to give it zero length.
    s = s[:0]           // now, length is zero, but s still points to original [0], so capacity is 6
    printSlice(s)       // len=0 cap=6 []

    // Extend its length.
    s = s[:4]           // now, length is 4, s points to original [0], so capacity is 6
    printSlice(s)       // len=4 cap=6 [2 3 5 7]

    // Drop its first two values.
    s = s[2:]           // now, length is 2, s points to original [2], so capacity is 6 - 2 = 4
    printSlice(s)       // len=2 cap=4 [5 7]

    s = s[:4]           // now, length is 4, s points to original [2], so capacity is 4
    printSlice(s)       // len=4 cap=4 [5 7 11 13]
}

func printSlice(s []int) {
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}

// if Length and Capacity of slice is 0, then slice is nil
var s []int
s == nil    // true

// Creating a dynamically sized array/slice
c := make([]int, 5)         // c = [0, 0, 0, 0, 0]
b := make([int], 1, 5)      // b = [0]  however, capacity is 5
d = b[:3]                   // d = [0, 0, 0], capacity is 5
e = b[2:]                   // e = [0, 0, 0], capaciy is 3

// 2D arrays/slices
board := [][]string{
    []string{"_", "_", "_"},
    []string{"_", "_", "_"},
    []string{"_", "_", "_"},
}

// Truly dynamic length slices

var s []int                     // s is nil             capacity is 0

// append works on nil slices.
s = append(s, 0)                // s = [0]              capacity is 2

// The slice grows as needed.  // s = [0, 1]            capacity is 2
s = append(s, 1)

// We can add more than one element at a time.
s = append(s, 2, 3, 4)         //s = [0,1,2,3,4]        capacity is 8

// Rules for increasing capacity (heuristic optimization, can change in future)
// If appending to the slice will increase its length by more than double, the
// new capacity is set to the new length.
// Otherwise, double the capacity if the current length is less than 1024,
// or by 25% if it is larger. Repeat this step until the new capacity fits
// the desired length.

// Loop arrays using range operator

var arr = []int{1, 2, 4, 8, 16, 32, 64, 128}

for i, v := range arr {
    fmt.Printf("2**%d = %d\n", i, v)
}

// ignore index
for _, v := range arr {
    fmt.Println(v)
}

```

#### Maps (dictionaries)
```go
type Vertex struct {
    Lat, Long float64
}

loc := make(map[string]Vertex)    // declaring a map string -> Vertex struct
loc["Bell Labs"] = Vertex{
    40.68433, -74.39967,
}
fmt.Println(loc["Bell Labs"])

// Other operations

m := make(map[string]int)

m["Answer"] = 42
fmt.Println("The value:", m["Answer"])          // The value: 42

m["Answer"] = 48
fmt.Println("The value:", m["Answer"])          // The value: 48

delete(m, "Answer")
fmt.Println("The value:", m["Answer"])          // The value: 0

fmt.Println("The value:", m["UndefinedAnswer"]) // The value: 0

v, ok := m["Answer"]
fmt.Println("The value:", v, "Present?", ok)    // The value: 0 Present? false


// Right way to check if a key is present is
v, ok := m["Answer"]
```

#### Functions as parameters (functions are first class members)
```go
func apply(fn func(float64, float64) float64) float64 {
    return fn(3, 4)
}

hypot := func(x, y float64) float64 {
    return math.Sqrt(x*x + y*y)
}
fmt.Println(hypot(5, 12))

fmt.Println(apply(hypot))
fmt.Println(apply(math.Pow))

// functions can be returned and closures are possible
func adder() func(int) int {
    sum := 0
    return func(x int) int {
        sum += x
        return sum
    }
}
```

#### Struct methods

You dont really define methods on struct (like classes),
instead you define a method with a receiver
```go

type Vertex struct {
    X, Y float64
}

func (v Vertex) Abs() float64 {        // v is the receiver (a value receiver specifically)
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
    v := Vertex{3, 4}
   fmt.Println(v.Abs())
}

// This is as good as passing v to Abs, just a better syntax
// Also, you cannot do this outside the package where struct is defined
// You can use type alias to define struct methods for structs outside packages e.g.

// Define a alias to a primitive type
type MyFloat float64

// You can use Abs in the same package, not outside it though
func (f MyFloat) Abs() float64 {
    if f < 0 {
        return float64(-f)
    }
    return float64(f)
}


// Pointer receivers: You can also have the methods on pointers to struct
// Why need em? In go, all data is passed by value
// (you read that right, _everything_ is passed by value)
// So you must use pointers if you want to mutate the passed value

// Now, for struct methods, if you have a value receiver,
it won't be able to change the struct's instance values

type Vertex struct {
    X, Y float64
}

func (v Vertex) Abs() float64 {
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func (v *Vertex) Scale(f float64) {
    v.X = v.X * f
    v.Y = v.Y * f
}
```

#### Important things to remember
- Use pointer receiver when you want to mutate the underlying struct, or its large (so that there is no overhead of copying)
- Use value receiver when you don't want to mutate

- A function which takes pointer as a parameter will not compile if you try to pass a value to it and vice-versa.
```go
func Scale(v *Vertex) {
    v.x = v.x * 100
}
v1 := Vertex(10, 20)
Scale(v1)                // ERROR, wont compile
Scale(&v1)               // Must pass pointer as defined
```
- However, a struct method, doesnt care if it has a value receiver or a pointer receiver. However, mutation of the receiver will succeed only if its a pointer recevier
```go
// Pointer receiver
func (v *Vertex) Scale() {
    v.x = v.x * 100
}
v := Vertex(10, 20)
v.Scale()               // OK, Go interprets this as (&v).Scale()
p := &v
p.Scale()               // OK


// Value receiver
func (v Vertex) Scale() {
    v.x = v.x * 100     // Since its a value receiver, mutation has no affect.
}
v := Vertex(10, 20)
v.Scale()               // OK, still no mutation
p := &v
p.Scale()               // OK, Go interprets this as (*v).Scale(), still no mutation
```

- A struct should either have value receivers or pointer receivers in all its method. Do not mix them. Why? Lets catch this up after Interfaces.

#### Interfaces
- Interface defined methods only
- If a struct that has the same methods as the interface, the compiler automatically infers the "struct as implementing that interface" (in compile time)

```go
package main

import "fmt"

type Abser interface {
    Abs() float64
}

type Vertex struct {X, Y float64}

func (v Vertex) Abs() float64 {
    return v.X*v.X + v.Y*v.Y
}

type MyFloat float64

func (f MyFloat) Abs() float64 {
    return float64(f)
}

func main() {
    var p1 Abser            // Define the abser interface
    var p2 Abser

    v1 := Vertex{10, 20}
    p1 = v1                // Abser interface matches with Vertex struct
    fmt.Println(p1.Abs())

    v2 := Vertex{10, 20}
    p1 = &v2                // Abser interface matches with Vertex struct pointer
    fmt.Println(p1.Abs())

    f1 := MyFloat(200)
    p2 = f1                 // Abser interface matched with MyFloat
    fmt.Println(p2.Abs())

    f2 := MyFloat(200)
    p2 = &f2                // Abser interface matched with MyFloat pointer
    fmt.Println(p2.Abs())
}
```

- So far so good, however, the following doesnt work

```go
type Abser interface {
    Abs() float64
}

type Vertex struct {X, Y float64}

func (v *Vertex) Abs() float64 {
    return v.X*v.X + v.Y*v.Y
}

func main() {
    var p1 Abser

    v1 := Vertex{10, 20}
    p1 = v1        // Compile time error:
                   // Vertex does not implement Abser (Abs method has pointer receiver)
    p1.Abs()
}
```
The reason for the compiler error is because Abs method is defined on Vertex pointer and NOT on Vertex. While Abser want it to be defined on value and not the pointer. To make this work, we can call Abs on a pointer.

```go
type Abser interface {
    Abs() float64
}

type Vertex struct {X, Y float64}

func (v *Vertex) Abs() float64 {
    return v.X*v.X + v.Y*v.Y
}

func main() {
    var p1 Abser

    v1 := Vertex{10, 20}
    p1 = &v1      // No error, p1 points to a pointer Vertex which implements Abs
    p1.Abs()
}
```
```go
// nil receiver. If you expect the receiver or the receiver pointer to be nil.
// do a nil check

type I interface {
    M()
}

func (t *T) M() {
    if t == nil {
        fmt.Println("<nil>")
        return
    }
    fmt.Println(t.S)
}

var i I
i.M()       // prints <nil>
```

#### Type Assertions

In one line:
> `x.(T)` asserts that `x` is not nil and that the value stored in `x` is of type `T`.

Why would I use them:

 - to check `x` is nil
 - to check if it's convertible (assert) to another type
 - convert (assert) to another type

What exactly they return:

 - `t := x.(T)` => t is of type `T`; if `x` is nil, it panics.

 - `t, ok := x.(T)` => if `x` is nil or not of type `T` => `ok` is `false` otherwise `ok` is `true` and `t` is of type `T`.

Lets take a scenario:

- You define 4 structs, Circle, Square, Rectangle, Triangle, all have a method called Area()
- You define a interface Shape with a Area() method
```go
shapes := []Shape[
    Circle{1},
    Square{1},
    Rectangle{1, 1},
    Traingle{1, 1, 1}
]

// Calculate area of all shapes
total_area := float64(0)
for _, s := range shapes {
    total_area = area + s.Area()
}
```

What if you want to extract Traingles out of the shapes. Type assertion helps:
```go
var traingles []Traingle
for _, s := range shapes {
    if traingle, ok := s.(Traingle); ok {
       append(traingles, traingle)
    }
}

// Use type switches
var traingles, circles, squares, rectangles []Shape
for _, s := range shapes {
    switch v := i.(type) {
    case Circle:                // If you want to match with pointer, use *Circle
        append(circles, v)
    case Traingle:
        append(traingles, v)
    case Square:
        append(squares, v)
    case Rectangle:
        append(rectangles, v)
    }
}
```

```go
// Internally, go provides a Stringer interface
type Stringer interface {
    String() string
}

// fmt.Println looks for it to print
// You can define a String() method to change the way fmt.Println prints a struct

// The error type is a built-in interface similar to fmt.Stringer:

type error interface {
    Error() string
}

// You can define custom errors as:
type MyError struct {
    When time.Time
    What string
}

func (e *MyError) Error() string {
    return fmt.Sprintf("at %v, %s",
        e.When, e.What)
}
```

#### Reading files
```go
// io package defines a interface io.Reader which needs
// to define Read() method

// file, network, connections, cipher all implement these

package main

import (
    "fmt"
    "io"
    "strings"
)

func main() {
    r := strings.NewReader("Hello, Reader!")

    b := make([]byte, 8)
    for {
        n, err := r.Read(b)                 // Read will read 8 bytes at a time, till io.EOF
                                            // because b is of size 8
        fmt.Printf("n = %v err = %v b = %v\n", n, err, b)
        fmt.Printf("b[:n] = %q\n", b[:n])
        if err == io.EOF {
            break
        }
    }
}
```

- Coming back to why should a struct not mix pointer receiver and value receivers, like we have seen above, if a struct defines a method and that method has a pointer receiver you will have to take the interface as pointer `i := &v` and if its a value receiver, you will have to do it as `i = v`.
Now, when you call the method on i, it wont be able to call those methods which are defined on the receiver of the other type.

#### Concurrency (The real reason to learn Go)

- Goroutines
```go
package main

import (
    "fmt"
    "time"
)

func say(s string) {
    for i := 0; i < 5; i++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s)
    }
}

func main() {
    go say("world")         // This will be async
    say("hello")
}
```

- Channels
Used to communicate between goroutines and synchronize them
```go
// Creating a channel which can be used to pass integers
ch := make(chan int)

// Send value v to channel ch.
ch <- v

// Receive from ch, and assign value to v
v := <-ch
```
Receiving and sending to channels are blocking functions.
- If the channel has a value, sending to it will be a blocking call
- If a channel has nothing in it and you try to receive from it, its a blocking call

To create a channel which can buffer a few values without blocking sending and receiving do `ch := make(chan int, 5)`
- If the channel has 5 elements, both sending and receiving will be non-blocking
- If the channel has 0 or 5 elements, receiving and sending will be blocking respectively

pingpong example:
```go
package main

import (
    "fmt"
    "time"
)

type Ball struct {hits int}

func main() {
    table := make(chan *Ball)               // table is the channel on which the ball will move
    go player("ping", table)                // "ping" player
    go player("pong", table)                // "pong" player

    table <- new(Ball)                      // Create a ball throw it on the table, this may block if
                                            // table already has a ball (in our case, there isn't)
    time.Sleep(5 * time.Second)             // Wait for 5 seconds and
    ball := <-table                         // The main() picks up the ball from table to stop the game
    fmt.Println("Main catches ball", ball.hits)
    panic("PANIC")                          // Dump the stack and the positions
}

func player(name string, table chan *Ball) {
    for {
        ball := <-table                     // blocks till there is a ball on the table
        ball.hits++                         // once it gets the ball, it hits the ball
        fmt.Println("Caught by ", name, ball.hits)
        sleepTime := 1 * time.Second        // Keeps the ball for a second
        fmt.Println("Sleeping for ", sleepTime)
        time.Sleep(sleepTime)
        table <- ball                       // Hits it back on the table
    }
}
```
- Don't rely on who will receive first. The order can be random it seems (not sure)
```go
// When receiving, you can check if the channel is still open:
v, ok = <-ch

// To continously loop till the channel is closed, use range
for i := range c {
    fmt.Println(i)
}

// Listening to multiple channels, use select
for {
    select {
        case c <- x:
            x, y = y, x+y
        case <-quit:
            fmt.Println("quit")
            return
        default:
            fmt.Println("Nothing here")
            time.Sleep(50 * time.Milliseconds)
    }
}
// This will block till any one condition gets unblocked.
// default gets run if all of them are blocking
```
More safety in channels can be obtained by making then receive only or send only
- `ch chan <- int` send only channel
- `ch <- chan int` receive only channel

```go
func ping(pings chan<- string, msg string) {
    pings <- msg
}

func pong(pings <-chan string, pongs chan<- string) {
    msg := <-pings
    pongs <- msg
}

func main() {
    pings := make(chan string, 1)
    pongs := make(chan string, 1)
    ping(pings, "passed message")
    pong(pings, pongs)
    fmt.Println(<-pongs)
}
```

#### Locks (shit hits the roof)
- If you want multiple goroutines to not access the same variable, we need to use locks
```go
// SafeCounter is safe to use concurrently.
type SafeCounter struct {
    v   map[string]int
    mux sync.Mutex
}

// Inc increments the counter for the given key.
func (c *SafeCounter) Inc(key string) {
    c.mux.Lock()
    // Lock so only one goroutine at a time can access the map c.v.
    c.v[key]++
    c.mux.Unlock()
}

// Value returns the current value of the counter for the given key.
func (c *SafeCounter) Value(key string) int {
    c.mux.Lock()
    // Lock so only one goroutine at a time can access the map c.v.
    defer c.mux.Unlock()
    return c.v[key]
}
```
