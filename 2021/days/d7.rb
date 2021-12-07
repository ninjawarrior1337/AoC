require "parallel"

module AOC
    class Day7 < AocDay

        def calc_move_cost_p1(curr, dest)
            (curr-dest).abs
        end

        def calc_move_cost_p2(curr, dest)
            calc_move_cost_p1(curr, dest) > 0 ? (1..(curr-dest).abs).reduce(:+) : 0
        end

        def part1
            @pos = @lines[0].split(",").map(&:to_i)
            @p1 = Parallel.map((0..@pos.max)){|p| @pos.map{|x| calc_move_cost_p1(x, p)}.reduce(:+) }.min
        end

        def part2
            # Thx Alwinfy#7306 for this crumb of knowledge
            @optimal = @pos.reduce(:+) / @pos.length
            @p2 = @pos.map{ |x| calc_move_cost_p2(x, @optimal)}.reduce(:+)

            # If you want to run the more expensive version of part 2, here it is
            # @p2 = Parallel.map((0..@pos.max)){|p| @pos.map{|x| calc_move_cost_p2(x, p)}.reduce(:+) }.min
        end
    end
end