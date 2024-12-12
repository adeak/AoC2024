from collections import defaultdict

import numpy as np
import scipy.ndimage as ndi


def day12(inp):
    garden = np.array([list(line) for line in inp.splitlines()])
    kinds = np.unique(garden)

    part1 = 0
    part2 = 0
    for kind in kinds:
        subgarden = garden == kind
        # pad with a layer of zeros for outer fence calculation
        subgarden = np.pad(subgarden, 1)
        labels, num_features = ndi.label(subgarden)

        areas = defaultdict(int)  # feature index -> area
        perimeters = defaultdict(int)  # feature index -> perimeter
        # go along rows first and compute area + perimeter (part 1)
        for i in range(labels.shape[0]):
            last_value = None
            for j in range(labels.shape[1]):
                value = labels[i, j]
                areas[value] += 1
                if last_value != value:
                    perimeters[last_value] += 1
                    perimeters[value] += 1
                last_value = value

        # now go along columns for final perimeter count (part 1)
        for j in range(labels.shape[1]):
            last_value = None
            for i in range(labels.shape[0]):
                value = labels[i, j]
                if last_value != value:
                    perimeters[last_value] += 1
                    perimeters[value] += 1
                last_value = value

        # delete bogus 0 counts
        del areas[0], perimeters[0]

        # part 2: find surrounding pixels, deduce boundary sections, then build edges
        labels = np.pad(labels, 1)
        edge_coords = defaultdict(set)  # label -> oriented (start, end) coordinates
        for label in range(1, num_features + 1):
            subsubgarden = labels == label
            dilated = ndi.binary_dilation(subsubgarden)
            outer_pixels = dilated ^ subsubgarden

            # for each outer pixel look around and identify relevant edges
            for i, j in np.array(outer_pixels.nonzero()).T:
                # watch out for orientation; always list coordinates counter-clockwise
                if labels[i + 1, j] == label:
                    # edge below
                    edge_coords[label].add(((i, j), (i, j + 1)))
                if labels[i - 1, j] == label:
                    # edge above
                    edge_coords[label].add(((i - 1, j + 1), (i - 1, j)))
                if labels[i, j + 1] == label:
                    # edge to the right
                    edge_coords[label].add(((i, j + 1), (i - 1, j + 1)))
                if labels[i, j - 1] == label:
                    # edge to the left
                    edge_coords[label].add(((i - 1, j), (i, j)))

        # now for each region assemble edges
        corners = defaultdict(int)  # label -> number of corners/"sides" of edges
        for label, edge_bag in edge_coords.items():
            edges = edge_bag.copy()
            path = []
            while edges:
                if not path:
                    start = edges.pop()
                    path.append(start)
                    last_delta = tuple(np.array(start[1]) - start[0])
                    continue

                next_edge = next(edge for edge in edges if path[-1][-1] == edge[0])
                edges.remove(next_edge)
                path.append(next_edge)

                # check if we have a new corner
                delta = tuple(np.array(next_edge[1]) - next_edge[0])
                if delta != last_delta:
                    corners[label] += 1
                last_delta = delta

                # check if we closed a loop
                if path[-1][-1] == path[0][0]:
                    # check last potential corner
                    first_delta = tuple(np.array(path[0][1]) - path[0][0])
                    if first_delta != delta:
                        corners[label] += 1
                    # start a new path
                    path = []
                    continue

        part1 += sum(areas[label] * perimeters[label] for label in areas)
        part2 += sum(areas[label] * corners[label] for label in areas)

    return part1, part2

if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp))
    testinp2 = open('day12.testinp2').read()
    print(day12(testinp2))
    inp = open('day12.inp').read()
    print(day12(inp))
