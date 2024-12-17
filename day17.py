from itertools import count


def day17(inp, only_part1=False):
    register_block, program_line = inp.strip().split('\n\n')

    registers = [int(line.split()[-1]) for line in register_block.splitlines()]
    program = list(map(int, program_line.split()[-1].split(',')))
    outputs = []

    def combo_op(op):
        if 0 <= op <= 3:
            return op
        if op >= 7:
            raise AssertionError('Hey!')
        return registers[op - 4]

    def adv(op):
        registers[0] = int(registers[0] / 2**combo_op(op))

    def bxl(op):
        registers[1] ^= op

    def bst(op):
        registers[1] = combo_op(op) % 8

    def jnz(op):
        if registers[0] == 0:
            return None
        return op

    def bxc(op):
        registers[1] ^= registers[2]

    def out(op):
        outputs.append(combo_op(op) % 8)
    
    def bdv(op):
        registers[1] = int(registers[0] / 2**combo_op(op))

    def cdv(op):
        registers[2] = int(registers[0] / 2**combo_op(op))

    instructions = [
        adv,
        bxl,
        bst,
        jnz,
        bxc,
        out,
        bdv,
        cdv,
    ]

    def execute_program(find_quine=False):
        ip = 0
        while 0 <= ip < len(program) - 1:
            instr, op = program[ip], program[ip + 1]
            fun = instructions[instr]
            jmp_target = fun(op)

            # early break for part 2
            if find_quine and fun.__name__ == "out" and outputs != program[:len(outputs)]:
                break

            # advance instruction pointer
            ip = jmp_target if jmp_target is not None else ip + 2

    # part 1: execute with given A value
    original_registers = registers.copy()
    execute_program()
    part1 = ','.join(map(str, outputs))
    if only_part1:
        return part1, None

    # part 2: look for a quine
    for A_init in count(1):
        registers = original_registers.copy()
        registers[0] = A_init
        outputs = []
        execute_program(find_quine=True)
        if outputs == program:
            part2 = A_init
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    testinp2 = open('day17.testinp2').read()
    print(day17(testinp, only_part1=True)[0], day17(testinp2)[1])
    inp = open('day17.inp').read()
    print(day17(inp))
