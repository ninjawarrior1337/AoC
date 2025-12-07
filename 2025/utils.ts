export const parseGridAs = <T>(input: string): T => {
    return input.split("\n").map(v => v.split("")) as T
}

export const unlines = (input: string) => input.split("\n")

export const memoize = <K extends { [k: string]: any }, V>(f: (arg: K) => V) => {
  const memo = new Map<string, V>();
  return (arg: K) => {
    const tKey = JSON.stringify(arg);
    const c = memo.get(tKey);
    if (c) {
      return c;
    }
    const res = f(arg);
    memo.set(tKey, res);
    return res;
  };
}