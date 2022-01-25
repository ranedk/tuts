## An attribute is metadata applied to some module, crate or item. This metadata can be used to/for:

- Conditional compilation of code
- Set crate name, version and type (binary or library)
- disable lints (warnings)
- enable compiler features (macros, glob imports, etc.)
- link to a foreign library
- mark functions as unit tests
- mark functions that will be part of a benchmark


e.g.
```rust
#[attribute(value, value2)]     // this attribute affects the module after this
OR
#[attribute(value, value2, value3,
            value4, value5)]

#![crate_attribute]   // with ! this attribute affects the crate
```

Disable lint `#[allow(dead_code)]`

```rust
// This crate is a library
#![crate_type = "lib"]
// The library is named "rary"
#![crate_name = "rary"]
```

## cfg
Config driven attributes:
```rust
#[cfg(target_os = "linux")]
fn are_you_on_linux() {
    println!("You are running linux!");
}
// OR
fn are_you_on_linux() {
    if cfg!(target_os = "linux") {
        println!("Yes. It's definitely linux!");
    } else {
        println!("Yes. It's definitely *not* linux!");
    }
}
```
**Custom CFG**
```rust
#[cfg(some_condition_1)]
fn conditional_function() {
    println!("condition 1 met!");
}

#[cfg(some_condition_2)]
fn conditional_function() {
    println!("condition 2 met!");
}

fn main() {
    conditional_function();
}
```
Compile the above with `rustc --cfg some_condition_1 custom.rs && ./custom`
to get first function to compile


## Derive traits via attributes
The compiler is capable of providing basic implementations for some traits via the `#[derive]` attribute. These traits can still be manually implemented if a more complex behavior is required.

The following is a list of derivable traits:

- Comparison traits: Eq, PartialEq, Ord, PartialOrd.
- Clone, to create T from &T via a copy.
- Copy, to give a type 'copy semantics' instead of 'move semantics'.
- Hash, to compute a hash from &T.
- Default, to create an empty instance of a data type.
- Debug, to format a value using the {:?} formatter.

e.g. `#[derive(PartialEq, PartialOrd)]`
