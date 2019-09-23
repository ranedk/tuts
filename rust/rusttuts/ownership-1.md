# Stack Vs Heap
For a detailed discussion:
https://stackoverflow.com/questions/79923/what-and-where-are-the-stack-and-heap

## Quick pointers:

### Stack
Typically, the compiler stores the code in the stack and as the execution progresses, it puts and removes functions and variables from the Stack.
Since, Stack is not dynamic, exact allocation is known to the compiler beforehand, which makes allocation, deallocation very fast.

- Very fast access, LIFO access
- Stored in RAM.
- Function calls are loaded here along with the local variables and function parameters passed.
- Space is freed automatically when program goes out of a scope.
- Stored in sequential memory.

### Heap
All variables which need memory dynamically during runtime, are stored in heap.
1) A check is needed to see how much space is need
2) Check if that space is available in a contigous chunk
3) If yes, then allocate, else increase heap size by asking OS for more space.
4) On deallocation, adds the heap to its free pool.

- Slow access comparatively to Stack.
- Stored in RAM.
- Dynamically created variables are stored here, which later requires freeing the allocated memory after use.
- Stored wherever memory allocation is done, accessed by pointer always.

Stack is thread specific and Heap is application specific.

# Ownership

## Rules
- Each value in Rust has a variable that’s called its owner.
- There can only be one owner at a time.
- When the owner goes out of scope, the value will be dropped.

All primitive types are stored in stack, `String` is stored in heap

### String type
String literals, like the ones used in `println!` statements are hardcoded into the code and are immutable.

Heap is used for dynamic strings only, one way to make string and not string literal is

```rust
let s = String::from("hello");
```

When it goes out of scope, rust internally calls `drop` which releases the memory back to the OS
Stack and heap are treated differently, because stack is efficient and only meant for primitive values (with known sizes), while heap is for dynamic values and slow.

Note: Primitive values (stored in stack) are copied on re-assignment, Complex values (stored in heap) are not copied since its slow.

```rust

    let x = 10;                                 // stored in stack
    let y = x;                                  // value 10 is copied in stack, both x,y point to different 10 in stack
    println!("x={}, y={}", x, y);


    let s1 = "hello boss";                      // stored in stack
    let s2 = s1;                                // value is copied again in stack like above, since this is a string literal
    println!("s1={}, s2={}", s1, s2);


    let s1 = String::from("hello boss");        // stored in heap
    let s2 = s1;                                // value is not copied, pointer is set to the same value
    println!("s1={}, s2={}", s1, s2);           // ERROR! s1 is invalid now (in rust this helps it maintain sanity and safety)


    let s1 = String::from("hello boss");        // stored in heap
    let s2 = s1.clone();                        // value is  copied (deepcopy) in heap (expensive)
    println!("s1={}, s2={}", s1, s2);
```

### Functions

- If a value is simply passed to the function, it takes the ownership of the value. Any reference to the value in the caller will be invalid after that.
- If a function takes a value and then returns the same value, the caller gets back the ownership of the value.

```rust
fn main() {
    let s0 = String::from("rust");

    takes_ownership(s0);                // calls to s0 after this will be invalid

    let s1 = gives_ownership();         // gives_ownership moves its return value into s1

    let s2 = String::from("hello");     // s2 comes into scope

    let s3 = takes_and_gives_back(s2);  // s2 is moved into takes_and_gives_back, which also
                                        // moves its return value into s3

} // Here, s3 goes out of scope and is dropped. s2 goes out of scope but was
  // moved, so nothing happens. s1 goes out of scope and is dropped.

fn takes_ownership(s: String) {
    println!("s={}", {})
}

fn gives_ownership() -> String {             // gives_ownership will move its
                                             // return value into the function
                                             // that calls it

    let some_string = String::from("hello"); // some_string comes into scope

    some_string                              // some_string is returned and
                                             // moves out to the calling
                                             // function
}

// takes_and_gives_back will take a String and return one
fn takes_and_gives_back(a_string: String) -> String { // a_string comes into scope

    a_string  // a_string is returned and moves out to the calling function
}
```

**You are return 2 values (tuples) from functions too**
```rust
fn main() {
    let s1 = String::from("hello");

    let (s2, len) = calculate_length(s1);

    println!("The length of '{}' is {}.", s2, len);
}

fn calculate_length(s: String) -> (String, usize) {
    let length = s.len(); // len() returns the length of a String
    (s, length)
}

```

## References and Borrowing

```rust
fn main() {
    let s1 = String::from("hello");

    let len = calculate_length(&s1);            // pass a reference using & operator (ownership is not changed)

    println!("The length of '{}' is {}.", s1, len);
}

fn calculate_length(s: &String) -> usize {      // function specifies that it needs a reference only
    s.len()                                     // This function can access reference, not modify it since its not the owner
}

fn change(s: &String) -> {
    s.push_str(" world");                       // ERROR! doesn't own, hence cannot mutate
}
```

### Mutable reference
Obviously, you cannot have mutable reference to a immutable variable.
```rust
fn main() {
    let mut s = String::from("hello");
    change(&mut s);                             // pass a mutable reference
}

fn change(some_string: &mut String) {           // function specifically wants a mutable reference
    some_string.push_str(", world");            // owns the reference, so can change it
}
```
However, to make it safe, you can only have ONE mutable reference at a time
```rust
let mut s = String::from("hello");

let r1 = &mut s;
let r2 = &mut s;            // ERROR! NO CAN DO

println!("{}, {}", r1, r2);
```
Because of only one reference, only one pointer will be able to change the data at any point (eliminates such race conditions)
```rust
let mut s = String::from("hello");

{
    let r1 = &mut s;

} // r1 goes out of scope here, so we can make a new reference with no problems.

let r2 = &mut s;
```
- You can have more than 1 immutable references _in the same scope_ (no one is changing data, so cool)
- If there are immutable references(s), you cannot have a mutable reference _in the same scope_ (to avoid surprise behavior for immutable reference holders, who can have their data change without their knowledge)

*In the same scope* - Scope is not just blocks or functions, but also, when a variable is not used in the code, rust automatically puts it out of scope after the last time it is used. Hence:
```rust
let mut s = String::from("hello");

let r1 = &s;        // first immutable reference
let r2 = &s;        // second immutable reference
println!("{} and {}", r1, r2);
// r1 and r2 are no longer used after this point, so not in the scope below this

let r3 = &mut s;    // mutable reference, fine here since immutable ref are out of scope
println!("{}", r3);
```
- A function cannot return a pointer for which the value was created inside the function
```rust
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s                  // ERROR: must return s instead of &s
                        // scope of s ends after this function, so the reference cannot be returned
}
```
## Slicing (only for ASCII only)
Much like python
```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];        // Initial index is 0


let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];        // Final index is end of string
```

String slice is of type `&str`
Similar rules of ownership apply on strings and their slices

```rust
// All other list types also have slices
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3]        Slice is of type &[i32]
```
NOTE: For slicing and general ownership guideline. At any point of time, there should only be one available way to modify a variable.

Consider the following:
```rust
    let mut a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let slice = &mut a[3..7];

    // We have created 2 ways to mutate the list, one via `a` and the other via `slice`

    // Only one of the below lines will be valid now, NOT BOTH (uncomment and check)

    // slice[2] = 100;
    // a[2] = 200;

    // println! means that the variable is in use and is in scope, depending on the above lines
    // the following lines will be valid or not. uncomment and check

    //println!("after a={:?}", a);
    //println!("after slice={:?}", slice);
```
