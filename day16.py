from heapq import heapify, heappop, heappush

import numpy as np


def day16(inp):
    board = np.array([list(line) for line in inp.splitlines()])
    deltas = {
        'v': [1, 0],
        '^': [-1, 0],
        '>': [0, 1],
        '<': [0, -1],
    }
    sane_turns = {
        'v': '<>',
        '^': '<>',
        '<': 'v^',
        '>': 'v^',
    }

    target = tuple(np.array((board == 'E').nonzero()).ravel())
    start = tuple(np.array((board == 'S').nonzero()).ravel())
    board[target] = board[start] = '.'

    orient = '>'
    path = (0, (start,), orient)
    paths = [path]  # heapq
    best_scores = {(path[1][-1], orient): path[0]}  # (pos, orientation) -> best score
    good_tiles = set()
    winning_score = np.inf
    while paths:
        score, tiles, orient = heappop(paths)

        # check forward step, and step after two potential meaningful turns
        next_orientations = orient + sane_turns[orient]
        costs = [1, 1001, 1001]
        for next_orient, cost in zip(next_orientations, costs):
            next_pos = tuple(np.array(tiles[-1]) + deltas[next_orient])
            if board[next_pos] == '.' and score + cost <= winning_score:
                next_state = (score + cost, tiles + (next_pos,), next_orient)
                if next_pos == target:
                    # we're done with this path
                    for tile in next_state[1]:
                        good_tiles.add(tile)

                    if winning_score == np.inf:
                        # first success, set winning score
                        winning_score = next_state[0]
                        # prune remaining states
                        paths = [path for path in paths if path[0] <= winning_score]
                        heapify(paths)

                    best_scores[next_pos, next_orient] = winning_score
                    continue

                if next_state[0] <= best_scores.get((next_pos, next_orient), winning_score):
                    # worth pursuing this step
                    heappush(paths, next_state)
                    best_scores[next_pos, next_orient] = next_state[0]

    part1 = winning_score
    part2 = len(good_tiles)
    return part1, part2

if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    print(day16(testinp))
    inp = open('day16.inp').read()
    print(day16(inp))
