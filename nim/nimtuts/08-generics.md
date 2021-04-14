# Generics

```nim
type Person = tuple[name:string, age:int]

type RecordType = tuple or Person

proc printFields[T: RecordType](rec: T) =
    for key, value in fieldPairs(rec):
        echo key, " = ", value


var p:Person = ("Devendra Rane", 30)

printFields(p)
# Output:
#   name = Devendra Rane
#   age = 30

printFields((field1: "one", field2: "two"))
# Output:
# field1 = one
# field2 = two
```

## Conditional generics

```nim
type
    Table[Key, Value] = object
        keys: seq[Key]
        values: seq[Value]
        when not (Key is string): # field available on a condition
            deletedKeys: seq[bool]
```

```nim
type TypeClass = int | string
var foo: TypeClass = 2    # During compile time this will be defined as int
```

## Compile time errors
```nim
proc getMax[T](a, b: T): T =
    if a < b:
        return b
    else:
        return a

echo getMax(5, 10)       # This works

type Person = object
    name: string

let p1 = Person(name: "Dev")
let p2 = Person(name: "Abhi")

echo getMax(p1, p2)     # COMPILE TIME ERROR
                        # since `>` is not defined for Person type
```

## Generics in objects

```nim
type
  BinaryTree[T] = ref object
    left, right: BinaryTree[T]
    data: T
```

## Constraining Generics

```nim
# Only allowed int and float
proc getMax[T: int | float](a, b: T): T =
    if a < b:
        return b
    else:
        return a

echo getMax("Hello", "World") # COMPILER ERROR
```

**Implementing a tuple equality**

```nim
proc `==`*(x, y: tuple): bool =
    ## requires `x` and `y` to be of the same tuple type
    ## generic ``==`` operator for tuples that is lifted from the components
    ## of `x` and `y`.
    result = true
    for a, b in fields(x, y):
        if a != b: result = false
```

# Concepts

`concept` is experimental. It allows you to define conditions which must be met for the generic behaviour to continue.
e.g. in above case `getMax` should only allow those types which implement the `<` operator.

```nim
type
    Comparable = concept a
        (a < a) is bool     # Concept defines that < operator should be implemented
                            # and must return a boolean value

proc getMax(a, b: Comparable): Comparable =
    if a < b:
        return b
    else:
        return a
```


