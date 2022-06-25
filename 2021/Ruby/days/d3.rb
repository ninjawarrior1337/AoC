module AOC

    class Day3 < AocDay
        
        def generate_gamma_epsilon(lines)
            zeros = Hash.new(0)
            lines.each {|l| 
                l.chars.each.with_index {|c, i| 
                    if c == "0" then
                        zeros[i] += 1
                    end
                }
            }
            gammaStr = ""
            (0...lines.first.length).each{|n|
                next gammaStr << "1" if zeros[n] <= lines.count/2
                next gammaStr << "0"
            }
            epsilonStr = gammaStr.chars.map{|x|
                if x == "0" then
                    1
                else
                    0
                end
            }.join

            return gammaStr, epsilonStr
        end

        def part1
            @p1 = generate_gamma_epsilon(@lines).reduce(1){|acc, x| acc *= x.to_i(2)}
        end

        def part2
            o2Lines = (0...@lines.first.length).reduce(@lines){ |acc, n|
                break acc[0] if acc.length == 1
                g, e = generate_gamma_epsilon(acc)
                acc.select{ |l|
                    l[n] == g[n]
                }
            }
            co2Lines = (0...@lines.first.length).reduce(@lines){ |acc, n|
                break acc[0] if acc.length == 1
                g, e = generate_gamma_epsilon(acc)
                acc.select{ |l|
                    l[n] == e[n]
                }
            }

            @p2 = o2Lines.to_i(2) * co2Lines.to_i(2)
        end

    end

end