import kotlin.math.absoluteValue

val PairSets = setOf(
    listOf(Pair(0, 0), Pair(1, 0), Pair(2, 0), Pair(3, 0)),
    listOf(Pair(0, 0), Pair(0, 1), Pair(0, 2), Pair(0, 3)),
    listOf(Pair(0, 0), Pair(1, 1), Pair(2, 2), Pair(3, 3)),
    listOf(Pair(0, 0), Pair(-1, 0), Pair(-2, 0), Pair(-3, 0)),
    listOf(Pair(0, 0), Pair(0, -1), Pair(0, -2), Pair(0, -3)),
    listOf(Pair(0, 0), Pair(-1, -1), Pair(-2, -2), Pair(-3, -3)),
    listOf(Pair(0, 0), Pair(1, -1), Pair(2, -2), Pair(3, -3)),
    listOf(Pair(0, 0), Pair(-1, 1), Pair(-2, 2), Pair(-3, 3)),
)

val PairSetsA = setOf(
    listOf(Pair(0, 0), Pair(1, 1), Pair(-1, -1)),
    listOf(Pair(0, 0), Pair(-1, 1), Pair(1, -1))
)

fun main() {
    fun countXMASAtLocation(grid: List<CharArray>, loc: Pair<Int, Int>): Int {
        return PairSets.map {
            list -> list.map {
                grid.getOrNull(loc.first + it.first)?.getOrNull(loc.second + it.second) ?: ' '
            }
        }.count { it.joinToString("") == "XMAS" }
    }

    fun isValidMAS(grid: List<CharArray>, loc: Pair<Int, Int>): Boolean {
        return PairSetsA.map {
        list -> list.map {
            grid.getOrNull(loc.first + it.first)?.getOrNull(loc.second + it.second) ?: ' '
            }
        }.all { it.toSet() == setOf('M', 'A', 'S') }
    }

    fun part1(input: List<CharArray>): Int {
        val xlocs = mutableSetOf<Pair<Int, Int>>()

        for ((r, line) in input.withIndex()) {
            for ((c, char) in line.withIndex()) {
                if(char == 'X') {
                    xlocs.add(Pair(r, c))
                }
            }
        }

        return xlocs.sumOf { countXMASAtLocation(input, it) }
    }

    fun part2(input: List<CharArray>): Int {
        val alocs = mutableSetOf<Pair<Int, Int>>()

        for ((r, line) in input.withIndex()) {
            for ((c, char) in line.withIndex()) {
                if(char == 'A') {
                    alocs.add(Pair(r, c))
                }
            }
        }

        return alocs.filter {isValidMAS(input, it)}.size
    }

    val input = readInputGrid("Day04")

    input.println()

    part1(input).println()
    part2(input).println()
}
