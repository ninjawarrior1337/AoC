use std::{collections::{HashSet, BinaryHeap}, ops::RangeInclusive, cmp::Reverse};

use aoc_macros::AoCSetup;

use rayon::{iter::{ParallelIterator, IntoParallelRefIterator}};
use tracing::{info};

use crate::AoCDay;

#[derive(Default, Debug, Eq, PartialEq, Clone)]
struct Card {
    num: u32,
    winning: HashSet<u32>,
    values: HashSet<u32>,
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
    fn duplicated_cards(&self) -> Option<RangeInclusive<u32>> {
        let winning_count = self.values.intersection(&self.winning).count() as u32;

        if winning_count > 0 {
            Some(self.num+1..=self.num+winning_count)
        } else {
            None
        }
    }
}


#[derive(AoCSetup, Default, Debug)]
pub struct D4 {
    base_cards: Vec<Card>,
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
    #[tracing::instrument(skip(self))]
    fn part1(&mut self) {
        let input = self.input();
        let cards: Vec<Card> = input.lines().map(|l| self.parse_line(l)).collect();
        self.base_cards = cards;

        let s: u32 = self.base_cards.iter().map(|c| c.score()).sum();

        info!(s);
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        // Time to invoke the computer science

        let processed = self.base_cards.par_iter().map(|c| {
            let mut pq  = BinaryHeap::new();
            pq.push(Reverse(c.num));

            let mut processed = 0;

            while let Some(Reverse(c)) = pq.pop() {
                processed += 1;
                let card_idx = self.base_cards.binary_search_by_key(&c, |c| c.num).unwrap();
                let card = &self.base_cards[card_idx];            
                
                if let Some(duped_cards) = card.duplicated_cards() {
                    for duped_card_num in duped_cards {
                        pq.push(Reverse(duped_card_num))
                    }
                }
            }

            return processed;
        }).sum::<u32>();        

        info!(processed)
    }
}
