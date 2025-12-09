import { Array, Data, HashSet, SortedMap, SortedSet } from "effect";
import { unlines } from "./utils";
import { Box, Errors, Line, Point, Polygon, Relations } from "@flatten-js/core";
// import { Point } from "@flatten-js/core";

const file = Bun.file("inputs/d9.txt");

type PointT = [number, number];

// const mkPoint = (v: [number, number]) => Data.array(v) as Point;

const pointsList = unlines(await file.text()).map(
  (v) => v.split(",").map((v) => parseInt(v)) as PointT
);

const area = (a: PointT) => (b: PointT) => {
  const dr = Math.abs(a[0] - b[0]) + 1;
  const dc = Math.abs(a[1] - b[1]) + 1;

  return dr * dc;
};

const fullRect =
  (a: PointT) =>
  (b: PointT): readonly [PointT, PointT, PointT, PointT] => {
    return [a, b, [a[0], b[1]], [b[0], a[1]]];
  };

const isRectInPoly = (poly: PointT[]) => {
  const polyF = new Polygon(poly.map((v) => new Point(v[0], v[1])));

  return (testa: PointT, testb: PointT) => {
    try {
      const box = new Box(
        Math.min(testa[0], testb[0]),
        Math.min(testa[1], testb[1]),
        Math.max(testa[0], testb[0]),
        Math.max(testa[1], testb[1])
      );
      return Relations.covered(box, polyF);
    } catch (e) {
      if (e === Errors.prototype.ZERO_DIVISION) {
        const line = new Line(new Point(testa[0], testb[0]), new Point(testa[1], testb[1]))

        return Relations.covered(line, polyF)
      }
    }
  };
};

const rects = pointsList.flatMap((a, aIdx) =>
  pointsList.slice(aIdx + 1).map((b) => fullRect(a)(b))
);

// const isPointInPointsPoly = isPointInPoly(pointsList);
const isRectInPointsPoly = isRectInPoly(pointsList);
const rectsInPoly = rects.filter((r) => isRectInPointsPoly(r[0], r[1]));

// console.log(rectsInPoly)
console.log(
  rectsInPoly
    .map(([a, b]) => ({ a, b, area: area(a)(b) }))
    .reduce((acc, v) => {
      console.log(v);
      return Math.max(acc, v.area);
    }, 0)
);
