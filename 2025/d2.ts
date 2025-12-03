import { Console, Effect, pipe, Stream } from "effect";

const isInvalidId = (by: RegExp) => (id: number) =>
  Effect.succeed(by.test(id.toString()));

const file = await Bun.file("input2.txt");
const ranges = (await file.text()).split(",");

const numsStream = Stream.fromIterable(ranges).pipe(
  Stream.flatMap((r) => {
    const [start, end] = r.split("-");
    return Stream.range(parseInt(start!), parseInt(end!));
  })
);

const part1 = pipe(
  numsStream,
  Stream.filterEffect(isInvalidId(/^(\d+)\1$/)),
);

const part2 = pipe(
  numsStream,
  Stream.filterEffect(isInvalidId(/^(\d+)\1+$/)),
);

const program = Effect.gen(function* () {
  const sol1 = yield* Stream.runSum(part1);
  const sol2 = yield* Stream.runSum(part2);

  yield* Console.log(sol1);
  yield* Console.log(sol2);
});

Effect.runSync(program);
