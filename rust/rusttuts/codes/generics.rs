struct Point<T, U> {
    x: T,
    y: U
}

impl <T, U> Point<T, U> {
    fn swap<V, W>(&self, other: &Point<V, W>) -> Point<T, W> {
        Point {
            x: self.x,
            y: other.y
        }
    }
}

fn main() {
    let p1 = Point{x: 5, y: 100};
    let p2 = Point{x: 343, y: 120};

    let p3 = p1.swap(&p2);

    println!("p3.x={}, p3.y={}", p3.x, p3.y);
    println!("p1.x={}, p1.y={}", p1.x, p1.y);
    println!("p2.x={}, p2.y={}", p2.x, p2.y);

}
