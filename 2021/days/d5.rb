require "parallel"

module AOC
    class Day5 < AocDay

        def parse_point_pairs
            @lines.each do |l|
                @pointPairs << l.split(" -> ").map{|c| c.split(",").map{|p| p.to_i}}
            end
        end

        def part1
            @pointPairs = []
            parse_point_pairs

            @grid = Hash.new()
            for i in (0..1000) do
                @grid[i] = Hash.new(0)
            end
            
            # Apply horizontal and vertical only for part 1
            @pointPairs.select{|pair|
                pair[0][0] == pair[1][0] || pair[0][1] == pair[1][1]
            }.each{|pair|
                xs = [pair[0][0], pair[1][0]]
                ys = [pair[0][1], pair[1][1]]
                for x in (xs.min..xs.max) do
                    for y in (ys.min..ys.max) do
                        @grid[y][x] += 1
                    end
                end
            }
            @p1 = (0..1000).map{|n|
                @grid[n].values.select{|c| c >= 2}.length
            }.reduce(:+)
        end

        def part2            
            # apply diagonal to the grid found in part 1
            @pointPairs.reject{|pair|
                pair[0][0] == pair[1][0] || pair[0][1] == pair[1][1]
            }.each{|pair|
                xRange = pair[0][0] < pair[1][0] ? (pair[0][0]..pair[1][0]) : pair[0][0].downto(pair[1][0])
                yRange = pair[0][1] < pair[1][1] ? (pair[0][1]..pair[1][1]) : pair[0][1].downto(pair[1][1])
                xRange.to_a.each.with_index{|x, i|
                    y = yRange.to_a[i]
                    @grid[y][x] += 1
                }
                # pp xRange.to_a, yRange.to_a
            }

            # for i in (0..9) do
            #     pp grid[i].values
            # end

            @p2 = (0..1000).map{|n|
                @grid[n].values.select{|c| c >= 2}.length
            }.reduce(:+)
        end
    end
end