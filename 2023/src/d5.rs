use aoc_macros::AoCSetup;
use nom::bytes::complete::tag;
use rayon::{iter::{ParallelIterator, IntoParallelRefIterator, IntoParallelIterator}, str::ParallelString};
use tracing::{debug, info, Level};
use tracing_subscriber::field::debug;

use crate::AoCDay;

#[derive(Debug)]
struct MapDef {
    dst: u64,
    src: u64,
    range: u64,
}

#[derive(Debug)]
struct Map(Vec<MapDef>);

impl TryFrom<Vec<u64>> for MapDef {
    type Error = String;

    fn try_from(value: Vec<u64>) -> Result<Self, Self::Error> {
        if value.len() != 3 {
            Err("Input too long".to_owned())
        } else {
            Ok(MapDef {
                dst: value[0],
                src: value[1],
                range: value[2],
            })
        }
    }
}

#[derive(Debug, Clone, Copy)]
struct Mappable(u64);

impl Mappable {
    #[tracing::instrument(level = "debug", ret)]
    fn remap(self, map: &Map) -> Mappable {
        for m in map.0.iter() {
            if (m.src..(m.src + m.range)).contains(&self.0) {
                return Mappable(m.dst + (self.0 - m.src));
            }
        }
        self
    }
}

#[derive(AoCSetup, Default, Debug)]
pub struct D5 {
    seeds: Vec<Mappable>,
    maps: Vec<Map>,
}

impl AoCDay for D5 {
    #[tracing::instrument(skip(self))]
    fn part1(&mut self) {
        let (seeds, maps) = self.input().split_once("\n\n").unwrap();

        self.seeds = seeds
            .split_once(": ")
            .unwrap()
            .1
            .split_whitespace()
            .filter_map(|n| n.parse().map(|n| Mappable(n)).ok())
            .collect();
        debug!(?self.seeds);

        self.maps = maps
            .split("\n\n")
            .map(|map_set| {
                let raw_map = map_set
                    .lines()
                    .filter(|l| l.starts_with(|c: char| c.is_numeric()))
                    .filter_map(|l| {
                        let a = l
                            .split_whitespace()
                            .filter_map(|c| c.parse().ok())
                            .collect::<Vec<_>>();
                        
                        a.try_into().ok()
                    })
                    .collect::<Vec<MapDef>>();

                Map(raw_map)
            })
            .collect::<Vec<Map>>();

        debug!(?maps);

        let mapped = self
            .seeds
            .iter()
            .cloned()
            .map(|mut s| {
                self.maps.iter().for_each(|map| {
                    s = s.remap(map);
                });
                s
            })
            .collect::<Vec<_>>();

        let p1 = mapped.iter().min_by_key(|m| m.0);

        debug!(?mapped);
        info!(?p1)
    }

    #[tracing::instrument(skip(self))]
    fn part2(&mut self) {
        let ranges: Vec<_> = self
            .seeds
            .chunks(2)
            .into_iter()
            .map(|v| v[0].0..(v[0].0 + v[1].0))
            .collect();

        let p2 = ranges
            .par_iter()
            .map(|range| {
                range.clone().into_par_iter().map(|e| {
                    let mut s = Mappable(e);
                    self.maps.iter().for_each(|map| {
                        s = s.remap(map);
                    });
                    s
                })
            })
            .flatten()
            .min_by_key(|e| e.0);

        info!(?p2);
    }
}
