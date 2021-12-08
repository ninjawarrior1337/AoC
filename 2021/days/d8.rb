require "parallel"

module AOC
    class Day8 < AocDay

        def gen_mappings(init_str)
            mappings = Hash.new(0)

            # parse obvious numbers
            strs = init_str.split(" ")
            strs.each{|x|
                if x.length == 2 then
                    mappings[x.split("").sort] = 1
                end
                if x.length == 4 then
                    mappings[x.split("").sort] = 4
                end
                if x.length == 3 then
                    mappings[x.split("").sort] = 7
                end
                if x.length == 7 then
                    mappings[x.split("").sort] = 8
                end
            }
            # Start figuring out what the rest are
            inv = mappings.invert

            # This part took a lot of paper
            for str in strs do
                segments = str.split("").sort
                if segments.count == 5 then
                    next mappings[segments.sort] = 2 if (segments-inv[4]).count == 3
                    next mappings[segments.sort] = 3 if (segments-inv[1]).count == 3
                    next mappings[segments.sort] = 5 if (segments-inv[1]).count == 4
                end
            end
            inv = mappings.invert
            for str in strs do
                segments = str.split("").sort
                if segments.count == 6 then
                    next mappings[segments.sort] = 6 if (segments-inv[1]).count == 5
                    next mappings[segments.sort] = 0 if (segments-inv[3]).count == 2
                    next mappings[segments.sort] = 9 if (segments-inv[3]).count == 1
                end
            end

            mappings
        end

        def part1
            chars = @lines.map{|l| l.split("|")[1].strip}
            @p1 = chars.map{|c|
                c.split(" ").map(&:length).map{|x|
                    1 if x == 2 || x == 4 || x == 3 || x == 7
                }.compact.reduce(:+)
            }.compact.reduce(:+)
        end

        def part2
            pp @lines.map{|l| l.split("|").map(&:strip)}.map{|x|
                m = gen_mappings(x[0])
                pp x[1].split(" ").map{|s| m[s.split("").sort]}
            }.reduce(0){|acc, n| acc+n.join.to_i}
        end
    end
end