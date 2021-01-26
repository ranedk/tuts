# Object oriented or something like that


**Declaring a class**

```nim
type Employee* = object
    name*, department*: string
    age: int
    salary: int

proc increment*(e: var Employee) =
  e.salary = int(1.2 * e.salary)

proc decrement*(e: var Employee) =
  e.salary = int(0.8 * e.salary)
```

**Usage**

```nim

# variable employee
var e1 = Employee(name: "Devendra rane", age:30, salary: 1_00_000)
e1.name = "Devendra K rane" # valid
e1.increment()
echo "e1 = ", e1

let e2 = Employee(name: "Nihira rane", age:3, salary: 10)

```
