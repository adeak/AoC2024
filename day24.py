from collections import defaultdict
from graphlib import TopologicalSorter


def day24(inp, only_part1=False, testing=False):
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

    # part 1: solve original input
    wires = generate_lines(wires, gates, dependencies)
    part1 = wires_to_int(wires, 'z')

    if only_part1:
        return part1, None

    # hacky, hand-crafted part 2
    # step 1: look at the rough structure to find some misplaced wires
    gates_var = defaultdict(list)
    for output, (op1, operation, op2) in gates.items():
        gates_var[tuple(sorted([op1, op2]))].append((operation, output))
    misplaced_wires = set()
    for key, val in sorted(gates_var.items()):
        # look at print(key, val) here to see what kind of mismatches we're looking for here
        if key[0].startswith(('x', 'y')):
            # neither AND nor XOR output must contain z except x00 XOR y00 -> z00
            for gate_type, output in val:
                if output.startswith('z') and output != 'z00':
                    misplaced_wires.add(output)
        elif len(val) == 2:
            # AND and XOR, exactly XOR must output to z
            val = dict(val)
            if val['AND'].startswith('z'):
                misplaced_wires.add(val['AND'])
            if not val['XOR'].startswith('z'):
                misplaced_wires.add(val['XOR'])
        else:
            # single OR, should not contain 'z' except z45 (final carry bit)
            if val[0][1].startswith('z') and val[0][1] != 'z45':
                misplaced_wires.add(val[0][1])
    # misplaced_wires contains 6 out of 8 misplaced keys with my input

    # step 2: start finding problematic wires from the input end
    num_bits = int(max(wire for wire in wires if wire.startswith('x'))[1:]) + 1  # input bit size
    for index in range(1, num_bits):  # x00 XOR y00 -> z00 still special-cased
        inp_wires = {f'x{index:02}', f'y{index:02}'}
        # XOR should go into a XOR should go into z{index}
        xor_wire = next(wire for wire, gate in gates.items() if set(gate) == inp_wires | {'XOR'})
        if xor_wire.startswith('z'):
            # this can't be right
            misplaced_wires.add(xor_wire)
        else:
            # this XOR should go into a XOR and an AND
            downstream_gates = [
                {wire: gate}
                for wire, gate in gates.items()
                if xor_wire in [gate[0], gate[2]]
            ]
            downstream_types = [next(iter(gate_dict.values()))[1] for gate_dict in downstream_gates]
            if set(downstream_types) != {'XOR', 'AND'}:
                misplaced_wires.add(xor_wire)

        # AND should go into an OR for carry
        and_wire = next(wire for wire, gate in gates.items() if set(gate) == inp_wires | {'AND'})
        if and_wire.startswith('z'):
            # this can't be right
            misplaced_wires.add(and_wire)
        else:
            # this AND should go into an OR
            downstream_gates = [
                {wire: gate}
                for wire, gate in gates.items()
                if and_wire in [gate[0], gate[2]]
            ]
            downstream_types = [next(iter(gate_dict.values()))[1] for gate_dict in downstream_gates]
            if downstream_types != ['OR']:
                misplaced_wires.add(and_wire)
    # now we happen to have all 8 misplaced wires for my input
    assert len(misplaced_wires) == 8
    return part1, ','.join(sorted(misplaced_wires))
    
    # (if this weren't enough, we'd also have to start looking from the output end,
    #  just watch out because z00 and z45 have to be special-cased)


def generate_lines(wires, gates, dependencies):
    ops = {
        'AND': lambda op1, op2: op1 & op2,
        'OR': lambda op1, op2: op1 | op2,
        'XOR': lambda op1, op2: op1 ^ op2,
    }

    outputs = wires.copy()
    toposorter = TopologicalSorter(dependencies)
    for output_wire in toposorter.static_order():
        if output_wire not in dependencies:
            # input wire, ignore
            continue
        op1, operator, op2 = gates[output_wire]
        outputs[output_wire] = ops[operator](outputs[op1], outputs[op2])
    return outputs


def wires_to_int(wires, prefix):
    digits = [
        str(wires[wire])
        for wire in sorted(wires, reverse=True)
        if wire.startswith(prefix)
    ]
    return int(''.join(digits), 2)


def int_to_bits(num, num_bits):
    return list(map(int, bin(num)[2:].zfill(num_bits)))


if __name__ == "__main__":
    testinp = open('day24.testinp').read()
    print(day24(testinp, only_part1=True)[0])
    inp = open('day24.inp').read()
    print(day24(inp))
