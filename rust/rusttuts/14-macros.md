# Macros (meta-programming bro!)

## Simple macro - no argument - block of code
```rust
macro_rules! say_hello {
    // `()` indicates that the macro takes no argument.
    () => {
        // The macro will expand into the contents of this block.
        println!("Hello!");
    };
}

fn main() {
    // This call will expand into `println!("Hello");`
    say_hello!()
}
```
## With arguments
The arguments of a macro are prefixed by a dollar sign $ and type annotated with a designator. E.g.
```rust
macro_rules! create_function {
    // creates a function named `$func_name`.
    // The `ident` designator is used for variable/function names.
    ($func_name: ident) => {
        fn $func_name() {
            // The `stringify!` macro converts an `ident` into a string.
            println!("You called {:?}()",
                     stringify!($func_name));
        }
    };
}
```

```rust
macro_rules! print_result {
    // This macro takes an expression of type `expr` and prints
    // it as a string along with its result.
    // The `expr` designator is used for expressions.
    ($expression:expr) => {
        // `stringify!` will convert the expression *as it is* into a string.
        println!("{:?} = {:?}",
                 stringify!($expression),
                 $expression);
    };
}
```

There are many other desginators in rust. e.g.:
- block
- expr is used for expressions
- ident is used for variable/function names
- item
- literal is used for literal constants
- pat (pattern)
- path
- stmt (statement)
- tt (token tree)
- ty (type)
- vis (visibility qualifier)

### Multiple arguments to macro
```rust
macro_rules! test {
    // Arguments don't need to be separated by a comma.
    // ^ each arm must end with a semicolon.
    // Any template can be used!
    ($left:expr; and $right:expr) => {
        println!("{:?} and {:?} is {:?}",
                 stringify!($left),
                 stringify!($right),
                 $left && $right)
    };
    // ^ each arm must end with a semicolon.
    ($left:expr; or $right:expr) => {
        println!("{:?} or {:?} is {:?}",
                 stringify!($left),
                 stringify!($right),
                 $left || $right)
    };
}

// Usage:
test!(1i32 + 1 == 2i32; and 2i32 * 2 == 4i32);
```

### Repeating patterns in template
```rust
macro_rules! find_min {
    // Base case:
    ($x:expr) => ($x);
    // `$x` followed by at least one `$y,`
    ($x:expr, $($y:expr),+) => (
        // Call `find_min!` on the tail `$y`
        std::cmp::min($x, find_min!($($y),+))
    )
}

// Usage:
find_min!(5u32, 2u32 * 3, 4u32));
```
