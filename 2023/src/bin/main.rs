use anyhow::Result;
use aoc2023::{self, aoc_bind, d1, AoCDay, AoCSetup};

fn main() -> Result<()> {
    tracing_subscriber::fmt::init();

    let mut days: Vec<_> = Vec::new();
    aoc_bind!(days, d1::D1);

    for (i, d) in (&mut days).iter_mut().enumerate() {
        println!("Day {}", i + 1);
        println!("P1");
        d.part1();
        println!("P2");
        d.part2();
    }

    return Ok(());
}
