// See https://aka.ms/new-console-template for more information
using AOC;

namespace AOC
{
    abstract class AoCDay {
        protected string[] lines {get;}
        public AoCDay(string linesRaw) {
            lines = linesRaw.Split("\n").Select(s => s.Trim()).ToArray();
        }

        virtual public string Part1() {
            return "TODO: Implement";
        }
        virtual public string Part2() {
            return "TODO: Implement";
        }
    }
}
class Application {
    static void Main(string[] args) {
        string obj = $"AOC.Day{args[0]}";
        var objType = Type.GetType(obj);

        string input = System.IO.File.ReadAllText($"./inputs/d{args[0]}.txt");
    
        AoCDay? day = (AoCDay?) Activator.CreateInstance(objType!, new object[]{input});
        Console.WriteLine($"Part 1: {day!.Part1()}");
        Console.WriteLine($"Part 2: {day!.Part2()}");
    }
}