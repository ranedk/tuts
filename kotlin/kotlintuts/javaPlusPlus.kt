/**
 * Created by rane on 27/1/18.
 */
package learn.kotlin.basics

import java.io.File

fun main(args: Array<String>) {
    println("How is Kotlin better than Java !?")
}
    /*
    Java getter and setter simplified.
    Syntax:
        var/val<propertyName>:<PropertyType>[=<property_initializer>]
        [<getter>]
        [<setter>]
    */

    class Student(name: String, age: Int) {  // Constructor
        public var Name = ""
            set(value) {            // Setter
                field = value       // Getter is automagically defined by kotlin compiler
            }
        public var Age = 20
            set(value) {            // Setter
                field = value
            }
        init {
            Name = name             // Backing field
            Age = age
        }
    }

    // Using properties, Like in python
    interface Shape {
        val Area: Double    // Immutable, only Getter, no Setter because "val"
            get;
    }
    class Rectangle(val width: Double, val height: Double) : Shape {
        override val Area: Double
            get() = width * height
        val isSquare: Boolean
            get() = width == height
    }

    var rect = Rectangle(10.0, 20.0)
    print("Rectangle's Area: ${rect.Area},  is square?: ${rect.isSquare}")

    // Caching with getter
    class Lookup {
        private var _keywords: HashSet<String>? = null
        val keywords: Iterable<String>
            get() {
                if (_keywords == null) {
                    _keywords = HashSet<String>()
                }
                return _keywords ?: throw RuntimeException("Invalid keywords")
            }
    }

    /*
    Visibility
        Setters can be made private or protected and general visilibity rules apply
    */

    /* Late Initialization:
    Use case:
        We don't want a property to be null, but the initialization is delayed.
        If I access is before initialization, throw exception, not let it not be null
    */

    class DelayedInstance (val number:Int)
    class Container {
        lateinit var delayedInitProperty: DelayedInstance
        fun initProperty(instance: DelayedInstance): Unit {
            this.delayedInitProperty = instance
        }
    }

    val cont = Container()
    // calling container.delayedInitProperty will throw exception
    cont.initProperty(DelayedInstance(10))   // Initialize later

    /*
        NOTE: There are a few restrictions when using delayed properties.
        Firstly, the property type cannot be a primitive type.
        Secondly, your property cannot make use of custom getter or setter code.
        And last but not least, accessing your property before it has been initialized
        will end up in kotlin.UninitializedPropertyAccessException.
    */


    /*
    Delegated properties:

    Composition is always better than inheritance. One of the best way of composing
    object out of different types without complexity is delegates.
    */

    class Example {
        var p: String by Delegate()     // "p" will be set and get using Delegate class
    }

    class Delegate {
        operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
            return "$thisRef, thank you for delegating '${property.name}' to me!"
        }

        operator fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
            println("$value has been assigned to '${property.name}' in $thisRef.")
        }
    }

    val e = Example()
    println(e.p)
    // Example@33a17727, thank you for delegating ‘p’ to me!

    e.p = "NEW"
    //NEW has been assigned to ‘p’ in Example@33a17727.

    /*
    Now since you can delegate the getter and setter to someone else, we can use kotlin's
    inbuilt delegates to do the following:

    Use cases:
        Computed lazily on first access
        Notify change to the property (Observables)
        Storing properties in a map, instead of a separate field for each property
    */

    // Lazy
    val lazyValue: String by lazy {
        println("computed!")        // Only executed the first time
        "Hello"                     // Return value everytime
    }

    println(lazyValue) // computer! Hello
    println(lazyValue) // Hello

    /*
    - By default, the evaluation of lazy us synchronized. That is, only in on thread.
    - If multiple threads can do the evaluation pass LazyThreadSafetyMode.PUBLICATION
    as a parameter to the lazy() function
    - If you are sure no thread safety is required since only one thread will execute it
    then pass LazyThreadSafetyMode.NONE
    */

    // Observable

    import kotlin.properties.Delegates

    class User {
        var name: String by Delegates.observable("<no name>") {
            prop, old, new ->
            println("$old -> $new")
        }
    }

    val user = User()
    user.name = "first"
    // <no name> -> first
    // prints first -> second
    user.name = "second"

    /*
    If you want to be able to intercept an assignment and "veto" it, use vetoable()
    instead of observable(). The handler passed to the vetoable is called before the assignment
    of a new property value has been performed.
    */

    // Storing properties in Map

    class User(val map: Map<String, Any?>) {
        val name: String by map
        val age: Int     by map     // Can be a var or a val, depending on Map or MutableMap
    }
    val user = User(mapOf(
            "name" to "John Doe",
            "age"  to 25
    ))
    println(user.name)
    // "John Doe"
    println(user.age)
    // 25

    // Locally delegated properties: If you want a variable to get computed locally only
    // if a condition is true
    fun example(computeFoo: () -> Foo) {
        val memoizedFoo by lazy(computeFoo)

        if (someCondition && memoizedFoo.isValid()) {
            // If someCondition is true, then memoizedFoo gets computed with computeFoo
            memoizedFoo.doSomething()
        }
    }

    /*
    Null Checks:

    If we were to do null checks in a nested object, the code looks very bad. e.g.

    class Person(name: String, val address: Address?)
    class Address(name: String, postcode: String, val city: City?)
    class City(name: String, val country: Country?)
    class Country(val name: String)
    fun getCountryName(person: Person?): String? {
        var countryName: String? = null
        if (person != null) {
            val address = person.address
            if (address != null) {
                val city = address.city
                if (city != null) {
                    val country = city.country
                    if (country != null) {
                        countryName = country.name
                    }
                }
            }
        }
        return countryName
    }

    Kotlin shortcut:

    fun getCountryNameSafe(person: Person?): String? {
        return person?.address?.city?.country?.name
    }

    Default in case of null.
    Suppose we want the default value in case the object of the property is null.

    val address: Address? // nullable address
    val postcode: String = address?.postcode ?: "default_postcode"

    if address or postcode is null, postcode is "default_postcode"

    Safe Casting:
        val location: Any = "London"    // This is Any
        val safeString: String? = location as? String   // Safely cast Any to String
        val safeInt: Int? = location as? Int    // Safely cast Any to Int
    */

    /* OPTIONALS  (java8 feature)

    Better null handling can be achieved in many cases using optionals. With optionals
    you can return a default value. e.g.
    */

    // Creating an optional with some value
    val optionalName: Optional<String> = Optional.of("william")

    // Creating an optional with empty value
    val empty: Optional<String> = Optional.empty() // empty is a singleton like null

    // How to use Optional?
    object OptionalTest {

        fun printWithNull(args: Array<String>) {
            val myString: String? = null
            if (myString != null) {
                println(myString.length)
            } else {
                println("null string")
            }
        }

        fun printWithOptional(args: Array<String>) {
            val myString = Optional.empty()
            myString.ifPresent({ x -> println(x.length) })  // COOL! Pythonic!
        }
    }


