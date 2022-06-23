namespace AOC {
    class Day4 : AoCDay {
        public Day4(string lines) : base(lines) {}

        private bool isValid(int num) {
            var digitArr = num.ToString().Split("").Select(d => Int32.Parse(d)).ToArray();
            var windows = digitArr.Windows(2);
            return false;
        }

        override public string Part1() {
            var r = lines[0].Split("-").Select(n => Int32.Parse(n)).ToArray();
            var range = Enumerable.Range(r[0], r[1]-r[0]);
            var pwCount = 0;
            foreach(var n in range) {
                if(isValid(n)) {
                    pwCount++;
                }
            }
            return pwCount.ToString();
        }
    }
}