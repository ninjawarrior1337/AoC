import { Array, Data, HashSet } from "effect";

type Cell = "S" | "|" | "^" | ".";

type Grid = Cell[][];

const file = await Bun.file("./inputs/d7.txt");

const parseGrid = (input: string): Grid => {
  return input.split("\n").map((v) => v.split("")) as Grid;
};

const combineRows = (rows: readonly Cell[][]): Cell[] =>
  rows.reduce((acc, v) => {
    if (acc.length == 0) {
      return v;
    }

    return acc.map((cellAcc, cellAccIdx): Cell => {
      if (cellAcc == "|" || v[cellAccIdx] == "|") {
        return "|";
      }

      return cellAcc;
    });
  }, [] as Cell[]);

const nextRow = ([prev, v]: [Cell[], Cell[]]) => {
  let splitCount = 0;
  let manyWorlds = HashSet.empty<readonly Cell[]>();

  v.forEach((cell, cellIdx) => {
    if (prev[cellIdx] == "S") {
      v = v.with(cellIdx, "|");
      return;
    }

    if (prev[cellIdx] == "|") {
      if (cell == "^") {
        splitCount++;
        manyWorlds = HashSet.add(manyWorlds, Data.array(v.with(cellIdx + 1, "|")));
        manyWorlds = HashSet.add(manyWorlds, Data.array(v.with(cellIdx - 1, "|")));
      }

      if (cell == ".") {
        v = v.with(cellIdx, "|");
      }
    }
  });

  return HashSet.size(manyWorlds) > 0
    ? { rows: HashSet.toValues(manyWorlds).map(v => Array.copy(v)), splitCount }
    : { rows: [v], splitCount };
};

const doSimPart1 = (grid: Grid) => {
  return grid.reduce(
    ({ grid: acc, splitCount }, v) => {
      const previous = acc.at(-1)!;

      const { rows, splitCount: sc } = nextRow([previous, v]);

      return { grid: [...acc, combineRows(rows)], splitCount: splitCount + sc };
    },
    { splitCount: 0, grid: [grid[0]] as Grid }
  );
};

const grid = parseGrid(await file.text());
// console.log(doSimPart1(grid).splitCount);

console.log(grid.length)

let initialConditions = [grid[0]!]
for(const row of grid.slice(1)) {
    initialConditions = initialConditions.flatMap(prev => {
        const {rows: worlds} = nextRow([prev, row])

        return worlds
    })
}

console.log(initialConditions.length)