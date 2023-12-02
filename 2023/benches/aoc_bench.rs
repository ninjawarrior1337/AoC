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
}

criterion_group!(aoc_benches, benches);
criterion_main!(aoc_benches);
