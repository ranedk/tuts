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

proc refDecr*(e: ref Employee) =
  e.salary = int(0.8 * float(e.salary))

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

#> Note: If you have a reference, you will ALWAYS be able to mutate the instance

e3.name = "Abhiruchi Chand"
e3.age = 28
e3.salary = 2_00_000

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
    revenue: float

func revenueProjection*(e: Employer) =
    e.revenue = 1.2 * e.revenue

# Creates company as a reference to Employer instance
let company = Employer(name: "Dunded mifflin", city: "Mumbai", revenue: 1_00_00_000)
company.revenueProjection()
echo "company revenue projection > ", company.name, " | ", company.city, " | ", company.revenue