use std::sync::{Mutex, Arc};
mod macros;

mod d1;

trait AoCSetup {
    fn new() -> Box<Self>;
    fn input(&self) -> &'static str;
}

trait AoCDay {
    fn part1(&mut self);
    fn part2(&mut self);
}

fn main() {
    let mut days: Vec<_> = Vec::new();
    aoc_bind!(days, d1::D1);
    for (i, d) in (&mut days).iter_mut().enumerate() {
        println!("Day {}", i+1);
        println!("P1");
        d.part1();
        println!("P2");
        d.part2();
    }
}
