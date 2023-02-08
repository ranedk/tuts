fn main() {

    let mut a = String::from("Hello ");
    let b = &mut a;

    a.push_str(" ?? ");
    b.push_str("World!");

    println!("b = {:?}", b);
    println!("a = {:?}", a);
}
