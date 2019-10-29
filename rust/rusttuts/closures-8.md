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
let add_one_v4 = |x|
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
Closures can borrow in 3 ways using traits:

- FnOnce (self) are functions that can be called once,
- FnMut (&mut self) are functions that can be called if they have &mut access to their environment
- Fn (&self) are functions that can still be called if they only have & access to their environment.
