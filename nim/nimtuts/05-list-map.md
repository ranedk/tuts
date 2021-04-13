# Tuples

`tuple` behave like python namedtuples:

```nim
type
    Person = tuple      # type representing a person
        name: string    # a person consists of a name
        age: int        # and an age
```

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

>Note: You can replace `I` with `int` above. However, it won't work for other ordinal types like `enum`

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

- Create sequence with `@` operator and with the `newSeq[T](n: int)` method
- Methods on sequence `add(item: T)`, `delete(idx: int)`
- Length by the property `len: int`, maximum index through `high: int`. Max index is `length - 1`
- Iteration with `items: T` and `pairs: tuple[i: int, v: T]`

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

# OpenArray

For methods which can take `seq` or `array` or `string`, then we use `openarray` e.g.

```nim
proc testOpenArray(x: openArray[int]) = echo repr(x)

testOpenArray([1,2,3])  # array[]
testOpenArray(@[1,2,3]) # seq[]
```

```nim
proc testOpenArray[T](x: openArray[T]) = echo repr(x)

testOpenArray([1,2,3])          # array[]
testOpenArray(@[1,2,3])         # seq[]
testOpenArray("some string")    # string
```

# List operations

`sequtils` takes care of `seq`, `array` and `string` by providing the `openarray` interface to its methods.
`sugar` provides functional methods on `openarray`.

So almost all list operations can be achieved with a mix of both

```nim
import sequtils, sugar

let scores = @[10, 12, 34, 5, 23, 76, 12, 74, 23, 65]

let parsed1 = scores.map(x => x*2).filter(x => x > 60)

let parsed2 = scores.mapIt(it * 2).filterIt(it > 60)

let parsed3 = collect(newSeq):
    for s in scores:
        let m = s * 2
        if m > 60:
            m

doAssert parsed1 == @[68, 152, 148, 130]
doAssert parsed1 == parsed2
doAssert parsed1 == parsed3

echo scores.any(x => x > 50)     # true
echo scores.anyIt(it > 50)       # true
echo scores.allIt(it < 100)      # true
echo scores.foldl(a + b)         # 334 (sum of all scores)
```

```nim
import sequtils
from strutils import join

let
  vowels = @"aeiou"     # creates a sequence @['a', 'e', 'i', 'o', 'u']
  foo = "The quick brown fox jumps over a lazy dog"

echo foo.filterIt(it notin vowels).join("")
# Output = Th qck brwn fx jmps vr  lzy dg
```

> NOTE: `foo.filterIt(it notin vowels).join("")` can also be written as `foo.filterIt(it notin vowels).join`. If method has no parameters, you dont have to call it. Do not use it, it looks fugly.

Other common methods:
```nim
proc concat[T](seqs: varargs[seq[T]]): seq[T]
proc count[T](s: openArray[T]; x: T): int
proc cycle[T](s: openArray[T]; n: Natural): seq[T]
proc repeat[T](x: T; n: Natural): seq[T]
proc deduplicate[T](s: openArray[T]; isSorted: bool = false): seq[T]
proc minIndex[T](s: openArray[T]): int
proc maxIndex[T](s: openArray[T]): int
proc zip[S, T](s1: openArray[S]; s2: openArray[T]): seq[(S, T)]
proc unzip[S, T](s: openArray[(S, T)]): (seq[S], seq[T])
proc distribute[T](s: seq[T]; num: Positive; spread = true): seq[seq[T]]
proc map[T, S](s: openArray[T]; op: proc (x: T): S {...}): seq[S] {...}
proc apply[T](s: var openArray[T]; op: proc (x: var T) {...}) {...}
proc apply[T](s: var openArray[T]; op: proc (x: T): T {...}) {...}
proc apply[T](s: openArray[T]; op: proc (x: T) {...}) {...}
proc filter[T](s: openArray[T]; pred: proc (x: T): bool {...}): seq[T] {...}
proc keepIf[T](s: var seq[T]; pred: proc (x: T): bool {...}) {...}
proc delete[T](s: var seq[T]; first, last: Natural)
proc insert[T](dest: var seq[T]; src: openArray[T]; pos = 0)
proc all[T](s: openArray[T]; pred: proc (x: T): bool {...}): bool
proc any[T](s: openArray[T]; pred: proc (x: T): bool {...}): bool
iterator filter[T](s: openArray[T]; pred: proc (x: T): bool {...}): T
iterator items[T](xs: iterator (): T): T
macro mapLiterals(constructor, op: untyped; nested = true): untyped
template filterIt(s, pred: untyped): untyped
template keepItIf(varSeq: seq; pred: untyped)
template countIt(s, pred: untyped): int
template allIt(s, pred: untyped): bool
template anyIt(s, pred: untyped): bool
template toSeq(iter: untyped): untyped
template foldl(sequence, operation: untyped): untyped
template foldl(sequence, operation, first): untyped
template foldr(sequence, operation: untyped): untyped
template mapIt(s: typed; op: untyped): untyped
template applyIt(varSeq, op: untyped)
template newSeqWith(len: int; init: untyped): untyped
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

