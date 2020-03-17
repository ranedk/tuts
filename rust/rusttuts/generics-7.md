# Generics

Hopefully, you understand generics in some other languages (like Java).
To summarize a few things:
1) Generics, generally denoted by `T` or other single letters, helps write code in way that the Function, Struct or Enum (lets call these constructs) can take any value
```rust
// Functions
fn first<T>(list: &[T]) -> &T {
    return &list[0];
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];
    let char_list = vec!['y', 'm', 'a', 'q'];

    println!("first number: {}", first(&number_list));
    println!("first char: {}", first(&char_list));
}

// ----------------------------------------

struct Point<T, U> {
    x: T,
    y: U,
}

// Struct methods

// implement generic <T, U> on Point
impl<T, U> Point<T, U> {
    fn x(&self) -> &T {
        &self.x
    }
}

// implement only if both T and U are f32
impl Point<f32, f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

// Major mixing generics
impl<T, U> Point<T, U> {            // implement a generic Point with <T, U>

   // implement method with on <T, U>, which is self, but input can be any other <V, W> Point
    fn mixup<V, W>(self, other: Point<V, W>) -> Point<T, W> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}

fn main() {
    let both_integer = Point { x: 5, y: 10 };
    let both_float = Point { x: 1.0, y: 4.0 };
    let integer_and_float = Point { x: 5, y: 4.0 };

    println!("p.x={}", integer_and_float.x())

    println!("p.distance_from_origin={}", both_float.distance_from_origin());   // both a f32

    println!("p.distance_from_origin={}", integer_and_float.distance_from_origin());   // Compile ERROR

    let p3 = both_integer.mixup(both_float);
}

// ----------------------------------------

// Enum
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```
2) The more generic you get, the more open the constructs become to receiving values, but the more constrained they are to call functions on them
```rust
fn largest<T>(list: &[T]) -> T {    // function can receive all types
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {     // Compile error, cannot call `>` on all types
            largest = item;
        }
    }

    largest
}
```
Although the greater than opertor `>` is defined for char and int, `T` by definition can be anything, and not everything implements `>` operator.
The `>` operator is defined for all types, which implement the `std::cmp::PartialOrd` trait/interface (read more to understand this, we will get back to this later)

# Traits (Define shared behaviour, like interfaces)

```rust
pub trait Summary {
    fn summarize(&self) -> String;  // whoever implements the Summary trait, must define summarize
}
```

Lets extend the `Summary` trait
```rust
pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {          // implement Summary trait for NewsArticle struct
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}
```
Note: In implementing a `trait` on a `struct`, either the `trait` or the `struct` must belong to you. Meaning, you cannot implement a `trait` for a `struct` when both belong to 3rd party crates. E.g. You can implement `Summary` on `Vec<T>` or `Display` (a 3rd party trait) on `NewsArticle`, but you cannot implement `Display` on `Vec<T>`

### Traits can implement default behaviour too
1) You can override the default behaviour, but cannot call default behaviour from overridden behaviour (like super in python)
2) Traits can call other functions in  the trait, even if they don't have implementation

```rust
pub trait Summary {
    fn summarize_author(&self) -> String;

    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}

// implementing trait
impl Summary for Tweet {
    fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }
}
```

### Polymorphism with traits
Much like Java, functions taking a trait as input, can take all implementing structs as inputs too.
```rust
pub fn notify(item: impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

// OR

pub fn notify<T: Summary>(item: T) {        // T is of type Summary trait
    println!("Breaking news! {}", item.summarize());
}
```
`notify` function, can call all methods that trait `Summary` defines.

You can use traits like mixins in functions. So one function can take objects which implement multiple traits `pub fn notify<T: Summary + Display>(item: T) {`

Multiple generic variables
```rust
fn some_function<T: Display + Clone, U: Clone + Debug>(t: T, u: U) -> i32 {

OR

fn some_function<T, U>(t: T, u: U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{

```
Returning a trait
```rust
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from("of course, as you probably already know, people"),
        reply: false,
        retweet: false,
    }
}
```
NOTE: When a function returns a `trait`, its return must be ONE concrete type. That is, the function `returns_summarizable`, cannot return a object type `Tweet` sometimes or a `NewsArticle` sometimes. It must return only one concrete type consistently.

To get a function to return different types (derived from the same implementation), use the box type:
```rust
fn summarizable (tweet: bool) -> Box<dyn Summary> {
    if tweet {
        Box::new(Tweet {
            username: "ranedk".to_string(),
            content: "Here goes by tweet, twat".to_string()
        })
    } else {
        Box::new(Blog{
            writer: "ranedk123".to_string(),
            article: "Here goes da blog...".to_string()
        })
    }
}

// Usage:
let t = summarizable(true);
println!("{}", t.summarize());
```

## Complications that arise
Largest function
```rust
fn largest<T>(list: &[T]) -> T {    // function can receive all types
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {     // Compile error, cannot call `>` on all types
            largest = item;
        }
    }

    largest
}
```

Looking back at the `largest` function example, the definition could be `fn largest<T: PartialOrd>(list: &[T]) -> T {`
However, it gives error on the line:
```
let mut largest = list[0];
  |                       ^^^^^^^
  |                       |
  |                       cannot move out of here
  |                       help: consider using a reference instead: `&list[0]``
```

In English, `list[0]` moves the first element of list into largest variable. For primitive types like `char` and `int`, this is actually a copy. So the loop works for everyone who implements the `Copy` trait (which the primitives implement by default)
So, the right signature should be `fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {`

Another implementation of largest could be to always use references instead of depending on `Copy` at all:
```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {   // takes and return references
    let mut largest = &list[0];

    for item in list.iter() {
        if item > largest {             // although both a references, rust always compares by value
            largest = item;
        }
    }

    largest
}
```

### Polymorphism with traits and structs
```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {    // new is implemented for ALL types of Pair
        Self {
            x,
            y,
        }
    }
}

impl<T: Display + PartialOrd> Pair<T> {     // cmp_display is implemented for only those Pairs which
    fn cmp_display(&self) {                 // implement Display and PartialOrd trait
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```

# Lifetimes - the crazy one
- Once the usage of the variable is no more, its no more in scope
- If it had a reference before, it should also be out of scope

Consider the following code:
```rust
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";

    let result = longest(string1.as_str(), string2);    // after this, string1 and string2 will be out of scope
    println!("The longest string is {}", result);       // result is reference to either string1 or string2
                                                        // so we don't know during compile time if result's lifetime
                                                        // should be equal to string1 or string2

                                                        // If the function longest was taking a single reference parameter
                                                        // rust would automatically figure out that result and input reference
                                                        // should have the same lifetime. In 2 parameters, its not certain
}

```
This doesn't compile and gives a lifetime error
Fix, `lifetime`
The syntax looks weird, but it requires a `'` followed by lifetime tag variable
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {     // This means, the output of the function will have the same lifetime
    if x.len() > y.len() {                              // as the minimum of the lifetimes of x or y
        x
    } else {
        y
    }
}

fn give_first<'a>(x: &'a str, y: &str) -> &'a str {     // This means, the output of the function will have the same lifetime
    x                                                   // as x
}
```

## Lifetimes in Structs
If a struct take a reference, we need to define how its lifetime would be dependent on the lifetime of the value for this the reference belong to
```rust
struct ImportantExcerpt<'a> {
    part: &'a str,              // part will have lifetime, as long a value for which its a reference
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.')
        .next()
        .expect("Could not find a '.'");
    let i = ImportantExcerpt { part: first_sentence };  //  i and i.part will have same lifetime as first_sentence
}
```

### Static lifetimes (lifetime as long as the program runs)
You can use `'static` to mark variable as having a static lifetime:
```rust
impl Config {
    //&'static str is the type of string literals, which is our error message type for now
    fn new(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let filename = args[2].clone();

        Ok(Config { query, filename })
    }
}
```

Make a constant live as long a the program lives:

```rust
// Make a constant with static lifetime.
static NUM: i32 = 18;

// Returns a reference to NUM where its 'static
// lifetime is coerced to that of the input argument.

fn coerce_static<'a>(_: &'a i32) -> &'a i32 {
    &NUM
}

fn main() {
    {
        // Make a string literal and print it:
        let static_string = "I'm in read-only memory";
        println!("static_string: {}", static_string);

        // When static_string goes out of scope, the reference
        // can no longer be used, but the data remains in the binary.
    }

    {
        // Make an integer to use for coerce_static:
        let lifetime_num = 9;

        // Coerce NUM to lifetime of lifetime_num:
        let coerced_static = coerce_static(&lifetime_num);

        println!("coerced_static: {}", coerced_static);
    }

    println!("NUM: {} stays accessible!", NUM);
}

```

## Associated types
Traits defined over generics (cool feature++)

If a trait is defined over generic, the implementation will have to be defined with proper types:
```rust
// Trait defined with generics
trait Contains<A, B> {
    fn contains(&self, _: &A, _: &B) -> bool; // Explicitly requires `A` and `B`.
    fn first(&self) -> i32; // Doesn't explicitly require `A` or `B`.
    fn last(&self) -> i32;  // Doesn't explicitly require `A` or `B`.
}
// Struct defined with types
struct Container(i32, i32);

// To implement struct with contains trait
impl Contains<i32, i32> for Container {

    fn contains(&self, number_1: &i32, number_2: &i32) -> bool {
        (&self.0 == number_1) && (&self.1 == number_2)
    }

    // Grab the first number.
    fn first(&self) -> i32 { self.0 }

    // Grab the last number.
    fn last(&self) -> i32 { self.1 }
}

fn difference<A, B, C>(container: C) -> i32 where C: Contains<A, B> {
    container.last() - container.first()
}
```

Associated Types make types defined in trait:
```rust
struct Container(i32, i32);

trait Contains {
    // Define generic types here which methods will be able to utilize.
    type A;
    type B;

    fn contains(&self, _: &Self::A, _: &Self::B) -> bool;
    fn first(&self) -> i32;
    fn last(&self) -> i32;
}

impl Contains for Container {
    // Specify what types `A` and `B` are. If the `input` type
    // is `Container(i32, i32)`, the `output` types are determined
    // as `i32` and `i32`.
    type A = i32;
    type B = i32;

    // `&Self::A` and `&Self::B` are also valid here.
    fn contains(&self, number_1: &i32, number_2: &i32) -> bool {
        (&self.0 == number_1) && (&self.1 == number_2)
    }
    // Grab the first number.
    fn first(&self) -> i32 { self.0 }

    // Grab the last number.
    fn last(&self) -> i32 { self.1 }
}

fn difference<C: Contains>(container: &C) -> i32 {
    container.last() - container.first()
}
```

## SuperTraits (sort of trait Inheritance)
```rust
trait Person {
    fn name(&self) -> String;
}

// Student is a supertrait of Person.
// Implementing Student requires you to also impl Person.
trait Student: Person {
    fn university(&self) -> String;
}

trait Programmer {
    fn fav_language(&self) -> String;
}

// CompSciStudent (computer science student) is a supertrait of both Programmer
// and Student. Implementing CompSciStudent requires you to impl both subtraits.
trait CompSciStudent: Programmer + Student {
    fn git_username(&self) -> String;
}

fn comp_sci_student_greeting(student: &dyn CompSciStudent) -> String {
    format!(
        "My name is {} and I attend {}. My Git username is {}",
        student.name(),
        student.university(),
        student.git_username()
    )
}

fn main() {}
```

If you derive from 2 traits, both implementing the same method, then to disambiguate, use:

`let username = <Form as UsernameWidget>::get(&form);`

