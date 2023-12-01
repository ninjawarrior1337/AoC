use criterion::{black_box, criterion_group, criterion_main, Criterion};

use aoc2023::{self, AoCDay, AoCSetup};

fn criterion_benchmark(c: &mut Criterion) {
    let mut d1 = aoc2023::d1::D1::new();
    c.bench_function("d1", |b| {
        b.iter(|| {
            d1.part1();
            d1.part2();
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
