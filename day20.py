from collections import defaultdict, Counter
from functools import cache
from heapq import heapify, heappush, heappop
from itertools import count

import numpy as np

from day10 import get_neighbs


def day20(inp, part1=True, minimum_savings=100):
    board = np.array([list(row) for row in inp.splitlines()])
    shape = board.shape
    start = tuple(np.array((board == 'S').nonzero()).ravel())
    target = tuple(np.array((board == 'E').nonzero()).ravel())
    walls = frozenset(zip(*np.array((board == '#').nonzero()).reshape(2, -1)))

    teleport_radius = 2 if part1 else 20

    # pre-processing: map out teleportation options within teleport_radius Manhattan distance
    i, j = np.mgrid[: teleport_radius+1, -teleport_radius : teleport_radius+1]
    valid_mask = (abs(i) + abs(j) >= 2) & (abs(i) + abs(j) <= teleport_radius)
    deltas = list(zip(i[valid_mask], j[valid_mask]))
    teleport_options = defaultdict(set)  # start -> set of end positions
    for i in range(shape[0]):
        for j in range(shape[1]):
            start_pos = i, j
            if start_pos in walls:
                continue
            for di, dj in deltas:
                end_pos = i + di, j + dj
                if end_pos in walls:
                    continue
                if not (0 <= end_pos[0] < shape[0] and 0 <= end_pos[1] < shape[1]):
                    continue
                teleport_options[start_pos].add(end_pos)
                teleport_options[end_pos].add(start_pos)

    # walk the maze from the end to compute distance for each position
    raw_times = walk_maze(target, walls, shape)
    base_time = raw_times[start]

    # walk the maze with teleportation options, make teleport option a part of the state
    unset_teleport_item = ((-1, -1), (-1, -1))  # need valid tuple vs tuple comparison for heapq
    state = (0, start, unset_teleport_item)  # (cost, position, (teleportation start, end))
    states = [state]  # heapq
    best_scores = {state[1:]: 0}  # (pos, teleport pair) -> best score
    while states:
        score, pos, used_teleport = heappop(states)

        if used_teleport is not unset_teleport_item:
            # we've already teleported, rest of the walk is vanilla
            cost = score + raw_times[pos]
            if cost > base_time - minimum_savings:
                # uninteresting result
                continue
            
            best_scores[target, used_teleport] = cost
            continue

        # continue non-teleport paths
        base_neighbs = [
            next_pos for next_pos in get_neighbs(pos, shape)
            if next_pos not in walls
        ]
        next_states = [(next_pos, used_teleport) for next_pos in base_neighbs]

        # we can also teleport now
        next_teleports = teleport_options[pos]
        for end_pos in next_teleports:
            next_states.append((end_pos, (pos, end_pos)))

        # generate all end states after step/teleport
        for next_state in next_states:
            next_pos, used_teleport = next_state
            next_score = score + abs(next_pos[0] - pos[0]) + abs(next_pos[1] - pos[1])
            if next_score > base_time - minimum_savings:
                # uninteresting path
                continue

            if next_pos == target:
                # we're done with this path
                best_scores[target, used_teleport] = next_score
                continue

            if next_score >= best_scores.get(next_state, float('inf')):
                # already here before with better score
                continue

            best_scores[next_state] = next_score
            heappush(states, (next_score, next_pos, used_teleport))

    # gather savings from best_scores[(target, *)]
    savings = sum(
        1
        for (pos, used_teleport), score in best_scores.items()
        if pos == target and used_teleport is not unset_teleport_item
    )
    return savings


def walk_maze(target, walls, shape):
    # walk the maze starting from the end to compute distance from all positions
    raw_times = {}
    seens = set()
    edges = {target}
    for distance in count():
        next_edges = set()
        for edge in edges:
            seens.add(edge)
            raw_times[edge] = distance

            for next_edge in get_neighbs(edge, shape):
                if next_edge in seens | walls:
                    # don't go there
                    continue
                next_edges.add(next_edge)
        edges = next_edges
        if not edges:
            break
    return raw_times


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(day20(testinp, minimum_savings=0), day20(testinp, part1=False, minimum_savings=50))
    inp = open('day20.inp').read()
    print(day20(inp), day20(inp, part1=False))
