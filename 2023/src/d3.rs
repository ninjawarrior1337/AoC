use std::collections::{HashSet};

use aoc_macros::AoCSetup;
use ndarray::{Array};

use rayon::{iter::ParallelIterator};
use tracing::{info};

use crate::AoCDay;

trait CharExt {
    fn is_symbol(&self) -> bool;
}

impl CharExt for char {
    fn is_symbol(&self) -> bool {
        return self.is_ascii_punctuation() && (self != &'.');
    }
}

#[derive(Debug, Hash, Eq, PartialEq, Clone, Copy)]
struct Part {
    num: u32,
    row: usize,
    start: usize,
    end: usize,
}

#[derive(AoCSetup, Default, Debug)]
pub struct D3 {
    schematic: ndarray::Array2<char>,
    parts: HashSet<Part>,
}

#[tracing::instrument(level = "debug", ret)]
fn parse_line(line: &str) -> Vec<(usize, usize)> {
    // 617*......
    let mut v = Vec::new();

    let mut is_in_a_number = false;
    let mut current_start = 0;
    let mut current_end = 0;

    line.char_indices()
        .for_each(|(pos, char)| match (char.is_numeric(), is_in_a_number) {
            (true, false) => {
                current_start = pos;
                current_end = pos;
                is_in_a_number = true;
            }
            (true, true) => {
                current_end += 1;
            }
            (false, true) => {
                v.push((current_start, current_end));
                is_in_a_number = false;
            }
            (false, false) => {}
        });

    if is_in_a_number {
        v.push((current_start, current_end));
    }

    v
}

impl D3 {
    #[tracing::instrument(level = "debug", skip(self), ret)]
    fn parts_from_coord(&self, column: usize, row: usize) -> HashSet<Part> {
        let x = column as isize;
        let y = row as isize;
        let neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y + 1),
            (x - 1, y - 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
        ];

        self.parts
            .iter()
            .filter(|p| {
                (p.start..=p.end)
                    .map(|col| (col as isize, p.row as isize))
                    .any(|coord| {neighbors.contains(&coord)})
            })
            .cloned()
            .collect()
    }
}

impl AoCDay for D3 {
    #[tracing::instrument(skip(self))]
    fn part1(&mut self) {
        self.parts = HashSet::new();
        let input = self.input();
        let r = input.lines().count();
        let c = input
            .lines()
            .next()
            .expect("there has to be a first line")
            .len();
        let v = input.chars().filter(|c| !c.is_whitespace()).collect();
        self.schematic = Array::from_shape_vec((r, c), v).unwrap();

        // Parse parts once
        input.lines().enumerate().for_each(|(line_num, line)| {
            let parsed_line = parse_line(line);
            for (start, end) in parsed_line {
                let n = line[start..=end].parse::<u32>().unwrap();
                self.parts.insert(Part {
                    num: n,
                    row: line_num,
                    start,
                    end,
                });
            }
        });

        // Solve
        let p1 = self.schematic
            .indexed_iter()
            .filter(|(_, c)| c.is_symbol())
            .map(|(coord, _)| self.parts_from_coord(coord.1, coord.0))
            .flatten()
            .collect::<HashSet<Part>>()
            .iter()
            .fold(0, |acc, p| acc+p.num);

        info!(?p1);
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        let p2 = self.schematic
        .indexed_iter()
        .filter(|(_, &c)| c == '*')
        .map(|(coord, _)| {
            let parts = self.parts_from_coord(coord.1, coord.0);
            if parts.len() == 2 {
                parts.iter().fold(1, |acc, p| acc * p.num)
            } else {
                0
            }
        })
        .fold(0, |acc, p| acc+p);

        info!(?p2);
    }
}
