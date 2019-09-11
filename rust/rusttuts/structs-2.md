# Structs

```rust
#[derive(Debug)]                // this over a struct means rust will help in printing it
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

let user1 = User {
    email: String::from("someone@example.com"),
    username: String::from("someusername123"),
    active: true,
    sign_in_count: 1,
};

user1.email = String::from("anotheremail@example.com");
println!("user1={:?}", user1);          // the syntax {:?} helps print the struct properly using #[derive(Debug)]

let email = String::from("admin");
let username = String::from("admin@gmail.com");

let u2 = User {
    email,          // you dont have to use email: <email> iff the variable name is also email
    username,       // syntax only possible if variable name is same as the struct key
    sign_in_count: 1,
    active: true
};

fn build_user(email: String, username: String) -> User {
    User {
        email,
        username,
        active: true,
        sign_in_count: 1,
    }
}

// Update syntax
let user3 = User {
    email: String::from("another@example.com"),
    username: String::from("anotherusername567"),
    ..user1                                             // Update using another struct
};

// Tuple struct without field names
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

let black = Color(0, 0, 0);
let origin = Point(0, 0, 0);

println!("origin.x={}", origin.0);
```
# Structs and methods

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {                // implement Rectangle methods
    fn area(&self) -> u32 {     // takes a immutable reference
        self.width * self.height
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

fn main() {
    let rect1 = Rectangle { width: 30, height: 50 };

    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );

    let rect2 = Rectangle { width: 10, height: 40 };
    let rect3 = Rectangle { width: 60, height: 45 };

    println!("Can rect2 hold rect3? {}", rect2.can_hold(&rect3));
}
```
NOTE: It doesn't matter if the struct method is defined on `self`, `&self`, `mut self` or `&mut self`. Calling `rect.area()` will do the right thing. However, the parameter passed must be of the right type `rect2.can_hold(&rect3)` CANNOT be written as `rect2.can_hold(rect3)`

**If original variable is defined as mutable `let mut rect = Rectangle {width: 10, height: 20}`. Then for defining methods**

|Passing  |  What it means |
| --- | --- |
|`self`  |  Immutable variable passed with ownership, you lose control to rect(cannot use it again) and function cannot mutate it either |
|`&self` |  Immutable reference passed, you retain control to use it again, the function cannot mutate it |
|`mut self` | Mutable variable passed with ownership, you lose control to rect, the function can mutate it though |
|`&mut self` | Mutable reference passed, you retain control to use it again, the function can mutate it |

## Static function
Like `String::from`

```rust
impl Rectangle {
    fn square(size: u32) -> Rectangle {             // Not called on self
        Rectangle { width: size, height: size }
    }
}
```

Multiple `impl` blocks are fine too
