require "parallel"

module AOC
    class Day6 < AocDay

        def step()
            if @fishMap[0] >= 1 then
                @fishMap[9] += @fishMap[0]
                @fishMap[7] += @fishMap[0]
                @fishMap[0] = 0
            end

            for i in (0..9) do
                @fishMap[i] = @fishMap[i+1]
            end
        end

        def part1
            @nums = @lines[0].split(",").map(&:to_i)
            
            # Load fishMap
            @fishMap = Hash.new(0)
            @nums.each{|n| @fishMap[n]+=1}
            pp @fishMap

            for _ in (0...80) do
                step()
            end
            @p1 = @fishMap.values.reduce(&:+)
        end

        def part2
            for _ in (80...256) do
                step()
            end
            @p2 = @fishMap.values.reduce(&:+)
        end
    end
end