from collections import defaultdict, Counter
from itertools import combinations, product


def day21(inp, part1=True):
    codes = inp.splitlines()

    door_map = {
        (0, 0): 'A',
        (0, -1): '0',
        (-1, 0): '3',
        (-1, -1): '2',
        (-1, -2): '1',
        (-2, 0): '6',
        (-2, -1): '5',
        (-2, -2): '4',
        (-3, 0): '9',
        (-3, -1): '8',
        (-3, -2): '7',
    }
    robot_map = {
        (0, 0): 'A',
        (0, -1): '^',
        (1, 0): '>',
        (1, -1): 'v',
        (1, -2): '<',
    }

    door_transfer = get_transitions(door_map)
    robot_transfer = get_transitions(robot_map)

    if part1:
        robot_transfer_count = 2
    else:
        robot_transfer_count = 25

    # only keep relevant door transfers
    final_door_transfer = {}
    for code in codes:
        for start_key, end_key in zip('A' + code, code):
            final_door_transfer[start_key, end_key] = door_transfer[start_key, end_key]
    door_transfer = final_door_transfer

    result = 0
    for code in codes:
        # for each code generate all possible binary path choices
        lowest_complexity = float('inf')
        for door_transfer_values in product(*door_transfer.values()):
            door_transfer_now = dict(zip(door_transfer, door_transfer_values))
            for robot_transfer_values in product(*robot_transfer.values()):
                robot_transfer_now = dict(zip(robot_transfer, robot_transfer_values))

                transfers = [door_transfer_now] + [robot_transfer_now] * robot_transfer_count

                path_counts = find_path_counts(code, transfers)
                path_length = sum(path_counts.values())  # fencepost minus implicit starting A
                complexity = int(code.rstrip('A')) * path_length
                if complexity < lowest_complexity:
                    lowest_complexity = complexity
        result += lowest_complexity

    return result


def get_transitions(coords):
    """Generate potential robot arm move instructions for any two buttons.

    Parameters
    ----------
    coords : dict[tuple, str]
        Key coordinates, keys are positions and values are the key
        label.

    Returns
    -------
    dict[tuple, list]
        Mapping from (start key, end key) tuples to a list of potential
        shortest moves from the start key to the end key. The final 'A'
        key is not included in the strings.
    """
    deltas = {
        'v': (1, 0),
        '^': (-1, 0),
        '>': (0, 1),
        '<': (0, -1),
    }
    reverses = dict(zip('v^><', '^v<>'))
    transfer = defaultdict(list)
    for start, end in combinations(coords, 2):
        start_key = coords[start]
        end_key = coords[end]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        vertical_dir = 'v' if dx > 0 else '^'
        horizontal_dir = '>' if dy > 0 else '<'
        vertical_part = vertical_dir * abs(dx)
        horizontal_part = horizontal_dir * abs(dy)
        paths = {vertical_part + horizontal_part, horizontal_part + vertical_part}
        if len(paths) == 1:
            # no-brainer
            path = paths.pop()
            transfer[start_key, end_key].append(path)
            transfer[end_key, start_key].append(''.join([reverses[c] for c in path[::-1]]))
            continue

        # check if any of the two options are invalid
        for path in paths:
            pos = start
            for step_dir in path:
                delta = deltas[step_dir]
                pos = pos[0] + delta[0], pos[1] + delta[1]
                if pos not in coords:
                    break
            else:
                transfer[start_key, end_key].append(path)
                transfer[end_key, start_key].append(''.join([reverses[c] for c in path[::-1]]))
    return dict(transfer)


def find_path_counts(code, transfers):
    """Generate a code through a series of keyboard transitions.

    Parameters
    ----------
    code : str
        The final target.

    transfers : list[dict]
        A list of transitions from `get_transitions()` corresponding to
        the order in which the paths have to be encoded.

    Returns
    -------
    collections.Counter
        The path section frequencies on the first keypad (corresponding
        to the last transfer mapping).
    """
    section_counts = Counter()
    target = code
    for section in zip('A' + code[:-1], code):
        section_counts[section] += 1
    for i, transfer in enumerate(transfers):
        next_section_counts = Counter()
        for section, multiplicity in section_counts.items():
            # watch out for missing (thing, thing) pairs
            subpath = transfer.get(section, '') + 'A'
            for next_section in zip('A' + subpath, subpath):
                next_section_counts[next_section] += multiplicity
        section_counts = next_section_counts

    return section_counts


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp), day21(testinp, part1=False))
    inp = open('day21.inp').read()
    print(day21(inp), day21(inp, part1=False))
