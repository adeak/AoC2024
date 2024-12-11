from collections import Counter


def day11(inp):
    # @topaz is a troll
    stones = Counter(inp.split())

    for i in range(1, 76):
        next_stones = Counter()
        for value, multiplicity in stones.items():
            if value == '0':
                next_stones['1'] += multiplicity
            elif len(value) % 2 == 0:
                split_index = len(value) // 2
                for new_value in value[:split_index], value[split_index:]:
                    next_stones[new_value.lstrip('0').zfill(1)] += multiplicity
            else:
                next_stones[str(int(value) * 2024)] += multiplicity
        stones = next_stones

        if i == 25:
            part1 = sum(stones.values())
    part2 = sum(stones.values())

    return part1, part2

if __name__ == "__main__":
    testinp = open('day11.testinp').read()
    print(day11(testinp))
    inp = open('day11.inp').read()
    print(day11(inp))
