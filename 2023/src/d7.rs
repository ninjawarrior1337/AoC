use core::num;
use std::{
    cmp::Ordering,
    collections::{BTreeMap, HashMap},
    str::Chars,
};

use aoc_macros::AoCSetup;
use tracing::{debug, info, Level};

use crate::AoCDay;

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Hand([char; 5]);

const SUITS: [char; 13] = [
    'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2',
];

const SUITS_JOKER: [char; 13] = [
    'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J',
];

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        if self.hand_type().cmp(&other.hand_type()) == Ordering::Equal {
            for (card, other_card) in self.0.iter().zip(other.0.iter()) {
                let self_pos = SUITS.iter().position(|x| x == card).unwrap();
                let other_pos = SUITS.iter().position(|x| x == other_card).unwrap();

                let ordering = self_pos.cmp(&other_pos);
                if ordering != Ordering::Equal {
                    return ordering.reverse();
                }
            }
            panic!("this should never happen");
        } else {
            self.hand_type().cmp(&other.hand_type())
        }
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(&other))
    }
}

#[derive(PartialEq, PartialOrd, Eq, Ord, Debug, Clone, Copy)]
enum HandType {
    HighCard,
    OnePair,
    TwoPair,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
}

trait HandTypeable {
    fn hand_type(&self) -> HandType;
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Joker(pub Hand);

impl HandTypeable for Joker {
    #[tracing::instrument]
    fn hand_type(&self) -> HandType {
        let mut counts: BTreeMap<char, usize> = BTreeMap::new();

        for c in self.0 .0 {
            counts.entry(c).and_modify(|curr| *curr += 1).or_insert(1);
        }

        let num_jokers = counts.get(&'J').cloned();

        debug!(?counts);

        if let Some(joker_count) = num_jokers {
            if joker_count < 5 {
                let mut non_joker = counts
                    .iter()
                    .map(|v| (*v.0, *v.1))
                    .filter(|(k, _)| k != &'J')
                    .collect::<Vec<_>>();
                non_joker.sort_by_key(|(_, count)| *count);

                debug!(?non_joker);

                {
                    let counts = &mut counts;
                    *counts.get_mut(&'J').unwrap() -= joker_count;
                    *counts.get_mut(&non_joker.last().unwrap().0).unwrap() += joker_count;
                }
            }
        }

        let mut values = counts.values().cloned().collect::<Vec<_>>();
        values.sort();
        values.reverse();

        debug!(?values);

        match values.as_slice() {
            &[5, ..] => HandType::FiveOfAKind,
            &[4, 1, ..] => HandType::FourOfAKind,
            &[3, 2, ..] => HandType::FullHouse,
            &[3, 1, 1, ..] => HandType::ThreeOfAKind,
            &[2, 2, 1, ..] => HandType::TwoPair,
            &[2, 1, 1, 1, ..] => HandType::OnePair,
            &[1, 1, 1, 1, 1, ..] => HandType::HighCard,
            &[..] => panic!("there must be at least one item"),
        }
    }
}

impl Ord for Joker {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        if self.hand_type().cmp(&other.hand_type()) == Ordering::Equal {
            for (card, other_card) in self.0 .0.iter().zip(other.0 .0.iter()) {
                let self_pos = SUITS_JOKER.iter().position(|x| x == card).unwrap();
                let other_pos = SUITS_JOKER.iter().position(|x| x == other_card).unwrap();

                let ordering = self_pos.cmp(&other_pos);
                if ordering != Ordering::Equal {
                    return ordering.reverse();
                }
            }
            panic!("this should never happen");
        } else {
            self.hand_type().cmp(&other.hand_type())
        }
    }
}

impl PartialOrd for Joker {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(&other))
    }
}

impl Hand {
    fn from_chars(s: Chars) -> Hand {
        let v: [char; 5] = s.take(5).collect::<Vec<_>>().try_into().unwrap();
        Hand(v)
    }
}

impl HandTypeable for Hand {
    #[tracing::instrument(level = "debug", ret)]
    fn hand_type(&self) -> HandType {
        let mut counts: BTreeMap<char, usize> = BTreeMap::new();

        for c in self.0 {
            counts.entry(c).and_modify(|curr| *curr += 1).or_insert(1);
        }
        let mut values = counts.values().cloned().collect::<Vec<_>>();
        values.sort();
        values.reverse();

        debug!(?values);

        match values.as_slice() {
            &[5, ..] => HandType::FiveOfAKind,
            &[4, 1, ..] => HandType::FourOfAKind,
            &[3, 2, ..] => HandType::FullHouse,
            &[3, 1, 1, ..] => HandType::ThreeOfAKind,
            &[2, 2, 1, ..] => HandType::TwoPair,
            &[2, 1, 1, 1, ..] => HandType::OnePair,
            &[1, 1, 1, 1, 1, ..] => HandType::HighCard,
            &[..] => panic!("there must be at least one item"),
        }
    }
}

#[derive(Debug)]
struct Play {
    hand: Hand,
    bet: u64,
}

#[derive(AoCSetup, Default, Debug)]
pub struct D7 {
    game: Vec<Play>,
}

impl AoCDay for D7 {
    #[tracing::instrument]
    fn part1(&mut self) {
        let input = self.input();

        let game = input
            .lines()
            .map(|play_str| {
                let (hand, bet) = play_str.split_once(" ").unwrap();
                let hand = Hand::from_chars(hand.chars());
                let bet = bet.parse().unwrap();

                Play { hand, bet }
            })
            .collect::<Vec<_>>();

        self.game = game;

        println!("{:?}", self.game[2].hand.hand_type());

        debug!(?self.game);
        self.game.sort_by_key(|p| p.hand);
        debug!(?self.game);

        let p1 = self
            .game
            .iter()
            .enumerate()
            .map(|(i, play)| play.bet as usize * (i + 1))
            .sum::<usize>();

        info!(p1);
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        self.game.sort_by_key(|p| Joker(p.hand));

        debug!(?self.game);

        let p2 = self
            .game
            .iter()
            .enumerate()
            .map(|(i, play)| play.bet as usize * (i + 1))
            .sum::<usize>();

        info!(p2);
    }
}
