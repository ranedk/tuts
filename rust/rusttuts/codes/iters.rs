#[derive(PartialEq, Debug)]
struct Shoe {
    size: u32,
    style: String,
}

fn shoes_in_my_size(shoes: Vec<&Shoe>, shoe_size: u32) -> Vec<&Shoe> {
    shoes.into_iter()
        .filter(|s| s.size == shoe_size)                // shoe size is accessible here
        .collect()
}

fn main() {
    let s1 = Shoe { size: 10, style: String::from("sneaker") };
    let s2 = Shoe { size: 13, style: String::from("sandal") };
    let s3 = Shoe { size: 10, style: String::from("boot") };
    let shoes = vec![
        &s1, &s2, &s3
    ];

    let in_my_size = shoes_in_my_size(shoes, 10);

    assert_eq!(
        in_my_size,
        vec![
            &s1, &s3
        ]
    );
}
