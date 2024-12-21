from collections import Counter
from heapq import heappush, heappop

import numpy as np

from day10 import get_neighbs


def day20(inp):
    board = np.array([list(row) for row in inp.splitlines()])
    shape = board.shape
    start = tuple(np.array((board == 'S').nonzero()).ravel())
    target = tuple(np.array((board == 'E').nonzero()).ravel())
    walls = frozenset(zip(*np.array((board == '#').nonzero()).reshape(2, -1)))

    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # find potential walls to remove as a cheat
    base_time = walk_maze(start, target, walls, shape)
    savings = Counter()  # saving in ps -> multiplicity
    for maybe_remove in walls:
        if maybe_remove[0] in {0, shape[0] - 1} or maybe_remove[1] in {0, shape[1] - 1}:
            # edge wall
            continue
        if sum(1 for dx, dy in deltas if (maybe_remove[0] + dx, maybe_remove[1] + dy) in walls) >= 3:
            # no path through this wall
            continue
        # otherwise we could have two paths across this wall(???)
        time = walk_maze(start, target, walls - {maybe_remove}, shape)
        saving = base_time - time
        if saving < 0:
            # no savings
            continue
        if saving < 100:
            # uninteresting
            continue
        savings[base_time - time] += 1

    part1 = sum(savings.values())
    part2 = None
    return part1, part2


def walk_maze(start, target, walls, shape):
    state = (0, start)
    states = [state]  # heapq
    best_scores = {start: 0}  # pos -> best score
    while states:
        score, pos = heappop(states)

        for next_pos in get_neighbs(pos, shape):
            next_score = score + 1
            if next_pos == target:
                # we're done
                return next_score

            if next_pos in walls:
                # can't go there
                continue

            if next_score >= best_scores.get(next_pos, float('inf')):
                # already here before
                continue

            best_scores[next_pos] = next_score
            heappush(states, (next_score, next_pos))


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(day20(testinp))
    inp = open('day20.inp').read()
    print(day20(inp))
