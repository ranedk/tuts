# Installation
`curl https://sh.rustup.rs -sSf | sh`

Put `$HOME/.cargo/bin:$PATH` in your .bashrc or .zshrc `PATH` variable

# Cargo - The package manager
Start new project
`cargo new hello`

Build the project
`cargo build`

Run the project
`cargo run`

Check for errors (do not build)
`cargo check`

# Single file - Hello World
Inside `main.rs`
```rust
fn main() {
    println!("Hello, World!");
}
```
```bash
rustc main.rs
./main      # Outputs "Hello World"
```

## Number guessing loop
```rust
use std::io;
use rand::Rng;
use std::cmp::Ordering;


fn main() {
    // loop is a infinite loop
    loop {
        // declare a new string
        let mut guess = String::new();

        // generate a random integer between 1 and 10
        let random = rand::thread_rng().gen_range(1, 10);

        // Get a user input, in case it fails, raise exception with "Failed to read"
        io::stdin().read_line(&mut guess).expect("Failed to read");

        // Take string input, convert it to u32, parse checkes LHS and converts accordingly
        // parse returns Option (Ok and Err) which are matched using match
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        // match works like switch case (explicit break)
        // break in the following code, breaks out of the loop
        match guess.cmp(&random) {
            Ordering::Less => println!("You guessed {}, smaller random is {}", guess, random),
            Ordering::Greater => println!("You guesses {}, greater random is {}", guess, random),
            Ordering::Equal => {
                println!("You got it, the random number is {}", random);
                break;
            },
        }
    }
}
```

## Basics
```rust
let x = 10;      // immutable by default
x = 100;         // Compile time error

let mut y = 10; // defined as mutable
y = 100;        // No problem, y is mutable

const PI: f32 = 22.0/7.0;      // const (immutable by default)

let a = 1;
let a = 4;      // shadowing variable is allowed
let a = a * 2;  // shadowing with previous value transformation is good too
```

### Data types
- Integer: i8, i16, i32, i64, i128, isize (as per architecture, i32 on 32 bit, i64 on 64 bit)
- Unsigned integer: u8, u16, u32, u64, u128, usize (as per archutecture, u32 on 32 bit, u64 on 64 bit)
- Number Literals
    - Decimal           98_222
    - Hex               0xff
    - Octal             0o77
    - Binary            0b1111_0000
    - Byte (u8 only)    b'A'

- Float: f32, f64
- Boolean: bool  (true, false)
- Characters: e.g. 'a', '😻' (single quoted)

- Complex types
    - Tuples
        ```rust
        let tup: (i32, f64, u8) = (500, 6.4, 1);
        let (x, y, z) = tup;                        // python like pattern match
        let a = tup.0                               // x.<index> to get elements
        ```
    - Arrays
        ```rust
        let a = [1, 2, 3, 4, 5];                    // inferred

        let a: [i32; 5] = [1, 2, 3, 4, 5];          // explict

        let a = [3; 5];                             // equivalent of let a = [3, 3, 3, 3, 3]
        ```
