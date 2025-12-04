import { Effect, Stream } from "effect";

const file = await Bun.file("inputs/d4.txt");

const dirs = [
  [1, 0],
  [-1, 0],
  [0, 1],
  [0, -1],
  [1, 1],
  [-1, -1],
  [-1, 1],
  [1, -1],
] as const;

const grid = (await file.text()).split("\n").map((x) => x.split(""));

type Grid = typeof grid;

const removeToiletPaper = (grid: Grid): [number, Grid] => {
  let count = 0;
  const newGrid = structuredClone(grid);

  grid.forEach((row, ridx) =>
    row.forEach((col, colIdx) => {
      const ct = dirs
        .map((dir) => {
          //JS Negatives
          const rN = ridx + dir[0];
          const cN = colIdx + dir[1];
          if (rN < 0 || cN < 0) {
            return undefined;
          }
          const v = grid.at(rN)?.at(cN);
          return v;
        })
        .reduce((acc, v) => (v === "@" ? acc + 1 : acc), 0);

      if (ct < 4 && col === "@") {
        count++;
        newGrid[ridx]![colIdx] = ".";
      }
    })
  );

  return [count, newGrid];
};

const [part1, _] = removeToiletPaper(grid);
console.log(part1);

const part2Effect = Stream.iterate([0, grid] as [number, Grid], ([_, g]) =>
  removeToiletPaper(g)
).pipe(
  Stream.drop(1),
  Stream.takeWhile((c) => c[0] > 0),
  Stream.map((v) => v[0]),
  Stream.runSum
);

const part2 = Effect.runSync(part2Effect);
console.log(part2);
