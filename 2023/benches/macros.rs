#[macro_export]
macro_rules! aoc_bench {
    ($c: ident, $v: ident) => {
        use aoc2023::$v::*;
        
        let mut $v = <upper!($v)>::new();
        $c.bench_function(stringify!($v), |b| {
            b.iter(|| {
                $v.part1();
                $v.part2();
            })
        });
    };
}
