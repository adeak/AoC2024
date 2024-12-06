from collections import defaultdict
from itertools import cycle, product

import numpy as np


def walk_board(rocks, start):
    bounds = np.max(list(rocks), axis=0)
    seens = {start}

    deltas = {
        '^': (-1, 0),
        'v': (1, 0),
        '>': (0, 1),
        '<': (0, -1),
    }
    directions = cycle('^>v<')

    # auxiliary logistics
    rocks_by_row = defaultdict(set)
    rocks_by_col = defaultdict(set)
    for rock in rocks:
        rocks_by_row[rock[0]].add(rock)
        rocks_by_col[rock[1]].add(rock)

    pos = start
    orient = next(directions)
    history = {(pos, orient)}
    while True:
        delta = deltas[orient]
        next_pos = pos[0] + delta[0], pos[1] + delta[1]
        if next_pos in rocks:
            orient = next(directions)
            continue
        if not (0 <= next_pos[0] <= bounds[0] and 0 <= next_pos[1] <= bounds[1]):
            # end of walk
            exited = True
            return exited, len(seens)
        if (next_pos, orient) in history:
            # infinite loop found
            exited = False
            return exited, len(seens)

        # take a step
        pos = next_pos
        seens.add(pos)
        history.add((pos, orient))


def day06(inp):
    board = np.array([list(row) for row in inp.strip().splitlines()])
    rocks = set(zip(*(board == '#').nonzero()))
    start = next(zip(*(board == '^').nonzero()))

    # part 1: no infinite loop
    _, part1 = walk_board(rocks, start)

    # part 2: check all new rocks
    bounds = np.max(list(rocks), axis=0)
    part2 = 0
    for new_rock in product(range(bounds[0] + 1), range(bounds[1] + 1)):
        if new_rock in rocks:
            continue
        if new_rock == start:
            continue
        rocks_now = rocks.copy()
        rocks_now.add(new_rock)
        exited, _ = walk_board(rocks_now, start)
        if not exited:
            part2 += 1

    return part1, part2


if __name__ == "__main__":
    testinp = open('day06.testinp').read()
    print(day06(testinp))
    inp = open('day06.inp').read()
    print(day06(inp))
