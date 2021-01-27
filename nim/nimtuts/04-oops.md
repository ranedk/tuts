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

# echo doesnt work with references :(
echo "e3 = ", e3.name, " | ", e3.age, "|",  e3.salary
# e3.decrement()  # ERROR: Invalid, decrement expects a variable, not a reference
e3.refDecr()
echo "e3 = ", e3.name, " | ", e3.age, "|",  e3.salary


# You can also create object which always returns a reference on initialization
type EmployeeRef* = ref Employee

let e4 = EmployeeRef(name: "Suresh", age: 20, salary: 1_000)
e4.refIncr()
# e4.increment()   # ERROR: Invalid, increment expects a variable, not a reference
echo "e4 = ", e4.name, " | ", e4.age, "|",  e4.salary

# You can also define an object which directly gives reference on initialization
type Employer = ref object
    name: string
    city: string

# Creates company as a reference to Employer instance
var company = Employer(name: "Dunded mifflin", city: "Mumbai")
```

> Note: If you have a reference, you will ALWAYS be able to mutate the instance.

# Dynamic and Static dispatch

**Dynamic dispatch**: TODO

`methods`
