import numpy as np


def day25(inp):
    blocks = inp.strip().split('\n\n')

    keys = []
    locks = []
    for block in blocks:
        board = np.array([list(row) for row in block.splitlines()])
        bucket = keys if board[0, 0] == '.' else locks
        heights = (board == '#').sum(0) - 1
        bucket.append(heights)

    keys = np.array(keys)  # (n_keys, 5)
    locks = np.array(locks)  # (n_locks, 5)
    sums = keys + locks[:, None, :]  # (n_locks, n_keys, 5)
    matches = (sums <= 5).all(axis=-1)  # (n_locks, n_keys) bool
    result = matches.sum()

    return result


if __name__ == "__main__":
    testinp = open('day25.testinp').read()
    print(day25(testinp))
    inp = open('day25.inp').read()
    print(day25(inp))
