# Structuring the project

In rust, you can structure your project in the following way:
**Packages**: A Cargo feature that lets you build, test, and share crates
**Crates**: A tree of modules that produces a library or executable
**Modules and use**: Let you control the organization, scope, and privacy of paths
**Paths**: A way of naming an item, such as a struct, function, or module

`cargo new project`
creates a binary package.

`cargo new --lib project`
creates a library package

Binary crate is the one with src/main.rs, it can have multiple binary crates
Library crate is the one with src/lib.rs, it can have only one library crate

Inside a library crate, src/lib.rs, you can create a `module` and `submodule` that can be used using the `use` keyword

```rust
fn serve_order() {}

mod front_of_house {
    pub mod hosting {                   // Expose as public, to be called outside
        pub fn add_to_waitlist() {}     // Expose function as public

        fn seat_at_table() {            // Not exposed, can't be called from outside
            super::serve_order();       // Call a method just ouside the mod scope
        }
    }

    mod serving {
        fn take_order() {}

        fn serve_order() {}

        fn take_payment() {}
    }
}


pub fn eat_at_restaurant() {
    // Absolute path
    crate::front_of_house::hosting::add_to_waitlist();

    // Relative path
    front_of_house::hosting::add_to_waitlist();
}
```

## Structs access
```rust
mod back_of_house {
    pub struct Breakfast {          // public struct
        pub toast: String,          // public field
        seasonal_fruit: String,     // private field
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {       // public struct method
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }

    pub enum Appetizer {            // public Enum
        Soup,                       // if enum is public, its variants are public but default
        Salad,
    }
}

pub fn eat_at_restaurant() {
    let mut meal = back_of_house::Breakfast::summer("Rye");
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);
}
```

## `use` to get the namespace in upper levels
```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

pub use crate::front_of_house::hosting; // hosting is now in package scope
                                        // can be accessed as front_of_house::hosting OR
                                        // crate::front_of_house:hosting OR
                                        // hosting

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();         // because of use, this is possible otherwise use longer path
    hosting::add_to_waitlist();
    hosting::add_to_waitlist();
}
```
