import { Cache, Data } from "effect";
import { memoize, memoizeData, unlines } from "./utils";

type Graph = {
  [key: string]: string[];
};

const file = Bun.file("inputs/d11.txt");
const lines = unlines(await file.text());

const g: Graph = {};

for (const l of lines) {
  const [node, edgesS] = l.split(": ");
  const edges = edgesS!.split(" ");

  g[node!] = edges;
}

type CacheKey = {
  start: string,
  end: string
}

const mkCacheKey = Data.case<CacheKey>()

const countPaths = (graph: Graph) => {
  const fn = memoizeData(
    ({ start, end }: CacheKey): number => {
      if (start === end) {
        return 1;
      }

      const edges = graph[start];
      return edges
        ?.map((n) => fn(mkCacheKey({ start: n, end })))
        .reduce((acc, v) => acc + v) ?? 0;
    }
  );

  return fn;
};

const countPathsG = countPaths(g);
console.log(countPathsG({ start: "you", end: "out" }));

console.log(
  countPathsG({ start: "svr", end: "dac" }) *
    countPathsG({ start: "dac", end: "fft" }) *
    countPathsG({ start: "fft", end: "out" }) +
    countPathsG({ start: "svr", end: "fft" }) *
      countPathsG({ start: "fft", end: "dac" }) *
      countPathsG({ start: "dac", end: "out" })
);
