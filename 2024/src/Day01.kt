import kotlin.math.absoluteValue

fun main() {
    fun extractLeftRight(input: List<String>): Pair<List<Int>, List<Int>> {
        return Pair(
            input.map { it.split("   ") }.map { it[0].toInt() },
            input.map { it.split("   ") }.map { it[1].toInt() }
        )
    }

    fun part1(input: List<String>): Int {
        val (left, right) = extractLeftRight(input)
        return left.sorted().zip(right.sorted()).sumOf { (it.first - it.second).absoluteValue }
    }

    fun part2(input: List<String>): Int {
        val (left, right) = extractLeftRight(input)
        return left.sumOf { it * right.count { a -> a == it } }
    }

    val input = readInputLines("Day01")
    part1(input).println()
    part2(input).println()
}
