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

