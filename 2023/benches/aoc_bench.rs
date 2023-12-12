mod macros;

use criterion::{criterion_group, criterion_main, Criterion};

use aoc2023::{self, AoCDay, AoCSetup};


fn benches(c: &mut Criterion) {
    use casey::upper;

    aoc_bench!(c, d1);
    aoc_bench!(c, d2);
    aoc_bench!(c, d3);
    aoc_bench!(c, d4);
    aoc_bench!(c, d5);
    aoc_bench!(c, d6);
    aoc_bench!(c, d7);
    aoc_bench!(c, d8);
    aoc_bench!(c, d9);
    aoc_bench!(c, d10);
    aoc_bench!(c, d11);
}

criterion_group!(aoc_benches, benches);
criterion_main!(aoc_benches);
