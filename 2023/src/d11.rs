use std::collections::HashMap;

use aoc_macros::AoCSetup;
use itertools::Itertools;

use rayon::iter::ParallelIterator;
use tracing::{debug, info};

use crate::AoCDay;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
enum Element {
    #[default]
    Empty,
    Galaxy,
}

impl TryFrom<char> for Element {
    type Error = ();

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            '#' => Ok(Self::Galaxy),
            '.' => Ok(Self::Empty),
            _ => Err(()),
        }
    }
}

#[derive(Debug)]
struct Universe(Vec<Vec<Element>>);

#[derive(Debug)]
struct SparseUniverse(HashMap<(usize, usize), Element>);

impl Universe {
    fn galaxies(&self) -> impl Iterator<Item = (usize, usize)> {
        let mut hs = Vec::new();
        for r in 0..self.0.len() {
            for c in 0..self.0[0].len() {
                if self.0[r][c] == Element::Galaxy {
                    hs.push((r, c));
                }
            }
        }
        hs.into_iter()
    }

    fn is_empty_row(&self, row: usize) -> bool {
        self.0[row].iter().all(|e| e == &Element::Empty)
    }

    fn is_empty_col(&self, col: usize) -> bool {
        self.0
            .iter()
            .map(|row| row[col])
            .all(|e| e == Element::Empty)
    }

    #[tracing::instrument(level = "debug", ret)]
    fn dist(p1: (usize, usize), p2: (usize, usize)) -> usize {
        p1.0.abs_diff(p2.0) + p1.1.abs_diff(p2.1)
    }

    #[tracing::instrument(skip(self), level = "debug", ret)]
    fn expanded(&self, by: usize) -> SparseUniverse {
        let mut hm = HashMap::new();
        self.galaxies().for_each(|coord| {
            hm.insert(coord, Element::Galaxy);
        });

        let empty_rows: Vec<usize> = (0..self.0.len())
            .filter(|&r| self.is_empty_row(r))
            .collect();
        let empty_cols: Vec<usize> = (0..self.0[0].len())
            .filter(|&c| self.is_empty_col(c))
            .collect();

        debug!(?empty_rows, ?empty_cols);

        // Expand time
        let added = by - 1;

        for (i, row) in empty_rows.iter().enumerate() {
            let keys: Vec<(usize, usize)> = hm.keys().cloned().collect();

            for k in keys.iter() {
                if k.0 > (*row + (i * added)) {
                    hm.remove(k);
                    hm.insert((k.0 + added, k.1), Element::Galaxy);
                }
            }
        }

        for (i, col) in empty_cols.iter().enumerate() {
            let keys: Vec<(usize, usize)> = hm.keys().cloned().collect();

            for k in keys.iter() {
                if k.1 > (*col + (i * added)) {
                    hm.remove(&k);
                    hm.insert((k.0, k.1 + added), Element::Galaxy);
                }
            }
        }

        SparseUniverse(hm)
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D11 {}

impl AoCDay for D11 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let universe_data = self
            .input()
            .lines()
            .map(|line| line.chars().filter_map(|c| c.try_into().ok()).collect())
            .collect();

        let universe = Universe(universe_data);
        let su = universe.expanded(2);
        debug!(?su);

        let lengths_sum: usize =
            su.0.keys()
                .combinations(2)
                .map(|pair| {
                    let p1 = pair[0];
                    let p2 = pair[1];

                    Universe::dist(*p1, *p2)
                })
                .sum();

        info!(?lengths_sum);
    }

    #[tracing::instrument]
    fn part2(&mut self) {
        let universe_data = self
            .input()
            .lines()
            .map(|line| line.chars().filter_map(|c| c.try_into().ok()).collect())
            .collect();

        let universe = Universe(universe_data);
        let su = universe.expanded(1_000_000);
        debug!(?su);

        let lengths_sum: usize =
            su.0.keys()
                .combinations(2)
                .map(|pair| {
                    let p1 = pair[0];
                    let p2 = pair[1];

                    Universe::dist(*p1, *p2)
                })
                .sum();

        info!(?lengths_sum);
    }
}
