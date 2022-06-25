module AOC 
    class Day2 < AocDay
        def reset
            @depth = 0
            @horiz = 0
            @aim = 0
        end

        def part1()
            reset()
            @lines.each{|l| 
                ins, amt = l.split
                amt = amt.to_i

                case ins
                in 'forward'
                    @horiz+=amt
                in 'down'
                    @depth+=amt
                in 'up'
                    @depth-=amt
                end
            }
            @p1 = @depth*@horiz
        end

        def part2()
            reset()
            @lines.each {|l|
                ins, amt = l.split
                amt = amt.to_i

                case ins
                in 'forward'
                    @horiz+=amt
                    @depth+=@aim*amt
                in 'down'
                    @aim += amt
                in 'up'
                    @aim -= amt
                end
            }
            @p2 = @depth*@horiz
        end
    end
end