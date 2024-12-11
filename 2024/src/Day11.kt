import java.util.LinkedList

fun blinkCounts(stones: Map<Long, Long>): Map<Long, Long> {
    return buildMap {
        stones.entries.forEach { (k, v) ->
            when {
                k == 0L -> merge(1, v, Long::plus)
                k.toString().length % 2 == 0 -> {
                    val t = k.toString()
                    val (l, r) = t.chunked(t.length / 2).map { it.toLong() }
                    merge(l, v, Long::plus)
                    merge(r, v, Long::plus)
                }
                else -> merge(k*2024, v, Long::plus)
            }
        }
    }
}

fun main() {
    val list = readInput("Day11").split(Regex("\\s+")).map { it.toLong() }
    val seq = generateSequence(list.groupingBy { it }.eachCount().mapValues {(_, v) -> v.toLong()}) { blinkCounts(it) }
    seq.elementAt(25).values.sum().println()
    seq.elementAt(75).values.sum().println()
}