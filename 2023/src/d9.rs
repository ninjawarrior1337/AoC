use aoc_macros::AoCSetup;

use rayon::{iter::ParallelIterator};
use tracing::{debug, info};
use crate::AoCDay;

#[derive(Debug, Clone)]
struct History(Vec<isize>);

impl History {
    #[tracing::instrument(level = "debug", ret)]
    fn diff(&self) -> Self {
        let v = self.0.windows(2).map(|pair| pair[1] - pair[0]).collect();
        History(v)
    }

    fn extrapolate(&self) -> isize {
        if self.0.iter().all(|x| x == &0) {
            return 0
        }

        let diff = self.diff();
        return self.0.last().unwrap() + diff.extrapolate();
    }

    fn extrapolate_backwards(&self) -> isize {
        if self.0.iter().all(|x| x == &0) {
            return 0
        }

        let diff = self.diff();
        return self.0.first().unwrap()-diff.extrapolate_backwards();
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D9 {
    histories: Vec<History>
}

impl AoCDay for D9 {
    #[tracing::instrument]
    fn part1(&mut self) {
        self.histories = self.input().lines().map(|l| {
            let nums = l.split_whitespace().filter_map(|v| v.parse().ok()).collect();

            History(nums)
        }).collect();

        let p1: isize = self.histories.iter().map(|h| h.extrapolate()).sum();

        debug!("{:?}", self.histories[0].extrapolate());
        info!(p1);
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        let p2: isize = self.histories.iter().map(|h| h.extrapolate_backwards()).sum();
        debug!("{:?}", self.histories[2].extrapolate_backwards());
        info!(p2);
    }
}
