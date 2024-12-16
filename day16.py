from heapq import heapify, heappop, heappush

import numpy as np

from day10 import get_neighbs


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
    state = (0, start, orient)
    paths = [state]  # heapq
    best_scores = {(start, orient): state[0]}  # state -> best score
    while True:
        score, pos, orient = heappop(paths)
        # try to step forward
        next_pos = tuple(np.array(pos) + deltas[orient])
        if board[next_pos] == '.':
            next_state = (score + 1, next_pos, orient)
            if next_pos == target:
                # we're done with part 1
                winning_score = next_state[0]
                return winning_score

            if next_state[0] <= best_scores.get(next_state[1:], np.inf):
                # worth pursuing this step
                heappush(paths, next_state)
                best_scores[next_state[1:]] = next_state[0]

        for sane_turn in sane_turns[orient]:
            # only worth turning if step after turn is valid
            next_pos = tuple(np.array(pos) + deltas[sane_turn])
            if board[next_pos] == '.':
                next_state = (score + 1001, next_pos, sane_turn)
                if next_pos == target:
                    # we're done
                    winning_score = next_state[0]
                    return winning_score
                if next_state[0] <= best_scores.get(next_state[1:], np.inf):
                    # worth pursuing this step
                    heappush(paths, next_state)
                    best_scores[next_state[1:]] = next_state[0]


def day16b(inp, winning_score):
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
    while paths:
        score, tiles, orient = heappop(paths)
        # try to step forward
        next_pos = tuple(np.array(tiles[-1]) + deltas[orient])
        if board[next_pos] == '.' and score + 1 <= winning_score:
            next_state = (score + 1, tiles + (next_pos,), orient)
            if next_pos == target:
                # we're done with this path
                best_scores[next_pos, orient] = winning_score
                for tile in next_state[1]:
                    good_tiles.add(tile)
                # and there's no point turning anymore
                continue

            if next_state[0] <= best_scores.get((next_pos, orient), winning_score):
                # worth pursuing this step
                heappush(paths, next_state)
                best_scores[next_pos, orient] = next_state[0]

        for sane_turn in sane_turns[orient]:
            # only worth turning if step after turn is valid
            next_pos = tuple(np.array(tiles[-1]) + deltas[sane_turn])
            if board[next_pos] == '.' and score + 1001 <= winning_score:
                next_state = (score + 1001, tiles + (next_pos,), sane_turn)
                if next_pos == target:
                    # we're done with this path
                    best_scores[next_pos, sane_turn] = winning_score
                    for tile in next_state[1]:
                        good_tiles.add(tile)
                    continue

                if next_state[0] <= best_scores.get((next_pos, sane_turn), winning_score):
                    # worth pursuing this step
                    heappush(paths, next_state)
                    best_scores[next_pos, sane_turn] = next_state[0]
    return len(good_tiles)

if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    score = day16(testinp)
    print(score, day16b(testinp, score))
    inp = open('day16.inp').read()
    score = day16(inp)
    print(score, day16b(inp, score))
