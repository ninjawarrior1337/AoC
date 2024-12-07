import java.util.BitSet
import kotlin.math.pow

enum class Operand {
    Mul,
    Add,
    Concat
}

data class Equation(val solution: Long, val nums: List<Long>) {
    fun determineOperands(): Boolean {
        val ops = mutableSetOf<List<Operand>>()
        val combinations = (3.toDouble()).pow(nums.windowed(2).size).toInt()

        for(i in 0..<combinations) {
            ops.add(i.toString(3).padStart(nums.windowed(2).size, '0').map {
                when(it) {
                    '0' -> Operand.Add
                    '1' -> Operand.Mul
                    '2' -> Operand.Concat
                    else -> throw Exception("WHat just happened")
                }
            })
        }

        val sol = ops.map { opList ->
            val v = nums.windowed(2).zip(opList).fold(nums[0]) {acc, v ->
                when(v.second) {
                    Operand.Add -> acc + v.first[1]
                    Operand.Mul -> acc * v.first[1]
                    Operand.Concat -> (acc.toString() + v.first[1].toString()).toLong()
                }
            }
//            println("$solution: $v: $opList")
            v
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

    equations.filter { it.determineOperands() }.sumOf { it.solution }.println()
}