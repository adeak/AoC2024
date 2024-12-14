from collections import Counter
from itertools import count
import math
import re


def day14(inp, size=(101, 103), testing=False):
    data = inp.splitlines()
    pattern = re.compile('^p=([-0-9]+),([-0-9]+) v=([-0-9]+),([-0-9]+)$')

    robots = []
    for line in data:
        px, py, vx, vy = map(int, pattern.match(line).groups())
        pos = [px, py]
        v = vx, vy
        robots.append((pos, v))

    for step in count(1):
        for robot in robots:
            pos, v = robot
            pos[0] = (pos[0] + v[0]) % size[0]
            pos[1] = (pos[1] + v[1]) % size[1]

        if step == 100:
            # part 1
            quadrant_counts = Counter()
            for pos, _ in robots:
                if pos[0] == size[0] // 2 or pos[1] == size[1] // 2:
                    # "middle" row or column
                    continue
                quadrant_counts[pos[0] < size[0] // 2, pos[1] < size[1] // 2] += 1
            part1 = math.prod(quadrant_counts.values())
            if testing:
                # no part 2
                part2 = None
                break
        if testing:
            # no part 2
            continue

        # part 2: try to check if none of the robots overlap
        if len({tuple(pos) for pos, _ in robots}) == len(robots):
            # import numpy as np
            # import matplotlib.pyplot as plt
            #
            # image = np.zeros(size, dtype=np.uint8)
            # for pos, _ in robots:
            #     image[tuple(pos)] += 1
            # plt.imshow(image.T)
            # plt.show()
            part2 = step
            break

    return part1, part2

if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(day14(testinp, size=(11, 7), testing=True))
    inp = open('day14.inp').read()
    print(day14(inp))
