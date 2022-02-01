# Tests

You can write tests annotate the with `#[cfg(test)]` and make all functions visible to the test module. e.g.

```rust
pub fn greeting(name: &str) -> String {
    format!("Hello {}!", name)
}

#[cfg(test)]            // This will be run when you run $ cargo test
mod tests {
    use super::*;       // Make all visible inside this module

    #[test]
    fn greeting_contains_name() {
        let result = greeting("Carol");
        assert!(result.contains("Carol"));
    }
}
```

## Basic assert macros

- `assert!`
- `assert_eq!`
- `assert_ne!`

## Check Panic

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic]
    fn greater_than_100() {         // This should panic
        Guess::new(200);
    }

    #[test]
    #[should_panic(expected = "This value must be greater than 200")]
    fn greater_than_200() {         // This should panic with the expected message
        Guess::new(400);
    }
}
```

Anything annotated with test will be run when you run `cargo test`

More options will `cargo test` available on the cargo test [documentation page](https://doc.rust-lang.org/1.30.0/book/second-edition/ch11-02-running-tests.html)

Write integration tests inside a test directory and import library directly inside it.

```rust
// inside tests/integration_test.rs
use adder;

#[test]
fn it_adds_two() {
    assert_eq!(4, adder::add_two(2));
}
```

Run using `cargo test --test integration_test`
