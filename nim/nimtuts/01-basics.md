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

**Type alias**: `type biggestFloat = int64` To create alias of basic types

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


block outermost:
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


