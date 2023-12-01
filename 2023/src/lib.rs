use std::sync::{Arc, Mutex};
mod macros;

pub mod d1;

pub trait AoCSetup {
    fn new() -> Box<Self>;
    fn input(&self) -> &'static str;
}

pub trait AoCDay {
    fn part1(&mut self);
    fn part2(&mut self);
}
