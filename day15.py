import numpy as np


class Crate:
    def __init__(self, poses):
        self.poses = poses  # tuple of 2-tuples (length 1 or 2)
    
    def can_move(self, delta, board, crates):
        for pos in self.poses:
            next_pos = tuple(np.array(pos) + delta)
            if board[next_pos] == '#':
                # can't move
                return False
            if board[next_pos] == '.':
                # can maybe move
                continue
            for crate in crates:
                if crate is self:
                    continue
                if next_pos in crate.poses:
                    could_move = crate.can_move(delta, board, crates)
                    if not could_move:
                        # we can't move either
                        return False
        return True
    
    def get_tree(self, delta, crates):
        children = set()
        for pos in self.poses:
            next_pos = tuple(np.array(pos) + delta)
            for crate in crates:
                if crate is self:
                    continue
                if next_pos in crate.poses:
                    children.update(crate.get_tree(delta, crates))
        return children | {self}


def day15(inp, part1=True):
    board_str, moves = inp.strip().split('\n\n')
    moves = moves.replace('\n', '')
    board = np.array([list(line) for line in board_str.splitlines()])
    deltas = {
        'v': [1, 0],
        '^': [-1, 0],
        '>': [0, 1],
        '<': [0, -1],
    }

    if part1:
        board = np.array([list(line) for line in board_str.splitlines()])
        crates = [
            Crate((pos,))
            for pos in zip(*np.array((board == 'O').nonzero()).reshape(2, -1))
        ]
    else:
        board_str = board_str.replace('O', '[]').replace('#', '##').replace('.', '..').replace('@', '@.')
        board = np.array([list(line) for line in board_str.splitlines()])
        crates = [
            Crate((start_pos, (start_pos[0], start_pos[1] + 1)))
            for start_pos in zip(*np.array((board == '[').nonzero()).reshape(2, -1))
        ]

    start = np.array((board == '@').nonzero()).ravel()
    board[tuple(start)] = '.'
    pos = start
    for move in moves:
        delta = deltas[move]
        next_pos = tuple(np.array(pos) + delta)
        if board[next_pos] == '#':
            # no move
            continue
        if board[next_pos] == '.':
            # move
            pos = next_pos
            continue

        # there's exactly one crate in our way here
        for crate in crates:
            if next_pos in crate.poses:
                could_move = crate.can_move(delta, board, crates)
                break
        if not could_move:
            # no move
            continue

        # we need to shift a hierarchy of crates
        shifting_inds = []
        for moved_crate in crate.get_tree(delta, crates):
            shifting_inds.extend(moved_crate.poses)
            moved_crate.poses = tuple(map(tuple, np.array(moved_crate.poses) + delta))
        shifting_inds = np.array(shifting_inds)
        new_inds = shifting_inds + delta
        old_contents = board[tuple(shifting_inds.T)]
        board[tuple(shifting_inds.T)] = '.'
        board[tuple(new_inds.T)] = old_contents
        pos = next_pos

    result = sum(crate.poses[0][0] * 100 + crate.poses[0][1] for crate in crates)
    return result


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp), day15(testinp, part1=False))
    inp = open('day15.inp').read()
    print(day15(inp), day15(inp, part1=False))
