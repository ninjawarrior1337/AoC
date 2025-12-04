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

let count = 0;

let rmQueue: [number, number][] = [];

do {
    rmQueue = []

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
        //   console.log(rN, cN, v);
          return v;
        })
        .reduce((acc, v) => (v === "@" ? acc + 1 : acc), 0);

      if (ct < 4 && col === "@") {
        count++;
        rmQueue.push([ridx, colIdx])
      }
    })
  );

  for(const v of rmQueue) {
    grid[v[0]]![v[1]] = "."
  }
} while (rmQueue.length > 0);

console.log(count);
