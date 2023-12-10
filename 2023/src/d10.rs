use std::{collections::{HashMap, BinaryHeap, VecDeque, HashSet}, default};

use aoc_macros::AoCSetup;
use nom::bytes::complete::tag;
use petgraph::{
    prelude::NodeIndex,
    visit::{IntoEdges, IntoNeighbors, IntoNodeReferences},
};
use rayon::{iter::ParallelIterator, str::ParallelString};
use tracing::{debug, info, Level};

use crate::AoCDay;

type PipeMap = HashMap<(isize, isize), Pipe>;

#[derive(Debug, Default, PartialEq, Eq, Clone, Copy, Hash)]
enum Direction {
    #[default]
    None,

    North,
    South,
    East,
    West,
}

impl Direction {
    fn inverse(&self) -> Self {
        match self {
            Direction::None => Self::None,
            Direction::North => Self::South,
            Direction::South => Self::North,
            Direction::East => Self::West,
            Direction::West => Self::East,
        }
    }
}

#[derive(Default, Debug, Hash, PartialEq, Eq, Clone)]
struct Connections(Vec<Direction>);

impl TryFrom<char> for Connections {
    type Error = ();

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            '|' => Ok(Connections(vec![Direction::North, Direction::South])),
            '-' => Ok(Connections(vec![Direction::East, Direction::West])),
            'L' => Ok(Connections(vec![Direction::North, Direction::East])),
            'J' => Ok(Connections(vec![Direction::North, Direction::West])),
            '7' => Ok(Connections(vec![Direction::South, Direction::West])),
            'F' => Ok(Connections(vec![Direction::South, Direction::East])),
            '.' => Ok(Connections(vec![])),
            'S' => Ok(Connections(vec![
                Direction::North,
                Direction::South,
                Direction::East,
                Direction::West,
            ])),
            _ => Err(()),
        }
    }
}

#[derive(Debug, Default, Hash, PartialEq, Eq, Clone)]
struct Pipe {
    connections: Connections,
    pos: (isize, isize),
    pipe_type: char,
}

impl Pipe {
    // fn start_pipe_type(&self, pipes: &PipeMap) -> char {
    //     assert!(self.pipe_type == 'S');

    //     let conn = self.connected_to(pipes);


    // }
    
    #[tracing::instrument(skip(pipes), level="debug")]
    fn connected_to<'a>(&self, pipes: &'a PipeMap) -> Vec<&'a Pipe> {
        let r = self.pos.0;
        let c = self.pos.1;
        let neighbors = [
            (r + 1, c, Direction::South),
            (r - 1, c, Direction::North),
            (r, c + 1, Direction::East),
            (r, c - 1, Direction::West),
        ].iter().filter(|(_, _, d)| self.connections.0.contains(d)).copied().collect::<Vec<_>>();
        
        neighbors
            .iter()
            .filter_map(|(r, c, d)| {
                let other = pipes.get(&(*r, *c))?;
                debug!(?other);

                if other.connections.0.contains(&d.inverse()) {
                    Some(other)
                } else {
                    None
                }
            })
            .collect()
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D10 {
    pipes: PipeMap,
    seen: HashSet<Pipe>
}

impl AoCDay for D10 {
    #[tracing::instrument(skip(self))]
    fn part1(&mut self) {
        for (r, row_str) in self.input().lines().enumerate() {
            for (c, pipe) in row_str.chars().enumerate() {
                // let nx = self.graph.add_node(());
                // self.pipes.push(Pipe { pipe_type: pipe.try_into().unwrap(), pos: (r, c), nx })
                self.pipes.insert(
                    (r as isize, c as isize),
                    Pipe {
                        connections: pipe.try_into().unwrap(),
                        pos: (r as isize, c as isize),
                        pipe_type: pipe
                    },
                );
            }
        }

        
        let start = self.pipes.values().filter(|f| f.pipe_type == 'S').nth(0).unwrap();
        let mut max_dist = 0;
        let mut queue: VecDeque<(&Pipe, usize)> = VecDeque::new();
        let mut seen: HashSet<&Pipe> = HashSet::new();
        queue.push_back((start, 0));

        while let Some(p) = queue.pop_front() {
            seen.insert(p.0);

            if p.1 > max_dist {
                max_dist = p.1
            }

            let pipe = p.0;
            let neighbors = pipe.connected_to(&self.pipes);

            for n in neighbors {
                if seen.contains(n) {
                    continue;
                }
                queue.push_back((n, p.1+1))
            }
        }

        // Save for part 2.
        self.seen = seen.iter().cloned().cloned().collect();

        info!(max_dist);
        // debug!(?self.pipes);
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        let rows = self.input().lines().count() as isize;
        let cols = self.input().lines().nth(0).unwrap().chars().count() as isize;

        let mut seen_map = HashMap::new();
        self.seen.iter().for_each(|pipe| {
            seen_map.insert(pipe.pos, pipe);
        });

        let mut enclosed = 0;

        // Crossing number rule
        for r in 0..rows {
            let mut inside = false;
            let mut crossing_number = 0;
            let mut previous_pipe: Option<&Pipe> = None;
            for c in 0..cols {  
                if let Some(pipe) = seen_map.get(&(r, c)) {
                    // Horizontal lines don't change the crossing number
                    if pipe.pipe_type == '-' {
                        continue;
                    }

                    // Back-to-back directional changes doesn't change the crossing number
                    if let Some(pp) = previous_pipe {
                        if (pp.pipe_type == 'F' && pipe.pipe_type == 'J') || (pp.pipe_type == 'L' && pipe.pipe_type == '7') {
                            continue;
                        }
                    }

                    // Ground doesn't change the crossing number.
                    if pipe.pipe_type == '.' {
                        continue;
                    }

                    crossing_number += 1;

                    previous_pipe = Some(pipe);

                    if crossing_number % 2 == 1 {
                        inside = true;
                    } else {
                        inside = false;
                    }
                } else {
                    if inside {
                        enclosed += 1;
                    }
                }
            }
        }

        info!(enclosed);
    }
}
