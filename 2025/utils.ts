export const parseGrid = (input: string) => {
    return input.split("\n").map(v => v.split(""))
}

export const unlines = (input: string) => input.split("\n")