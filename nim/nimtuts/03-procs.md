# Procs

You can also create generic `proc`

```nim
let zero = ""

# Implement a plus operator for strings (Bad idea)
proc `+`(a, b: string): string =
  a & b

proc `*`[T](a: T, b: int): T =
  result = zero
  for i in 0..b-1:
    result = result + a  # calls `+` defined above
```

# Procs as lambdas

Functions can be declared as:
- `proc`
- `do` notation (like lambda in python)
- `(x) =>` notation like Javascript (using `import sugar`)

```nim
import sequtils
import sugar

let powersOfTwo = @[1, 2, 4, 8, 16, 32, 64, 128, 256]

proc greaterThan32(x: int): bool = x > 32
echo powersOfTwo.filter(greaterThan32)

# OR

echo(powersOfTwo.filter do (x: int) -> bool: x > 32)

# OR

echo powersOfTwo.filter(proc (x: int): bool = x > 32)

# OR

# => macro provided by sugar
echo powersOfTwo.filter( (x) => x > 32)
```

# Functions which take proc as arguments

`sugar` also provides a `->` macro to define a function as an argument to a function.
e.g. `(int, int) -> float` denotes `proc` takes 2 `int` arguments and return a `float`

```nim
import sugar

proc map(str: string, fun: (char) -> char): string =
  for c in str:
    result &= fun(c)


echo "foo".map((c) => char(ord(c) + 1))

# OR

echo "foo".map(proc (c: char): char = char(ord(c) + 1))

# OR

echo "foo".map do (c: char) -> char: char(ord(c) + 1)
```
