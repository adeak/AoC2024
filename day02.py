import numpy as np


def day02(inp):
    reports = [
        list(map(int, line.split()))
        for line in inp.strip().splitlines()
    ]

    safe_count = semisafe_count = 0
    for report in reports:
        for drop_index in range(len(report) + 1)[::-1]:
            diffs = np.diff(report[:drop_index] + report[drop_index + 1 : ])
            diffsigns = set(np.sign(diffs))
            if diffsigns != {-1} and diffsigns != {1}:
                # non-monotonic
                continue
            if (abs(diffs) > 3).any():
                # too large diff
                continue
            # if we're here we're (semi)safe
            if drop_index == len(report):
                safe_count += 1
            else:
                semisafe_count += 1
            break

    return safe_count, safe_count + semisafe_count


if __name__ == "__main__":
    testinp = open('day02.testinp').read()
    print(day02(testinp))
    inp = open('day02.inp').read()
    print(day02(inp))
