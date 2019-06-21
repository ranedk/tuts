# Coroutines
Concurrency, not parallelism

```kotlin
import kotlinx.coroutines.*

fun main() {
    GlobalScope.launch { // launch a new coroutine in background and continue
        delay(1000L)
        println("World!")
    }
    println("Hello,") // main thread continues here immediately
    runBlocking {     // but this expression blocks the main thread
        delay(2000L)  // ... while we delay for 2 seconds to keep JVM alive
    }
}
```
The above launches co-routine in the GlobalScope, which takes too many resources. A more efficient way it to launch co-routines in a local scope. As long as the local-scoped co-routine runs, the main thread will not exit.
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking { // this: CoroutineScope
    launch { // launch a new coroutine in the scope of runBlocking
        delay(1000L)
        println("World!")
    }
    println("Hello,")
}
```
If you dont want to block current thread till its children have stopped, we use `coroutineScope`
```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking { // this: CoroutineScope
    launch {
        delay(200L)
        println("Task from runBlocking")
    }

    coroutineScope { // Creates a coroutine scope
        launch {
            delay(500L)
            println("Task from nested launch")
        }

        delay(100L)
        println("Task from coroutine scope") // This line will be printed before the nested launch
    }

    println("Coroutine scope is over") // This line is not printed until the nested launch completes
}
```
To execute a function in non-blocking way inside a co-routine, use `suspend`
```kotlin
import kotlinx.coroutines.*
fun main() = runBlocking {
    launch { doWorld() }
    println("Hello,")
}

// this is your first suspending function
suspend fun doWorld() {
    delay(1000L)
    println("World!")
}
```
suspending functions can use other suspending functions

Two-way communication between co-routines is possible using `channels`
```kotlin
val channel = Channel<Int>()
launch {
    for (x in 1..5) channel.send(x * x)
    channel.close() // we're done sending
}
// here we print received values using `for` loop (until the channel is closed)
for (y in channel) println(y)
println("Done!")
```
Channels act as blocking queues.
