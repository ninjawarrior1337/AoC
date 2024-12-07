import kotlin.math.pow

enum class Operand {
    Mul,
    Add,
    Concat
}

data class Equation(val solution: Long, val nums: List<Long>) {
    private fun determineOpList(opTypes: Set<Operand>): Set<List<Operand>> {
        val base = opTypes.size
        val ops = mutableSetOf<List<Operand>>()
        val combinations = (base.toDouble()).pow(nums.windowed(2).size).toInt()

        for (i in 0..<combinations) {
            ops.add(i.toString(base).padStart(nums.windowed(2).size, '0').map {
                when (it) {
                    '0' -> Operand.Add
                    '1' -> Operand.Mul
                    '2' -> Operand.Concat
                    else -> throw Exception("WHat just happened")
                }
            })
        }
        return ops
    }

    fun canBeSolved(opTypes: Set<Operand>): Boolean {
        val ops = determineOpList(opTypes)

        val sol = ops.map { opList ->
            nums.windowed(2).zip(opList).fold(nums[0]) { acc, v ->
                when (v.second) {
                    Operand.Add -> acc + v.first[1]
                    Operand.Mul -> acc * v.first[1]
                    Operand.Concat -> (acc.toString() + v.first[1].toString()).toLong()
                }
            }
        }.filter { it == solution }

        return sol.firstOrNull() != null
    }
}

fun main() {
    val input = readInputLines("Day07")
    val equations = input.map { line ->
        val (sol, nums) = line.split(": ")
        Equation(sol.toLong(), nums.split(" ").map { it.toLong() })
    }

    equations.parallelStream().filter { it.canBeSolved(setOf(Operand.Add, Operand.Mul)) }.map { it.solution }
        .reduce(Long::plus).get().println()

    equations.parallelStream().filter { it.canBeSolved(setOf(Operand.Add, Operand.Mul, Operand.Concat)) }
        .map { it.solution }.reduce(Long::plus).get().println()
}