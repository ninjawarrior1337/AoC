use anyhow::Result;
use aoc2023::{self, aoc_bind, d1, d2, AoCDay, AoCSetup};
use clap::Parser;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Day number
    #[arg(short, long, value_parser = clap::value_parser!(usize))]
    day: Option<usize>,
}

fn main() -> Result<()> {
    let args = Args::parse();
    tracing_subscriber::fmt::init();

    let mut days: Vec<Box<dyn AoCDay>> = Vec::new();
    aoc_bind!(days, d1::D1);
    aoc_bind!(days, d2::D2);

    if let Some(d) = args.day {
        let day = &mut days[d - 1];

        day.part1();
        day.part2();
    } else {
        for (i, d) in (&mut days).iter_mut().enumerate() {
            println!("Day {}", i + 1);
            println!("P1");
            d.part1();
            println!("P2");
            d.part2();
        }
    }

    return Ok(());
}
