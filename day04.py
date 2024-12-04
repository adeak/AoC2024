import numpy as np


def day04(inp):
    board = np.array([
        list(line)
        for line in inp.strip().splitlines()
    ])

    part1 = 0
    for x_start in range(board.shape[0]):
        x_inds_ref = np.arange(x_start, x_start + 4)
        for y_start in range(board.shape[1]):
            y_inds_ref = np.arange(y_start, y_start + 4)

            ind_pairs = [
                (x_inds_ref, np.full_like(y_inds_ref, fill_value=y_start)),
                (x_inds_ref[::-1], np.full_like(y_inds_ref, fill_value=y_start)),
                (np.full_like(x_inds_ref, fill_value=x_start), y_inds_ref),
                (np.full_like(x_inds_ref, fill_value=x_start), y_inds_ref[::-1]),
                (x_inds_ref, y_inds_ref),
                (x_inds_ref[::-1], y_inds_ref),
                (x_inds_ref, y_inds_ref[::-1]),
                (x_inds_ref[::-1], y_inds_ref[::-1]),
            ]
            for x_inds, y_inds in ind_pairs:
                if (x_inds < 0).any() or (x_inds >= board.shape[0]).any() or (y_inds < 0).any() or (y_inds >= board.shape[1]).any():
                    # out of bounds
                    continue
                if (board[x_inds, y_inds] == list('XMAS')).all():
                    part1 += 1

    part2 = 0
    mask_ref = np.array([[True, False, True], [False, True, False], [True, False, True]])
    inds_ref_x, inds_ref_y = mask_ref.nonzero()
    valid_strings = {'MSAMS', 'SSAMM', 'SMASM', 'MMASS'}
    for x_shift in range(board.shape[0] - 2):
        for y_shift in range(board.shape[1] - 2):
            if ''.join(board[inds_ref_x + x_shift, inds_ref_y + y_shift]) in valid_strings:
                part2 += 1

    return part1, part2


if __name__ == "__main__":
    testinp = open('day04.testinp').read()
    print(day04(testinp))
    inp = open('day04.inp').read()
    print(day04(inp))
