# Packages
Top of the file contains the package declaration has nothing to do with the filename

```kotlin
package learn.kotlin.klass

fun baz() {}

class Goo() {}
```
Usage:
```kotlin
    import learn.kotlin.klass.*    // baz, Goo can be accessed directly
    import learn.kotlin.klass.baz  // baz accessible directly
    import learn.kotlin.klass.Goo  // Goo accessible directly

    import learn.kotlin.klass.Goo as Gao   // Goo available as Gao
```
# Class
To instantiate a class, no `new` keyword required

```kotlin
// the line directly below is the primary constructor, cannot contain any code
class PersonWithoutMembers constructor(firstName: String, age: Int?) {
    init {
        require(firstName.trim().isNotEmpty()) {"Invalid firstName"}
        if(age != null) {
            require(age in 0..100) {"Invalid age"}
        }
        println("Class body init part 1 ${firstName}");
    }

    // Class body
    // class member customerKey
    val customerKey = firstName.toUpperCase()

    init {
        println("Class body init part 2 ${firstName}")
    }

    // Class body
    // class member customerKeyHash
    fun normalName(): String = this.firstName.toLowerCase()
}
```
The above class Person, has a primary constructor.
`class PersonTypeOne constructor(var firstName: String, val age: Int?) {`
You can omit the constructor keyword (if there are no modifiers (discussed later))
`class PersonTypeOne(var firstName: String, val age: Int?) {`

If you want firstName and age to be class Members then, use `var` and `val` keywords in the constructor:
```kotlin
class PersonWithMembers constructor(var firstName: String, val age: Int?) {
    // Note the var and val
    // the class has firstName and age as its class members
    init {
        require(firstName.trim().isNotEmpty()) {"Invalid firstName"}
        if(age != null) {
            require(age in 0..100) {"Invalid age"}
        }
        println("Class body init part 1 ${firstName}");
    }

    // Class body
    // class member customerKey
    val customerKey = firstName.toUpperCase()

    init {
        println("Class body init part 2 ${firstName}")
    }

    // Class body
    // class member customerKeyHash
    fun normalName(): String = this.firstName.toLowerCase()
}
```
Usage:
```
var p1 = PersonWithoutMembers("Devendra", 20)
    p1.firstName        Error - Property does not exist
    p1.age              Error - Property does not exist
    p1.customerKey      Exists - "DEVENDRA"
    p1.normalName       Exists

var p2 = PersonWithMembers("Devendra", 20)
    p2.firstName        Exists - "Devendra"
    p2.age              Exists - 20
    p2.customerKey      Exists - "DEVENDRA"
    p2.normalName  Exists
```
# Visibility modifiers

- public (by default)
- private (visible only in the file containing the declaration
- internal (visible inside the package/module only)
- protected (visible in sub-classes, not file-level type of declaration)
    the sub-class can decide to override it and make it public
```kotlin
open class Container {
    // Cannot be accessed by Container instance
    protected open val fieldA: String = "Some value"
}
class DerivedContainer : Container() {
    // Can be accessed by DerivedContainer instance
    public override val fieldA: String = "Something else"
}
```
## Nested Class: Class inside a class
```kotlin
class Outer(param: String) {

    private val someField = 1
    private val myField = param
    public val alsoMyField = param.toUpperCase()

    fun method () {
        println("Method of Outer class")
    }

    class Inner {
        fun method() {
            println("Method of Inner class")
            println("Cannot access someField")
            println("Cannot access alsoMyField")
        }
    }

    inner class InnerWithPrivateAccess {
        private val myField = 20
        fun method() {
            println("Method of Inner class")
            println("Can access $someField")
            println("myField of InnerWithPrivateAccess ${this.myField}")
            println("myField of InnerWithPrivateAccess ${this@InnerWithPrivateAccess.myField}")
            println("myField of Outer ${this@Outer.myField}")
            println("alsoMyField of Outer ${this@Outer.alsoMyField}")
        }

    }
}
```
To declare objects of Inner class
`var inner = Outer.Inner()`

To declare objects of InnerWithPrivateAccess class
`var innerWPA = Outer().innerWithPrivateAccess()`

When do we use Nested Classes?
- Mostly used with anonymous classes (see advanced classes tutorial)

# Data classes (like Named tuples in python)
Frequently used classes which only need to hold data and no methods
```kotlin
data class Customer(val id:Int, val name:String, var address:String)

var c1 = Customer(1, "Dev", "some road, some gully")

println("Customer string is ${c1.toString()}")
// prints > Customer string is Customer(id=1, name=Dev, address=some road some gully)

// With default values
data class CustomerWithDefaults(val id:Int = 0, val name:String, var address:String = "")

var c2 = CustomerWithDefaults(name="Rane")

println("Customer with defaults ${c2.toString()}")
// prints > Customer with defaults CustomerWithDefaults(id=0, name=Rane, address=)
```
Data classes
    - Auto-generate equals, hashCode and toString methods (unless base class has it or they are explicitly defined class body)
    - Cannot be open (cannot be extended), abstract, sealed or inner
    - Must have either one `var` or `val` in their primary constructor
    - Copy
        ```kotlin
        val jack = User(name = "Jack", age = 1)
        val olderJack = jack.copy(age = 2)
        ```
    - De-structuring
        ```kotlin
        val jane = User("Jane", 35)
        val (name, age) = jane
        ```
# Enum classes
```kotlin
enum class Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

enum class Fruit(val color: String, val weight: Int) {
    APPLE("Red", 10),
    ORANGE("Orange", 12),
    WATERMELON("Green", 40),
    BANANA("Yellow", 5);
}

Fruit.values()                  // returns a list of all values defined
Fruit.valueOf("BANANA")         // will return BANANA, the Fruit object
Day.valueOf("TUESDAY")          // will return TUESDAY, the Day object
Day.valueOf("TUESDAY").name     // will return "TUESDAY"
Fruit.valueOf("BANANA").color   //will return "Yellow"

// Enums can inherit an interface and each enum value will have to implement it separately

interface Printable {
    fun print(): Unit
}

public enum class Word : Printable {
    HELLO {
        override fun print() {
            println("Word is HELLO")
        }
    },
    BYE {
        override fun print() {
            println("Word is BYE")
        }
    }
}

val w= Word.HELLO
w.print()
```
## Static methods
Static methods are not supposed to go into a class, they are declared in the file and can be accessed by the package directly. Makes sense!

## Singleton
Since there is no static method, you cannot implement a Singeton using regular classes. The way to implement a Singleton in kotlin is using the `object` keyword
```kotlin
object Counter {
    private var ctr = 0
    fun incr(i: Int) {
        ctr += i
        println("Ctr has been incremented to $ctr")
    }
    fun getCtr() {
        return ctr
    }
}

// Usage:
var ctr = Counter
ctr.incr(5)         // ctr.getCtr() gives 5
var ictr = Counter
ictr.incr(2)        // ctr.getCtr() gives 7
```

You wish there was a way we can have a shared singleton between all instances of a class
Kaboom: We have `object companion` which creates a singleton shared between all instances of the containing class (works like static fields in Java) (is picked from Scala)
```kotlin
class MyRegularClass {
    companion object Factory {
        val info = "This is factory"
        fun getMoreInfo():String { return "This is factory fun" }
    }
}

MyRegularClass.info             // This is factory
MyRegularClass.getMoreInfo()    // This is factory fun
```
Obviously, companion object will have no access to any methods in the class which require a instance.
- They are to be treated like static methods of a class
- You also cannot call them through a class instance.

## Sealed Classes

If there is a base class which you want to extend only for internal classes, and don't want anyone else to extend you can mark it as sealed. If its marked sealed, classes in the same file can extend it but outside the file you cannot extend it. You can ofcourse extend the extended classes further.
A great use case for this is casting a set of objects using polymorphism
```kotlin
sealed class Organism
data class Dog(val height: Float, val weight: Float): Organism()    // data class
class Animal(val type: String, var legs: Int): Organism()           // regular class
object NotAnOrganism: Organism()                                    // Singleton

// Polymorohism Usage:
fun giveSomeAttribute(obj: Organism): Float = when(obj) {
    is Dog -> obj.height
    is Animal -> obj.legs
    NotAnOrganism -> Float.NaN
    // the `else` clause is not required because we've covered all the cases
}
```
# Interfaces (aka Contracts)
If a class is implementing an interface, it MUST implement methods and variables that the interface implements (with some basic rules)
- All variables MUST be overridden
- Variable CANNOT be initialized
- Methods which are not implemented, must be overridden
- Methods which have been implemented, need not be overridden and will be accessible like regular methods
```kotlin
interface Document {
    val version: Int    // must be overridden
    var size: Int       // must be overridden
    // var some:Int = 0 // ERROR, variables cannot be initialized

    fun save(i: Int): Int   // Not implemented, so must be overridden and declared
    fun load(i: Int) {      // Implemeted, so need not be overridden
        println("Interface load")
    }
}

# Usage
class MyDocument: Document {
    override val version: Int = 0
    override var size: Int = 0

    override fun save(i: Int): Int {
        return i * 2
    }
}
```
# Inheritance and super - Calls to the parent class
```kotlin
// no primary constructor takes a parameter
class ChequePayment : Payment {

// child primary constructor takes a parameter
class ChequePayment(num1:Int, num2:Int) : Payment {

// child and parent primary constructor take a parameter
class ChequePayment(num1:Int, num2:Int) : Payment(num1) {

// child and parent secondary constructor take a parameter
class ChequePayment(num1:Int, num2:Int) : Payment(num1) {
    constructor(num1: Int, num3: Int): super(num1) {
         ...
     }
```
>Note: unless "open" keyword is used, class cannot be extended (that is sealed)

>Note: A class can extend ANY number of interfaces but only ONE class (in any order)
 `class TextDocument(title: String) : IPersistable, Document(title), IPrintable {`

## Abstract classes
 ```kotlin
abstract class A {
    // MUST be overridden in the derived class (unless derived class is abstract)
    abstract fun doSomething()
}
```
- Cannot create a instance of the abstract class
- Abstract class can itself is derived from a regular class
- The method which the abstract class overrides as abstract, will need to be redefined in the class derived from the abstract class

```kotlin
// Regular class open to extension
open class AParent protected constructor() {
    open fun someMethod(): Int = Random().nextInt()     // method with its own implementation
}
// Abstract class derived from regular class
abstract class DDerived : AParent() {
    abstract override fun someMethod(): Int             // abstract method losses definition
}

// Regular class derived from abstract class
class AlwaysOne : DDerived() {
    override fun someMethod(): Int {                    // must be redefined in derived class
        return 1
    }
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

### Abstract class OR Interface
    - Interface means "Derived class CAN DO things that interface has defined"
    - Class means "Derived class IS A type of the base class"
    - If the base type can provide implementations use class
    - If a methods is added to an interface, it MUST be implemented in all child classes, this can be skipped for abstract classes

Understand a few core programming concepts:
- Polymorphism
    - An Array of different types of objects, sharing the same base type
    - Calling a method on a collection of different types of objects, sharing the same base type
    - How JVM implements vtable for lookups during runtime

- Ambiguity management
    - If you derive from one class and one interface with common method names, you must override

- Inheritance Vs Composition

# Class Delegation ("by" keyword)
Mostly, composition is preferred over composition. What a delegation does is that it allows
a class to delegate some of its methods to an object its composed of. E.g.
```kotlin
interface UIElement {
    fun getHeight(): Int
    fun getWidth(): Int
}

class Rectangle(val x1: Int, val x2: Int, val y1: Int, val y2: Int) :
    UIElement {
    override fun getHeight() = y2 - y1
    override fun getWidth() = x2 - x1
}

class Panel(val rectangle: Rectangle) : UIElement by rectangle

val panel = Panel(Rectangle(10, 100, 30, 100))
println("Panel height: ${panel.getHeight()}")        // this calls panel.rectangle.getHeight()
println("Panel witdh: ${panel.getWidth()}")          // this calls panel.rectangle.getHeight()
```

### Overriding methods
```kotlin
open class BaseK {
    open fun v() {}
    fun nv() {}
}
class DerivedK() : BaseK() {
    override fun v() {}
}
class DerivedFK() : BaseK() {
    final override fun v() {}
}

fun main(args: Array<String>) {
    Day.valueOf("WEDNESDAY").
}
```
# How the control flows in the class constructors:

The init blocks and the class body is executed in the order top to bottom
Followed by constructors themselves.

Consider a "Parent" class and a inherited class "Child"
```kotlin
// explicitly open needs to be written for Parent to be extendable
open class Parent {
    private val a = println("Parent.a")

    constructor(arg: Unit=println("Parent primary constructor default argument")) {
        println("Parent primary constructor")
    }

    init {
        println("Parent.init")
    }

    private val b = println("Parent.b")
}

class Child : Parent {
    val a = println("Child.a")

    init {
        println("Child.init 1")
    }

    constructor(arg: Unit=println("Child primary constructor default argument")) : super() {
        println("Child primary constructor")
    }

    val b = println("Child.b")

    constructor(arg: Int, arg2:Unit = println("Child secondary constructor default argument")): this() {
        println("Child secondary constructor")
    }

    init {
        println("Child.init 2")
    }
}
```
if we construct an instance of Child by calling its secondary constructor with Child(1)
Following is how the code flows during construction

Child secondary constructor default argument
Child primary constructor default argument
Parent primary constructor default argument
Parent.a
Parent.init
Parent.b
Parent primary constructor
Child.a
Child.init 1
Child.b
Child.init 2
Child primary constructor
Child secondary constructor
