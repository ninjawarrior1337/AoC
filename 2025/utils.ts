import { MutableHashMap } from "effect";

export const parseGridAs = <T>(input: string): T => {
    return input.split("\n").map(v => v.split("")) as T
}

export const unlines = (input: string) => input.split("\n")

export const memoize = <K extends { [k: string]: any }, V>(f: (arg: K) => V) => {
  const memo = new Map<string, V>();
  return (arg: K) => {
    // console.log(memo)
    const fKey = Object.keys(arg).filter(v => !v.startsWith("_")).reduce((obj, key) => Object.assign(obj, {[key]: arg[key]}), {})
    const tKey = JSON.stringify(fKey, Object.keys(fKey).sort());
    const c = memo.get(tKey);
    if (c) {
      return c;
    }
    const res = f(arg);
    memo.set(tKey, res);
    return res;
  };
}

export const memoizeData = <K, V>(f: (arg: K) => V) => {
  let memo = MutableHashMap.make()

  return (arg: K): V => {
    const c = MutableHashMap.get(memo, arg)
    if(c._op === "Some") {
      return c.value as V
    } else {
      const res = f(arg)
      memo = MutableHashMap.set(memo, arg, res)
      return res
    }
  }
}