from collections import Counter

import numpy as np


def day01(inp):
    dat = np.fromstring(inp, sep=' ', dtype=int).reshape(-1, 2)
    first, second = dat.T

    # part 1
    part1 = abs(np.sort(second) - np.sort(first)).sum()

    # part 2
    counter = Counter(second)
    part2 = sum(val * counter[val] for val in first)

    return part1, part2


if __name__ == "__main__":
    testinp = open('day01.testinp').read()
    print(day01(testinp))
    inp = open('day01.inp').read()
    print(day01(inp))
