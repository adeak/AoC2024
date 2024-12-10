from collections import defaultdict
from functools import cache

import numpy as np


def day10(inp):
    board = np.array([list(line) for line in inp.strip().splitlines()]).astype(int)

    starts = set(zip(*(board == 0).nonzero()))
    ends = set(zip(*(board == 9).nonzero()))

    done_paths = []
    for start in starts:
        paths = [(start,)]
        while paths:
            next_paths = []
            for path in paths:
                pos = path[-1]
                for neighb in get_neighbs(pos, board.shape):
                    if board[neighb] != board[pos] + 1:
                        # impassable
                        continue
                    if neighb in ends:
                        # this path is done
                        done_paths.append(path + (neighb,))
                    else:
                        # go on with this path
                        next_paths.append(path + (neighb,))

            # continue with next step
            paths = next_paths

    tracks = defaultdict(set)
    ratings = defaultdict(int)  # Counter
    for path in done_paths:
        trailhead = path[0]
        summit = path[-1]
        tracks[trailhead].add(summit)
        ratings[trailhead] += 1
    part1 = sum(len(summits) for summits in tracks.values())
    part2 = sum(ratings.values())

    return part1, part2


@cache
def get_neighbs(pos, shape):
    neighbs = []
    for delta in (0, 1), (0, -1), (1, 0), (-1, 0):
        next_pos = pos[0] + delta[0], pos[1] + delta[1]
        if 0 <= next_pos[0] < shape[0] and 0 <= next_pos[1] < shape[1]:
            neighbs.append(next_pos)
    return neighbs


if __name__ == "__main__":
    testinp = open('day10.testinp').read()
    print(day10(testinp))
    inp = open('day10.inp').read()
    print(day10(inp))
