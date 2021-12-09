require "parallel"
require "chunky_png"

module AOC
    class Day9 < AocDay

        def get_adjacent(mat, x, y)
            adj = []
            xs = (0...@mat.column_count)
            ys = (0...@mat.row_count)
            adj << [mat[y, x+1], x+1, y] if xs.include? x+1
            adj << [mat[y, x-1], x-1, y] if xs.include? x-1
            adj << [mat[y+1, x], x, y+1] if ys.include? y+1
            adj << [mat[y-1, x], x, y-1] if ys.include? y-1
            adj
        end

        def part1
            @mat = Matrix.rows @lines.map{|l| l.split("").map(&:to_i)}
            @mat2 = @mat.clone
            # We need this variable for part 2
            @lowPoints = []
            for y in (0...@mat.row_count) do
                for x in (0...@mat.column_count) do
                    adj = get_adjacent(@mat, x, y)
                    adj = adj.map{|x| x[0]}
                    
                    # pp adj, @mat[y, x], [x, y]
                    @lowPoints << [x, y] if adj.min > @mat[y, x]
                    @mat2[y,x] = adj.min > @mat[y, x] ? @mat[y, x]+1 : 0
                end
            end
            @p1 = @mat2.to_a.flatten.reduce(&:+)
        end

        def part2
            # Cool visualization bc why not
            png = ChunkyPNG::Image.new(@mat.column_count, @mat.row_count, ChunkyPNG::Color::TRANSPARENT)
            for y in (0...@mat.row_count) do
                for x in (0...@mat.column_count) do
                    png[x, y] = case @mat[y, x]
                    when 0
                        ChunkyPNG::Color("red")
                    when 1
                        ChunkyPNG::Color("orange")
                    when 2
                        ChunkyPNG::Color("yellow")
                    when 3
                        ChunkyPNG::Color("green")
                    when 4
                        ChunkyPNG::Color("blue")
                    when 5
                        ChunkyPNG::Color("indigo")
                    when 6
                        ChunkyPNG::Color("violet")
                    when 7
                        ChunkyPNG::Color("pink")
                    when 8
                        ChunkyPNG::Color("white")
                    when 9
                        ChunkyPNG::Color("black")
                    end
                end
            end
            png.save("d9.png")

            # Now for the actual solve
            @visited = Hash.new()
            for i in (0..100) do
                @visited[i] = Hash.new(false)
            end

            def get_basin(x, y)
                @visited[y][x] = true
                sum = 1

                adj = get_adjacent(@mat, x, y)
                for a in adj do
                    sum += get_basin(a[1], a[2]) if a[0] < 9 && !@visited[a[2]][a[1]]
                end

                sum
            end
            @p2 = @lowPoints.map{|lp| get_basin(lp[0], lp[1])}.sort[-3..-1].reduce(&:*)
        end
    end
end