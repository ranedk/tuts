# Closures - Anonymouns functions - Lambdas

```rust
let doubler = |num| {               // no types required
    num * 2
};

println!("{}", doubler(10));        // output: 20


println!("{}", doubler(10.0));      // output: Compiler time error

// once you called the closure with a type, you cannot change it. so calling it with
// integer type first, makes the closure only take integer types
```

```rust
// Different versions of function and closures

fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v3 = |x|             x + 1 ;
```

Lets implement a `struct` which caches a closure output on a cool way:

```rust
struct Cacher<T>                // Cacher implements generic type T
    where T: Fn(u32) -> u32     // T is a function/closure, takes u32 give out u32
                                // Fn is a trait, more on this below
{
    calculation: T,             // calculation should store the function/closure
    value: Option<u32>,         // cached value, initially None, so its Option type
}

// Methods on Cacher:
impl<T> Cacher<T>
    where T: Fn(u32) -> u32
{
    fn new(calculation: T) -> Cacher<T> {
        Cacher {
            calculation,
            value: None,
        }
    }

    fn value(&mut self, arg: u32) -> u32 {
        match self.value {
            Some(v) => v,
            None => {
                let v = (self.calculation)(arg);
                self.value = Some(v);
                v
            },
        }
    }
}
```

Unlike functions, closure can capture local environments. Functions have no access to local variables. Closure have multiple ways to capture local environment variables:

```rust
fn main() {
    let x = 4;

    let equal_to_x = |z| z == x;

    let y = 4;

    assert!(equal_to_x(y));
}
```

Closures borrow local variables mutably or immutably by default depending on the use case:

```rust
let mut l = vec![1,2,3,4];
let mut doubler = || {          // immutable borrow happens here
    println!("{:?}", l)         // equivalent of '&l'
}
```

```rust
let mut l = vec![1,2,3,4];
let mut doubler = || {          // mutable borrow happens here
    l[0] = l[0] * 2;            // equivalent of '& mut l'
}
```
Hence, Closures borrow in 3 ways using:

- Fn: the closure captures by reference (&T)
- FnMut: the closure captures by mutable reference (&mut T)
- FnOnce: the closure captures by value (T)

This is more of a guideline and rust will find the least restrictive way to borrow.

To define generic closures, the traits Fn, FnMut and FnOnce are used as follows:

```rust
// A function which takes a closure as an argument and calls it.
// <F> denotes that F is a "Generic type parameter"
fn apply<F>(f: F) where F: FnOnce() {
    f();
}
```

Returning closures:

```rust
// Returns a function that adds `y` to its input
fn make_adder_function(y: i32) -> impl Fn(i32) -> i32 {
    let closure = move |x: i32| { x + y };
    closure
}

fn main() {
    let plus_one = make_adder_function(1);
    assert_eq!(plus_one(2), 3);
}
```
