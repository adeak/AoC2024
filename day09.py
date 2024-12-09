from collections import deque
from itertools import count


def day09(inp):
    data = inp.strip()

    blocks = {}  # file_id -> (start, end)
    gap_sizes = {}  # gap_start -> gap_size
    pos = 0
    it = iter(data)
    for file_id in count():
        file_size = int(next(it))
        bounds = pos, pos + file_size - 1  # inclusive
        blocks[file_id] = bounds
        pos += file_size

        gap_size = int(next(it, -1))
        if gap_size < 0:
            # end of stream
            break
        gap_sizes[pos] = gap_size
        pos += gap_size

    # part 1
    file_poses = deque([
        (pos, file_id)
        for file_id, bounds in blocks.items()
        for pos in range(bounds[0], bounds[1] + 1)
    ])
    gap_poses = (
        pos
        for start_pos, gap_size in gap_sizes.items()
        for pos in range(start_pos, start_pos + gap_size)
    )
    # loop gap positions from the left
    for gap_pos in gap_poses:
        # loop file positions from the right
        orig_pos, file_id = file_poses.pop()
        if orig_pos < gap_pos:
            # we're all out of gaps, undo this last pop
            file_poses.append((orig_pos, file_id))
            break
        # put moved positions at the left of the deque for safe keeping
        file_poses.appendleft((gap_pos, file_id))

    part1 = sum(pos * file_id for pos, file_id in file_poses)

    # part 2
    for file_id in range(max(blocks), 0, -1):
        bounds = blocks[file_id]
        file_size = bounds[1] - bounds[0] + 1

        matching_gap = None
        for gap_start in sorted(gap_sizes):
            gap_size = gap_sizes[gap_start]
            if gap_size < file_size:
                continue
            if gap_start > bounds[0]:
                break
            # we have a matching gap, store starting position
            matching_gap = gap_start
            break

        if matching_gap is None:
            # no matching gap, nothing to do with this file
            continue

        # move into start of matching gap
        delta = bounds[0] - matching_gap
        blocks[file_id] = bounds[0] - delta, bounds[1] - delta

        # check if smaller gap is left
        if gap_sizes[matching_gap] > file_size:
            leftover_gap_size = gap_sizes[matching_gap] - file_size
            leftover_gap_start = matching_gap + file_size
            gap_sizes[leftover_gap_start] = leftover_gap_size
        del gap_sizes[matching_gap]

    part2 = sum(
        pos * file_id
        for file_id, bounds in blocks.items()
        for pos in range(bounds[0], bounds[1] + 1)
    )

    return part1, part2


if __name__ == "__main__":
    testinp = open('day09.testinp').read()
    print(day09(testinp))
    inp = open('day09.inp').read()
    print(day09(inp))
