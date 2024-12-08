from itertools import combinations

import numpy as np


def day08(inp, part2=False):
    board = np.array([list(line) for line in inp.strip().splitlines()])
    freqs = np.unique(board)
    freqs = freqs[freqs != '.']

    result = 0
    antinodes = set()
    for freq in freqs:
        i0s, j0s = (board == freq).nonzero()
        for inds in combinations(range(i0s.size), 2):
            # two antenna positions
            first = i0s[inds[0]], j0s[inds[0]]
            second = i0s[inds[1]], j0s[inds[1]]
            # vector from first to second
            delta = np.array(second) - first
            if part2:
                # step delta in both directions "far enough"
                # 0 index includes first and second antenna
                step_range = range(max(board.shape))
            else:
                # only step one outside in each direction
                step_range = [1]
            for i in step_range:
                antinodes.add(tuple(second + i*delta))
                antinodes.add(tuple(first - i*delta))
    # count antinodes inside the board
    result += sum(
        1
        for antinode in antinodes
        if 0 <= antinode[0] < board.shape[0] and 0 <= antinode[1] < board.shape[1]
    )

    return result


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    print(day08(testinp), day08(testinp, part2=True))
    inp = open('day08.inp').read()
    print(day08(inp), day08(inp, part2=True))
