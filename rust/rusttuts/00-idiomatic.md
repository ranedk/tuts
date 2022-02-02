# Idiomatic Rust - Patterns and Packages

If you have covered all the other Rust concepts, this chapter convers most commonly used idioms and packaged while doing rust development.

## IDE

- IntelliJ (Community edition) with Rust plugin - Debugging support not available
- [VSCode with CodeLLDB extension](https://levelup.gitconnected.com/rust-with-visual-studio-code-46404befed8) - With debugging
- CLion (paid) - Best IDE with native debugging
- [Neovim setup](https://www.youtube.com/watch?v=CcgO_CV3iDo&list=PLu-ydI-PCl0OEG0ZEqLRRuCrMJGAAI0tW)

## Tips

- Always use `&str` for function arguments instead of `&String`, `&[T]` instead of `&Vec<T>` and `&T` over `&Box<T>` for more flexibility in calling function.
- `format!` to add and format strings instead of `push_str` (which is faster, but looks bad) or `+` operator
- `::new` static method as constructor (the `Default` trait if the implementation is a default)


## Serialization/Deserialization using Serde

Serde is the most complete and fast module in rust to manage multiple types of data formats.

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let point = Point { x: 1, y: 2 };

    // Convert the Point to a JSON string.
    let serialized = serde_json::to_string(&point).unwrap();

    // Prints serialized = {"x":1,"y":2}
    println!("serialized = {}", serialized);

    // Convert the JSON string back to a Point.
    let deserialized: Point = serde_json::from_str(&serialized).unwrap();

    // Prints deserialized = Point { x: 1, y: 2 }
    println!("deserialized = {:?}", deserialized);
}
```

#### Custom json

```rust
#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]  // <-- this is a container attribute
struct S {
    #[serde(default)]  // <-- this is a field attribute
    f: i32,
}

#[derive(Serialize, Deserialize)]
#[serde(rename = "e")]      // <-- this is also a container attribute
enum E {
    #[serde(rename = "a")]  // <-- this is a variant attribute
    A(String),
}
```

More complicated and detailed customization is [possible with serde](https://serde.rs/attributes.html)

## Other packages

- Reading environment variables - [Envy](https://crates.io/crates/envy)
- Easier error management - [Anyhow](https://docs.rs/anyhow/1.0.53/anyhow/)
- Date time management - [Chrono](https://docs.rs/chrono/0.4.19/chrono/)
- Logging - [Log](https://docs.rs/log/0.4.14/log/)
- [Opentelemetry](https://docs.rs/opentelemetry/0.17.0/opentelemetry/) 
- Http clients - [Hyper](https://hyper.rs/guides/client/basic/) , [Reqwest](https://docs.rs/reqwest/0.11.9/reqwest/)
- Command line argument parser - [Clap](https://crates.io/crates/clap)
- Caching Memoization - [Cached](https://crates.io/crates/cached)
- Filesystem walking - [WalkDir](https://crates.io/crates/walkdir), [Glob](https://docs.rs/glob/0.3.0/glob/)


