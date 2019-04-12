/**
 * Created by rane on 16/7/17.
 */


/*
Generics : Classed with type parameters
*/

class Box<T>(t: T) {
    var value = t
}

val box1: Box<Int> = Box<Int>(1)        // explicit
val box2 = Box(1)                       // inferred

/*
Type Variance or what the fuss between dynamic and static languages

    Apple is a subtype of fruit
    but should Crate<Apple> be a subtype of Crate<Fruit>
    Not necessary, it could actually be inverted depending on what we want.

    Before we start, few known things:
        - Functions are allowed to take sub-types as input, so fun foo(f:Fruit), can be
        called with foo(apple) or foo(orange) (Apple and Orange being sub-types of Fruit)

    class Fruit {
        fun isSafeToEat(): Boolean { ... }
    }
    class Apple : Fruit()
    class Orange : Fruit()

    class Crate<T>(val elements: MutableList<T>) {      // Just a wrapper around MutableList
        fun add(t: T) = elements.add(t)
        fun last(): T = elements.last()
    }

    Now, suppose we define a function which adds Apple to a Crate<Fruit>
    sounds cool.

    fun foo(crate: Crate<Fruit>): Unit {
        crate.add(Apple())
    }

    And we try to use it as

    val oranges = Crate(mutableListOf(Orange(), Orange()))  // crate of oranges
    foo(oranges)                                            // add apple to crate of oranges

    We are calling foo with a Crate<Orange> which should be possible if Crate<Orange> was a
    sub-type of Crate<Fruit>
    However, this is not allowed in Kotlin (its allowed in some language, its a compiler design
    thing, religious stuff, just have faith that it was done for good reasons and don't ask why.

    But since you ask Why? This may lead to weird runtime errors, like below

        val oranges = Crate(mutableListOf(Orange(), Orange()))  // crate of oranges
        foo(oranges)                                            // add apple to crate of oranges
        val orange: Orange = oranges.last()                     // get the last fruit(apple) as orange - NO CAN DO

    You have polluted a crate of Orange with Apple, which is wrong sub-type of Fruit in this context.

    So Kotlin compiler decides to not have a super or sub type relation between Crate<Fruit>
    and Crate<Apple> even if there is a relation between Fruit and Apple
    This is called being "INVARIANT". Crate<Fruit and Crate<Apple> are invariant

    ----------------------------------------------------------------------------------------------------

    Now, suppose we need to get fruits in a crate which are safe to eat. We can write a generic function
    which take any crate of fruits and find the ones safe to eat

        fun isSafe(crate: Crate<Fruit>): Boolean = crate.elements.all{
            it.isSafeToEat()
        }

    Now, we already know the following code won't compile, because Invariance of Crate<Fruit> and Crate<Orange>:
        val oranges = Crate(mutableListOf(Orange(), Orange()))
        isSafe(oranges)

    I can define it separately for Apple and Orange, but its not respecting DRY.
    However, there are no side-effects of this. So it should be possible to do so.
    We want Crate<Fruit> to be a super type of Crate<Apple>

    We want them to be "COVARIANT". Crate<Fruit> should be super type of Crate<Apple> because Fruit is a
    super type of Apple.
    We can implement it like below

    class CovariantCrate<out T>(val elements: List<T>) {
        fun last(): T = elements.last()
    }

    Three things to notice:
        - The keyword "out" makes it COVARIANT
        - Since it "COVARIANT", it CANNOT have any methods which take T as INPUT (except constructor),
            T as output is fine. this constraint is imposed, so that there is no way to take an Orange
            where a Fruit is expected, and no way to add or pollute the CovariantCrate with bad sub-types.
            Basically, immutable.
        - This is derived from List instead of MutableList, since MutableList adds the method "add" to this
            which takes T as input, which is prohibited from the law above.

    Now I can call isSafe method with a CovariantCrate<Apple> or CovariantCrate<Orange>, Respect DRY.

    What if a method returns a super-type (Fruit), that works fine since I can check if Fruit instance is
    of specific type

    Compiler feels happy and safe.
    ----------------------------------------------------------------------------------------------------

    If we want a Crate<Fruit> to be a sub-type Crate<Apple>. Invert the relationship. This is called
    CONTRAVARIANT
    
    Why would you want it?

    Suppose there is a EventStream class, which produces a event of type T.
    The EventStream class also takes a Listener<T> which is invoked each time an event is generated

        interface Listener<T> {
            fun onNext(t: T): Unit
        }

        class EventStream<T>(val listener: Listener<T>) {
            fun start(): Unit = ...
            fun stop(): Unit = ...
        }

    Let's implement a String Listener based on the Listener interface:

        val stringListener = object : Listener<String> {
            override fun onNext(t: String) = println(t)
        }

        val stringStream = EventStream<String>(stringListener)
        stringStream.start()

    Let's implement a Date Listener

        val dateListener = object : Listener<Date> {
            override fun onNext(t: Date) = println(t)
        }

        val dateStream = EventStream<Date>(dateListener)
        dateStream.start()

    There is repetition here, so we should be able  to do it generically:

        val loggingListener = object : Listener<Any> {
            override fun onNext(t: Any) = println(t)
        }

        val anyStream = EventStream<Stream>(loggingListener) // Error

    EventStream<T> needs a Listener<T>
    This doesn't work because loggingListener which of type Listener<Any> needs to be a subtype of
    Listener<String> because EventStream<Stream> expects it to be.


    So, we need to define it properly as ContraVariant, as below:

        interface Listener<in T> {
            fun onNext(t: T): Unit
        }

        class EventStream<T>(val listener: Listener<T>) {
            fun start(): Unit = ...
            fun stop(): Unit = ...
        }

    Now we can use this for any type we want:

        EventStream<Double>(loggingListener).start()
        EventStream<BigDecimal>(loggingListener).start()


    For CoVariance, methods of the class are not allowed to have T as input, but only as output
    For ContraVariance, methods of the class are allowed to have T as input, but NOT as output

    Summary: Properly using Variance needs effort and thinking. In general, the rules is
    something like this:

        If the objects are derived as
        A(base), B(derived from A), C(derived from B)  A -> B -> C

        Covariance is easier to understand, If you want the same relationship to extend to generic types
        say P<A> -> P<B> -> P<C>

        class P<out T>( ... makes it covariant

        So, P<out T> cannot have methods which take any "T" and "sub-types of T". So you can safely use
        the constructor to give it type "T", and later, take anything from P<out T> and it will always
        be of the initial type "T"

        P<out T> is a Producer of "T" and "super-types of T". Never consumes it.

        In case of ContraVariance, P<in T> means that the relationship is P<A> <- P<B> <- P<C>

        So, it will never return anything of type "T" or "sub-type of T". It will take "T" and "sub-types"
        P<in T> will be a consumer of "T" or "sub-type of T", but will never produce it
*/

/*
    Type Projections:

    If we are using a library which already has defined the classes and the generic types, and we want to
    change the generic types to Covariant and Contravariant types without re-writing them completely, we
    can use type projections.

    In the examples above, we had the Crate class, which was invariant and we couldn't add an Orange to
    a Crate<Fruit>

        class Crate<T>(val elements: MutableList<T>) {
            fun add(t: T) = elements.add(t)
            fun last(): T = elements.last()
        }

    We ended up defining CoVariantCrate and removing the add method, so that isSafe can work.
    Using type projection, we can make isSafe convert a Crate into a CoVariantCrate (and tell compiler
    that we will not call add on it)

        fun isSafe(crate: Crate<out Fruit>): Boolean = crate.elements.all{
            it.isSafeToEat()
        }

    This is cool!!

    Also, in the EventListener example, we had to redefine loggingListener as Contravariant, which we can
    do simply as below now:

        class EventStream<T>(val listener: Listener<in T>) {
            fun start(): Unit = ...
            fun stop(): Unit = ...
        }

    Another good example for a Type Projection is:

        fun copy(from: Array<out Any>, to: Array<Any>) {
            // ... to.addAll(from)
        }

    For a copy method, you would want to add the "from" array to the "to" array, and not change the
    "from" array. So, we define it as "out", which means you cannot call a method on it that can
    potentially change it. Immutable "from" array.

 */
