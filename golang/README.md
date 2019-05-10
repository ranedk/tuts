# Golang

## Why and where use Go?
Brilliant for I/O related tasks, websockets, http-crawlers etc. Very few keywords (you can learn the basics in a day). Concurrency with channels is a breeze and easy to setup. Compiler helps in finding deadlocks and concurency issues. (not as good as Rust, but the overhead to learn this is not very high). Very efficient for data transformations. So if you are writing a data pipeline with transformations and I/O, this is the language. Great fit for your first statically typed language.

Basic visual code setup is good enough for efficient coding. No need to anything Jetbrains.

## The Bad
Best practices and some corners are difficult to get right and will require experience.

## Lets begin

### Installation:
```bash
$ sudo tar -xvf go1.12.2.linux-amd64.tar.gz  // (get the latest version from https://golang.org/dl/)
$ sudo mv go /usr/local

$ export GOROOT=/usr/local/go           // this is where all go binaries and compiler go
$ export GOPATH=$HOME/Projects/Go       // this is where go libraries and dependencies go

# put this in your zshrc (or bashrc)

$ go version  // verify installation
$ go env  // verify installation
```

### Starting a project
```bash
$ cd /home/user/my-working-directory
$ mkdir hello

$ go mod init github.com/ranedk/hello   // initialize a go package, creates a file go.mod

# installing go dependencies
$  go get github.com/SlyMarbo/rss       // Will install the package in $GOPATH and make an entry in go.mod
```

### Basics
Create a file names hello.go
```go
package main

import (
    "fmt"
    "time"
    "math/rand"         // math is the folder name, rand is the package name
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

a, b := swap("hello", "world")      // since a and b have not been defined yet, use :=, this infers types automatically

x := 10
y := 20

x = x + y      // := not required since x is already defined

// Named returned values (this is confusing, don't use)
func split(sum int) (x, y int) {    // find x and y in the function definition and returns them without explicit call
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

#### Types
bool: true/false

string: "Hello world", 'hello world', `hello world` (backticks allow multi-line strings)

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
    if v := math.Pow(x, n); v < lim {       // v is scoped only inside if and else statement
        return v
    } else {
        fmt.Printf("%g >= %g\n", v, lim)
    }
    return lim
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

fmt.Println(v1, v2)     // prints complete v1 and v2 nicely (beautiful for debugging)

v1.X = 100      // Access struct params

p1 := &v1       // pointer to struct

Xvalue := (*p1).X   // The old and painful C like way to access

Xvalue := p1.X      // Go is awesome, access works in the same way with values or pointers
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
var s []int = primes[1:4]                   // this refers to the original array, changing
                                            // values in s, will change value in primes

// Like python, slice has lower_bound:upper_bound, which default to 0:length_of_array

var MySlice = []int{1, 2, 3, 4, 5}          // This is a slice since length is not mentioned, but is also an array

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
    printSlice(s)               // len=6 cap=6 [2 3 5 7 11 13]

    // Slice the slice to give it zero length.
    s = s[:0]                   // now, length is zero, but s still points to original [0], so capacity is 6
    printSlice(s)               // len=0 cap=6 []

    // Extend its length.
    s = s[:4]                   // now, length is 4, s points to original [0], so capacity is 6
    printSlice(s)               // len=4 cap=6 [2 3 5 7]

    // Drop its first two values.
    s = s[2:]                   // now, length is 2, s points to original [2], so capacity is 6 - 2 = 4
    printSlice(s)               // len=2 cap=4 [5 7]

    s = s[:4]                   // now, length is 4, s points to original [2], so capacity is 4
    printSlice(s)               // len=4 cap=4 [5 7 11 13]
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
// If appending to the slice will increase its length by more than double, the new capacity is set to the new length.
// Otherwise, double the capacity if the current length is less than 1024, or by 25% if it is larger. Repeat this step until the new capacity fits the desired length.

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

```


