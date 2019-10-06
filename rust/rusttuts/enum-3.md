# Enums are awesome to manage states (read this carefully)

```rust
// Definition
enum IpAddrKind {
    V4,
    V6,
}

// Usage
let four = IpAddrKind::V4;
let six = IpAddrKind::V6;

fn route(ip_kind: IpAddrKind) { }

// With Structs for state
struct IpAddr {
    kind: IpAddrKind,
    address: String,
}
let home = IpAddr {
    kind: IpAddrKind::V4,
    address: String::from("127.0.0.1"),
};
let loopback = IpAddr {
    kind: IpAddrKind::V6,
    address: String::from("::1"),
};

// Better Struct usage (enums with params)
enum IpAddr {
    V4(String),
    V6(String),
}

let home = IpAddr::V4(String::from("127.0.0.1"));
let loopback = IpAddr::V6(String::from("::1"));

// Much better usage
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);
let loopback = IpAddr::V6(String::from("::1"));
```
Unlike `struct`, `enum` can only be of one type. In the above example, `home` and `loopback` both are of type `IpAddr` but can either be of type `IpAddr::V4` or `IpAddr::V6`

For a game, which has a series of inputs, you can manage the state with Enums as:
```rust
enum Input {
    Quit,
    Up {x: i32, y: i32},
    Down {x: i32, y: i32},
    Left {x: i32, y: i32},
    Right {x: i32, y: i32},
}

impl Input {
    fn call(&self) {
        // method body would be defined here
    }
}

// Usage
let m = Message::Up{34, 43}
m.call();
```

# Match and Enums
```rust
#[derive(Debug)] // so we can inspect the state
enum UsState {
    Alabama,
    Alaska,
    // ...
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => {
            println!("Its penny!");
            1
        },
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state => {
            println!("For state {:?}", state);
            25
        },
    }
}
```


# The Option Enum (so much better than Null values)
This idea comes from functional languages, but has gained lot of attention being a nice idea.
To avoid null values, wrap around a possible null value into a Option enum, so we always manage null values effectively.
```rust
enum Option<T> {
    Some(T),
    None,
}
```
Usage:
```rust
let x: i8 = 5;
let y: Option<i8> = Some(5);

let sum = x + y;    // ERROR: Cannot add int and option type
```

Option is always checked with match and then used (as below)
```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
```

# Default case
```rust
let some_u8_value = 0u8;
match some_u8_value {
    1 => println!("one"),
    3 => println!("three"),
    5 => println!("five"),
    7 => println!("seven"),
    _ => (),                    // Just return the unit value
}
```

# if - let

If the match only has one thing to match and ignore everything else
```rust
if let Some(3) = some_u8_value {
    println!("three");
}
```

```rust
let mut count = 0;
if let Coin::Quarter(state) = coin {
    println!("State quarter from {:?}", state);
} else {
    count += 1;
}
```
