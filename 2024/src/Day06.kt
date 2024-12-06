import kotlin.math.absoluteValue

enum class Facing {
    Up,
    Down,
    Left,
    Right;

    fun rot90(): Facing {
        return when (this) {
            Up -> Right
            Right -> Down
            Down -> Left
            Left -> Up
        }
    }
}

class GameState(private val board: List<CharArray>, private var position: Pair<Int, Int>, private var facing: Facing) {
    private fun isInFrontOfObstacle(): Boolean {
        return when (facing) {
            Facing.Up -> board.getOrNull(position.first - 1)?.getOrNull(position.second) == '#'
            Facing.Down -> board.getOrNull(position.first + 1)?.getOrNull(position.second) == '#'
            Facing.Left -> board.getOrNull(position.first)?.getOrNull(position.second - 1) == '#'
            Facing.Right -> board.getOrNull(position.first)?.getOrNull(position.second + 1) == '#'
        }
    }

    private fun move() {
        if (isInFrontOfObstacle()) {
            facing = facing.rot90()
            return
        }
        val (r, c) = position
        position = when (facing) {
            Facing.Up -> Pair(r - 1, c)
            Facing.Down -> Pair(r + 1, c)
            Facing.Left -> Pair(r, c - 1)
            Facing.Right -> Pair(r, c + 1)
        }
    }

    fun simulatePositions(): Set<Pair<Int, Int>> {
        val positions = mutableSetOf<Pair<Int, Int>>()

        while (position.first in board.indices && position.second in board[0].indices) {
            positions.add(position)
            move()
        }

        return positions
    }

    fun simulateLoopCheck(): Boolean {
        val positions = mutableSetOf<Triple<Int, Int, Facing>>()

        while (position.first in board.indices && position.second in board[0].indices) {
            if(!positions.add(Triple(position.first, position.second, facing))) {
                return false
            }
            move()
        }

        return true
    }
}

fun main() {
    fun getGuardPosition(input: List<CharArray>): Pair<Int, Int>? {
        for ((rIdx, r) in input.withIndex()) {
            for ((cIdx, c) in r.withIndex()) {
                if (c == '^') {
                    return Pair(rIdx, cIdx)
                }
            }
        }
        return null
    }

    var posS = setOf<Pair<Int, Int>>()

    fun part1(input: List<CharArray>): Int {
        val pos = getGuardPosition(input)!!
        val state = GameState(input, Pair(pos.first, pos.second), Facing.Up)

        posS = state.simulatePositions()

        return posS.size
    }

    fun part2(input: List<CharArray>): Long {
        val pos = getGuardPosition(input)!!

        val states = posS.map {
            val newInput = input.map { i -> i.copyOf() }
            newInput[it.first][it.second] = '#'
            GameState(newInput, Pair(pos.first, pos.second), Facing.Up)
        }

        return states.parallelStream().filter {!it.simulateLoopCheck()}.count()
    }

    val input = readInputGrid("Day06")
    part1(input).println()
    part2(input).println()
}
