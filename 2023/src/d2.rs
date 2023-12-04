use aoc_macros::AoCSetup;

use rayon::{str::ParallelString, iter::ParallelIterator};
use tracing::{info, Level};

use crate::AoCDay;

#[derive(Debug, Default)]
struct Pull {
    red: u32,
    green: u32,
    blue: u32,
}
#[derive(Debug)]
struct Game {
    num: u32,
    pulls: Vec<Pull>,
}

impl Game {
    #[tracing::instrument(level = Level::DEBUG, ret)]
    fn max_pulls(&self) -> (u32, u32, u32) {
        (
            self.pulls.iter().max_by_key(|x| x.red).unwrap().red,
            self.pulls.iter().max_by_key(|x| x.green).unwrap().green,
            self.pulls.iter().max_by_key(|x| x.blue).unwrap().blue
        )
    }

    #[tracing::instrument(level = Level::DEBUG, ret)]
    fn parse(s: &str) -> Game {
        // Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

        let (game, res) = s.split_once(": ").expect("must be a valid game line");
        let num = game
            .chars()
            .filter(|c| c.is_numeric())
            .collect::<String>()
            .parse()
            .unwrap();

        let pulls = res
            .split("; ")
            .map(|p| {
                let mut pull_obj = Pull::default();
                p.split(", ").for_each(|e| {
                    let (number, color) = e.split_once(" ").unwrap();
                    // debug!(number, color);
                    match color {
                        "red" => pull_obj.red = number.parse().unwrap(),
                        "blue" => pull_obj.blue = number.parse().unwrap(),
                        "green" => pull_obj.green = number.parse().unwrap(),
                        c => panic!("unknown color {c}"),
                    }
                });
                pull_obj
            })
            .collect();

        Game { num, pulls }
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D2 {}

const LIMITS: (u32, u32, u32) = (12, 13, 14);

impl AoCDay for D2 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let input = self.input();
        let g: u32 = input
            .par_lines()
            .map(|l| Game::parse(l))
            .filter(|g| {
                let c = g.max_pulls();
                c.0 <= LIMITS.0 && c.1 <= LIMITS.1 && c.2 <= LIMITS.2
            })
            .fold(|| 0, |acc, g| acc + g.num)
            .sum();

        info!(?g);
    }

    #[tracing::instrument]
    fn part2(&mut self) {
        let input = self.input();
        let g: u32 = input
            .par_lines()
            .map(|l| Game::parse(l))
            .map(|g| {
                let c = g.max_pulls();
                c.0 * c.1 * c.2
            })
            .sum();

        info!(?g);
    }
}
