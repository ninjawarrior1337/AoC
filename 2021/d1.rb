lines = File.readlines("inputs/d1.txt")

countConsecutiveIncreases=->e{
    e.each_with_index.map{ |m, i| 
        0 if i == 0
        m > e.map(&:to_i)[i-1] ? 1 : 0
    }.reduce(&:+)
}

#Part 1
puts countConsecutiveIncreases.call lines.map(&:to_i)

#Part 2
puts countConsecutiveIncreases.call lines.map(&:to_i).each_cons(3).map{|e|
    e.reduce(&:+)
}