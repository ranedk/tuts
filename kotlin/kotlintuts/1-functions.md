# Functions in kotlin
With kotlin, we get lambdas and higher order functions

```kotlin
val ints = listOf(1, 2, 3, 4, 5, 6)
val odds = ints.filter({ it % 2 == 1 })     // Lambda: higher order function
val evens = ints.filter { it % 2 == 0 }     // filter takes lambda, parenthesis optional

// Anonymous functions: leave the name
val evens = ints.filter(fun(k: Int) = k % 2 == 0) // using anonymous functions

// Signature of a function which takes another function
fun foo(str: String, fn: (String) -> String): Unit {    // (String) -> String
    val applied = fn(str)
    println(applied)
}

//Returning a function
fun modulo(k: Int): (Int) -> Boolean = { it % k == 0 }  // returning a lambda

// Usage
val ints = listOf(1, 2, 3, 4, 5, 6)
val odd = ints.filter(modulo(1))
val evens = ints.filter(modulo(2))

val isEven: (Int) -> Boolean = modulo(2)  // hold function in a variable, that is lambda
listOf(1, 2, 3, 4).filter(isEven)         // filter expects a variable or a lambda
// OR
val evens2 = ints.filter{ it -> it % 2 == 0}   // explicit input
// OR
val evens3 = ints.filter{it % 2 == 0}     // Input optional (`it` is generic for all loops and lambdas)
```

## Multiple ways to define the variable
>NOTE: there is not `fun` prefix, its `val`)

```kotlin
// `valEven` is defined as a function reference, instead of a function
val valEven: (Int) -> Boolean = modulo(2)  // hold function in a variable
// OR
val valEven : (Int) -> Boolean = { it % 2 == 0 }
// OR
val valEven = { k : Int -> k % 2 == 0 }

// `funEven` is defined as a function
fun funEven(k: Int): Boolean = k % 2 == 0

// `filter` takes function reference
listOf(1, 2, 3, 4).filter(valEven)

// !! ERROR
listOf(1, 2, 3, 4).filter(funEven)

// You need to use:
(1, 2, 3, 4).filter{ funEven(it)}

//OR

listOf(1, 2, 3, 4).filter(::funEven)
```
> Note: `val` creates a function reference, `fun` creates a function. To convert a function, into a reference use `::`

## Member or extension functions reference
A function which takes 3 params, the last one is a function
```kotlin
fun foo(a: Double, b: Double, f: (Double, Double) -> Double) = f(a, b)

// Regular way:
foo(1.0, 2.0, { a, b -> Math.pow(a, b) })

// Kotlin way:
foo(1.0, 2.0, Math::pow )   // pass the reference of Math.pow
```
## Extension function:
```kotlin
fun Int.isOdd(): Boolean = this % 1 == 0

// First way
ints.filter { it.isOdd() }    // Actually calling the method

// Another way:
ints.filter( Int::isOdd )     // Passing a reference
```
## What if the function is bound to a instance, like compare
```kotlin
// Note: this keyword
fun String.isSameAs(other: String) = this.toLowerCase() == other.toLowerCase()

// The bound function's arity doesn't match because its bound.
// First way, create an unbound reference:

listOf("foo", "moo", "boo").filter {
    (String::isSameAs)("bar", it)   // Notice the parenthesis around String::isSameAs
}

// The kotlin way:
listOf("foo", "baz", "BAR").filter("bar"::isSameAs) // "bar" get bound to this
```

*Receiver* of a function is the instance corresponds to the "this" keyword

In Kotlin, function parameters can be defined to accept a receiver when they are invoked. We do that using the following syntax:

```kotlin
fun foo(fn: String.() -> Boolean): Unit {    // function which takes a function as an argument
            "stringReceiver".fn()            // which must be a extension method of a string
}
```

## Coolness
Awesome kotlin has some real coolness. Function literals (statements between {}) are very helpful for higher order functions. If a function takes its last input parameter as a function, you can define it as a function literal.
```kotlin
fun <T, U> withPrint(res: T, fn: (T) -> U): U  {  // function's second input is a function fn
    return fn(res)
}

fun cprint(str: String): Int {                    // a sample function
    println("Printing string inside cprint: ${str}")
    return str.length
}

withRes("Kotlin is cool", ::cprint)     // this is fine, very predictable

var str1 = "Kotlin is awesome"
var len1 = withRes(str1) {              // using function literals, the last input function
    print("Inside nowhere: ${str1}")    // is auto-magically used with a cool syntax!
    str1.length
}
print("Length of str ${len1}")
```
#### When do you use this cool feature

Function that handles resources in a safe manner: that is, the resource will always be closed correctly, even if the code throws an exception
```kotlin
fun <T: AutoCloseable, U> withResource(resource: T, fn: (T) -> U): U {
    try {
        return fn(resource)
    } finally {
        resource.close()
    }
}

// Usage:
fun characterCount(filename: String): Int {
    val input = Files.newInputStream(Paths.get(filename))
    return withResource(input) {
        input.buffered().reader().readText().length
    }
}
```
This works great, however functions in kotlin are first-class objects, hence they are implemented as classes in JVM, if the above code is used tons of times it will end up creating tons of objects. So its better if its just a function

To tackle this optimization, use the work "inline". Makes sure that JVM treats them as functions
```kotlin
inline fun <T: AutoCloseable, U> withResourceImproved(resource: T, fn: (T) -> U): U {
    try {
        return fn(resource)
    } finally {
        resource.close()
    }
}
```
The inline modifier affects both the function itself and the lambdas passed to it. All of those will be inlined into the call site, so the generated code size increases but the efficiency advantages are huge

If you want a function that is being passed to an inline function to not be inlined during
code generation use the word "noinline" e.g.
```kotlin
inline fun <T : AutoCloseable, U, V> withResourceNew(resource: T, before: (T) -> U, noinline after: (U) -> V): V {
    val u = try {
        before(resource)
    } finally {
        resource.close()
    }
    return after(u)
}
```

## Memoization: Caching calls from a function

Lets look at a different implementation of fibonacci
```kotlin
fun fib(k: Int): Long = when (k) {
    0 -> 1
    1 -> 1
    else -> fib(k - 1) + fib(k - 2)
}
```
Multiple calls will be made to the same parameters, we should cache them. EASY.
```kotlin
val map = mutableMapOf<Int, Long>()
fun memfib(k: Int): Long {
    return map.getOrPut(k) {
        when (k) {
            0 -> 1
            1 -> 1
            else -> memfib(k - 1) + memfib(k - 2)
        }
    }
}
```
#### Generic memoization implementation
```kotlin
fun <A, R> memoize(fn: (A) -> R): (A) -> R {
    val map = ConcurrentHashMap<A, R>()
    return { a ->
        map.getOrPut(a) {
            fn(a)
        }
    }
}

// Usage
// Suppose "query" is a function, which needs to be memoized.
val memquery = memoize(::query)
```

A much smart Kotlin way would be to make it as a extension function on a function!
```kotlin
fun <A, R> Function1<A, R>.memoized(): (A) -> R {
    val map = ConcurrentHashMap<A, R>()
    return {
        a -> map.getOrPut(a) {
        this.invoke(a)              // this calls the receiver which is a function
    }
    }
}

// Usage:
val memquery = ::query.memoized()
```
> Note: `invoke` keyword. Calls the function via the receiver

# TypeAlias: like Elm

This makes the whole thing more readable, when you give types to existing simple and complex types
```kotlin
// Simple:
typealias Width = Int
typealias Length = Int
typealias Height = Int
fun volume(width: Width, length: Length, height: Height): Int

//Complex:
typealias Cache = HashMap<String, Boolean>
typealias HttpExchange = Exchange<HttpRequest, HttpResponse>

// Usage
fun process2(exchange: HttpExchange): HttpExchange
```
They are simple replaced in the generated code


# Functional concepts:
Imagine a scenario when there is a function call which can return 2 types to values. Since in the function definition, you can only return one type of value, you define a composite type which can have 2 types of values. If the function returns the first type, the second is `Nothing` and vice-versa

In functional languages there is a concept of "Either" object. It can have two values only (Left and Right (where Left is Null or Error, Right is Success) and based on the value, further "fold" happens, that is, we call two different functions depending on the value of Either(Null/Error or Success)

Lets implement "Either" in Kotlin
```kotlin
sealed class Either<out L, out R>                   // Either defined with L and R types
class Left<out L>(value: L): Either<L, Nothing>()   // Either when R is Nothing
class Right<out R>(value: R): Either<Nothing, R>()  // Either when L is Nothing

// Lets implement fold inside Either class

sealed class Either<out L, out R> {
    fun <T> fold(lfn: (L) -> T, rfn: (R) -> T): T = when (this) {
        is Left -> lfn(this.value)      // When Either is Left, call lfn
        is Right -> rfn(this.value)     // When Either is Right, call rfn
    }
}

// Usage:

class User(val name: String, val admin: Boolean)
object ServiceAccount
class Address(val town: String, val postcode: String)

fun getCurrentUser(): Either<ServiceAccount, User> = ... // Gets User from a service
fun getUserAddresses(user: User): List<Address> = ...    // Gets Address from a service

// getCurrentUser returns a `ServiceAccount` if its a anonymous user, else the current user

val addresses = getCurrentUser().fold({
        emptyList<Address>()
    }, {
        getUserAddresses(it)
    }
)
```
Gives a super clean API

# Projections
If you want to attach cool functional stuff like map, filter to "Either", we can do that.
This looks complicated so look carefully.

Just that way we implemented "fold" in "Either", we need to implement projections so that dependent on Left or Right, we can call a projection on it or just ignore it. That is, we decide that for leftProjections, we will call proper map, else we will ignore or vice-versa.

Updated `Either` class:
```kotlin
sealed class Either<out L, out R> {
    fun <T> fold(lfn: (L) -> T, rfn: (R) -> T): T = when (this) {
        is Left -> lfn(this.value)
        is Right -> rfn(this.value)
    }
    fun leftProjection(): Projection<L> = when (this) { // If we ask for leftProjection, and we get Right
        is Left -> ValueProjection(this.value)          // value, then do noOp
        is Right -> EmptyProjection<L>()
    }
    fun rightProjection(): Projection<R> = when (this) {
        is Left -> EmptyProjection<R>()
        is Right -> ValueProjection(this.value)
    }
}
```
The way we will choose to implement this is to create two projection subclasses:
The ValueProjection will implement the functions (map, filter etc.)
The EmptyProjection will implement no-ops.

As implemented above, dependent on which projection (left or right), Value and Empty
projections will be executed

Projection supertype:
```kotlin
sealed class Projection<out T> {
    abstract fun <U> map(fn: (T) -> U): Projection<U>
    abstract fun getOrElse(or: () -> T): T
}
```

We're going to start with two functions for now: map , which will transform the value if the projection is one we are interested in, and getOrElse , which will return the value or apply a default function.
```kotlin
class ValueProjection<out T>(val value: T) : Projection<T>() {
    override fun <U> map(fn: (T) -> U): Projection<U> =
        ValueProjection(fn(value))
    override fun getOrElse(or: () -> T): T = value
}

class EmptyProjection<out T> : Projection<T>() {
    override fun <U> map(fn: (T) -> U): Projection<U> =
            EmptyProjection<U>()
    override fun getOrElse(or: () -> T): T = or()
}

fun <T> Projection<T>.getOrElse(or: () -> T): T = when (this) {
    is EmptyProjection -> or()
    is ValueProjection -> this.value
}
```
`getOrElse` is implemented as an extension function on Projection itself because the function signature requires that T is an output in the `or` function. Check the chapter on variance

```kotlin
// Usage:
val postcodes = getCurrentUser().rightProjection()      // Interested in rightProjection only
    .map { getUserAddresses(it) }
    .map { addresses.map { it.postcode } }
    .getOrElse { emptyList() }
// If the Either returned was not a Right value, then the maps would have no effect.
```


# Custom DSLs
Using `infix`, we can create pretty magical DSLs.
Lets try creating DSLs for testing framework
```kotlin
infix fun Any.shouldEqual(other: Any): Unit {
    if (this != other)
        throw RuntimeException("$this was not equal to $other")
}

// Usage: "foo" shouldEqual "bar"
listOfNames.contains("george") shouldEqual true

// But this looks sad, it should read more like:
listOfNames shouldContain "george"

infix fun <E> Collection<E>.shouldContain(element: E): Unit {
    if (!this.contains(element))
        throw RuntimeException("Collection did not contain $element")
}
// Usage: listOfNames shouldContain 10.0
```
How about: listOfNames shouldContain "george" or listOfNames should beEmpty()
`infix fun Unit.or(other: Unit): Unit`
would not work because our assertions throw an exception, the left-hand side could have already thrown an exception before or is invoked, meaning we can't catch it. In which case, we need to invoke the assertions after they have been combined.
At the same time, can we avoid duplicating the repeated left-hand side(listOfNames)?

Lets define a type called Matcher, which can help catch the exception and then apply "or" on it
```kotlin
// The interface
interface Matcher<T> {
    fun test(lhs: T): Unit
}

// The implementation for contain and beEmpty
fun <T> contain(rhs: T) = object : Matcher<Collection<T>> {
    override fun test(lhs: Collection<T>): Unit {
        if (!lhs.contains(rhs))
            throw RuntimeException("Collection did not contain $rhs")
    }
}
fun <T> beEmpty() = object : Matcher<Collection<T>> {
    override fun test(lhs: Collection<T>) {
        if (lhs.isNotEmpty())
            throw RuntimeException("Collection should be empty")
    }
}

// define "should" to run the matcher tests
infix fun <T> T.should(matcher: Matcher<T>) {
    matcher.test(this)
}

// Add "or" to the Matcher interface
interface Matcher<T> {
    fun test(lhs: T): Unit
    infix fun or(other: Matcher<T>): Matcher<T> = object : Matcher<T> {
        override fun test(lhs: T) {
            try {
                this@Matcher.test(lhs)
            } catch (e: RuntimeException) {
                other.test(lhs)
            }
        }
    }
}

// We can use the above to write
listOfNames should (contain("george") or beEmpty())

// Instead of defining an "and", we can also write
listOfNames should {
    contain("george")
    beEmpty()
}
```

### Validation and Error Accumulation

_Part 1_
Lets implement base class
```kotlin
sealed class Validation

object Valid: Validation()      // Valid is a singleton

class Invalid(val errors: List<String>) : Validation<Nothing>() {
    companion object {
        operator fun invoke(error: String) = Invalid(listOf(error))
    }
}
```
>Note: operator invoke gets call then you call the class e.g. Invalid("Error goes here") will call the invoke method

Implementating validation classes:
```kotlin
class Student(val name: String, val studentNumber: String, val String)

fun isValidName(name: String): Validation {
    return if (name.trim().length > 2)
        Valid
    else
        Invalid("Name $name is too short")
}
fun isValidStudentNumber(studentNumber: String): Validation {
    return if (studentNumber.all { Character.isDigit(it) })
        Valid)
    else
    Invalid("Student number must be only digits: $studentNumber")
}
fun isValidEmailAddress(email: String): Validation {
    return if (email.contains("@"))
        Valid
    else
        Invalid("Email must contain an '@' symbol")
}
```
_Part 2_
Lets implement error accumulation with plus operator
```kotlin
sealed class Validation {
    abstract infix operator fun plus(other: Validation): Validation
}
class Invalid(val errors: List<String>) : Validation() {
    companion object {
        operator fun invoke(error: String) = Invalid(listOf(error))
    }
    override fun plus(other: Validation): Validation = when (other) {
        is Invalid -> Invalid(this.errors + other.errors)
        is Valid -> this
    }
}
object Valid : Validation() {
    override fun plus(other: Validation): Validation = when (other) {
        is Invalid -> other
        is Valid -> this
    }
}

// Usage:
val validation = (
    isValidName(student.name) +
    isValidStudentNumber(student.studentNumber) +
    isValidEmailAddress(student.email)
)
```
