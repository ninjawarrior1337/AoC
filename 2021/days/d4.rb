require "parallel"
require "matrix"

module AOC
    class Day4 < AocDay
        def parseBoard(matGrid)
            mat = Matrix.empty
            matGrid.each {|r|
                mat = Matrix.rows(mat.to_a << r.split(" ").map(&:to_i).to_a)
            }
            mat
        end

        def sum_missing(board, seen) 
            return (board.to_a.flatten - seen).reduce(:+)
        end

        def part1
            @nums = @lines[0].split(",").map(&:to_i)
            @boards = @lines[2...].select {|l| l != ""}.each_slice(5).map{parseBoard(_1)}
            
            @turnsToWin = Parallel.map(@boards){|b|
                seen = []
                catch(:stop) do
                    @nums.each{|n|
                        seen << n
                        (0...5).each{|r|
                            throw :stop if (b.column(r).to_a-seen).length == 0
                            throw :stop if (b.row(r).to_a-seen).length == 0
                        }
                    }
                end
                [sum_missing(b, seen)*seen.last, seen.length]
            }

            @p1 = @turnsToWin.detect{|t| t.include?(@turnsToWin.map{_1[1]}.min)}[0]
        end

        def part2
            @p2 = @turnsToWin.detect{|t| t.include?(@turnsToWin.map{_1[1]}.max)}[0]
        end
    end
end