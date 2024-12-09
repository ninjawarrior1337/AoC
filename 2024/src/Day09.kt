data class Span(val length: Int, val content: Int?)

data class Disk(val map: List<Long>) {
    val layout: List<Long?>
        get() = map.flatMapIndexed {idx, v ->
            val isDataBlock = idx % 2 == 0
            val blockContent = idx / 2

            if(!isDataBlock) {
                return@flatMapIndexed List(v.toInt()) {null}
            }

            List(v.toInt()) {blockContent.toLong()}
        }

    val spans: List<Span>
        get() = map.mapIndexed { idx, v ->
            val isDataBlock = idx % 2 == 0
            val blockContent = idx / 2

            if(!isDataBlock) {
                return@mapIndexed Span(v.toInt(), null)
            }

            Span(v.toInt(), blockContent)
        }

    fun defragment(): MutableList<Long?> {
        val layout = this.layout.toMutableList()
        var lPtr = 0
        var rPtr = layout.size-1

        while(lPtr < rPtr) {
            if(layout[lPtr] != null) {
                lPtr++
                continue
            }
            if (layout[rPtr] == null) {
                rPtr--
                continue
            }

            layout[lPtr] = layout[rPtr].also { layout[rPtr] = layout[lPtr] }

            lPtr++
            rPtr--
        }

        return layout
    }

    fun goodDefragment(): MutableList<Span> {
        val spans = this.spans.toMutableList()
        var rSpanPtr = spans.size-1

        while(rSpanPtr > 0) {
            while (spans[rSpanPtr].content == null ) {
                rSpanPtr--
            }

            for(i in 0..<(rSpanPtr)) {
                val lSpan = spans[i]
                val rSpan = spans[rSpanPtr]

                if(lSpan.length >= rSpan.length && lSpan.content == null) {
                    val extra = lSpan.length - rSpan.length

                    spans.removeAt(rSpanPtr)
                    spans.add(rSpanPtr, Span(rSpan.length, null))
                    spans.removeAt(i)
                    spans.add(i, rSpan)
                    if(extra > 0) {
                        spans.add(i+1, Span(extra, null))
                    }
                    break
                }
            }
            rSpanPtr--
        }

        return spans
    }
}

fun main() {
    val input = readInput("Day09")

    val disk = Disk(input.map { it.toString().toLong() })

    disk.defragment().withIndex().filter { (i, v) -> v != null }.sumOf { (i, v) -> i*v!! }.println()
    disk.goodDefragment().flatMap { span -> List(span.length) {span.content?.toLong()} }.withIndex().filter { (i, v) -> v != null }.sumOf { (i, v) -> i*v!! }.println()
}