# Smart pointers

A basic vanilla pointer is the one which holds a reference to a memory holding the actual value. So `&a` is the pointer reference to the location `a` where data is stored.

**Smart pointers** also hold meta-data with them to manage more complex tasks. E.g. a Reference counting smart pointer will hold the number of owners of the data, and when the number drops to zero, make it available for garbage collection or deletion. Its available in multiple languages (like C++).

`String` and `Vec<T>` in rust are _smart pointers_ because they hold the meta-data of how many elements are a part of the data-structure. `String` manages valid utf-8 characters using some meta-data.

In Rust, which uses the concept of ownership and borrowing, an additional difference between references and smart pointers is that references are pointers that only borrow data; in contrast, **in many cases, smart pointers own the data they point to.**

Smart pointers implemented as structs, implement the `Deref` and `Drop` traits.

- The Deref trait allows you can write code that works with either references or smart pointers.
- The Drop trait allows you run code when an instance of the smart pointer goes out of scope.

## Box types
Box types discussed in collections and generics are Smart pointers which help you to put data in heap. It implements `Deref` and `Drop` to help pass `Box` type as a reference to the data and delete it when it goes out of scope.

## Understanding Deref
```rust
// Lets implement a basic MyBox type
struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

// Adding Deref trait to MyBox
use std::ops::Deref;

impl<T> Deref for MyBox<T> {
    type Target = T;        // associated type for Deref (covered later)

    fn deref(&self) -> &T {
        &self.0
    }
}

// Usage:
let x = 5;
let y = MyBox::new(x);

assert_eq!(5, x);
assert_eq!(5, *y);  // This works because Deref trait.
                    // Rust understands what to do with the *y
                    // by calling *(y.deref())
```
The deref operator works with 3 cases:

- From &T to &U when T: Deref<Target=U>
- From &mut T to &mut U when T: DerefMut<Target=U>
- From &mut T to &U when T: Deref<Target=U>

## Drop trait
```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

// This just prints the message when rust is dropping the struct instance
```
The `drop` method is called directly by the rust compiler. You are **not allowed** to call the method. Instead, you have to call `std::mem::drop` method to drop objects.

# Reference Counted Smart Pointer Rc\<T>

Use case is to have multiple owners of a single instance and drop it when number of owners becomes zero.
Only used for single threaded scenarios.

## Immutable reference

This one is easy since immutable.

```rust
#[derive(Debug)]
enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};       // import from the current crate
use std::rc::Rc;


fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    println!("count after creating a = {}", Rc::strong_count(&a));

    let b = Cons(3, Rc::clone(&a)); // Clones ownership to b, 2 owners
                                    // This wont work if instead of Rc we are using Box
    println!("count after creating b = {}", Rc::strong_count(&a));

    {
        let c = Cons(4, Rc::clone(&a));
        println!("count after creating c = {}", Rc::strong_count(&a));
    }

    println!("count after c goes out of scope = {}", Rc::strong_count(&a));
}
```

## Mutable reference using RefCell\<T>

The rust compiler is always trying to do things strictly. This might not work for some cases where we know something that the compiler doesn't. For e.g.

1. When programming a low hardware level, your hardware may provide you a memory address to mutate directly, this is unsafe, but the rust compiler doesn't know it.
2. Interacting with code written in another language (like C,C++ etc.). You assume and tell the compiler that its safe to use it and the developer has checked for safety.
3. When using concurrency primitives, if you are "logically" making sure that each thread gets mutable reference to a pointer after all checks have been made. The compiler doesn't know that the "logic" is making the code safe. So you mark the code as unsafe to take the responsibility of safety.
4. Rarely, if there are patterns which the rust borrower-checker is not able to understand in terms of safety and you want to take the onus of safety.
5. Very very rarely, for performance optimizations.

Generally, all these are avoidable. PLEASE AVOID AT CALL COSTS.

However, suppose there is a 3rd party code, which doesn't take mutable objects, then you may need to use `RefCell` to make it extensible. e.g.

```rust
// External code that you have no control on it
pub trait Messenger {
    fn send(&self, msg: &str);
}
//----------------------------------------------

// Suppose I want to extend it

struct MockMessenger {
    sent_messages: Vec<String>,
}

impl MockMessenger {
    fn new() -> MockMessenger {
        MockMessenger { sent_messages: vec![] }
    }
}

impl Messenger for MockMessenger {
    fn send(&self, message: &str) {
        // This wont work because Messenger trait borrow immutably
        // and we are trying to mutate sent_messages
        self.sent_messages.push(String::from(message));  // Compiler error
    }
}
```

To make it work:

```rust
// External code that you have no control on it
pub trait Messenger {
    fn send(&self, msg: &str);
}
//----------------------------------------------

// Suppose I want to extend it

struct MockMessenger {
    sent_messages: RefCell<Vec<String>>,
}

impl MockMessenger {
    fn new() -> MockMessenger {
        MockMessenger { sent_messages: RefCell::new(vec![]) }
    }
}

impl Messenger for MockMessenger {
    fn send(&self, message: &str) {
        // Borrow sent_messages mutably and mutate, even though self
        // is borrowed immutably
        self.sent_messages.borrow_mut().push(String::from(message));

        // To borrow it immutable, you need to use borrow()
        println!("Length: {}", self.sent_messages.borrow().len())
    }
}
```

Note: Remember, you need to use `borrow_mut` and `borrow` with `RefCell`


