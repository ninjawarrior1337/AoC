import { memoize, unlines } from "./utils";

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

const countPaths = (graph: Graph) => {
  const fn = memoize(
    ({ start, _end: end }: { start: string; _end: string }): number => {
      if (start === end) {
        return 1;
      }

      const edges = graph[start];
      return edges
        ?.map((n) => fn({ start: n, _end: end }))
        .reduce((acc, v) => acc + v) ?? 0;
    }
  );

  return fn;
};

// const countPathsContaining = (graph: Graph) => {
//   const fn = memoize(
//     ({
//       start,
//       _end,
//       seen_dac,
//       seen_fft,
//     }: {
//       start: string;
//       _end: string
//       seen_dac: boolean;
//       seen_fft: boolean;
//     }): number => {
//       if (start === "out") {
//         if (seen_dac && seen_fft) {
//           return 1;
//         }
//         return 0;
//       }

//       const edges = graph[start]!;

//       const ret = edges
//         .map((n) => {
//           return fn({
//             start: n,
//             _end,
//             seen_dac: seen_dac || start === "dac",
//             seen_fft: seen_fft || start === "fft",
//           });
//         })
//         .reduce((acc, v) => acc + v);
//       return ret;
//     }
//   );

//   return fn;
// };

const countPathsG = countPaths(g);
console.log(countPathsG({ start: "you", _end: "out" }));

console.log(
  countPathsG({ start: "svr", _end: "dac" }) *
    countPathsG({ start: "dac", _end: "fft" }) *
    countPathsG({ start: "fft", _end: "out" }) +
    countPathsG({ start: "svr", _end: "fft" }) *
      countPathsG({ start: "fft", _end: "dac" }) *
      countPathsG({ start: "dac", _end: "out" })
);

// const countPathsCt = countPathsContaining(g);
// console.log(
//   countPathsCt({ start: "svr", _end: "out", seen_dac: false, seen_fft: false })
// );
