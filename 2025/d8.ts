import { Array, Effect, Option, pipe, Stream } from "effect";
import { unlines } from "./utils";

const file = Bun.file("inputs/d8.txt");

type JunctionBox = [number, number, number];

const junctions = unlines(await file.text()).map(
  (l) => l.split(",").map((v) => parseInt(v)) as JunctionBox
);

const distanceFrom = (src: JunctionBox) => (dest: JunctionBox) =>
  Math.sqrt(
    src.map((e, eIdx) => (e - dest[eIdx]!) ** 2).reduce((acc, v) => acc + v)
  );

const distances = junctions
  .map((src) => ({ src, fn: distanceFrom(src) }))
  .flatMap(({ src, fn }, jDIdx) =>
    junctions.slice(jDIdx + 1).map((dest) => ({ src, dest, dist: fn(dest) }))
  );

const sortedDistances = distances.toSorted(({ dist: a }, { dist: b }) => a - b);

type Circuit = JunctionBox[];

const findCircuitContaining = (circuits: Circuit[], box: JunctionBox) =>
  circuits.reduce(
    (acc, circuit, circuitIdx) =>
      circuit.map((b) => JSON.stringify(b)).includes(JSON.stringify(box))
        ? circuitIdx
        : acc,
    -1
  );

const foldSrcDestPairs = (
  circuits: Circuit[],
  { src, dest }: { src: JunctionBox; dest: JunctionBox; dist: number }
) => {
  const srcCircuit = findCircuitContaining(circuits, src);
  const destCircuit = findCircuitContaining(circuits, dest);
  const srcIn = srcCircuit !== -1;
  const destIn = destCircuit !== -1;

  if (srcIn && destIn) {
    if (srcCircuit === destCircuit) {
      return circuits;
    } else {
      return pipe(
        circuits,
        Array.modify(srcCircuit, (a) => Array.appendAll(a, circuits[destCircuit]!)),
        Array.remove(destCircuit)
      );
    }
  } else if (srcIn && !destIn) {
    return pipe(
      circuits,
      Array.modify(srcCircuit, (a) =>
        Array.append(a, dest)
      )
    );
  } else if (!srcIn && destIn) {
    return pipe(
      circuits,
      Array.modify(destCircuit, (a) =>
        Array.append(a, src)
      )
    );
  } else if (!srcIn && !destIn) {
    return pipe(circuits, Array.append([src, dest]));
  }

  throw new Error("unexpected state");
};

const part1Effect = Stream.fromIterable(sortedDistances).pipe(
  Stream.take(1000),
  Stream.runFold([] as Circuit[], foldSrcDestPairs),
  Effect.andThen((v) =>
    v
      .map((v) => v.length)
      .toSorted((a, b) => b - a)
      .slice(0, 3)
      .reduce((acc, v) => acc * v, 1)
  )
);

console.log(Effect.runSync(part1Effect));

const part2Effect = Stream.fromIterable(sortedDistances).pipe(
  Stream.runFoldWhile(
    {
      last: Option.none<{
        src: JunctionBox;
        dest: JunctionBox;
        dist: number;
      }>(),
      circuits: [] as Circuit[],
    },
    ({ circuits }) => {
      return circuits.at(0)?.length !== junctions.length;
    },
    ({ circuits }, v) => {
      const nextCircuits = foldSrcDestPairs(circuits, v);
      return { last: Option.some(v), circuits: nextCircuits };
    }
  )
);

console.log(
  Effect.runSync(part2Effect).last.pipe(
    Option.map(({ src, dest }) => src[0] * dest[0]),
    Option.getOrThrow
  )
);
