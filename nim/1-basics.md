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



