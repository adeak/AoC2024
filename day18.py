from heapq import heappop, heappush

from day10 import get_neighbs


def day18(inp, size=71, part1_count=1024):
    byte_poses = [tuple(map(int, line.split(','))) for line in inp.splitlines()]
    start = (0, 0)
    target = (size - 1, size - 1)

    for byte_count in range(part1_count, len(byte_poses)):
        walls = set(byte_poses[:byte_count])
        state = (0, start)
        states = [state]  # heapq
        best_scores = {start: 0}  # pos -> best score
        while states:
            score, pos = heappop(states)

            for next_pos in get_neighbs(pos, (size, size)):
                next_score = score + 1
                if next_pos == target:
                    # we're done
                    if byte_count == part1_count:
                        part1 = next_score
                    break

                if next_pos in walls:
                    # can't go there
                    continue

                if next_score >= best_scores.get(next_pos, float('inf')):
                    # already here before
                    continue

                best_scores[next_pos] = next_score
                heappush(states, (next_score, next_pos))
            else:
                continue
            # exit found
            break
        else:
            # part 2 done
            part2 = ','.join(map(str, byte_poses[byte_count - 1]))
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp, size=7, part1_count=12))
    inp = open('day18.inp').read()
    print(day18(inp))
