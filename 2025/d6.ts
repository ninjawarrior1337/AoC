import { Chunk, Effect, pipe, Stream } from "effect";
import { unlines } from "./utils";

type Operation = "+" | "*";

const file = Bun.file("inputs/d6.txt");

const lines = unlines(await file.text());

const rows = lines.map((v) => v.split(/\s+/).filter((v) => v.length > 0));

const operations = rows.at(-1)!.map((v) => v as Operation);

const colCt = rows[0]!.length;

const part1Effect = Stream.range(0, colCt - 1).pipe(
  Stream.zip(Stream.fromIterable(operations)),
  Stream.mapEffect(([colIdx, operation]) =>
    pipe(
      rows.slice(0, -1),
      Stream.fromIterable,
      Stream.map((v) => parseInt(v[colIdx]!)),
      Stream.runFold(
        operation == "*" ? 1 : operation == "+" ? 0 : -1,
        (acc, v) => {
          switch (operation) {
            case "+":
              return acc + v;
            case "*":
              return acc * v;
          }
        }
      )
    )
  ),
  Stream.runSum
);

console.log(Effect.runSync(part1Effect))

const columns = lines.at(0)!.length;

const st = Stream.range(0, columns - 1).pipe(
  Stream.map((c) => lines.map((l) => l.at(c)!)),
  Stream.split((col) => col.reduce((acc, char) => char == " " && acc, true)),
  Stream.map((chunk) => {
    const arr = Chunk.toReadonlyArray(chunk);
    const operation = arr[0]?.at(-1)! as Operation;
    const fst = arr[0]!.slice(0, -1);

    const newArr = [fst, ...arr.slice(1)]
      .map((v) => v.filter((c) => c != " "))
      .map((v) => parseInt(v.join("")))
      .reduce(
        (acc, v) => {
          switch (operation) {
            case "+":
              return acc + v;
            case "*":
              return acc * v;
          }
        },
        operation === "*" ? 1 : operation === "+" ? 0 : -1
      );

    return newArr;
  }),
);

console.log(pipe(st, Stream.runSum, Effect.runSync));
