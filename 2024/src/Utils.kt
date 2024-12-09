import java.math.BigInteger
import java.security.MessageDigest
import kotlin.io.path.Path
import kotlin.io.path.readText
import kotlin.math.absoluteValue
import kotlin.math.sqrt

/**
 * Reads lines from the given input txt file.
 */
fun readInput(name: String) = Path("src/$name.txt").readText().trim()
fun readInputLines(name: String) = Path("src/$name.txt").readText().trim().lines()
fun readInputGrid(name: String) = readInputLines(name).map { it.toCharArray() }

/**
 * Converts string to md5 hash.
 */
fun String.md5() = BigInteger(1, MessageDigest.getInstance("MD5").digest(toByteArray()))
    .toString(16)
    .padStart(32, '0')

/**
 * The cleaner shorthand for printing output.
 */
fun Any?.println() = println(this)

typealias Point2D = Pair<Int, Int>

operator fun Point2D.minus(other: Point2D) = Point2D(this.first - other.first, this.second - other.second)
operator fun Point2D.plus(other: Point2D) = Point2D(this.first + other.first, this.second + other.second)
operator fun Point2D.times(other: Int) = Point2D(this.first * other, this.second * other)

fun Iterable<CharArray>.printlnIterChar() = this.forEach { ts ->
    println(ts)
}

fun List<CharArray>.indexedGridIterator(): List<Triple<Int, Int, Char>> {
    return this.flatMapIndexed {rIdx, r -> r.mapIndexed { cIdx, c -> Triple(rIdx, cIdx, c) }}
}

fun List<CharArray>.inBounds(p: Point2D): Boolean = this.getOrNull(p.first)?.getOrNull(p.second) != null

fun Pair<Int, Int>.euclideanDistanceTo(other: Pair<Int, Int>): Double {
    val dx = (this.second - other.second).toDouble()
    val dy = (this.first - other.first).toDouble()

    val dy2 = dy*dy
    val dx2 = dx*dx

    return sqrt(dy2+dx2)
}

fun Pair<Int, Int>.manhattanDistanceTo(other: Pair<Int, Int>): Int {
    val dx = (this.second - other.second).absoluteValue
    val dy = (this.first - other.first).absoluteValue

    return dy+dx
}