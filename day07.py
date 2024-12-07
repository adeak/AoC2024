from itertools import product
import operator


def day07(inp, part2=False):
    equations = inp.strip().splitlines()

    ops = {
        '+': operator.add,
        '*': operator.mul,
    }
    if part2:
        ops['||'] = lambda first, second: int(str(first) + str(second))

    result = 0
    for equation in equations:
        target, *operands = equation.split()
        target, *operands = map(int, [target[:-1], *operands])

        num_ops = len(operands) - 1
        for current_ops in product(ops.keys(), repeat=num_ops):
            value, *rest = operands
            for current_op, next_value in zip(current_ops, rest):
                value = ops[current_op](value, next_value)
            if value == target:
                result += target
                break
            else:
                # no luck
                continue
            # we had a match
            break

    return result


if __name__ == "__main__":
    testinp = open('day07.testinp').read()
    print(day07(testinp), day07(testinp, part2=True))
    inp = open('day07.inp').read()
    print(day07(inp), day07(inp, part2=True))
