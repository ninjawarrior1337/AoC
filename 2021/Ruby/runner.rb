require "benchmark"

module AOC
    class AocDay
        attr_reader :p1, :p2

        FORMAT = "%n #{Benchmark::FORMAT}"

        def initialize(lines) 
            @lines = lines
        end

        def run()
            p1time = Benchmark.measure("Part 1") {part1}
            p2time = Benchmark.measure("Part 2") {part2}

            puts "Timings: #{Benchmark::CAPTION}"
            puts p1time.format(FORMAT)
            puts p2time.format(FORMAT)
        end

        def part1()
            @p1 = "TODO: Compute"
        end

        def part2() 
            @p2 = "TODO: Compute"
        end
    end
end

Dir["./days/*.rb"].each{|f| require f}

lines = File.readlines("inputs/d#{ARGV[0]}.txt").map(&:strip)
day = "AOC::Day#{ARGV[0]}".split('::').inject(Object) {|o,c| o.const_get c}.new lines

day.run

puts "Part 1: #{day.p1}"
puts "Part 2: #{day.p2}"