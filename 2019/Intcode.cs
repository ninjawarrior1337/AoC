namespace AOC {
    class IntComputer {
        private int ptr = 0;
        public List<Int32> ins = new List<Int32>();

        public void Load(string program) {
            this.ins = program.Split(",").Select(l => Int32.Parse(l)).ToList();
            ptr = 0;
        }

        public void Run(int noun, int verb) {
            this.ins[1] = noun;
            this.ins[2] = verb;

            while (true)
            {
                switch(ins[ptr]) {
                    case 1:
                        ins[ins[ptr+3]] = ins[ins[ptr+1]] + ins[ins[ptr+2]];
                        break;
                    case 2:
                        ins[ins[ptr+3]] = ins[ins[ptr+1]] * ins[ins[ptr+2]];
                        break;
                    case 99:
                        return;
                    default:
                        throw new Exception($"Unknown opcode: {ins[ptr]}");
                }
                ptr += 4;
            }
        }
    }
}