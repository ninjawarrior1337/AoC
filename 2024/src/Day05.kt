import java.util.stream.Collectors

data class Rule(val before: Int, val after: Int)

data class Page(val rules: List<Rule>, val num: Int) : Comparable<Page> {
    override fun compareTo(other: Page): Int {
        val rGt = rules.firstOrNull { it.before == this.num && it.after == other.num }
        val rLt = rules.firstOrNull { it.after == this.num && it.before == other.num }
        return when {
            rGt != null -> -1
            rLt != null -> 1
            else -> 0
        }
    }
}

data class ProblemSet(val rules: List<Rule>, val pages: List<List<Int>>) {
    companion object {
        fun fromInput(input: List<String>): ProblemSet {
            val rules = input.subList(0, input.indexOfFirst { it.isBlank() });
            val pages = input.subList(input.indexOfFirst { it.isBlank() } + 1, input.size)

            return ProblemSet(
                rules.map { rule -> rule.split("|") }.map { rule -> Rule(rule[0].toInt(), rule[1].toInt()) },
                pages.map { p -> p.split(",").map { it.toInt() } }
            )
        }
    }

    fun isPageListValid(pages: List<Int>): Boolean {
        return pages.map { Page(this.rules, it) }.windowed(2).all { it[0].compareTo(it[1]) == -1 }
    }

    fun fixPageList(pages: List<Int>): List<Int> {
        return pages.map { Page(this.rules, it) }.sorted().map { it.num }
    }
}

fun main() {
    val input = readInputLines("Day05")
    val ps = ProblemSet.fromInput(input)
    fun part1(input: List<String>): Int {
        return ps.pages.filter { ps.isPageListValid(it) }.sumOf { it[it.size / 2] }
    }

    fun part2(input: List<String>): Int {
        return ps.pages.filter { !ps.isPageListValid(it) }.map { pages -> ps.fixPageList(pages) }.sumOf { it[it.size / 2] }
    }

    part1(input).println()
    part2(input).println()
}
