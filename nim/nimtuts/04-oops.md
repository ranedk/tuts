# Object oriented or something like that

Before going ahead with OOPS, lets clarify a couple of things:

1) `object` are essentially clusters of primitive types, allocated as continous chunk.
2) `object` initialized with `var p = Point(x: 1, y:1)` will be allocated on stack
3) `object` initialized with `var p = new(Point)` or instance of a `ref` type will be allocated on the heap, with the reference put on stack
4) Nim or any other language (including Rust) cannot implement REAL immutability, since threads work on local stacks which get copied around a lot.
5) Immutability can be managed by not having mutating methods on an object.

```nim
# Declaring a class
type Employee* = object
    name*, department*: string
    age: int
    salary: int

# Note the keyword "var", this expects a mutable instance
proc increment*(e: var Employee) =
  e.salary = int(1.2 * float(e.salary))

# Note the keyword "var", this expects a mutable instance
proc decrement*(e: var Employee) =
  e.salary = int(0.8 * float(e.salary))

# This expects any instance (mutable or not)
proc salaryProjection(e: Employee): int =
  return int(1.2 * float(e.salary))

# This expects a reference of the instance
proc refDecr*(e: ref Employee) =
  e.salary = int(0.8 * float(e.salary))

# This expects a reference of the instance
proc refIncr*(e: ref Employee) =
  e.salary = int(1.2 * float(e.salary))

# variable employee - created on stack
var e1 = Employee(name: "Devendra rane", age:30, salary: 1_00_000)
e1.name = "Devendra K rane"
e1.increment()
echo "e1 = ", e1

# immutable Employee - created on stack
let e2 = Employee(name: "Nihira rane", age:3, salary: 10)
# e2.increment()  # ERROR: Invalid, increment expects a mutable
echo "e2 salary projection = ", e2.salaryProjection()


# Create a reference to the Employee on stack after allocation in heap
let e3: ref Employee = new(Employee)
# e3 is immutable reference, so it will always point to this Employee instance
# Employee instance is mutable, so we can use e3 to mutate the instance

e3.name = "Abhiruchi Chand"
e3.age = 28
e3.salary = 2_00_000

# echo doesnt work with references :(, [] is the deref operator
echo "e3 = ", e3[]
# e3.decrement()  # ERROR: Invalid, decrement expects a variable, not a reference
e3.refDecr()
echo "e3 = ", e3[]


# You can also create object which always returns a reference on initialization
type EmployeeRef* = ref Employee

let e4 = EmployeeRef(name: "Suresh", age: 20, salary: 1_000)
e4.refIncr()
# e4.increment()   # ERROR: Invalid, increment expects a variable, not a reference
echo "e4 = ", e4[]


# You can also define an object which directly gives reference on initialization
type Employer = ref object
    name: string
    revenue: float
    city: string

func revenueProjection*(e: Employer): float =
    e.revenue = 1.2 * e.revenue
    return e.revenue

# Creates company as a reference to Employer instance
var company = Employer(name: "Dunded mifflin", city: "Mumbai")
echo "company revenue projection", company.revenueProjection()
```

> Note: `[]` is the de-ref operator, which gets the object from the reference

> Note: If you have a reference, you will ALWAYS be able to mutate the instance.

# Inheritance

Always use `ref` for inheritance. Otherwise, it becomes extremely complicated to manage. So instead of `Vehicle = object of RootObj` we use `Vehicle = ref object of RootObj`

```nim
# This is a simple ref object
type Flower {.requiresInit.} = ref object
    color: string

# Inherit from RootObj (like Python's `object`)
type Fruit = ref object of RootObj
    color: string

type Vehicle = ref object of RootObj
    numOfWheels: int
    color: string

type Car = ref object of Vehicle
    isSedan: bool

type Bike = ref object of Vehicle

type Mercedes = ref object of Car
    isAdjustable: bool
```

Note above that  `Flower` doesn't share the same family tree since every other object has `RootObj` at its inheritance root.

```nim
let merc = Mercedes(numOfWheels: 4, isAdjustable: true)
echo "merc = ", merc[]
# prints merc = (isAdjustable: true, isSedan: false, numOfWheels: 4, color: "")

echo "Is merc Mercedes : ", merc of Mercedes    # true
echo "Is merc Car : ", merc of Car              # true
echo "Is merc Vehicle : ", merc of Vehicle      # true
echo "Is merc Bike : ", merc of Bike            # false
echo "Is merc Fruit: ", merc of Fruit           # false

# Cannot compare of check object type
# echo "Is merc Flower: ", merc of Flower       # ERROR, incompatible
```

Base objects inherit `proc` of parent. Overriding works as expected.

```nim
proc vroom(v: Vehicle) =
    echo "Vehicle Vrooommmmm"

proc vroom(c: Car) =
    echo "Car Vrooommmmm"

merc.vroom()
# prints Car Vroommmm
```

# Dynamic and Static dispatch

**Dynamic dispatch**: Generally, the function to be called is known in compile time. However, there are cases where inhertance leads to cases where function to be called is decided dynamically at runtime. This is called Dynamic dispatching.
This is very often the case when you do composition or you have a inheritance with a tree structure.

`proc` doesn't support dynamic dispatch, for those we have `method`

```nim
import strformat

type Tyre = ref object of RootObj
    name: string
proc price(t: Tyre): string = t.name & " Base tyre: $0"

type BudgetTyre = ref object of Tyre
proc price(b: BudgetTyre): string = b.name & " Budget tyre: $100"

type FlatTyre = ref object of Tyre
proc price(f: FlatTyre): string = f.name & " Flat tyre: -$100"

type WornTyre = ref object of Tyre
proc price(w: WornTyre): string = w.name & " Worn tyre: $50"


type Car = ref object of RootObj
    color: string
    l1Tyre: Tyre
    l2Tyre: Tyre
    r1Tyre: Tyre
    r2Tyre: Tyre

let c = Car(
    color: "green",
    l1Tyre: BudgetTyre(name: "l1"),
    l2Tyre: FlatTyre(name: "l2"),
    r1Tyre: WornTyre(name: "r1"),
    r2Tyre: BudgetTyre(name: "r2")
)

echo fmt"""
    l1tyrePrice:{c[].l1Tyre.price()},
    l2tyrePrice:{c[].l2Tyre.price()},
    r1tyrePrice:{c[].r1Tyre.price()},
    r2tyrePrice:{c[].r2Tyre.price()}
"""
```

Outputs:
```text
    l1tyrePrice:l1 Base tyre: $0,   # All calls to tyre for to base
    l2tyrePrice:l2 Base tyre: $0,
    r1tyrePrice:r1 Base tyre: $0,
    r2tyrePrice:r2 Base tyre: $0
```

Because `proc` do not support dynamic call, all calls to `tyre` go to base tyre
Lets simply change `proc` to `method`

```nim
import strformat

type Tyre = ref object of RootObj
    name: string
method price(t: Tyre): string = t.name & " Base tyre: $0"

type BudgetTyre = ref object of Tyre
method price(b: BudgetTyre): string = b.name & " Budget tyre: $100"

type FlatTyre = ref object of Tyre
method price(f: FlatTyre): string = f.name & " Flat tyre: -$100"

type WornTyre = ref object of Tyre
method price(w: WornTyre): string = w.name & " Worn tyre: $50"


type Car = ref object of RootObj
    color: string
    l1Tyre: Tyre
    l2Tyre: Tyre
    r1Tyre: Tyre
    r2Tyre: Tyre

echo fmt"""
    l1tyrePrice:{c[].l1Tyre.price()},
    l2tyrePrice:{c[].l2Tyre.price()},
    r1tyrePrice:{c[].r1Tyre.price()},
    r2tyrePrice:{c[].r2Tyre.price()}
"""
```

Output:
```text
    l1tyrePrice:l1 Budget tyre: $100,   # Dynamic dispatch works!
    l2tyrePrice:l2 Flat tyre: -$100,
    r1tyrePrice:r1 Worn tyre: $50,
    r2tyrePrice:r2 Budget tyre: $100
```

You can use `method` and never use `proc`. There is although a little bit of overhead in terms of using `method`. But for most applications, you can ignore them.

> Note: Dynamic dispatch using `method` only works with `ref` object

## Calling super using `procCall`

```nim
type Thing = ref object of RootObj

type Unit = ref object of Thing
    x: int

method m(a: Thing) {.base.} =   # must annotate base implementation with .base.
  echo "base"

method m(a: Unit) =
  # Call the base method:
  procCall(m(Thing(a)))         # call super method m
  echo "1"
```

`procCall` means call the super method. Its call `procCall` because instead of doing dynamic call, it means use `proc` like lookup and call super

### For more dope on OOPS

http://goran.krampe.se/2014/11/30/nim-and-oo-part-iv/

