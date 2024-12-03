import re


def day03(inp):
    data = ' '.join(inp.strip().splitlines())

    part1 = 0
    mul_matcher = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    for x_str, y_str in mul_matcher.findall(data):
        part1 += int(x_str) * int(y_str)

    part2 = 0
    pieces = []
    rest = data
    while rest:
        next_dont = rest.find("don't()")
        if next_dont < 0:
            pieces.append(rest)
            break
        pieces.append(rest[:next_dont])
        rest = rest[next_dont + 4:]
        next_do = rest.find("do()")
        if next_do < 0:
            break
        rest = rest[next_do:]
    data = ' '.join(pieces)
    for x_str, y_str in mul_matcher.findall(data):
        part2 += int(x_str) * int(y_str)
        
    return part1, part2


if __name__ == "__main__":
    testinp = open('day03.testinp').read()
    testinp2 = open('day03.testinp2').read()
    print(day03(testinp)[0], day03(testinp2)[1])
    inp = open('day03.inp').read()
    print(day03(inp))
