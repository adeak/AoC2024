from heapq import heappop, heappush

import numpy as np

from day10 import get_neighbs


def day16(inp, part1=True):
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
                # we're done
                result = next_state[0]
                return result
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
                    result = next_state[0]
                    return result
                if next_state[0] <= best_scores.get(next_state[1:], np.inf):
                    # worth pursuing this step
                    heappush(paths, next_state)
                    best_scores[next_state[1:]] = next_state[0]

    return result


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    print(day16(testinp))#, day16(testinp, part1=False))
    inp = open('day16.inp').read()
    print(day16(inp))#, day16(inp, part1=False))
