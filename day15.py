import numpy as np


class Crate:
    def __init__(self, poses):
        self.poses = poses  # tuple of 2-tuples
    
    def try_move(self, delta, board, crates):
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
                    could_move = crate.try_move(delta, board, crates)
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


def day15(inp):
    board_str, moves = inp.strip().split('\n\n')
    moves = moves.replace('\n', '')
    board = np.array([list(line) for line in board_str.splitlines()])
    deltas = {
        'v': [1, 0],
        '^': [-1, 0],
        '>': [0, 1],
        '<': [0, -1],
    }

    # part 1
    start = np.array((board == '@').nonzero()).ravel()
    board[tuple(start)] = '.'
    pos = start
    for move in moves:
        delta = deltas[move]
        next_pos = pos + delta
        if board[tuple(next_pos)] == '.':
            # no-brainer move
            pos = next_pos
            continue
        if board[tuple(next_pos)] == '#':
            # no-brainer non-move
            continue
        bump_pos = next_pos + delta
        while board[tuple(bump_pos)] == 'O':
            bump_pos += delta
        if board[tuple(bump_pos)] == '#':
            # can't actually move
            continue
        # teleport first box to last position
        board[tuple(next_pos)] = '.'
        board[tuple(bump_pos)] = 'O'
        pos = next_pos
    box_x, box_y = (board == 'O').nonzero()
    part1 = (100 * box_x + box_y).sum()

    # part 2
    board_str = board_str.replace('O', '[]').replace('#', '##').replace('.', '..').replace('@', '@.')
    board = np.array([list(line) for line in board_str.splitlines()])
    start = np.array((board == '@').nonzero()).ravel()
    board[tuple(start)] = '.'
    crates = [
        Crate((start_pos, (start_pos[0], start_pos[1] + 1)))
        for start_pos in zip(*np.array((board == '[').nonzero()).reshape(2, -1))
    ]
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
                could_move = crate.try_move(delta, board, crates)
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
    box_x, box_y = (board == '[').nonzero()
    part2 = (100 * box_x + box_y).sum()

    return part1, part2

if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp))
    inp = open('day15.inp').read()
    print(day15(inp))
