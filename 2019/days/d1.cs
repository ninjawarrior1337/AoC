namespace AOC {
    class Day1 : AoCDay {
        public Day1(string linesRaw): base(linesRaw) {}
        
        override public string Part1() {
            return this.lines.Select(m => {
                var i = Int32.Parse(m);
                return i / 3 -2;
            }).Sum().ToString();
        }

        override public string Part2() {
            return this.lines.Select(m => {
                var i = Int32.Parse(m);
                var masses = new List<Int32>();
                masses.Add(i / 3 - 2);
                do {
                    masses.Add(masses.Last() / 3 - 2);
                } while (masses.Last() > 0);

                return masses.GetRange(0, masses.Count()-1).Sum();
            }).Sum().ToString();
        }
    }
}