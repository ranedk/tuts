# Patterns and advanced class concepts

## Initialization-on-demand holder pattern (or lazy loading Singleton)

Often times you want a Singleton to load only when you need it (heavy loading class)
To accomplish this in Java, we declare a static class inside the Singleton class, which holds the
instance of the Singleton. The getInstance method of the class will return this static class holder
```kotlin
public class ClassWithHeavyInitialization {

    // Private constructor, nobody can instantiate outside
    private ClassWithHeavyInitialization() {
    }

    // Static class having access to outer class private methods
    private static class LazyHolder {

        // holder of the outer class instance
        public static final ClassWithHeavyInitialization INSTANCE = new ClassWithHeavyInitialization();
    }

    public static ClassWithHeavyInitialization getInstance() {
        return LazyHolder.INSTANCE;
    }
}
```
How this helps in lazy loading, is that until you call `getInstance`, the Singleton instance is never created.

Is there a better way? Kotlin provides the following:
```kotlin
public class ClassWithHeavyInitialization private constructor() {
    // Singleton class Holder
    private object Holder {
        val INSTANCE = ClassWithHeavyInitialization()
    }

    // Declare a static singleton
    companion object {      // companion makes it static inner, object makes it singleton
        val instance: ClassWithHeavyInitialization by lazy {
            Holder.INSTANCE
        }
    }
}

// Usage
// ClassWithHeavyInitialization.instance which lazily evaluates Holder.INSTANCE
```
## Anonymous classes using object expression and object declarations

If a supertype has a constructor, appropriate constructor parameters must be passed to it.
Many supertypes may be specified as a comma-separated list after the colon:
```kotlin
open class ASuper(x: Int) {
    public open val y: Int = x
}

interface B { }

val anonInstance: ASuper = object : ASuper(1), B {    // anonymous class's instance
    override val y = 15
}

// If there are no super-types, then

fun inst() {           // single instance of
    val adHoc = object {
        var x: Int = 0
        var y: Int = 0
    }
    print(adHoc.x + adHoc.y)
}
```
The use case for anonymous objects is only when a function, like a mouseEventListener
demands an object of a certain class and don't want to define a class just for that.

They are best avoided because of complexity in the rules around them, but makes sense if only single instance of the class exists.
