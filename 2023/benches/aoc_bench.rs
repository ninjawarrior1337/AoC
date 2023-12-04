use criterion::{criterion_group, criterion_main, Criterion};

use aoc2023::{self, AoCDay, AoCSetup};

fn benches(c: &mut Criterion) {
    let mut d1 = aoc2023::d1::D1::new();
    c.bench_function("d1", |b| {
        b.iter(|| {
            d1.part1();
            d1.part2();
        })
    });

    let mut d2 = aoc2023::d2::D2::new();
    c.bench_function("d2", |b| {
        b.iter(|| {
            d2.part1();
            d2.part2();
        })
    });

    let mut d3 = aoc2023::d3::D3::new();
    c.bench_function("d3", |b| {
        b.iter(|| {
            d3.part1();
            d3.part2();
        })
    });

    let mut d4 = aoc2023::d4::D4::new();
    c.bench_function("d4", |b| {
        b.iter(|| {
            d4.part1();
            d4.part2();
        })
    });
}

criterion_group!(aoc_benches, benches);
criterion_main!(aoc_benches);
