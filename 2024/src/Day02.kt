import kotlin.math.abs
import kotlin.math.absoluteValue

enum class DiffType {
    Increasing,
    Decreasing
}

fun main() {
    fun parseRow(s: String): List<Int> {
        return s.split(" ").map { it.toInt() }
    }

    fun levelsAreSafe(levels: List<Int>): Boolean {
        val diffMarkers = levels.windowed(2).map {
            if (it[0] > it[1]) DiffType.Decreasing else DiffType.Increasing
        }

        return (diffMarkers.all { it == DiffType.Increasing } || diffMarkers.all { it == DiffType.Decreasing }) && levels.windowed(
            2
        ).all { (it[0] - it[1]).absoluteValue in 1..3 }
    }

    fun part1(input: List<String>): Int {
        val levels = input.map { parseRow(it) }
        return levels.map { levelsAreSafe(it) }.count { it }
    }

    fun part2(input: List<String>): Int {
        val levels = input.map { parseRow(it) }

        return levels.map { level ->
            val removed = mutableSetOf<List<Int>>()
            for(i in level.indices) {
                removed.add(level.filterIndexed {idx, _ -> idx != i})
            }
            levelsAreSafe(level) || removed.any { levelsAreSafe(it) }
        }.count {it}
    }

    val input = readInput("Day02")
    part1(input).println()
    part2(input).println()
}
