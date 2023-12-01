#[macro_export]
macro_rules! aoc_bind {
    ($v: ident, $d: ty) => {
        $v.push(<$d>::new())
    };
}
