use aoc_macros::AoCSetup;

use rayon::{iter::ParallelIterator};
use tracing::{debug, info};

use crate::AoCDay;

#[derive(Debug, Clone, Copy)]
struct RaceParameters {
    distance: u64,
    time: u64,
}

#[derive(AoCSetup, Default, Debug)]
pub struct D6 {
    races: Vec<RaceParameters>,
}

fn compute_max_distance(held_time: u64, params: &RaceParameters) -> u64 {
    let remaining_time = params.time - held_time;
    held_time * remaining_time
}

impl AoCDay for D6 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let (times, distances) = self.input().split_once("\n").unwrap();
        let times = times.split_once(": ").unwrap().1;
        let distances = distances.split_once(": ").unwrap().1;

        self.races = times
            .split_whitespace()
            .zip(distances.split_whitespace())
            .map(|(time, dist)| RaceParameters {
                time: time.parse().unwrap(),
                distance: dist.parse().unwrap(),
            })
            .collect();

        debug!(?self.races);

        let p1 = self
            .races
            .iter()
            .map(|race| {
                (0..=race.time)
                    .map(|held_time| compute_max_distance(held_time, race))
                    .filter(|dist| dist > &race.distance)
                    .count()
            })
            .fold(1, |acc, v| acc * v);

        info!(p1);
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        let single_race_time: u64 = self
            .races
            .iter()
            .map(|r| r.time.to_string())
            .collect::<String>()
            .parse()
            .unwrap();
        let single_race_dist: u64 = self
            .races
            .iter()
            .map(|r| r.distance.to_string())
            .collect::<String>()
            .parse()
            .unwrap();

        let rp = RaceParameters {
            time: single_race_time,
            distance: single_race_dist,
        };

        let p2 = (0..=rp.time)
            .map(|held_time| compute_max_distance(held_time, &rp))
            .filter(|dist| dist > &rp.distance)
            .count();

        info!(p2);
    }
}
