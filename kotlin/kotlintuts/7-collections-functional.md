# Collections and functional programming

This is what separated Kotlin from other language and makes it closer to Python, Javascript etc. Lets dig deeper.

```kotlin
import kotlin.random.Random

enum class Gender {
    MALE,
    FEMALE
}

data class Person(var name: String, var height: Float, var weight: Int, var gender: Gender)

fun main() {
    var nlist = mutableListOf<Person>(
        Person("Dev", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.MALE),
        Person("Abhi", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE),
        Person("Raju", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.MALE),
        Person("Kiran", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE),
        Person("Tinku", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.MALE),
        Person("Aman", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.MALE),
        Person("Ankur", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.MALE),
        Person("Anant", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.MALE),
        Person("Smita", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE),
        Person("Ananya", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE),
        Person("Madhu", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE)
    )

    println(nlist);

    var hundredth = nlist.getOrNull(100)
    // > null

    var thousandth = nlist.getOrElse(100) { nlist[nlist.size - 1] }
    // > Person(name=Anant, height=5.9306016, weight=73)

    // Range is denoted by 4..100 step 3
    for (idx in 2..nlist.size - 1 step 3) {
        println(nlist[idx].name)
    }
    // Raju, Aman, Smita

    var idxOfFirstAnanya = nlist.indexOfFirst { it.name == "Ananya" }
    var idxOfLastAnanya = nlist.indexOfLast { it.name == "Ananya" }

    var ananya = nlist[idxOfFirstAnanya]
    var idxOfAnanya = nlist.indexOf(ananya)

    // Insert new entry to 3rd position
    nlist.add(3, Person("Anu", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE))

    // Insert another list at 5th position
    nlist.addAll(
        5, listOf(
            Person("Pratibha", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE),
            Person("Ira", 4 + Random.nextFloat() * 2, Random.nextInt(40, 100), Gender.FEMALE)
        )
    )

    // replace all persons with ananya
    //nlist.fill(ananya)

    // remove a particular element
    nlist.remove(ananya)

    // remove by index
    var fifth = nlist.removeAt(5)

    nlist.sortBy { it.name }

    // list of sorted names
    nlist.forEach { println("> ${it.name}") }

    // shuffle nlist
    nlist.shuffle()

    // sort by multiple criteria
    nlist.sortWith(compareBy<Person> { it.gender }.thenBy { it.name } )

    // list of sorted names
    nlist.forEach { println(">> ${it.gender} - ${it.name}") }

```

## Other important functions

```kotlin
var numbers = (65..89 step 3).toMutableList();
// numbers > [65, 68, 71, 74, 77, 80, 83, 86, 89]

var n1 = numbers.map { it.toChar() }
// n1 > [A, D, G, J, M, P, S, V, Y]

var n2 = numbers.mapIndexed {idx, ele -> "$idx - ${ele.toChar()}" }
// n2 > [0 - A, 1 - D, 2 - G, 3 - J, 4 - M, 5 - P, 6 - S, 7 - V, 8 - Y]

// Create a list which has nulls at random places
var nullableNumbers:MutableList<Int?> = (65..89 step 3).toMutableList();
nullableNumbers.addAll(4, listOf(100, null, 103, null, null, null))
// nullableNumbers > [65, 68, 71, 74, 100, null, 103, null, null, null, 77, 80, 83, 86, 89]

// mapNotNull filters all those which give null on transformation
var n3 = nullableNumbers.mapNotNull { it?.toChar() }
// n3 > [A, D, G, J, d, g, M, P, S, V, Y]

var n4 = nullableNumbers.mapIndexedNotNull { idx, it -> "$idx - ${it?.toChar()}"}
// [0 - A, 1 - D, 2 - G, 3 - J, 4 - d, 5 - null, 6 - g, 7 - null, 8 - null, 9 - null, 10 - M, 11 - P, 12 - S, 13 - V, 14 - Y]

var n5 = nullableNumbers.mapIndexedNotNull { idx, it -> it?.let {"$idx - ${it?.toChar()}" } }
// [0 - A, 1 - D, 2 - G, 3 - J, 4 - d, 6 - g, 10 - M, 11 - P, 12 - S, 13 - V, 14 - Y]
```

```kotlin
val words = listOf("one", "two", "three", "four")
val nums = listOf(1, 2, 3, 4)
var z1 = words zip nums
// z1 is List<Pair<String, Int>>
// [(one, 1), (two, 2), (three, 3), (four, 4)]

val oneTwo = listOf(1, 2)
var z2 = words.zip(oneTwo)
// [(one, 1), (two, 2)]

var newData = words.zip(nums) { w, n ->
    Pair<String, String>(w.toUpperCase(), (n * 2).toString())
}
// [(ONE, 2), (TWO, 4), (THREE, 6), (FOUR, 8)]
```

```kotlin
val numbers = listOf("one", "two", "three", "four", "five")

var n1 = numbers.associateWith { it.length }
// {one=3, two=3, three=5, four=4, five=4

var n2 = numbers.associateBy(keySelector = { it.first().toUpperCase() }, valueTransform = { it.length })
// {O=3, T=5, F=4}

val names = listOf("Vinit Singh", "Premanshu Singh", "Abhiruchi Chand", "Devendra Rane")
var n3 = names.associate { name -> name.split(" ").let { it[0] to it[1] } }
// {Vinit=Singh, Premanshu=Singh, Abhiruchi=Chand, Devendra=Rane}

val numberSets = listOf(setOf(1, 2, 3), setOf(4, 5, 6), setOf(1, 2))
var n4 = numberSets.flatten()
// [1, 2, 3, 4, 5, 6, 1, 2]

var n5 = numbers.joinToString(separator = " | ", prefix = "start: ", postfix = ": end")
// start: one | two | three | four | five: end

var n6 = numbers.joinToString(limit = 3, truncated = "...")
// one, two, three, ...

```

```kotlin
val numbers = listOf("one", "two", "three", "four")
val longerThan3 = numbers.filter { it.length > 3 }
// [three, four]

val numbersMap = mapOf("key1" to 1, "key2" to 2, "key3" to 3, "key11" to 11)
val filteredMap = numbersMap.filter { (key, value) -> key.endsWith("1") && value > 10 }
//{key11=11}


val filteredIdx = numbers.filterIndexed { index, s -> (index != 0) && (s.length < 5) }
// [two, four]

val filteredNot = numbers.filterNot { it.length <= 3 }
//[three, four]

// IS INSTANCE LOOP for mixed type lists
val words = listOf(null, 1, "two", 3.0, "four")
var n1 = words.filterIsInstance<String>()
// [two, four]

val (match, rest) = numbers.partition { it.length > 3 }
// match : [three, four]
// rest : [one, two]


var n2 = numbers.any { it.endsWith("e") }
// true

var n3 = numbers.none { it.endsWith("a") }
//true

var n4 = numbers.all { it.endsWith("e") }
// false

var n5 = emptyList<Int>().all { it > 5 }
// true    !! This is a vacous truth and debated in mathematics and computer science
```

## Grouping and slicing
```kotlin
val numbers = listOf("one", "two", "three", "four", "five")

val n1 = numbers.groupBy { it.first().toUpperCase() }
// {O=[one], T=[two, three], F=[four, five]}

val n2 = numbers.groupBy(keySelector = { it.first() }, valueTransform = { it.toUpperCase() })
//{o=[ONE], t=[TWO, THREE], f=[FOUR, FIVE]}


var n3 = numbers.slice(1..3)
//[two, three, four]

var n4 = numbers.slice(0..4 step 2)
//[one, three, five]

var n5 = numbers.slice(setOf(3, 4, 0))
//[four, five, one]

println(numbers.take(3))
//[one, two, three]

println(numbers.takeLast(3))
//[three, four, five]

println(numbers.drop(1))
//[two, three, four, five]

println(numbers.dropLast(3))
// [one, two]

println(numbers.takeWhile { !it.startsWith('f') })
// [one, two, three]

println(numbers.takeLastWhile { it != "three" })
//[four, five]

println(numbers.dropWhile { it.length == 3 })
//[three, four, five]

println(numbers.dropLastWhile { it.contains('i') })
//[one, two, three, four]

println((0..18).toList().chunked(3))
// [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18]]

// Window function
println(numbers.windowed(3))
// [[one, two, three], [two, three, four], [three, four, five]]

println((1..15).toList().windowed(5, step = 3, partialWindows = true))
// [[1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [7, 8, 9, 10, 11], [10, 11, 12, 13, 14], [13, 14, 15]]
```

## Sets
```kotlin
val set1 = setOf("A", "B", "C", "D", "E", "F")
val set2 = setOf("A", "E", "G", "H")

println(set1 union set2)
// [A, B, C, D, E, F, G, H]

println(set1 intersect set2)
//[A, E]

println(set1 subtract set2)
//[B, C, D, F]
```