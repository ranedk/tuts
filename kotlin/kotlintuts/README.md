# Why Kotlin?

- Its java with much-much better syntax
- Java + C# = Kotlin as a programming language construct
- Only other language that words natively on Android
- It compiles to JS (someday, can potentially replace TypeScript)
- Can also help you write DSLs
- Native Kotlin (llvm) will someday get rid of JVM and could possibly be one language to rule them all
- Manages `null` better than Java

# Installation
```bash
$ curl -s https://get.sdkman.io | bash
$ sdk install kotlin
```

## Hello world!
Create a file named `hello.kt`
```kotlin
package learn.kotlin

fun main(args: Array<String>) {
    println("Lets get started with Kotlin!")
}
```
To compile and execute code:
```bash
$ kotlinc hello.kt -include-runtime  -d hello.jar
$ java -jar hello.jar
```

Start a kotlin repl using `kotlinc`

# How to learn

Valid Java is valid Kotlin. So think java, write kotlin.
The syntactical sugar is very Java 9ish and better.
Its also a little pythonic.

# What is null pointer exception?

Without initializing the object, we end up running a method on it.
```
    Object obj = null
    print(obj.length)  // NullPointerException
```

You can initialize the object to a default value, but it will give rise to another set of bugs.
The right way to manage NullPointerExceptions is to check it every time.  Kotlin provides a much better way.

## Type system
| <type> |    <bit width> |
| --- | --- |
|Double |     64 (default decimal is Double)|
|Float  |     32|
|Long   |     64|
|Int    |     32 (default number is Integer)|
|Short  |     16|
|Byte   |     8|

```kotlin
// Explicit declaration
var long: Long = 1234L
var hexadecimal: Int = 0xFFFFFF
var binary:Int = 0b0000111100001111
var double:Double = 10e2
var float:Float = 3.143F

// Inferred declaration
var long = 1234L                    // Inferred Type: Long
var hexadecimal = 0xFFFFFF          // Inferred Type: Integer (from hexadecimal)
var binary = 0b0000111100001111     // Inferred Type: Int (from binary)
var double = 10e2                   // Inferred Type: Double
var float = 3.143F                  // Inferred Type: Float

// Using underscores for readability
val oneMillion = 1_000_000
val creditCardNumber = 1234_5678_9012_3456L         // Inferred type: Long
val socialSecurityNumber = 999_99_9999L
val hexBytes = 0xFF_EC_DE_5E                        // Inferred type: Int (from hexadecimal)
val bytes = 0b11010010_01101001_10010100_10010010   // Inferred type: Int (from binary)

/*
Boxed numbers (Nullable reference)
Number will be in stored as primitive types in JVM
However, to manage nullable numbers better (the dreaded NullPointerException),
Kotiln provides nullable number reference which is "Boxed" inside an object
*/

val nonNullable:Int = 1000      // primitive type
val boxedNullable:Int? = 1000   // Boxed type

print(nonNullable == boxedNullalble)     // equality check -> prints true
print(nonNullable === boxedNullable)     // identity check -> prints false

/*
Type Conversions
smaller types are NOT implicitly converted to bigger ones
*/

val b1: Byte = 1
// val i1: Int = b1       !! ERROR
val i1: Int = b1.toInt()  // Correct way

/*
All number types support:
toByte()
toShort()
toInt()
toChar()
toFloat()
toDouble()
toLong()

// Operators will appropriate conversions based on inferred type
// <char> + <byte> = <char>
// <char> + <int> = ERROR!
```

## Type System

The objective of type system in Kotlin is to save us from getting NullPointerExceptions
So, the type system is designed to manage Nullable and non-Nullable things properly

All classes have a super class `Any`. Its the base class if not mentioned.

`Unit` type is like void in Java
If a function returns "no value" it returns `Unit`
`Unit` is proper type with a "singleton instance" also referred to as Unit or ()

This is for consistency, so all functions have something to return
- if they return nothing then they are returning Unit)
- there is always some argument that they will take (if nothing, then its Unit)

e.g. Unit can be mentioned explicitly as
```kotlin
    fun doSomething(): Unit {
        Log.d("Hello", "World")
    }
```

Kotlin also has `Nothing`, the *sub class* of all types (It means a value that never exists)

*What does it mean?*
A function which goes into a loop or throws an exception, essentially returns Nothing (if it returns nothing, it returns Unit, but if it always throws an exception or goes into a loop, then it returns Nothing
```kotlin
fun fail() {
    throw RuntimeException("Something went wrong")
}

val data = intent.getStringExtra("key") ?: fail()
textView.text = data
```
if `fail()` returns nothing, then data becomes `Unit` and it will throw error when you try assigning textView.text to data, since it expects a `CharSequence`
if `fail()` returns `Nothing`, then data becomes a subtype of `String` called `Nothing` and it works without throwing a NullPointerException
So the return type of fail() should be `Nothing`

>Note: If you want to create a immutable list of empty Strings e.g.return someInputArray?.filterNotNull() ?: emptyArray()
> Instead of creating a empty list of Nulls and then getting into NullPointer hell, use emptyList or emptyArray, which creates a list/array of "Nothing", which can be used to assign to a pointer expecting a list of String

## Operators

| Operator | Doc |
| --- | --- |
|shl(bits) | signed shift left (Java's <<)|
|shr(bits) | signed shift right (Java's >>)|
|ushr(bits) | unsigned shift right (Java's >>>)|
|and(bits) | bitwise and|
|or(bits) | bitwise or|
|xor(bits) | bitwise xor|
|inv() | bitwise inversion|

## Characters

*Single quotes for characters literals*
Escaping special characters '\n', '\r', '\uFF00'

## Booleans
Operators - ||, &&, !

## Arrays
Base Class exposing following methods:
- get
- set
- iterator (all overridable)

Templated array type: used as Array<TYPE>

```kotlin
// arr type is inferred as Int array
val arr1 = arrayOf(1, 3, 5, 7, 9)

// explicit type
val arr2: Array<Int> = arrayOf(1, 3, 5, 7, 9)

// !! ERROR: Wrong type, no conversion here from int to float
val arr: Array<Float> = arrayOf(1, 3, 5, 7, 9)

// Right
val arr3: Array<Float> = arrayOf(1F, 3F, 5F, 7F, 9F)

// asc inferred type is Array<Int>
val asc1 = Array(5, { i -> (i*i) })

// asc inferred type is Array<String>
val asc2 = Array(5, { i -> (i*i).toString() })

// explicit declaration
val asc3:Array<String> = Array(
        5, { i -> (i*i).toString() }
)
```

### Specialized Arrays of primitive types are provded by Kotlin
- IntArray
- FloatArray
- StringArray etc.

These have NO RELATION to Array<TYPE> and are completely separate implementations (also unboxed, so no boxing overheads)

```kotlin
var irr1:IntArray = intArrayOf(1, 2, 3, 4, 5)   // explicit IntArray
var irr1 = intArrayOf(1, 2, 3, 4, 5)            // inferred IntArray

// var frr1 = floatArrayOf(1, 2, 3, 4, 5)       # !! ERROR, no type conversions
var frr1 = floatArrayOf(1F, 2F, 3F, 4F, 5F)     // Correct way

var irr2:Array<Int> = arrayOf(1, 2, 3, 4, 5)    // Array<Int>
```
> Note: irr1 and irr2 have two *completely different* types

## Strings
- Immutable (why? hashmaps, concurrency, a lot of settings (db name etc) is in strings
- Characters forming String can be accessed by indexing
- Can loop over them
- Double quotes (escape special)
- Triple quotes (no escaping with backslashes)

```kotlin
var c1 = "Hello\nWorld"
var c2 = """Hello
World"""               // Indentation is a problem here, I know!

print(c1 == c2) // True

// Indentation solution!

val st1 = """Twinkle twinkle
little star
how I wonder
what you are"""

val st2 = """Twinkle twinkle
        >little star
        >how I wonder
        >what you are""".trimMargin(">")

// trimMargin() : remove leading characters (prefix default '|' )

print(st1 == st2) // True
```

### String templates
`${<expression>}` inside a string will run expression

```kotlin
val num = 10
val snum = "num = $num"
print(snum)            // prints> num = 10

var alp = "abcd"
var stxt = "$alp.length is ${alp.length}"
print(stxt)            // prints> abcd.length is 4
```

# Control Flow

## Single line if else
```kotlin
    var a = 10
    var b = 20
    val max1 = if (a > b) a else b
    print(max1)              // prints > 20
```

## if else - auto return
```kotlin
val max2 = if(a > b) {
    print("Choose $a")
    a                       // Cool! returns a to max
} else {
    print("Choose $b")
    b                       // Cool! returns b to max
}
print(max2)
```
> Note: If value of `if` expression is getting assigned to something it should have an `else` otherwise its an error (this is a another cool thing to avoid nulls)

## When statement/expression - Powerful Switch-Case

As a statement
```kotlin
var x = 3
when(x) {
    1 -> print("x == 1")
    2 -> print("x == 2")
    else -> {
        print("x is not 1 or 2")
    }
}
```

As an expression
```kotlin
var x = 2
var d = when(x) {
    1 -> 10
    2 -> 20
    else -> 0
}
```
> Note 1: Only first satisfying condition is picked rest are ignored
> Note 2: If value of when expression is getting assigned to something it MUST have an `else`

Arbitary expressions
```kotlin
when(x) {
    in 1..10 -> print("x is in range")
    !in 10..20 -> print("x is in big range")
    0, 1 -> print("x is 0 or 1")
    parse(x) -> print("x parsed")
    is String -> print("X starts with pre? ${x.startsWith("prefix")}")  // Smart casting x into string
    else -> print("WTF")
}
```

> Note 3: Everytime we check in `if-else` or `when` using `is` operator, *SMARTCASTS* happen and you can use all object methods inside that code block

When w/o arguments - Can be used as if-elseif-if-else
```kotlin
when {
    x.isOdd() -> print("x is Odd")
    x.isEven() -> print("x is Even")
    else -> print("x is Ghost")
}
```

## For Loops

```kotlin
var collection = intArrayOf(10, 20, 30, 40, 50)
for(item in collection) print(item)

for(item:Int in collection) {
    print(item)
}
```
`Collection` for a `type` is any class which:
- Has member or extension-function `iterator()` which returns a `type`
- Has member or extension-function `next()` and `hasNext()`

```kotlin
for(i in collection.indices) {
    print(collection[i])
}

for((index, value) in collection.withIndex()) {
    println("The element at $index is $value")
}
```

## while and do..while loops
```kotlin
var itr = 10
while(itr > 0) {
    println(itr--)
}

var itr = 10
do {
    println(itr)
} while(itr != 0)
```

### `break` and `continue` work as expected but work *better* with `LABELS`
```kotlin
outer@ for(i in 1..10) {
    for(j in 1..10) {
        if((i == 5) && (j==5)) {
            break@outer
        }
        print("($i, $j)")
    }
}
```
"return" gives control back to nearest enclosing function
```kotlin
fun foo() {
    ints.forEach {     // List comprehension
        if (it == 0) {
            return
            // nonlocal return from inside lambda directly to the caller of foo()
        }
        print(it)
    }
}
```
However, in the case above, you want the return to go back to the forEach loop, Alternatives:
```kotlin
fun foobar() {
    ints.forEach lit@ {
        if (it == 0) return@lit
        print(it)
    }
}

// OR

fun foobear() {
    ints.forEach(fun(value: Int) {
        if (value == 0) {
            return
            // local return to the caller of the anonymous fun, i.e. the forEach loop
        }
        print(value)
    })
}
```
> Note: If return wants to return a value use "return@<label> <value>"

# Functions

```kotlin
fun getLowerName(name: String): String {
    return name.toLowerCase()
}

// Cool Shortcut
// Use these to define local functions which are short
fun getLowerName2(name: String): String = name.toLowerCase()
```

### Named Parameters

`fun deleteFiles(filePattern: String, recursive: Boolean, ignoreCase: Boolean, deleteDirectories: Boolean): Unit`

Compare the two different styles of calling this function:
`deleteFiles("*.jpg", true, true, false)`
`deleteFiles("*.jpg", recursive = true, ignoreCase = true, deleteDirectories = false)`
> Rule: Once you have named one parameter, all subsequent ones need to be named

Default parameters work the regular way

### `VarArgs` : Python like, but better

```kotlin
fun multiprint(prefix: String, vararg strings: String, suffix: String): Unit {
    println(prefix)
    for (string in strings)
        println(string)
    println(suffix)
}
// Usage: suffix is always named
multiprint("Twinkle", "Twinkle", "Little", suffix="Star!")
```

### Spread operator : behaves like * in python, when you pass array to function
```kotlin
val strings = arrayOf("Twinkle", "Twinkle", "Little", "Star!")
multiprint("Start", *strings, suffix = "End")
```

### `Apply` : To apply a method of an instance and mimic chaining

```kotlin
// Regular java code
val task = Runnable { println("Running") }
val thread = Thread(task)
thread.setDaemon(true)
thread.start()

// Kotlin code
val task = Runnable { println("Running") }
val thread = Thread(task).apply { setDaemon(true) }.start()
```

### `let` the magic begin
```kotlin
File("a.txt").let { it ->
    // the file is now in the variable "it"
}
```

This is very useful when you want to execute a code only if there are non-nullable values. for e.g.
```kotlin
findUser(id)?.let {
    // only run if findUser() returned a non null value
}
```

This is awesome, since you are not using a variable to store the output of fileUser and then check it for nullability
Another form is:
```kotlin
findUser(id)?.let { user ->
    user.apply {
        sendMail()
        markEvent()
    }
    // only run if findUser() returned a non null value
}
```
### `with` statements : Take a instance and inside the closure to apply all methods on the instance
```kotlin
val instance = with(instance) {       // Optional to assign the output to anything
    instanceMethod1()
    instanceMethod2()
    instanceMethod3()
    this                              // return the same back - Also Optional
}

# Also, achieved by

val instance = Class().apply {
    instanceMethod1()
    instanceMethod2()
    instanceMethod3()
}
```

### `run` statements: This is a combo of `with` and `let`
Confused between let, with, run etc. Refer:
https://medium.com/@tpolansk/the-difference-between-kotlins-functions-let-apply-with-run-and-else-ca51a4c696b8

### lazy evaluation
Run only when accessed or used
```kotlin
fun readStringFromDatabase(): String = ... // expensive operation
val lazyString = lazy { readStringFromDatabase() }

val string = lazyString.value
```

### `repeat`
```kotlin
repeat(10, { println("Hello") })  // second argument is a lambda
```

### require/assert/check

Require: throws an exception and it is used to ensure that arguments match the input conditions
Assert: throws an AssertionException exception and it is used to ensure that our internal state is consistent
Check: throws an IllegalStateException exception and it is also used for internal state consistency

# Generic functions
If we have a function for which we don't want to restrict the type of
objects that it can take as input and output, there are two way to do it.

```kotlin
    fun generic_fun1(param1: Any, param2: Any, param3:Any): Any {
        println("Do something with param1, param2, param3")
    }
```
Casting Rule:
    - Sub-types can be casted to Super-types
    - Super-type cannot be casted to a sub-type

This works because any input parameter will be cast into `Any`

However, the output type will always be "Any", which cannot be casted into anything else (run time exception ClassCastException)

The way to solve this is using Generics in functions
```kotlin
fun <T> generic_fun2(param1: T, param2: T, param3: T): T {
    println("Do something with param1, param2, param3")
    return param1
}

fun <K, V> generic_fun3(param1:K, param2:V): V {
    println("Do something with param1, param2")
    return param2
}

//Usage:

generic_fun2(10, 11, 12)    // inferred type is Int
```

> Note: If you are new to generics, using `param1: Any` or `param1: T`, we can only call those methods on param1 which are defined in `Any` or `T`, Since `T` is the most generic template, its just another way to say `Any`

```kotlin
fun <T> gen_fun(param1: T, param2: T) = param1 + param2   // Compile time error
# Error, since "plus" is not defined for "Any"

fun <T> gen_fun(param1: T, param2: T) = param1.toString() + param2.toString()
# Works, since "toString" is defined in "Any"
```

The real use case is with upper-bounds. We can tell the compiler that T can be of one and more possible types
```kotlin
fun <T : Comparable<T>>min(first: T, second: T): T {
    val k = first.compareTo(second)
    return if (k <= 0) first else second
}

# Usage:
min(5, 8)
min(5, "8")     // Error, both have to be of same time
```
Method min will take any object which extends Comparable interface (gives a compareTo method)
Anything else will give compile time error

You can specify multiple bounds too
```kotlin
fun <T>minSerializable(first: T, second: T): T
        where T : Comparable<T>, T : Serializable {
    val k = first.compareTo(second)
    return if (k <= 0) first else second
}
```

Generic functions can use generics to do generic list things
```kotlin
fun <E> drop(k: Int, list:List<E>): List<E> {
    val newSize = list.size - k
    when {
        newSize <= 0 -> return emptyList<E>()
        else -> {
            var newList = ArrayList<E>(newSize)
            for(index in k..list.size){
                newList.add(list[index])
            }
            return newList
        }
    }
}
```
The above is the good old java style, we can do better in kotlin by writing an extension.
The problem with this approach is chaining, we will do reverse(take(3, drop(2, list))), to do it the better way list.drop(2).take(3).reverse(), we do the following
```kotlin
fun <E> List<E>.drop(k: Int): List<E> {
    val resultSize = size - k
    when {
        resultSize <= 0 -> return emptyList<E>()
        else -> {
            val list = ArrayList<E>(resultSize)
            for (index in k until size - 1) {
                list.add(this[index])            // this refers to the calling list
            }
            return list
        }
    }
}
```
You can define extension functions inside a class in which case they will be available only inside the class

## Infix functions: When the operator is placed in the middle, e.g.
```kotlin
infix fun String.goingTo(toPlace:String): String {
    println("Going from ${this} to ${toPlace} now")
}

// Usage
val whatYouDoing = "Mumbai" goingTo "Delhi"
```

## Operator overloading
Operators are defined as class methods with operator keyword.  You can overload only specific operators with method names as below

| Operation | Function name|
| --- | --- |
| a + b | a.plus(b) |
| A – b | a.minus(b) |
| A * b | a.times(b) |
| A / b | a.div(b) |
| A & b | a.mod(b) |
| a..b | a.rangeTo(b) |
| +a  | a.unaryPlus() |
| -a | a.unaryMinus() |
| !a | a.not() |

Example implementation on Matrix plus operator
```kotlin
class Matrix(val a: Int, val b: Int, val c: Int, val d: Int) {
    operator fun plus(matrix: Matrix): Matrix {
        return Matrix(a + matrix.a, b + matrix.b, c + matrix.c, d +
                matrix.d)
    }
}

// Usage
val m1 = Matrix(1, 2, 3, 4)
val m2 = Matrix(5, 6, 7, 8)
val m3 = m1 + m2
```
## Special operators

*in/contains* : `3 in arrayOf(1, 2, 3)` equivalent to `arrayOf(1, 2, 3).contains(3)`
*[]* operator is implemented using `get` and `set`
Example:
```kotlin
enum class Piece {
    Empty, Pawn, Bishop, Knight, Rook, Queen, King
}
class ChessBoard() {
    private val board = Array<Piece>(64, { Piece.Empty })

    operator fun get(rank: Int, file: Int): Piece = board[file * 8 + rank]

    operator fun set(rank: Int, file: Int, value: Piece): Unit {
        board[file * 8 + rank] = value
    }
}

// Usage:

val board = ChessBoard()
board[0, 4] = Piece.Queen
println(board[0, 4])
```

## Comparison operators
- All operators `>, >=, <, <=` require `compareTo` to be implemented
- This function must return an `Int` and must be consistent with the Comparator interface in Java.
Example
```kotlin
class BingoNumber(val name: String, val age: Int) {
    operator fun compareTo(other: BingoNumber): Int {
        return when {
            age < other.age -> -1
            age > other.age -> 1
            else -> 0
        }
    }
}

// Usage
val a = BingoNumber("Key to the Door", 21)
val b = BingoNumber("Jump and Jive", 35)
println(a < b) // true
println(b > a) // false
```

## Assign operators
 | Operation | Function name |
 | --- | --- |
 | a += b | a.plusAssign(b) |
 | a -= b | a.minusAssign(b) |
 | a \*= b | a.timesAssign(b) |
 | a /= b | a.divAssign(b) |
 | a %= b | a.modAssign(b) |

This is super cool, I can actually create classes with complex assign operators on them
Example
```kotlin
class Counter(var k: Int) {
    operator fun plusAssign(j: Int): Unit {
        k += j
    }
}
var counter = Counter(1)
counter += 2
```
> NOTE: All operator overloading works from Java to Kotlin if function signatures match, (since Java has no operator overloading, the function name and signature is matched to determine if it can be used in Kotlin as an operator

# Function literals : Simple functions
To define a function we can put an expression between { } and it becomes a function
```kotlin
val printSomething = { print("Something")}
printSomething()
```

If Function literals need a input:
```kotlin
    val ldouble = { n: Int -> n * n}
    ldouble(2)
    // If Kotlin can infer "n"'s type, you don't have to define the type
```

# Tail recursion

There are multiple ways to write a recursive function. However, if a recursive function
keeps a stack of all the calls before it, then its not very memory efficient.
A tail recursion is when a recursive function's last call is a call to the same function
so that the compiler need not maintain a stack.
To tell the compile not to keep a stack, we use the keywork tailrec

Factorial recursive implemented bad
```kotlin
fun factorial(k: Int): Int {
    if (k == 0) return 1
    else return k * fact(k - 1)         // Still need to keep the function call on stack
                                        // because the result needs to be multiplied
}
```

```kotlin
fun factorialImproved(k: Int): Int {
    tailrec fun factTail(m: Int, n: Int): Int { // tell the compiler to not maintain a stack
        if (m == 0) return n
        else return factTail(m - 1, m * n)  // Function keep calling itself, no stack required
    }
    return factTail(k, 1)
}
```
# Companion
Lets first understand `static classes` in Java.
In a scenario where an _Outer class_ has an _Inner class_, each instance of _outer class_ will have a _inner class definition_ and to create an _instance of the inner class_, you need to create a _instance of the outer class_, then use it to create an _instance of the inner class_.

If the _inner class_ is marked static, there is only one instance of the _inner class definition_. To create an instance of _inner class_, you dont have to create an _instance of outer class_ and directly use the _outer class_ to create an _instance of inner class_.

```java
class OuterClass {
   private static String msg = "GeeksForGeeks";

   // Static nested inner class
   public static class NestedStaticClass {

       // Only static members of Outer class is directly accessible in nested static class
       public void printMessage() {

         // Try making 'message' a non-static variable, there will be
         // compiler error
         System.out.println("Message from nested static class: " + msg);
       }
    }

    // non-static nested class - also called Inner class
    public class InnerClass {

       // Both static and non-static members of Outer class are accessible in this Inner class
       public void display() {
          System.out.println("Message from non-static nested class: "+ msg);
       }
    }
}

class Main {
    // How to create instance of static and non static nested class?
    public static void main(String args[]) {

       // create instance of nested Static class
       OuterClass.NestedStaticClass printer = new OuterClass.NestedStaticClass();

       // call non static method of nested static class
       printer.printMessage();

       // In order to create instance of Inner class we need an Outer class
       // instance. Let us create Outer class instance for creating
       // non-static nested class
       OuterClass outer = new OuterClass();
       OuterClass.InnerClass inner  = outer.new InnerClass();

       // calling non-static method of Inner class
       inner.display();

       // we can also combine above steps in one step to create instance of
       // Inner class
       OuterClass.InnerClass innerObject = new OuterClass().new InnerClass();

       // similarly we can now call Inner class method
       innerObject.display();
    }
}
```
In case of kotlin, the `companion` keyword create a `static` inner class and if there is no name of the class, exposes it as a class named `Companion`

