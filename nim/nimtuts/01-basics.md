# Variables

```nim
# mutable variable
var a = "foo"
var b: string = "bar"

a = "boo"
a.add("far")
echo "a = ", a

# immutable variable
let c = 1000000

echo "c = ", c

c = 10  # ERROR!
```

## Const
`const` variables are evaluated compile time. (a lot like `#ifdef` `#define` in C). **They cannot be modified in runtime**.

```nim
proc myName(): string = "Devendra Rane"
const name = myName()
```

## Types

**Booleans**: `bool`

> Notes: Boolean values are `true`, `false`. Operators `and` `or` for booleans

**Integers**: `int int8 int16 int32 int64 uint uint8 uint16 uint32 uint64`

```nim
var x: int = 1_23_345   # underscores for readability
```

**Float**: `float float32 float64`

**Characters**: `char`

> Notes: the `$` operator converts `char` to `string`. `ord(c)` to get integer from character. `chr(i)` to get character from integer.

**Strings**: `string`, `cstring` (for C compatibility)

> Notes: String are mutable (and efficient) and UTF-8 encoded. Use `add` to append to a string and `&` to concatenate strings.
> Notes: `s[i]` to get ith character of string, which is useless for unicode strings. You need runeLen, which is a part of the `unicode` package.

```nim
import unicode
let s = "नमस्ते"

# Characters in s - Useless and unprintable
for i in 0..len(s)-1:
    echo ">", s[i]

# Unicode runes in s - printable as न म स ्त े
for i in 0..s.runeLen-1:
    echo ">", s.runeAtPos(i)
```

**Null**: `nil`

**Type alias**: To create alias of basic types `type biggestFloat = float64`

**Enums**:
```nim
import typetraits    # provides <var>.type.name to get type of a variable

type Direction = enum NORTH, EAST, WEST, SOUTH

var num = Direction.WEST
echo "num = ", num
echo "string representation of num is = ", $(num)
echo "integer value of num = ", ord(num)
echo "num is ", num.type.name

# To give different ordinal values to enums:
type VOLTAGE = enum
    LOW = 1,
    MID = 10,
    HIGH = 220,
    JURASSIC_PARK = 10000

# Must be integers and orders in acsending order
```

#### Ordinal types

All types which behave like a bounded array (and have limited small size)
Properties of ordinal types:

| Operation | Comment |
|-----------|---------|
| ord(x) | returns the integer value that is used to represent x's value |
| inc(x) | increments x by one |
| inc(x, n) | increments x by n; n is an integer |
| dec(x) | decrements x by one |
| dec(x, n) | decrements x by n; n is an integer |
| succ(x) | returns the successor of x |
| succ(x, n) | returns the n'th successor of x |
| pred(x) | returns the predecessor of x |
| pred(x, n) | returns the n'th predecessor of x |

> Note: `ordinal` values can be used as array indices or sets

### Casting and Type conversions

```nim
var x = int(1 / 3.0)  # type conversion
```

## Default values

By default, Nim will initialize variable to their default primitive values:

|Type|default value|
|----|-------------|
|any integer type|0|
|any float|0.0|
|char|'\0'|
|bool|false|
|ref or pointer type|nil|
|procedural type|nil|
|sequence|@[]|
|string|""|
|tuple[x: A, y: B, ...]|(default(A), default(B), ...) (analogous for objects)|
|array[0..., T]|[default(T), ...]|
|range[T]|default(T); this may be out of the valid range|
|T = enum|cast\[T\](0); this may be an invalid value|


# Functions (aka procedures - proc)

```nim
# Simple example
proc simple(fname: string, lname: string): string =
    return fname & lname

echo "fullname: ", simple("Devendra", "Rane")
```

Alternatively, all `proc` expose a `result` variable, which is initialized to the default value of the return type. It gets returned automatically at the end of the function call.

```
proc simple(fname: string, lname: string): string =
    result = fname & lname

echo "fullname: ", simple("Devendra", "Rane")
```
> Notes: Do not override result by overwriting `result`

**Functions can be called as methods too. e.g.`foo(a, b)` or `a.foo(b)`**

## Pragmas with procs

Procs can be decorated with pragmas e.g. {.noSideEffect.}

```nim
proc minus(x, y: int): int {. noSideEffect .} =
    echo x  # error: 'minus' can have side effects
    x - y

```
This will make sure that any attempt to modify `x` or `y` inside `proc minus`
 will give compiler error.

More on [Pragmas](02-pragmas.md)

## Exporting procs or other symbols

Annotating a proc/symbol with `*` will make it exposed from that module:

```nim
# module1

proc foo*(): int = 2
proc bar(): int = 3

#module2

import module1

let a = foo()        # <-- import module1 exposes foo
let b = bar()        # ERROR <-- bar doesn't get exposed
```

# Conditionals

## If - elif - else

Very close to Python synatically. `break` support labels (like Kotlin)

```nim
import random

randomize()
let num = rand(20)

echo "num = ", num

if num == 0:
    echo "num is zero"
elif num < 1:
    echo "num is between zero & one"
elif num < 2:
    echo "num is between one & two"
else:
    echo "num is greater than two"


block outermost:          # blocks are used to create new scoping
    while true:
        var guess = rand(num)
        if guess > int(num / 2):
            echo "guess > ", num/2, ".. exiting"
            break outermost
        else:
            echo "guess < ", num/2, ".. continuing"
            continue
```

## case - of

Like switch-case in other languages.
- case must be known at **compile time**
- case can be a string or a set or a range of _ordinal types_ (explained above)
- all cases must be covered
- case can be used as expression (i.e. output can be assigned to a variable)

```nim
import random

randomize()
let num = rand(6)
echo "num = ", num

case num:
    of 1,2,3,4,5:
        echo "num < 5"
    of 0:
        echo "num is zero"
    else:
        echo "num is 6"
```

# Loops and iterators

Nim implements Iterators like other languages, which implement methods `items` or `pairs`. The `iterators` can be used in for loops with `break` and `continue`. Iterators **do not** have the `result` variable implicit.

**Simple iterator**

```nim
iterator iterByThree(a: int, b: int): int =
    var i = a
    while i <= b:
        yield i
        i += 3

for i in iterByThree(4, 20):
    echo "i = ", i
```

**Object based iterator**

```nim
type
  CustomRange = object
    low: int
    high: int

iterator items(range: CustomRange): int =
  var i = range.low
  while i <= range.high:
    yield i
    inc i

iterator pairs(range: CustomRange): tuple[a: int, b: char] =
  for i in range:  # uses CustomRange.items
    yield (i, char(i + ord('a')))


for i in CustomRange(low: 0, high: 3):
  echo "i = ", i

for i, c in CustomRange(low: 0, high: 3):
  echo "(i, c) = ", i, ", ", c

#[
Output:
    i = 0
    i = 1
    i = 2
    i = 3
    (i, c) = 0, a
    (i, c) = 1, b
    (i, c) = 2, c
    (i, c) = 3, d
]#
```

# Operators

All random operators can be defined. DSLs can take lot of advantage of this.

```nim
import math

proc `**`(a: int, b: int): int =
    result = a ^ b

# Boring function call
echo "2^10 = ", `**`(2, 10)

# Cool, operator call
echo "2^10 = ", 2**10
```

> Note: The `math` library implements `^` as power operator in the same way

You can even mix operators with iterators!

```nim
iterator `...`(a: int, b: int): int =
  var res = a
  while res <= b:
    yield res
    res += 1

for i in 0...5:
  echo i

for i in `...`(0, 5):
    echo i
```

> Note: Iterators are by default inline. Meaning the call in the code, gets replaces by the complete function. So there are no function call overheads, but the code size increases. There are cases though, when iterator cannot be inlined, when they have closures (iterators holding external state in them)

**Closure iterator**

```nim
proc incrBy(incr: int): iterator(a:int, b:int): int =
  return iterator(a: int, b:int): int =
    var i = a
    while i <= b:
      yield i
      i += incr

let incr3 = incrBy(3)

for i in incr3(4, 20):
    echo "i = ", i
```
Since this iterator maintains the state `incr`, it cannot be inlined since the iterator gets the state in runtime. This is hence a closure iterator.

**Another way to use iterators**

```nim
let incr4 = incrBy(4)

var output = ""
while true:
  let next = incr4(4, 20)
  if finished(incr4):
    break
  output.add($next & " ")

echo "output = ", output
# output = 4 8 12 16 20
```
