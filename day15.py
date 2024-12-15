import numpy as np


class Crate:
    def __init__(self, poses, walls):
        self.poses = poses  # tuple of 2-tuples (length 1 or 2)
        self._walls = walls  # frozenset of 2-tuples
    
    def can_move(self, delta, crates):
        for pos in self.poses:
            next_pos = tuple(np.array(pos) + delta)
            if next_pos in self._walls:
                # can't move
                return False
            if next_pos not in crates:
                # can maybe move
                continue
            next_crate = crates[next_pos]
            if next_crate is self:
                continue

            could_move = next_crate.can_move(delta, crates)
            if not could_move:
                # we can't move either
                return False
        return True
    
    def get_tree(self, delta, crates):
        children = set()
        for pos in self.poses:
            next_pos = tuple(np.array(pos) + delta)
            next_crate = crates.get(next_pos)
            if next_crate is not None and next_crate is not self:
                children.update(next_crate.get_tree(delta, crates))
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
        board = np.array([list(line) for line in board_str.splitlines()])  # not updated beyond this point
        walls = frozenset(zip(*np.array((board == '#').nonzero()).reshape(2, -1)))
        crates = {
            pos: Crate((pos,), walls)
            for pos in zip(*np.array((board == 'O').nonzero()).reshape(2, -1))
        }  # crate position -> crate instance
    else:
        board_str = board_str.replace('O', '[]').replace('#', '##').replace('.', '..').replace('@', '@.')
        board = np.array([list(line) for line in board_str.splitlines()])  # not updated beyond this point
        walls = frozenset(zip(*np.array((board == '#').nonzero()).reshape(2, -1)))
        crates = {
            start_pos: Crate((start_pos, (start_pos[0], start_pos[1] + 1)), walls)
            for start_pos in zip(*np.array((board == '[').nonzero()).reshape(2, -1))
        }  # crate position -> crate instance for all positions in a moment
        for crate in list(crates.values()):
            crates[crate.poses[1]] = crate

    start = np.array((board == '@').nonzero()).ravel()
    board[tuple(start)] = '.'
    pos = start
    for move in moves:
        delta = deltas[move]
        next_pos = tuple(np.array(pos) + delta)
        if next_pos in walls:
            # no move
            continue
        if next_pos not in crates:
            # move
            pos = next_pos
            continue

        # there's exactly one crate in our way here
        hit_crate = crates[next_pos]
        could_move = hit_crate.can_move(delta, crates)
        if not could_move:
            # no move
            continue

        # we need to shift a hierarchy of crates
        moved_crates = hit_crate.get_tree(delta, crates)
        for crate in moved_crates:
            for crate_pos in crate.poses:
                del crates[crate_pos]
            crate.poses = tuple(tuple(np.array(crate_pos) + delta) for crate_pos in crate.poses)
        for crate in moved_crates:
            for crate_pos in crate.poses:
                crates[crate_pos] = crate
        pos = next_pos

    result = sum(crate.poses[0][0] * 100 + crate.poses[0][1] for crate in set(crates.values()))
    return result


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp), day15(testinp, part1=False))
    inp = open('day15.inp').read()
    print(day15(inp), day15(inp, part1=False))
