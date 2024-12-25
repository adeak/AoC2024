from collections import defaultdict
from graphlib import TopologicalSorter


def day24(inp):
    inputs, gate_block = inp.strip().split('\n\n')

    wires = defaultdict(lambda: None)
    for inp in inputs.splitlines():
        wire, val = inp.split(': ')
        wires[wire] = int(val)

    gates = {}
    dependencies = defaultdict(set)
    for gate_line in gate_block.splitlines():
        *gate_data, output = gate_line.replace('-> ', '').split()  # op1 OP op2 output
        gates[output] = gate_data
        dependencies[output] |= {gate_data[0], gate_data[2]}

    ops = {
        'AND': lambda op1, op2: op1 & op2,
        'OR': lambda op1, op2: op1 | op2,
        'XOR': lambda op1, op2: op1 ^ op2,
    }

    toposorter = TopologicalSorter(dependencies)
    for output_wire in toposorter.static_order():
        if output_wire not in dependencies:
            # input wire, ignore
            continue
        op1, operator, op2 = gates[output_wire]
        wires[output_wire] = ops[operator](wires[op1], wires[op2])

    part1 = int(''.join(str(wires[wire]) for wire in sorted(wires, reverse=True) if wire.startswith('z')), 2)

    part2 = None
    return part1, part2


if __name__ == "__main__":
    testinp = open('day24.testinp').read()
    print(day24(testinp))
    inp = open('day24.inp').read()
    print(day24(inp))
