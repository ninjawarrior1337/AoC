use anyhow::Result;
use aoc2023::*;
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
    aoc_bind!(days, d3::D3);
    aoc_bind!(days, d4::D4);
    aoc_bind!(days, d5::D5);
    aoc_bind!(days, d6::D6);

    if let Some(d) = args.day {
        let day = &mut days[d - 1];

        day.part1();
        day.part2();
    } else {
        for (_, d) in (&mut days).iter_mut().enumerate() {
            d.part1();
            d.part2();
        }
    }

    return Ok(());
}
