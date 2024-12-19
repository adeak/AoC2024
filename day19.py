from functools import cache
import re


def day19(inp):
    blocks = inp.strip().split('\n\n')
    patterns = blocks[0].split(', ')
    designs = blocks[1].splitlines()

    @ cache
    def count_configurations(design):
        count = 0
        for pattern in patterns:
            if not design.startswith(pattern):
                continue
            rest = design.removeprefix(pattern)
            if not rest:
                count += 1

            count += count_configurations(rest)
        return count

    part1 = part2 = 0
    for design in designs:
        # part2: find all combinations
        count = count_configurations(design)
        if count:
            part1 += 1
        part2 += count

    return part1, part2



if __name__ == "__main__":
    testinp = open('day19.testinp').read()
    print(day19(testinp))
    inp = open('day19.inp').read()
    print(day19(inp))
