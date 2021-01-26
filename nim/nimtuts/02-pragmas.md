# Pragmas

Pragmas are like `annotations` in Java. They give compiler extra information to act on. There are lots of `pragmas` and some are filling in for beta-features that may be implemented better in future.

## Pure Pragmas

These are hints to the compiler/linker with no semantic effects on the source code. A different compiler could decide to not support the pragma and give the same results.

#### noInit

`noInit` pragma won't initialize the variables to default (e.g. int to 0), but that doesn't mean it will be initialized to `nil`. It gets whatever value was in the stack/heap when compiler provisioned the space. _This removes overhead of initialization, but that may introduce bugs if not handled well_

If applied on `proc`, this doesn't initialize `result` variable

#### requiresInit

Only works on `object`. This makes it mandatory to initialize the instance

```nim
type Point {.requiresInit.} = object
  x: float
  y: float

let p1 = Point(x: 10, y:20)   # Initialized
let p2 = Point()              # ERROR: Must be initialized
```

#### deprecated

```nim
proc thing(x: bool) {.deprecated: "use thong instead".}
```

#### noReturn

Rarely useful, this tells a `proc` that it must not return anything, not even `nil`. These `proc` either `quit` exiting the running program or always raise an exception.

```nim
proc killTheProgram {.noReturn.} =
  echo "Exiting the program"
  quit(0)

proc raiseSomething {.noReturn.} =
  echo "raising it"
  raise newException(ValueError, "Something")
```

#### acyclic

If there are cyclic structures (like linked list), however the program logic can guarantee that this won't results in cyclic structures, then marking `acyclic` will tell the compiler to not consider it as cyclic. _This is an optimization. Marking cycyclic as `acyclic` may result in memory leaks_

```nim
type
  Node {.acyclic.} = ref object
    left, right: Node
    data: string
```

There are more and documentation is available at : https://nim-lang.org/docs/manual.html#pragmas


**Syntax Pragmas**

These change the semantics and all compiler MUST respect them and implement the same way.

**Core language syntax pragmas**

`global, discardable, borrow, raises, tags, compileTime`

**OOP syntax pragmas**

`final, base, inheritable`

**Concurrency syntax pragmas**

`thread, threadvar, guard, locks`

**Template pragmas**

**FFI pragmas**

`union, packed, importC, exportC, importCpp, importObjC`

**Debugging pragmas**

`breakpoint, watchpoint, debugger, profiler`

