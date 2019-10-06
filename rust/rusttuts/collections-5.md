# Collections

Collections can contain multiple values.  Is stored on the heap, which means the amount of data does not need to be known at compile time and can grow or shrink as the program runs.

# Vector

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
v.push(4);                      // Compiler error: already borrowed in the above line
                                // any part of v, once borrowed, makes v completely borrowed
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
for i in v {                   // This is like ownership to the for loop
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


    for i in v {
        println!(">{}", i);
    }
}
```

#### The right way
```rust
let mut v = vec![100, 32, 57];
for i in &mut v {               // pass a mutable borrow
    *i += 50;
}
```
