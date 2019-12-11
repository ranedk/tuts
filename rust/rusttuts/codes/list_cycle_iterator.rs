struct Cycle<'a, T> {
    arr: &'a [T],
    _count: usize
}

impl<'a, T> Cycle<'a, T> {
    fn new(arr: &'a [T]) -> Cycle<'a, T> {
        Cycle {
            arr,
            _count: 0
        }
    }
}

impl<'a, T> Iterator for Cycle<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<Self::Item> {
        self._count += 1;

        if self._count == self.arr.len() {
            self._count = 0;
        }
        Some(&self.arr[self._count])
    }
}


fn main() {
    let list: Vec<String> = "abcdef".chars().map(|x| x.to_string()).collect();
    println!("{:?}", list);
    let c = Cycle::new(&list);
    for (idx, mut i) in c.enumerate() {
        println!("{} - {}", idx, i);
        if idx == 20 {
            break;
        }
    }
}
