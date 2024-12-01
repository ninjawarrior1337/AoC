import kotlin.math.absoluteValue

fun main() {
    fun part1(input: List<String>): Int {
        var list1 = input.map { it.split("   ") }.map { it[0].toInt() }
        var list2 = input.map { it.split("   ") }.map { it[1].toInt() }

        list1 = list1.sorted()
        list2 = list2.sorted()

        return list1.zip(list2).map { (it.first - it.second).absoluteValue }.sum()
    }

    fun part2(input: List<String>): Int {
        val list1 = input.map { it.split("   ") }.map { it[0].toInt() }
        val list2 = input.map { it.split("   ") }.map { it[1].toInt() }

        return list1.sumOf { it * list2.count { a -> a == it } }
    }

    // Test if implementation meets criteria from the description, like:
//    check(part1(listOf("test_input")) == 1)

    // Read the input from the `src/Day01.txt` file.
    val input = readInput("Day01")
    part1(input).println()
    part2(input).println()
}
