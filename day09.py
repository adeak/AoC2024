from itertools import count


def day09(inp, part1=True):
    data = inp.strip()

    blocks = {}  # file_id -> (start, end)
    gaps = {}  # gap_id -> (start, end)
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
        bounds = pos, pos + gap_size - 1  # inclusive
        pos += gap_size
        gaps[file_id] = bounds

    if part1:
        poses = {
            pos: file_id
            for file_id, bounds in blocks.items()
            for pos in range(bounds[0], bounds[1] + 1)
        }
        poses.update({
            pos: None
            for file_id, bounds in gaps.items()
            for pos in range(bounds[0], bounds[1] + 1)
        })

        for file_id in range(max(blocks), -1, -1):
            bounds = blocks[file_id]
            for pos in range(bounds[1], bounds[0] - 1, -1):
                try:
                    new_pos = min(item for item in poses.items() if item[1] is None)[0]
                except ValueError:
                    new_pos = float('inf')
                if new_pos > pos:
                    # we're done
                    poses = {pos: val for pos, val in poses.items() if val is not None}
                    result = sum(key * value for key, value in poses.items())
                    return result

                del poses[pos]
                poses[new_pos] = file_id

    # part 2
    gap_sizes = {bounds[0]: bounds[1] - bounds[0] + 1 for bounds in gaps.values()}
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

        # add new gap and merge gaps around old position
        gap_sizes[bounds[0]] = file_size
        current_gap, *rest = sorted(gap_sizes)
        current_gap_size = gap_sizes[current_gap]
        for next_gap in rest:
            if next_gap == current_gap + gap_sizes[current_gap]:
                # merge
                current_gap_size += gap_sizes[next_gap]
                continue
            gap_sizes[current_gap] = current_gap_size
        gap_sizes[current_gap] = current_gap_size

    poses = {
        pos: file_id
        for file_id, bounds in blocks.items()
        for pos in range(bounds[0], bounds[1] + 1)
    }
    result = sum(key * value for key, value in poses.items())
    return result


if __name__ == "__main__":
    testinp = open('day09.testinp').read()
    print(day09(testinp), day09(testinp, part1=False))
    inp = open('day09.inp').read()
    print(day09(inp), day09(inp, part1=False))
