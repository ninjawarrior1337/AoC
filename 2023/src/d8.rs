use std::{collections::HashMap, iter::repeat};


use aoc_macros::AoCSetup;

use num::integer::lcm;
use rayon::{iter::ParallelIterator};
use tracing::{debug, info};

use crate::AoCDay;

#[derive(Debug)]
enum Direction {
    Left,
    Right
}

impl TryFrom<char> for Direction {
    type Error = ();

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            'L' => Ok(Direction::Left),
            'R' => Ok(Direction::Right),
            _ => Err(())
        }
    }
}

#[derive(Debug, Hash, PartialEq, Eq, Clone)]
struct Loc(String);

impl Loc {
    fn from_str(s: &str) -> Loc {
        Loc(s.to_owned())
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D8 {
    nav: Vec<Direction>,
    graph: HashMap<Loc, (Loc, Loc)>
}

impl AoCDay for D8 {
    #[tracing::instrument(skip(self))]
    fn part1(&mut self) {
        let mut current_location = Loc::from_str("AAA");
        let target = Loc::from_str("ZZZ");

        let (nav_str, graph_lines) = self.input().split_once("\n\n").unwrap();
        self.nav = nav_str.chars().filter_map(|x| x.try_into().ok()).collect();
        debug!(?self.nav);

        for graph_line in graph_lines.lines() {
            let (src, dests) = graph_line.split_once(" = ").unwrap();
            let src = Loc::from_str(src);

            let (left, right) = dests.strip_prefix("(").unwrap().strip_suffix(")").unwrap().split_once(", ").unwrap();
            let left = Loc::from_str(left);
            let right = Loc::from_str(right);

            self.graph.insert(src, (left, right));
        }

        debug!(?self.graph);

        for (n, d) in self.nav.iter().cycle().enumerate() {
            match d {
                Direction::Left => current_location = self.graph.get(&current_location).unwrap().0.clone(),
                Direction::Right => current_location = self.graph.get(&current_location).unwrap().1.clone(),
            };

            if current_location == target {
                info!("{}", n+1);
                break;
            }
        }
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        let mut current_locations: Vec<Loc> = self.graph.keys().filter(|loc| loc.0.ends_with("A")).cloned().collect();

        let mut hit_nums: Vec<usize> = repeat(0).take(current_locations.len()).collect();

        for (n, d) in self.nav.iter().cycle().enumerate() {
            for (idx, current_location) in current_locations.iter_mut().enumerate() {
                if current_location.0.ends_with("Z") && hit_nums[idx] == 0 {
                    hit_nums[idx] = n;
                }

                match d {
                    Direction::Left => *current_location = self.graph.get(&current_location).unwrap().0.clone(),
                    Direction::Right => *current_location = self.graph.get(&current_location).unwrap().1.clone(),
                };
            }
            
            let all_end = hit_nums.iter().all(|hit| hit > &0);
            if all_end {
                break;
            }
        }

        debug!(?hit_nums);

        let p2 = hit_nums.iter().fold(1, |acc, hit| lcm(acc, *hit));
        info!(p2);
    }
}
