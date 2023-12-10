mod macros;

pub mod d1;
pub mod d2;
pub mod d3;
pub mod d4;
pub mod d5;
pub mod d6;
pub mod d7;
pub mod d8;
pub mod d9;
pub mod d10;

pub trait AoCSetup {
    fn new() -> Box<Self>;
    fn input(&self) -> &'static str;
}

pub trait AoCDay {
    fn part1(&mut self);
    fn part2(&mut self);
}
