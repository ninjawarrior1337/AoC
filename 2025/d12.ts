import { pipe } from "effect"
import { unlines } from "./utils"

const txt = await Bun.file("inputs/d12.txt").text()

type Data = {
    presents: boolean[][][]
    trees: {
        rows: number,
        columns: number,
        counts: number[]
    }[]
}

const parse = (input: string) => {
    const parts = input.split("\n\n")

    const presents = parts.filter(v => /^\d:/.test(v)).map(v => {
        const present = v.substring(3)
        return present.split("\n").map(v => v.split("").map(c => c === "#"))
    })

    const treesStr = parts.filter(v => !/^\d:/.test(v)).at(0)!
    const trees = unlines(treesStr).map(t => {
        const [dims, counts] = t.split(": ")
        const [rows, columns] = dims!.split("x").map(v => parseInt(v))!

        return {
            rows,
            columns,
            counts: counts?.split(" ").map(v => parseInt(v))!
        }
    })

    return {
        presents,
        trees
    } as Data
}

const part1 = (d: Data) => d.trees.filter(t => t.rows*t.columns >= 9 * t.counts.reduce((acc, v) => acc+v)).length
console.log(pipe(
    txt,
    parse,
    part1
))