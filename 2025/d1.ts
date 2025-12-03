import { Chunk, Console, Data, Effect, pipe, Stream } from "effect";

const file = Bun.file("./input.txt");

const lines = await file.text().then((v) => v.split("\n"));

type Move = {
  _tag: "move";
  direction: "L" | "R";
  rotation: number;
};

const mkMove = Data.tagged<Move>("move");

const parseMove = (move: string): Move => {
  const v = parseInt(move.substring(1));
  return mkMove({
    direction: move[0] as Move["direction"],
    rotation: v,
  });
};

const rem_euclid = (lhs: number, rhs: number) => ((lhs + rhs) % rhs) % rhs;
const moveAsInt = (m: Move) => (m.direction == "L" ? -m.rotation : m.rotation);
const doMove = (move: Move) => (start: number) =>
  rem_euclid(start + moveAsInt(move), 100);
const moves = Stream.fromIterable(lines).pipe(Stream.map(parseMove));

const part1 = pipe(
  moves,
  Stream.scan(50, (pos, move) => doMove(move)(pos)),
  Stream.filter((v) => v == 0)
);

const clickStream = (start: number, move: Move) => {
  return Stream.iterate(
    start,
    doMove(mkMove({ direction: move.direction, rotation: 1 }))
  ).pipe(Stream.take(move.rotation + 1));
};

const part2 = pipe(
  moves,
  Stream.scan({ pos: 50, stream: Stream.make<number[]>() }, (st, move) => {
    return {
      pos: doMove(move)(st.pos),
      stream: clickStream(st.pos, move),
    };
  }),
  Stream.flatMap((v) => v.stream),
  Stream.sliding(2),
  Stream.filter((v) => {
    const a = Chunk.toReadonlyArray(v);
    return a[0] != a[1] && a[1] == 0;
  })
);

const program = Effect.gen(function* () {
  const p1 = yield* Stream.runCount(part1);
  const p2 = yield* Stream.runCount(part2);
  console.log(p1);
  console.log(p2);
});

Effect.runSync(program);
