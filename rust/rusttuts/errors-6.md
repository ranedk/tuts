# Error handling

- Non-recoverable error `panic!`
- Recoverable error `Result<T, E>` (e.g. file not found before reading)

Adding the following to Cargo.toml will lead to lower binary size. This will not give any tracebacks in case of panics
```
[profile.release]
panic = 'abort'
```

To get complete traceback in case in panic
```bash
$ RUST_BACKTRACE=1 cargo run
```

## Result<T, E>

The internal implementation of `Result`
```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

### Usage:
```rust
let f = File::open("hello.txt");

let f = match f {
    Ok(file) => file,
    Err(error) => {
        panic!("Problem opening the file: {:?}", error)
    },
};
```

### To catch only specific error
```rust
let f = File::open("hello.txt");

let f = match f {
    Ok(file) => file,
    Err(error) => match error.kind() {
        ErrorKind::NotFound => match File::create("hello.txt") {
            Ok(fc) => fc,
            Err(e) => panic!("Problem creating the file: {:?}", e),
        },
        other_error => panic!("Problem opening the file: {:?}", other_error),
    },
};
```

### Using Closure - more rusty
```rust
let f = File::open("hello.txt").unwrap_or_else(|error| {
    if error.kind() == ErrorKind::NotFound {
        File::create("hello.txt").unwrap_or_else(|error| {
            panic!("Problem creating the file: {:?}", error);
        })
        } else {
        panic!("Problem opening the file: {:?}", error);
    }
});
```

### Shortcuts (unwrap and expect)
```rust
// panic on error
let f = File::open("hello.txt").unwrap();

// manage exceptions on error
let f = File::open("hello.txt").expect("Failed to open hello.txt");
```
Other shortcuts:

- `unwrap`:
    - Unwraps a result, yielding the content of an `Ok`.
    - Panics if the value is an `Err`, with a panic message provided by the `Err`'s value.

- `expect`:
    - Unwraps a result, yielding the content of an `Ok`.
    - Panics if the value is an `Err`, with a panic message including the passed message, and the content of the `Err`.

- `unwrap_err`:
    - Unwraps a result, yielding the content of an `Err`.
    - Panics if the value is an `Ok`, with a custom panic message provided by the `Ok`'s value.

- `expect_err`:
    - Unwraps a result, yielding the content of an `Err`.
    - Panics if the value is an `Ok`, with a panic message including the passed message, and the content of the `Ok`.

- `unwrap_or_default`:
    - Returns the contained value or a default. Consumes the self argument then, if Ok, returns the contained value, otherwise if Err, returns the default value for that type.
    - Code:
    ```rust
        let good_year_from_input = "1909";
        let bad_year_from_input = "190blarg";
        let good_year = good_year_from_input.parse().unwrap_or_default();
        let bad_year = bad_year_from_input.parse().unwrap_or_default();

        assert_eq!(1909, good_year);
        assert_eq!(0, bad_year);
    ```

### Raise error inside a function
```rust

// The regular boring way
fn read_username_from_file() -> Result<String, io::Error> {     // output signature
                                                                // is result with error
    let f = File::open("hello.txt");

    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),                // return error
    };

    let mut s = String::new();

    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),                       // this returns, then match returns
    }
}

// Rust provides a shortcut
fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;   // notice the `?`
    let mut s = String::new();
    f.read_to_string(&mut s)?;              // return error to function
    Ok(s)
}

// The rust cool way
fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new();

    File::open("hello.txt")?.read_to_string(&mut s)?;   // chain with `?`

    Ok(s)
}
```

> Note: The `?` stuff works only if methods don't panic, but return `Result<T, E>`

Interesting, consider the following snippet:
```rust
    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),                       // this returns, then match returns
    }
```
The shortcut to this is:
```rust
if let Err(e) = f.read_to_string(&mut s) {
    println!("Application error: {}", e);
}
```

#### Particularly for reading a file, you don't have to do the above. you can simply
```rust
fs::read_to_string("hello.txt")
```

## How to make a function return Result, None and Error

This is pretty cool
```rust
use std::num::ParseIntError;

fn double_first(vec: &Vec<&str>) -> Result<Option<i32>, ParseIntError> {
    let opt = vec.first().map(|first| {
        first.parse::<i32>().map(|n| 2 * n)
    });

    opt.map_or(Ok(None), |r| r.map(Some))
}


fn print_result(res: Result<Option<i32>, ParseIntError>) {
    match res {
        Ok(o) => {
            match o {
                Some(r) => { println!("Result is {:?}", r) }
                None => { println!("No result") }
            }
        }
        Err(e) => {
            println!("Error happened {:?}", e);
        }
    }
}


fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    println!("Result of the operations is: {:?}", double_first(&numbers));

    print_result(double_first(&numbers));
    print_result(double_first(&empty));
    print_result(double_first(&strings));
}
```
Interesting utility functions on `Result` instances:

- `map`: Maps a `Result<T, E>` to `Result<U, E>` by applying a function to a contained `Ok` value, leaving an `Err` value untouched
```rust
let line = "1\n2\n3\n4\n";

for num in line.lines() {
    match num.parse::<i32>().map(|i| i * 2) {
        Ok(n) => println!("{}", n),
        Err(..) => {}
    }
}
```

- `map_or`: Applies a function to the contained value (if any), or returns the provided default (if not)
```rust
let result_is_ok: Result<_, &str> = Ok("foo");
assert_eq!(result_is_ok.map_or(42, |v| v.len()), 3);
// If result_is_ok has contained value (foo), apply lambda |v| v.len()

let result_is_err: Result<&str, _> = Err("bar");
assert_eq!(result_is_err.map_or(42, |v| v.len()), 42);
// If result_is_err has contained value, apply lambda |v| v.len(), else give 42
```

- `map_err`: Maps a `Result<T, E>` to `Result<T, F>` by applying a function to a contained `Err` value, leaving an `Ok` value untouched
```rust
fn stringify(x: u32) -> String { format!("error code: {}", x) }

let x: Result<u32, u32> = Ok(2);
assert_eq!(x.map_err(stringify), Ok(2));

let x: Result<u32, u32> = Err(13);
assert_eq!(x.map_err(stringify), Err("error code: 13".to_string()));
```

- `map_or_else`: Maps a `Result<T, E>` to `U` by applying a function to a contained `Ok` value, or a fallback function to a contained `Err` value.
```rust
let k = 21;

let x : Result<_, &str> = Ok("foo");
assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 3);

let x : Result<&str, _> = Err("bar");
assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 42);
```

## Errors in a loop
If you get errors while looping a iterable and doing a map operation, rust gives you cool ways to manage the output values:

```rust
let strings = vec!["tofu", "93", "18"];
let numbers: Result<Vec<_>, _> = strings
    .into_iter()
    .map(|s| s.parse::<i32>())
    .collect();                    // panics since "tofu" cannot be parsed
println!("Results: {:?}", numbers);
```

```rust
let strings = vec!["tofu", "93", "18"];
let numbers: Vec<_> = strings
    .into_iter()
    .map(|s| s.parse::<i32>())
    .filter_map(Result::ok)     // Filter with only Ok values, then collect
    .collect();
println!("Results: {:?}", numbers);
```

```rust
let strings = vec!["tofu", "93", "18"];
let (numbers, errors): (Vec<_>, Vec<_>) = strings
    .into_iter()
    .map(|s| s.parse::<i32>())
    .partition(Result::is_ok);  // Collects while separating Ok and Err into
                                // two vector tuples
println!("Numbers: {:?}", numbers);
println!("Errors: {:?}", errors);
```
