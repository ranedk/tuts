# Installation
`curl https://sh.rustup.rs -sSf | sh`
Put `$HOME/.cargo/bin:$PATH` in your .bashrc or .zshrc `PATH` variable

# Cargo - The package manager

# Hello World
Create a file `main.rs`
```rust
fn main() {
    println!("Hello, World!");
}
```
```bash
rustc main.rs
./main      # Outputs "Hello World"
```
