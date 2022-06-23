namespace AOC {
    class Day2 : AoCDay {
        public Day2(string linesRaw): base(linesRaw) {}
        
        private IntComputer comp = new IntComputer();
        override public string Part1() {
            comp.Load(lines[0]);
            comp.Run(12, 2);
            return comp.ins[0].ToString();
        }

        override public string Part2() {
            foreach(int n in Enumerable.Range(0, 100)) {
                foreach(int v in Enumerable.Range(0, 100)) {
                    comp.Load(lines[0]);
                    comp.Run(n, v);
                    if(comp.ins[0] == 19690720) {
                        return (100 * n + v).ToString();
                    }
                }
            }
            return "Couldn't find";
        }
    }
}