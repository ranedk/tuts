# Cargo - Package manager

## Basics

`cargo build`
`cargo build --release`

## Cargo.toml

```
[profile.dev]       // dev build profile
opt-level = 0       // optimization level - more means more compile time

[profile.release]   // release build profile
opt-level = 3
```

## Documentation and comments

### Comments - `//`

### Documenting a item

If you want to document the function, you need to put the comments starting with `///` before the function

```rust
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```
To create the document `cargo doc --open`

### Documenting a crate

If you want to document the library or the crate, you need to use `//!` and put this at the top of the crate

```rust
//! # My Crate
//!
//! `my_crate` is a collection of utilities to make performing certain
//! calculations more convenient.

/// Adds one to the number given.
```

### Creating better APIs for a create

```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub use self::kinds::PrimaryColor;          // becomes available public
pub use self::kinds::SecondaryColor;
pub use self::utils::mix;

pub mod kinds {
    // --snip--
}

pub mod utils {
    // --snip--
}
```

### Publish a crate
`crate publish`

# Workspace
Multiple related packages that are developed in tandem, like libraries or apps inside a big project

**Create a project**

`$ mkdir add`

**Create file** `Cargo.toml`

```
[workspace]

members = [
    "adder",
]
```
**Create workspace for main binary**

`adder` will host the binary (main entry point) code

`cargo new adder`

Project structure

```
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

**Create workspace for library**
In file `Cargo.toml`

```
[workspace]

members = [
    "adder",
    "add-one",
]

[dependencies]
add-one = { path = "../add-one" }
```
`cargo new add-one --lib`

**Workspace dependencies inside workspace Cargo.toml**

In file `add-one/Cargo.toml`, put dependencies:

```
[dependencies]

rand = "0.3.14"
```

**Run main project**

`cargo run -p adder`


### Install cargo binaries in the system

`cargo install`

This way you can install binaries like ripgrep using cargo
