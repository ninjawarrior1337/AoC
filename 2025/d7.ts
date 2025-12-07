import { Array } from "effect";

type Cell = "S" | "|" | "^" | ".";

type Grid = Cell[][];

const file = await Bun.file("./inputs/d7.txt");

const parseGrid = (input: string): Grid => {
  return input.split("\n").map((v) => v.split("")) as Grid;
};

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

const timelines = (memo: Map<string, number>, input: Grid) => {
  const fn = (r: number, c: number) => {
    if (r == input.length) {
      return 1;
    }

    const cacheV = memo.get(`${r} ${c}`);
    if (cacheV) {
      return cacheV;
    }

    let res = 0;

    if (input.at(r)?.at(c) === "^") {
      res += fn(r + 1, c + 1) + fn(r + 1, c - 1);
    } else {
      res += fn(r + 1, c);
    }

    memo.set(`${r} ${c}`, res);

    return res;
  };

  return fn;
};

const mkTimelines = timelines(new Map(), grid);
const loc = grid.at(0)!.findIndex((x) => x == "S");

console.log(mkTimelines(0, loc));
