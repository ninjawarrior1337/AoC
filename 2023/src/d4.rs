use std::collections::{HashSet, HashMap, BinaryHeap};

use aoc_macros::AoCSetup;
use nom::bytes::complete::tag;
use rayon::{iter::ParallelIterator, str::ParallelString};
use tracing::{debug, info, Level};

use crate::AoCDay;

#[derive(Default, Debug, Eq, PartialEq, Clone)]
struct Card {
    num: u32,
    winning: HashSet<u32>,
    values: HashSet<u32>,
}

impl Ord for Card {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.num.cmp(&self.num)
    }
}

impl PartialOrd for Card {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Card {
    #[tracing::instrument(level = "debug", ret)]
    fn score(&self) -> u32 {
        let winning_count = self.values.intersection(&self.winning).count() as u32;
        if winning_count > 0 {
            2_u32.pow(winning_count-1)
        } else {
            0
        }
    }

    #[tracing::instrument(level = "debug", ret)]
    fn duplicating_cards(&self) -> Vec<u32> {
        let winning_count = self.values.intersection(&self.winning).count() as u32;

        if winning_count > 0 {
            (self.num+1..=self.num+winning_count).collect()
        } else {
            Vec::new()
        }
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D4 {
    base_cards: Vec<Card>,
    card_counts: HashMap<Card, u32>
}

impl D4 {
    #[tracing::instrument(level = "debug", ret)]
    fn parse_line(&self, line: &str) -> Card {
        let mut c = Card::default();
        let (card, res) = line.split_once(": ").unwrap();

        c.num = card
            .chars()
            .filter(|c| c.is_numeric())
            .collect::<String>()
            .parse()
            .unwrap();

        let (winning_str, values_str) = res.split_once(" | ").unwrap();

        c.winning = winning_str
            .split_whitespace()
            .filter_map(|s| s.parse().ok())
            .collect();
        c.values = values_str
            .split_whitespace()
            .filter_map(|s| s.parse().ok())
            .collect();

        return c;
    }
}

impl AoCDay for D4 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let input = self.input();
        let cards: Vec<Card> = input.lines().map(|l| self.parse_line(l)).collect();
        self.base_cards = cards;

        let s: u32 = self.base_cards.iter().map(|c| c.score()).sum();

        info!(s);
    }

    #[tracing::instrument]
    fn part2(&mut self) {
        // Time to invoke the computer science
        let mut pq: BinaryHeap<Card>  = BinaryHeap::new();
        
        for c in &self.base_cards {
            pq.push(c.clone());
        }
        
        let mut processed = 0;
        while let Some(c) = pq.pop() {
            processed += 1;
            let cards = c.duplicating_cards();
            for card_num in cards {
                let card = self.base_cards.binary_search_by_key(&card_num, |c| c.num).unwrap();
                pq.push(self.base_cards[card].clone())
            }
        }

        info!(processed)
    }
}
