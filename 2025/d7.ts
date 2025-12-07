import { Array } from "effect";
import { memoize, parseGridAs } from "./utils";

type Cell = "S" | "|" | "^" | ".";

type Grid = Cell[][];

const file = await Bun.file("./inputs/d7.txt");

const parseGrid = (input: string): Grid => parseGridAs<Grid>(input);

const nextRow = ([prev, v]: [Cell[], Cell[]]) => {
  let splitCount = 0;

  const nRow = Array.copy(v);
  v.forEach((cell, cellIdx) => {
    if (prev[cellIdx] == "S") {
      nRow[cellIdx] = "|";
      return;
    }

    if (prev[cellIdx] == "|") {
      if (cell == "^") {
        splitCount++;
        nRow[cellIdx + 1] = "|";
        nRow[cellIdx - 1] = "|";
      }

      if (cell == ".") {
        nRow[cellIdx] = "|";
      }
    }
  });

  return { next: nRow, splitCount };
};

const doSimPart1 = (grid: Grid) => {
  return grid.slice(1).reduce(
    (state, row) => {
      const { next, splitCount: sc } = nextRow([state.prev, row]);

      return { prev: next, splitCount: sc + state.splitCount };
    },
    { splitCount: 0, prev: grid.at(0)! }
  );
};

const grid = parseGrid(await file.text());

console.log(doSimPart1(grid).splitCount);

const mkTimelines = (input: Grid) => {
  const fn = memoize(({ r, c }: { r: number; c: number }) => {
    if (r == input.length) {
      return 1;
    }

    let res = 0;

    if (input.at(r)?.at(c) === "^") {
      res += fn({ r: r + 1, c: c + 1 }) + fn({ r: r + 1, c: c - 1 });
    } else {
      res += fn({ r: r + 1, c });
    }

    return res;
  });

  return fn;
};

const timelines = mkTimelines(grid);
const loc = grid.at(0)!.findIndex((x) => x == "S");

console.log(timelines({ r: 0, c: loc }));
