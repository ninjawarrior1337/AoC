require "parallel"

module AOC
    class Day1 < AocDay
        def countConsecutiveIncreases(e)
            e.each_with_index.map { |m, i| 
                0 if i == 0
                m > e.map(&:to_i)[i-1] ? 1 : 0
            }.reduce(&:+)
        end

        def part1
            @p1 = countConsecutiveIncreases @lines.map(&:to_i)
        end

        def part2
            @p2 = countConsecutiveIncreases @lines.map(&:to_i).each_cons(3).map{|e|
                e.reduce(&:+)
            }
        end
    end
end