import { Data } from "effect";

const file = await Bun.file("inputs/d3.txt");
const banks = (await file.text()).split("\n");

const parse = (lines: string[]) => {
  return lines.map((v) => v.split("").map((v) => parseInt(v)));
};

type MaxJoltageInput = {
  _tag: "MaxJoltageInput";
  bank: readonly number[];
  limit: number;
};

const mkMaxJoltageInput = Data.tagged<MaxJoltageInput>("MaxJoltageInput");

const maxJoltage = (input: MaxJoltageInput): number => {
  const curr: number[] = [];

  let lastPos = 0;
  for (let i = input.limit; i > 0; i--) {
    const maxPos = input.bank
      .slice(lastPos, input.bank.length - i + 1)
      .reduce(
        (acc, v, idx) => (v > acc.lgst ? { pos: lastPos + idx, lgst: v } : acc),
        {
          pos: lastPos,
          lgst: 0,
        }
      );
    curr.push(maxPos.lgst);
    lastPos = maxPos.pos + 1;
  }

  return curr.reduce((acc, v) => 10 * acc + v);
};

console.log(
  parse(banks)
    .map((v) => [v, v] as const)
    .map(
      ([v1, v2]) =>
        [
          maxJoltage(mkMaxJoltageInput({ bank: Data.array(v1), limit: 2 })),
          maxJoltage(mkMaxJoltageInput({ bank: Data.array(v2), limit: 12 })),
        ] as const
    )
    .reduce(
      (acc, v) => ({
        p1: acc.p1 + v[0],
        p2: acc.p2 + v[1],
      }),
      { p1: 0, p2: 0 }
    )
);
