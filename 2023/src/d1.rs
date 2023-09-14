use crate::AoCDay;
use aoc_macros::AoCSetup;

#[derive(AoCSetup, Default)]
pub struct D1 {
    packs: Vec<i32>,
}

impl AoCDay for D1 {
    fn part1(&mut self) {
        let s: &str = self.input();
        self.packs = s
            .split("\n\n")
            .map(|e| {
                e.split("\n")
                    .map(|c| c.parse::<i32>().unwrap())
                    .sum::<i32>()
            })
            .collect();

        println!("{}", self.packs.iter().max().unwrap())
    }

    fn part2(&mut self) {
        self.packs.sort();

        println!("{}", self.packs.iter().rev().take(3).sum::<i32>())
    }
}
