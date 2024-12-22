from collections import defaultdict
from itertools import combinations


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

    transfers = [door_transfer, robot_transfer, robot_transfer]#, robot_transfer]
    result = 0
    for code in codes:
        path = find_path(code, transfers)
        complexity = int(code.rstrip('A')) * len(path)
        result += complexity

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


def find_path(code, transfers):
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
    str
        The shortest path on the first keypad (corresponding to the last
        transfer mapping).
    """
    targets = [code]
    for transfer in transfers:
        # filter targets for shortest transfer in this step
        shortests = []
        best_cost = float('inf')
        for target in targets:
            char = 'A'
            cost = 0
            for next_char in target:
                cost += len(transfer.get((char, next_char), [''])[0]) + 1  # account for "A"
            if cost > best_cost:
                continue
            if cost == best_cost:
                # add this contender
                shortests.append(target)
            else:
                # discard earlier winners
                shortests = [target]

        targets = shortests

        all_paths = []
        for target in targets:
            char = 'A'
            paths = ['']
            for next_char in target:
                # watch out for missing (thing, thing) pairs
                subpaths = transfer.get((char, next_char), [''])
                paths = [
                    path + subpath + 'A'
                    for path in paths
                    for subpath in subpaths
                ]
                char = next_char
        
            # # always keep all the shortest paths in each step
            # shortest_new_length = min(len(s) for s in paths)
            # old_length = float('inf') if not all_paths else len(all_paths[0])
            # shortest_length = min(old_length, shortest_new_length)
            # all_paths = [
            #     path
            #     for path in all_paths + paths
            #     if len(path) == shortest_length
            # ]
            all_paths.extend(paths)
        targets = all_paths
    target = min(targets, key=len)

    return target


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp))#, day21(testinp, part1=False))
    inp = open('day21.inp').read()
    # not deterministic, run several times for minimum...
    print(day21(inp))#, day21(inp, part1=False))
