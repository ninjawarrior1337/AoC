use std::{default, collections::HashMap};

use aoc_macros::AoCSetup;
use itertools::{repeat_n, Itertools};
use memoize::memoize;
use nom::{bytes::complete::tag, Slice};
use rayon::{str::ParallelString, iter::ParallelIterator};
use tracing::{debug, info, Level};

use crate::AoCDay;

#[derive(Default, PartialEq, Eq, Debug, Clone, Copy, Hash)]
enum Status {
    Broken,
    Working,

    #[default]
    Unknown
}

impl TryFrom<char> for Status {
    type Error = ();

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            '#' => Ok(Self::Broken),
            '.' => Ok(Self::Working),
            '?' => Ok(Self::Unknown),
            _ => Err(())
        }
    }
}

#[derive(Debug)]
struct Record {
    states: Vec<Status>,
    pattern: Vec<usize>
}

impl Record {
    #[tracing::instrument(level="debug", ret)]
    fn is_valid(&self) -> bool {
        if self.states.iter().any(|s| s == &Status::Unknown) {
            return false;
        }

        let v: Vec<_> = self.states.split(|e| e == &Status::Working).filter(|e| e.len() > 0).map(|e| e.len()).collect();

        v == self.pattern
    }

    #[tracing::instrument(level = "debug", skip(self), ret)]
    fn possibilities_count(&self) -> usize {
        #[memoize]
        fn rec_poss_count(states: Vec<Status>, pattern: Vec<usize>) -> usize {

            match (states.as_slice(), pattern.as_slice()) {
                (&[], &[]) => 1,
                (&[], &[_]) => 0,

                (&[Status::Working], _) => rec_poss_count(states[1..].to_vec(), pattern),
                (&[Status::Unknown], _) => {
                    let mut working_slice = states.to_owned();
                    let mut broken_slice = states.to_owned();

                    working_slice[0] = Status::Working;
                    broken_slice[0] = Status::Broken;

                    return rec_poss_count(working_slice, pattern.clone()) + rec_poss_count(broken_slice, pattern.clone())
                },
                (&[Status::Broken], &[]) => 0,
                
            }

        //     if states.len() == 0 {
        //         return if pattern.len() == 0 {
        //             1
        //         } else {
        //             0
        //         }
        //     }

        //     if states.starts_with(&[Status::Working]) {
        //         return rec_poss_count(states[1..].to_vec(), pattern)
        //     }

        //     if states.starts_with(&[Status::Unknown]) {
        //         // Two universes, one where ? is # and one where its .
        //         let mut working_slice = states.to_owned();
        //         let mut broken_slice = states.to_owned();

        //         working_slice[0] = Status::Working;
        //         broken_slice[0] = Status::Broken;

        //         return rec_poss_count(working_slice, pattern.clone()) + rec_poss_count(broken_slice, pattern.clone())
        //     }

        //     if states.starts_with(&[Status::Broken]) {
        //         if pattern.len() == 0 {
        //             return 0;
        //         }

        //         if states.len() < pattern[0] {
        //             return 0;
        //         }

        //         if states[0..pattern[0]].iter().any(|c| c == &Status::Working) {
        //             return 0;
        //         }
                
        //         if pattern.len() > 1 {
        //             if states.len() < pattern[0] + 1 || states[pattern[0]] == Status::Broken {
        //                 return 0
        //             }

        //             return rec_poss_count(states[pattern[0]+1..].to_vec(), pattern[1..].to_vec())
        //         } else {
        //             return rec_poss_count(states[pattern[0]..].to_vec(), pattern[1..].to_vec())
        //         }
        //     }

        //     panic!("wtf");
        // }

        rec_poss_count(self.states.clone(), self.pattern.clone())
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D12 {}

impl AoCDay for D12 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let records = self.input().lines().map(|line| {
            let (states, pattern) = line.split_once(' ').unwrap();

            let states = states.chars().filter_map(|c| c.try_into().ok()).collect();
            let pattern = pattern.split(",").filter_map(|n| n.parse().ok()).collect();

            Record {
                states,
                pattern
            }
        });

        
        let p1: usize = records.map(|r| {
            r.possibilities_count()
        }).sum();

        info!(?p1);
    }

    #[tracing::instrument]
    fn part2(&mut self) {
        let records = self.input().lines().map(|line| {
            let (states, pattern) = line.split_once(' ').unwrap();
            let states = repeat_n(states, 5).join("?");

            let states: Vec<Status> = states.chars().filter_map(|c| c.try_into().ok()).collect();
            let mut pattern: Vec<usize> = pattern.split(",").filter_map(|n| n.parse().ok()).collect();

            // println!("{:?}", states);

            pattern = pattern.repeat(5);

            Record {
                states,
                pattern
            }
        });

        
        let p2: usize = records.map(|r| {
            r.possibilities_count()
        }).sum();

        info!(?p2);
    }
}
