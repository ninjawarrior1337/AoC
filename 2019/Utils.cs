namespace AOC {
    public static class IEnumerableExtensions {
        public static IEnumerable<T[]> Windows<T>(this T[] e, int size) {
            for(var i = 0; i < e.Length-size; i++) {
                yield return e.Skip(i).Take(size).ToArray();
            }
            yield break;
        }
    }
}