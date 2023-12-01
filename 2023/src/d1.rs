

use aoc_macros::AoCSetup;

use tracing::{info, Level};

use crate::AoCDay;

#[derive(AoCSetup, Default, Debug)]
pub struct D1 {}

#[tracing::instrument(level = Level::DEBUG, ret)]
fn extract_nums(s: &str) -> (u32, u32) {
    let v: Vec<u32> = s.chars().filter_map(|c| c.to_digit(10)).collect();

    (
        v.first().copied().expect("there must be a first digit"),
        v.last().copied().expect("there must be a last digit"),
    )
}

#[tracing::instrument(level = Level::DEBUG, ret)]
fn extract_words(s: &str) -> (u32, u32) {
    const NUM_MAP: [(&str, &str); 9] = {
        [
            ("one", "one1one"),
            ("two", "two2two"),
            ("three", "three3three"),
            ("four", "four4four"),
            ("five", "five5five"),
            ("six", "six6six"),
            ("seven", "seven7seven"),
            ("eight", "eight8eight"),
            ("nine", "nine9nine"),
        ]
    };
    let replaced = NUM_MAP
        .iter()
        .fold(s.to_owned(), |acc, (k, v)| acc.replace(k, v));
    extract_nums(&replaced)
}

impl AoCDay for D1 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let s: &str = self.input();

        let a = s
            .split("\n")
            .map(|s| extract_nums(s))
            .map(|(d1, d2)| d1 * 10 + d2)
            .sum::<u32>();

        info!(a)
    }

    #[tracing::instrument]
    fn part2(&mut self) {
        let s: &str = self.input();

        let a = s
            .split("\n")
            .map(|s| extract_words(s))
            .map(|(d1, d2)| d1 * 10 + d2)
            .sum::<u32>();

        info!(a)
    }
}
