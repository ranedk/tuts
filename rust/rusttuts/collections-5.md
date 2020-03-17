# Collections

Collections can contain multiple values.  Is stored on the heap, which means the amount of data does not need to be known at compile time and can grow or shrink as the program runs.

# Vectors

```rust
let mut v: Vec<i32> = Vec::new();   // vector to store i32 only

let mut v = vec![1, 2, 3];          // Macro which infers Vec type, same as above

v.push(10);

let third = v[2];

let tenth = v.get(11);          // tenth gets inferred as Option type
match tenth {
    None => println!("None"),
    Some(i) => println!("{}", i)
}

let ninth = v[9];               // runtime error, out of bounds


let n = &v[1];                  // Immutable borrow, n has borrowed some part of v
```

### Scenario 1
```rust
let v = vec![100, 32, 57, 34, 76, 43, 34, 65, 23];
for i in &v {                   // for-loop is borrowing the ownership of v
    println!("{}", i);
}
v.push(10);                     // Invalid, since v is defined a immutable
```

### Scenario 2
```rust
let mut v = vec![100, 32, 57, 34, 76, 43, 34, 65, 23];
for i in &v {                   // This is like passing the reference to for loop
    println!("{}", i);
}
v.push(10);                     // Valid, since v is mutable and reference was passed above
```

### Scenario 3
```rust
let mut v = vec![100, 32, 57, 34, 76, 43, 34, 65, 23];
for i in v {                   // This is like ownership to the for loop, v is moved
    println!("{}", i);
}
v.push(10);                     // Invalid, since ownership is not here anymore
```

## Changing values in a loop

```rust
fn main() {
    let mut v = vec![1,2,3,4,5,6,7];

    /*
    for i in v {
        i *= 2;
    }
    // ERROR: error[E0384]: cannot assign twice to immutable variable `i`
    // This doesn't work because i is immutable
    */


    /*
    for mut i in v {
        i *= 2;
    }
    // Compiles, but since v is moved, it cannot be used anymore, so useless
    */


    // for mut i in &v {        // i is a mutable pointer to a immutable v, cannot change *i

    // for mut i in &mut v {    // i is a mutable pointer to a mutable v, can change v

    for i in &mut v {           // i is pointer to a mutable v, can change v
        *i *= 2;
    }

    // display in a loop. no need for mutable reference
    for i in &v {
        println!(">{}", i);     // i or *i, both work
    }
}
```

### The right way
```rust
let mut v = vec![100, 32, 57];
for i in &mut v {               // pass a mutable borrow
    *i += 50;
}
```

## Multi-type Vectors using Enum

```rust
enum SpreadSheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

let row = vec![
    SpreadsheetCell::Int(3),
    SpreadsheetCell::Text(String::from("blue")),
    SpreadsheetCell::Float(10.12),
];

// use match to loop and do the rest
```

### Helpers
- pop
- push


# String & Slices

- `str` is immutable, stored in stack
- `String` is stored in heap and is mutable.
- you never interact with `str`, you will always get `&str` to code with
- `&String` get coerced to Slice `&str` by the compiler
- `String` and `str` are not coerced and are different types

```rust
let mut s = String::from("foo");    // equivalent to let mut s = "foo".to_string()

s.push('r');                        // append a characer

s.push_str("ba");                   // append strings, push_str takes a slice and not a string
                                    // since, if it took a string and the ownership, the appended string
                                    // would be useless e.g.
let mut s1 = String::from("foo");
let s2 = "bar";
s1.push_str(s2);                    // if push_str would take a string and the ownership, s2 couldn't be used later
println!("s2 is {}", s2);           // this works, because push_str takes a slice
```

## Concat using + operator
```rust
let s1 = String::from("Hello, ");
let s2 = String::from("world!");
let s3 = s1 + &s2;                  // s1 has been moved here and can no longer be used

let s4 = &s1 + &s2;                 // wont compile, operator is written on String and not &String
let s5 = s1 + s2;                   // wont compile, operator expects a &String and not String

let s5 = s1 + &s2[0..3];            // Compiles! the second param is &str and not &String, but this works.
                                    // the operator takes &str actually, so even if you pass &String (like
                                    // above, it works, since &String can be coerced to &str by compiler.
                                    // Internally, it take ownership of s1, appends s2 and return s1 back
```

### Best way to concatenate - format
```rust
let s = s1 + "-" + s2 + "-" + s3 + "-";     // Ownership is difficult to comprehend, so better not use this

let s = format!("{}-{}-{}", s1, s2, s3);
```

## Unicode

Unicode string are difficult to index, because unlike ascii characters, where each ascii character takes 1 byte, unicode characters may take more than 1 byte. e.g.
"д", "й" are 2 bytes

```rust
let s = "hello дравствуй";

let s1 = &s[0..4];          // s1 become "hell"

let s2 = &s[0..8]           // s2 becomes "hello д"

let s3 = &s[0..9]           // PANIC: Runtime error, 9 is between character boundary
```

So the right way to query strings is:
```rust
for c in "नमस्ते".chars() {
    println!("{}", c);      // prints न म स् ते on separate lines
}

for b in "नमस्ते".bytes() {
    println!("{}", b);      // prints the byte values 224, 164 on separate lines
}
```

# Hashmaps (HashMap<K, V>)

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

// You can also create hashmaps using tuples

let teams  = vec![String::from("Blue"), String::from("Yellow")];
let initial_scores = vec![10, 50];

let scores: HashMap<_, _> = teams   // _ works for type, compiler infers
    .iter()
    .zip(initial_scores.iter())
    .collect();                     // collect is magical, can give different
                                    // output, depending on the LHS (Hashmap here)
```

Keys can be passed by value or by reference. Hashmap owns the ownership is passed directly
```rust
let s0 = String::from("sunday");
let s1 = String::from("monday");

let h = HashMap::new();

h.insert(s0, 0);                     // cannot use `s0` now, hashmap owns s0


let m = HashMap::new();

m.insert(&s1, 0);                   // HashMap will only take reference as keys now
                                    // s1 can be used

println!("{}", m[&s1]);             // outputs 0

let s3 = String::from("tuesday");

let v = m.get(&s3);                 // v is Option<&T>

m.insert(&s1, 2);                   // overwrite value

h.entry(String::from("sunday")).or_insert(50);     // check if key exists, if not, update value
h.entry(String::from("blue")).or_insert(50);

print("{:?}", h)
```

> How hashmaps behave:
> 1) The key can either be a reference or a value, not both.
> 2) Lookups are always done with reference.
> 3) Primitive types like Integers are copied and hashmap doesn't own it.
> 4) Lookups are compared by value (hash value), even if they are created using reference or value

### Loop hashmap
```rust
for (key, value) in &scores {
    println!("{}: {}", key, value);
}
```

### Update existing value
```rust
let text = "hello world wonderful world";

let mut map = HashMap::new();

for word in text.split_whitespace() {
    let count = map.entry(word).or_insert(0);       // Like python defaultdict
    *count += 1;                                    // count is reference, so use `*`
}

println!("{:?}", map);
```

# Box types

- If stack allocated types (e.g. primitive types) are to be allocated in heap, with a pointer to them, then use Box types:
```rust
#[derive(Debug)]
struct Point {
    x: f64,
    y: f64,
}

fn origin() -> Point {
    Point { x: 0.0, y: 0.0 }
}

fn boxed_origin() -> Box<Point> {
    // Allocate this point on the heap, and return a pointer to it
    Box::new(Point { x: 0.0, y: 0.0 })
}

// -------

// Without a box
let point: Point = origin();   // Stack allocated, since space is known to the compiler

// Box point
let boxed_point: Box<Point> = Box::new(origin());

// Box in a box
let box_in_a_box: Box<Box<Point>> = Box::new(boxed_origin());

// Unbox from a box
let unboxed_point: Point = *boxed_point;
```
Boxed instance can call class methods of the boxed class.

## Use cases for Box<T>

1) To create a recursive type, the rust compiler believes they are of infinite size. So use a boxed type as:
```rust
struct Node<T> {
    val: T,
    ptr: Option<Box<Node<T>>>
}
```

2) When you are returning a `Trait` (interface! remember), from a function, you cannot just say `fn func() -> MyTrait` or `fn func() -> &MyTrait`. It doesn't make sense in rust, you have to say either of the following:
    ```rust
    fn get_figure(a: i32, b: i32) -> impl TwoDimension {
        // ...
    }
    ```
    This is called a static dispatch. Meaning that rust compiler finds all the types for which the above have been called and generates the functions with all those types during compile time.

    Also, you cannot return 2 different concrete types from the functions. All return types of the functions MUST be of the same type (because its compile time and compiler must be sure).
    `impl TwoDimension` checks for concrete type implementing the trait

    ```rust
    fn get_point(a: i32, b: i32) -> Box(dyn TwoDimension) {
        // ...
    }
    ```
    The above is called dynamic dispatche, meaning that rust will not do anything in compile time and resolve everything in runtime. Also, you can return different types of concrete types implementing the same trait.
    `dyn TwoDimension` checks for dynamic type implementing the trait

    Dynamic dispatch is slower than Static dispatch (don't care so much about this yet)

3) For performance if T is large and is being moved around a lot, using a Box<T> instead will avoid doing big `memcpys` (memory copy)
