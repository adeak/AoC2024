from math import prod
import re


def day03(inp):
    data = ' '.join(inp.strip().splitlines())

    part1 = part2 = 0
    all_matcher = re.compile(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")
    enabled = True
    for match in all_matcher.finditer(data):
        if match.group() == 'do()':
            # part 2
            enabled = True
        elif match.group() == "don't()":
            # part 2
            enabled = False
        else:
            contribution = prod(map(int, match.groups()))
            part1 += contribution
            if enabled:
                part2 += contribution

    return part1, part2


if __name__ == "__main__":
    testinp = open('day03.testinp').read()
    testinp2 = open('day03.testinp2').read()
    print(day03(testinp)[0], day03(testinp2)[1])
    inp = open('day03.inp').read()
    print(day03(inp))
