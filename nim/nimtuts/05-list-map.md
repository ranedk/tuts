# Arrays

Size is specified at compile-time and cannot be changed later

```nim
let a1: array[3, string] = ["Jasmine", "Ktisztina", "Kristof"]

# OR

let a1: array[0..3, string] = ["Jasmine", "Ktisztina", "Kristof"]

# OR

let a2 = ["Jasmine", "Ktisztina", "Kristof"]

var a3: array[3, string]

echo a3
# outputs: ["", "", ""]
```

Arrays in other languages are implemented as `array[T]`, in Nim, arrays are implemented as `array[I: static[int], T]` or `array[I: static int, T]`. This means that the size is a part of the definition and can be represented as any `ordinal` type. Its marked as `static` which will be explained later.


```nim
proc zip[I, T, U](a: array[I, T], b: array[I, U]): array[I, tuple[a: T, b: U]] =
  for i in low(a)..high(a):
    result[i] = (a[i], b[i])


echo zip([10, 20, 30], ["apple", "boy", "cat"])
# outputs: [(a: 10, b: "apple"), (a: 20, b: "boy"), (a: 30, b: "cat")]
```

**Any ordinal value can be used as array index**

```nim
type ArrowKey = enum
   UP, DOWN, RIGHT, LEFT

let move: array[ArrowKey, string] = [
    "jump", "crouch", "backward", "forward"
]

echo move
# Outputs: ["jump", "crouch", "backward", "forward"]

echo move[ArrowKey.UP], " - ",  move[ArrowKey.DOWN]
# Outputs: jump - crouch

# echo "> ", move[0], " - ",  move[1]   # ERROR, indexes aren't integers
```
This looks like a look-up table

Even an integer range is an ordinal, so:
```nim
let a: array[3..8, int] = [1,2,3,4,5,6]

echo "> ", a
echo "> ", a[3], a[4]
# echo "> ", a[0]       # ERROR, index is 3..8
```

## static[T] the weird, buggy dark corner of nim

The creator of Nim, doesn't like `static[T]` it seems!

When using generics, the compiler checks how many types have been used for the generic part and "generates code" for all those parts. So if you have defined `proc foo[T](a: T)` and called it as `foo(10)` and `foo("a")`, compiler will generate foo for `int` and `string both`.

There are some requirements, you want to generate multiple `proc` for each "value". So if you define a `proc voodoo(a: static int)`, and call it as `voodoo(10)` and `voodoo(20)`, the compiler will generate 2 `proc` for values 10 and 20. Its used for say `precompiledRegex` will need to replace all calls of a certain regex with the the regex compiled at compiletime.


## Matrix or deep arrays

Lets define a new type `Matrix`. Since its got 2 dimensions, it will be of generic type `[W, H, T]` for Width, Height and type`T`. We fix `T` as int for simplicity. However, `W` and `H` are not of type `int`, they MUST be of type `static int`. Meaning that the compiler will treat them as generic BUT the values must be known at compile time.

```nim
type Matrix[W, H: static int] = array[W, array[H, int]]

let mat1: Matrix[2, 2] = [[1, 0],
                          [0, 1]]
let mat2: Matrix[2, 2] = [[0, 1],
                          [1, 0]]

proc `+`[W, H](a, b: Matrix[W, H]): Matrix[W, H] =
  for i in 0..high(a):
    for j in 0..high(a[0]):
      result[i][j] = a[i][j] + b[i][j]

echo mat1 + mat2
# Outputs: [[1,1], [1,1]]
```

Rust calls `static T` as `phantomTypes`. They are equally confusing and weird in Rust.

This looks complicated because `array` type is treated very differently than `seq` (seqence) type, which is a dynamic list. `array` is generally used to extract the last ounce of efficiency. If confused, always use sequence (its as simple as python lists!)

# Sequence - Dynamic Lists

Create sequence with `@` operator and with the `newSeq[T](n: int)` method
Methods on sequence `add(item: T)`, `delete(idx: int)`
Length by the property `len: int`, maximum index through `high: int`. Max index is `length - 1`
Iteration with `items: T` and `pairs: tuple[i: int, v: T]`

```nim
import strformat

let s = @[1,2,3,4]

echo fmt"length of s = {s.len()}"
echo fmt"max index of s = {s.high()}"

for i in s:
    echo fmt"> {i}"

for i, e in s:
    echo fmt"({i}, {e})"

# s.add(10)     # ERROR, s is immutable (let s)

var l = @[1, 2, 3]
l.add(10)
echo fmt"updated l = {l}"
```

Sequences are assigned on heap and reference is made available.
`let` creates a immutable reference
`var` creates a mutable reference

```nim
# pass by value, immutable array, so compile time error
# proc passImmutable(a: seq[int]) =
#    a[0] = 100
```

```nim
# pass by ref (var or ref)
proc passMutable(a: var seq[int]) =
    a[0] = 100

passMutable(l)
echo fmt"updated l = {l}"
```

## Matrix

After the complicated mechanism of arrays and Matrix in arrays, this will be a easy peasy.

```nim
import strformat

var s = @[[1,2,3,4], [4,6,7,8]]
# the size/type of all types must be same
# else you get compile error

echo "s = ", s
s = @[[1, 2, 3, 4], [4, 6, 7, 8]]


# Dynamic allocations

var l: seq[seq[int]]

for i in 0..3:
    var s: seq[int]
    for j in 0..3:
        s.add(i * j)
    l.add(s)

echo "l = ", l
l = @[@[0, 0, 0, 0], @[0, 1, 2, 3], @[0, 2, 4, 6], @[0, 3, 6, 9]]
```

# BitSets

Set operations are available and implemented using `bitsets`. They are ordinal types hence a set cannot have more than 2^16 elements. However, they implement a lot cool set operations (like Python set type)


|Operator|Description|Example Code|
|--------|-----------|------------|
|a in B|is a an element of B?|'d' in {'a'..'z'}|
|a notin B|is a not an element of B?|40 notin \{2..20\}|
|A + B|union of A with B|\{'a'..'m'\} + \{'n'..'z'\} == \{'a'..'z'\}|
|A - B|relative complement of A in B|\{'a'..'z'\} - \{'b'..'d'\} == \{'a', 'e'..'z'\}|
|A + {b}|add element b to set A|\{'b'..'z'\} + \{'a'\} == \{'a'..'z'\}|
|A - {b}|remove element b from set A|\{'a'..'z'\} - \{'a'\} == \{'b'..'z'\}|
|A * B|intersection of A with B|\{'a'..'m'} * \{'c'..'z'\} == \{'c'..'m'\}|
|A <= B|is A a subset of B?|\{'a'..'c'\} <= \{'a'..'z'\}|
|A < B|is A a strict subset of B?|\{'b'..'c'\} < \{'a'..'z'\}|



