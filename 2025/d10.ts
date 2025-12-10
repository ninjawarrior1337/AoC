import { Array } from "effect";
import { unlines } from "./utils";
import { solve, type Coefficients, type Constraint } from "yalps";

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

console.log(data.map(solveIndicatorLights).reduce((acc, v) => acc+v))

const solveJoltageRequirements = (init: Initialization) => {
  const constraints = new Map<string, Constraint>();

  for (const [idx, jTgt] of init.joltage.entries()) {
    constraints.set(`j${idx}`, { equal: jTgt });
    constraints.set(`ct`, { min: 1 });
  }

  const variables = new Map<string, Coefficients>();
  for (const [idx, btn] of init.buttons.entries()) {
    const v = new Map<string, number>();
    for (const b of btn) {
      v.set("j" + b.toString(), 1);
    }
    v.set("ct", 1);
    variables.set(`p${idx}`, v);
  }
  const model = {
    direction: "minimize" as const,
    objective: "ct",
    constraints,
    variables: variables,
    integers: true,
  };
  const solution = solve(model);

  return solution;
};

console.log(
  data
    .map((r) => {
      return solveJoltageRequirements(r).result;
    })
    .reduce((acc, v) => acc + v)
);
