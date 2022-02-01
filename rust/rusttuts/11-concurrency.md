# Concurrency

## Threading
Rust tries to have ZERO runtime, so it has no green threads. So it uses os threads:

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from the spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {} from the main thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
    handle.join().unwrap();     // join call, to wait for thread to finish
}
```

```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(move || {    // v in the environment will be moved to the thread now
        println!("Here's a vector: {:?}", v);
    });

    handle.join().unwrap();
    // v is not accessble here now
}
```

# Channel based (just like Go, Elixir)
```rust
use std::thread;
use std::sync::mpsc;

fn main() {
    // create a multi-producer, single consumer channel
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        // send return a Result<T, E>, unwrap in case receiver has been dropped, panic
        tx.send(val).unwrap();
        // val is not unreachable, since another thread owns it now.
    });

    // recv call blocks till something is received. If tx is dropped, unwrap will panic
    // try_recv is another call which doesn't block
    let received = rx.recv().unwrap();
    println!("Got: {}", received);
}
```

## Multiple transmitter
You can clone transmitters

```rust
let (tx, rx) = mpsc::channel();

let tx1 = mpsc::Sender::clone(&tx);
thread::spawn(move || {
    let vals = vec![
        String::from("hi"),
        String::from("from"),
        String::from("the"),
        String::from("thread"),
    ];

    for val in vals {
        tx1.send(val).unwrap();
        thread::sleep(Duration::from_secs(1));
    }
});

thread::spawn(move || {
    let vals = vec![
        String::from("more"),
        String::from("messages"),
        String::from("for"),
        String::from("you"),
    ];

    for val in vals {
        tx.send(val).unwrap();
        thread::sleep(Duration::from_secs(1));
    }
});

for received in rx {
    println!("Got: {}", received);
}
```
