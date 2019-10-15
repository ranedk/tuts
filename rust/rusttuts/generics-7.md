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
Returning functions
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
