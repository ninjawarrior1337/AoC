data class Line(val a: Point2D, val b: Point2D) {
    fun delta() = a-b
}

data class AntennaMap(private val grid: List<CharArray>) {
    private val antennaPositions = mutableMapOf<Char, MutableSet<Pair<Int, Int>>>()

    init {
        this.grid.indexedGridIterator().filter { it.third != '.' }.forEach { (rIdx, cIdx, c) ->
            val v = this.antennaPositions.getOrPut(c) { mutableSetOf() }
            v.add(Pair(rIdx, cIdx))
        }
    }

    private fun getAntiNodesForAntennaId(aId: Char, full: Boolean = false): List<Point2D> {
        val antennaPos = this.antennaPositions[aId]!!

        val lines = antennaPos.flatMap { p ->
            antennaPos.filter { s -> s != p }.map {
                s -> Line(p, s)
            }
        }.toSet()

        return when(full) {
            true -> lines.flatMap { line ->
                val delta = line.delta()
                generateSequence(line.a) { it-delta }.takeWhile { grid.inBounds(it) }.toSet() +
                generateSequence(line.a) { it+delta }.takeWhile { grid.inBounds(it) }.toSet()
            }
            false -> lines.flatMap {
                val delta = it.delta()
                listOf(it.a + delta, it.b - delta)
            }.filter { grid.inBounds(it) }
        }
    }

    fun findAntiNodes(full: Boolean = false): Set<Pair<Int, Int>> {
        return this.antennaPositions.keys.flatMap { aId ->
            this.getAntiNodesForAntennaId(aId, full)
        }.toSet()
    }
}

fun main() {
    val input = readInputGrid("Day08")

    val a = AntennaMap(input)

    a.println()

    a.run {
        findAntiNodes(full = false).size.println()
        findAntiNodes(full = true).size.println()
    }
}