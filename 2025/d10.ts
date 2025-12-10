import { Array } from "effect";
import { unlines } from "./utils";

import { init } from "z3-solver";

interface Initialization {
  indicator_target: boolean[];
  buttons: number[][];
  joltage: number[];
}

const parseInitialization = (input: string) => {
  const re = /\[([\.#]+)\] ((?:\([\d,]*\) ?)+) {([\d,]+)}/;
  const matches = input.match(re)!;
  return {
    indicator_target: matches[1]!.split("").map((c) => c === "#"),
    buttons: matches[2]!.split(" ").map((v) =>
      v
        .substring(1, v.length - 1)
        .split(",")
        .map((v) => parseInt(v))
    ),
    joltage: matches[3]!.split(",").map((v) => parseInt(v)),
  } as Initialization;
};

const file = Bun.file("inputs/d10.txt");

const data = unlines(await file.text()).map(parseInitialization);

const solveIndicatorLights = (init: Initialization) => {
  const traverse = (
    start: Initialization["indicator_target"],
    button: Initialization["buttons"][number]
  ) => {
    return button.reduce(
      (arr, ind) => Array.modify(arr, ind, (v) => !v),
      start
    );
  };

  const mkStart = () => Array.makeBy(init.indicator_target.length, () => false);

  const queue: { state: boolean[]; depth: number }[] = [
    { state: mkStart(), depth: 0 },
  ];

  for (;;) {
    const state = queue.shift()!;
    if (
      state.state.reduce(
        (acc, v, idx) => v === init.indicator_target[idx] && acc,
        true
      )
    ) {
      return state.depth;
    } else {
      queue.push(
        ...init.buttons.map((b) => ({
          state: traverse(state.state, b),
          depth: state.depth + 1,
        }))
      );
    }
  }
};

// const solveJoltageRequirements = (init: Initialization): number => {
//   type State = { joltage: number[]; depth: number };
//   type Ret = { minDepth: number; turn: number };

//   const cache = new Map<string, Ret>();

//   const traverse = (start: number[], btn: number[]) => {
//     return btn.reduce(
//       (arr, ind) => Array.modify(arr, ind, (v) => v + 1),
//       start
//     );
//   };

//   const fn = (state: State): Ret => {
//     console.log(cache);
//     const cacheV = cache.get(JSON.stringify(state.joltage));

//     if (cacheV) {
//       if (state.depth >= cacheV.turn) {
//         return cacheV;
//       }
//     }

//     // if()

//     // Any joltage went over
//     if (
//       state.joltage.reduce(
//         (acc, j, jIdx) => j > init.joltage[jIdx]! || acc,
//         false
//       )
//     ) {
//       cache.set(JSON.stringify(state.joltage), {
//         minDepth: Infinity,
//         turn: state.depth,
//       });
//       return { minDepth: Infinity, turn: state.depth };
//     }

//     // Joltage matches exactly
//     if (
//       state.joltage.reduce(
//         (acc, v, idx) => v === init.joltage[idx] && acc,
//         true
//       )
//     ) {
//       cache.set(JSON.stringify(state.joltage), {
//         minDepth: state.depth,
//         turn: state.depth,
//       });
//       return { minDepth: state.depth, turn: state.depth };
//     }

//     let res = Infinity;
//     for (const btn of init.buttons) {
//       res = Math.min(
//         res,
//         fn({ joltage: traverse(state.joltage, btn), depth: state.depth + 1 })
//           .minDepth!
//       );
//     }

//     let ret = { minDepth: res, turn: state.depth };
//     cache.set(JSON.stringify(state.joltage), ret);

//     return ret;
//   };

//   return fn({
//     joltage: Array.makeBy(init.indicator_target.length, () => 0),
//     depth: 0,
//   }).minDepth;
// };

const { Context } = await init();
const { Optimize, Int, Sum } = Context("main");
const solveJoltageRequirements = async (init: Initialization) => {
  const opt = new Optimize();

  const presses = init.buttons.map((b) => Int.const(`${b}`));

  for (const [p, btn] of Array.zip(presses, init.buttons)) {
    for (const b of btn) {
      opt.add();
    }
  }

  presses.forEach(p => opt.add(p.ge(0)))
//   opt.minimize(presses.reduce((acc, v) => acc.add(v)));

  await opt.check()
  const m = opt.model();

  return presses
    .map((p) => parseInt(`${m.get(p)}`))
    .reduce((acc, v) => acc + v);
};

for(const d of data) {
    await solveJoltageRequirements(d)
}

// console.log(
//   data.map((r) => {
//     console.log(`Solving ${r.joltage}`);
//     return solveJoltageRequirements(r);
//   })
// );
// .reduce((acc, v) => acc+v));
