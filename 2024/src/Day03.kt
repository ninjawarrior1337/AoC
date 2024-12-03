import kotlin.math.absoluteValue

fun main() {
    fun part1(input: String): Int {
        val re = Regex("mul\\((\\d{1,3}),(\\d{1,3})\\)")

        val matches = re.findAll(input)

        var total = 0
        for (m in matches) {
            total += m.groupValues[1].toInt() * m.groupValues[2].toInt()
        }

        return total
    }

    fun part2(input: String): Int {
        val re = Regex("mul\\((\\d{1,3}),(\\d{1,3})\\)|do\\(\\)|don't\\(\\)")

        val matches = re.findAll(input)

        var total = 0
        var enabled = true

        for (m in matches) {
            when(m.value) {
                "don't()" -> enabled = false
                "do()" -> enabled = true
                else -> {
                    if (enabled) {
                        total += m.groupValues[1].toInt() * m.groupValues[2].toInt()
                    }
                }
            }
        }

        return total
    }

    val input = readInput("Day03")
    part1(input).println()
    part2(input).println()
}
