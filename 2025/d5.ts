const file = Bun.file("./inputs/d5.txt");

const [ranges, ingredients] = (await file.text())
  .split("\n\n")
  .map((v) => v.split("\n"));

type Range = [number, number];

const rangeFromString = (range: string) =>
  range.split("-").map((v) => parseInt(v)) as Range;
const insideRange = (r: Range, n: number) => n >= r[0] && n <= r[1];

const composeRange = (a: Range, b: Range): Range[] => {
  if (a[1] < b[0]) {
    return [a, b];
  }

  const trueMin = Math.min(a[0], b[0]);
  const trueMax = Math.max(a[1], b[1]);

  return [[trueMin, trueMax]];
};

const part1 = ingredients!
  .map((v) => parseInt(v))
  .map((i) =>
    ranges!
      .map(rangeFromString)
      .reduce((acc, r) => insideRange(r, i) || acc, false)
  )
  .reduce((acc, v) => (v ? acc + 1 : acc), 0);

console.log(part1);

const sortedRanges = ranges!
  .map(rangeFromString)
  .toSorted((a, b) => a[0] - b[0]);

const nonOverlapping = sortedRanges.reduce(
  (acc, v) => [...acc.slice(0, -1), ...composeRange(acc.at(-1)!, v)],
  [sortedRanges[0]] as Range[]
);

const part2 = nonOverlapping.reduce((acc, v) => acc + (v[1] - v[0] + 1), 0)

console.log(part2);
