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

proc salaryProjection(e: Employee): int =
  return int(1.2 * float(e.salary))


# variable employee - created on stack
var e1 = Employee(name: "Devendra rane", age:30, salary: 1_00_000)
e1.name = "Devendra K rane"
e1.increment()
echo "e1 = ", e1

# immutable Employee - created on stack
let e2 = Employee(name: "Nihira rane", age:3, salary: 10)
# e2.increment()  # ERROR: Invalid, increment expects a variable
echo "e2 salary projection = ", e2.salaryProjection()


# Create a reference to the Employee on stack after allocation in heap
let e3: ref Employee = new(Employee)

e3.name = "Abhiruchi Chand"
e3.age = 28
e3.salary = 2_00_000

echo "e3 = ", e3.name, " | ", e3.age, "|",  e3.salary
echo "e3 = ", e3.name, " | ", e3.age, "|",  e3.salary