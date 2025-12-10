import { Box, Point, Polygon, Relations } from "@flatten-js/core";
import {
  Chunk,
  Effect,
  Option,
  pipe,
  Stream
} from "effect";
import { unlines } from "./utils";
import { compose } from "effect/Function";
// import { Point } from "@flatten-js/core";

const file = Bun.file("inputs/d9.txt");

type PointT = [number, number];
type Rect = [PointT, PointT];

// const mkPoint = (v: [number, number]) => Data.array(v) as Point;

const pointsList = unlines(await file.text()).map(
  (v) => v.split(",").map((v) => parseInt(v)) as PointT
);

const area = (rect: Rect) => {
  const dr = Math.abs(rect[0][0] - rect[1][0]) + 1;
  const dc = Math.abs(rect[0][1] - rect[1][1]) + 1;

  return dr * dc;
};

const isRectInPoly = (poly: PointT[]) => {
  const polyF = new Polygon(poly.map((v) => new Point(v[0], v[1])));

  return ([testa, testb]: Rect) => {
    try {
      const box = new Box(
        Math.min(testa[0], testb[0]),
        Math.min(testa[1], testb[1]),
        Math.max(testa[0], testb[0]),
        Math.max(testa[1], testb[1])
      );
      return Relations.covered(box, polyF);
    } catch (e) {
      return true;
    }
  };
};

const rects = pointsList.flatMap((a, aIdx) =>
  pointsList.slice(aIdx + 1).map((b) => [a, b] as Rect)
);

// const isPointInPointsPoly = isPointInPoly(pointsList);
const rectsInPoly = rects.toSorted((a, b) => area(b) - area(a));
const not = (v: boolean) => !v

console.log(area(rectsInPoly[0]!))

console.log(
  Stream.fromIterable(rectsInPoly).pipe(
    Stream.dropWhile(compose(isRectInPoly(pointsList), not)),
    Stream.take(1),
    Stream.runCollect,
    Effect.andThen((rect) =>
      pipe(rect, Chunk.get(0), Option.map(area), Option.getOrNull)
    ),
    Effect.runSync
  )
);
