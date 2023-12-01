use std::collections::HashMap;

use crate::AoCDay;
use aoc_macros::AoCSetup;
use nom::{InputIter, FindSubstring};

#[derive(AoCSetup, Default)]
pub struct D1 {}

fn extract_nums(s: String) -> (u32, u32) {
    let v: Vec<char> = s.chars()
        .filter(|c| c.is_numeric())
        .collect();

    return (str::parse(&v.first().unwrap().to_string()).unwrap(), str::parse(&v.last().unwrap().to_string()).unwrap())
}

fn extract_words(s: &str) -> (u32, u32) {
    let num_map: HashMap<&str, &str> = [
        ("one", "one1one"),
        ("two", "two2two"),
        ("three", "three3three"),
        ("four", "four4four"),
        ("five", "five5five"),
        ("six", "six6six"),
        ("seven", "seven7seven"),
        ("eight", "eight8eight"),
        ("nine", "nine9nine"),
    ].iter().cloned().collect();
    // let mut replace_order = num_map.keys()
    //     .map(|&k| (s.find_substring(k), k))
    //     .filter(|f| f.0.is_some())
    //     .map(|f| (f.0.unwrap(), f.1))
    //     .collect::<Vec<_>>();

    // replace_order.sort_by_key(|e| e.0);

    let mut new_s = s.to_owned();
    for (&k, &v) in num_map.iter() {

        new_s = new_s.replace(k, v)
    }
    extract_nums(new_s)
}

impl AoCDay for D1 {
    fn part1(&mut self) {
        let s: &str = self.input();
        
        let a = s.split("\n")
        .map(|s| extract_nums(s.to_owned()))
        .map(|(d1, d2)| d1*10 + d2)
        .sum::<u32>();

        println!("{}", a)
    }

    fn part2(&mut self) {
        let s: &str = self.input();
        
        let a = s.split("\n")
        .map(|s| extract_words(s))
        .map(|(d1, d2)| d1*10 + d2)
        .sum::<u32>();

        println!("{}", a)
    }
}
