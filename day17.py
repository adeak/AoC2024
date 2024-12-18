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

    # part 2: look for a quine (runs too long for production input)
    for A_init in count(1):
        registers = original_registers.copy()
        registers[0] = A_init
        outputs = []
        execute_program(find_quine=True)
        if outputs == program:
            part2 = A_init
            break

    return part1, part2


def day17_special(inp):
    # hand-crafted part 2 for specific real input
    program_line = inp.strip().split('\n\n')[-1]
    program = list(map(int, program_line.split()[-1].split(',')))

    # The program looks something like this (your mileage may vary):
    #
    # def execute_program(A):
    #     outputs = []
    #     while True:
    #         B = (A % 8) ^ 3
    #         C = A // 2**B
    #         B = (B ^ 5) ^ C
    #         outputs.append(B % 8)
    #         A //= 8
    #         if A == 0:
    #             return outputs
    #
    # So in each iteration B and C are computed from scratch, and A is divided by 8.
    # We could almost compute A iteration by iteration from the output's end,
    # multiplying the previous iteration's A value by 8 and trying different
    # remainders (mod 8), but `C = A // 2**B` can pick up contributions from
    # future iterations of this process. So instead we need to increase octal
    # digits for A digit by digit until we hit each output (still starting from
    # the back), and backtracking when we run out of octal digits in a given
    # position. What we have to be careful about is that after backtracking we
    # might end up breaking output digits that were correct earlier, so we need to
    # recheck the output from the start (actually: end) to make sure we catch
    # errors arising from this.

    octal_digits = [0] * len(program)
    octal_digits[0] = 1
    i = 0
    while i < len(octal_digits):
        output = program[::-1][i]
        while True:
            A = sum(value * 8**i for i, value in enumerate(octal_digits[: i + 1][::-1]))

            B = (A % 8) ^ 3
            C = A // 2**B
            if (B ^ 5 ^ C) % 8 == output:
                # we have a hit, advance to next digit
                i += 1
                break

            # we missed, increment digits
            octal_digits[i] += 1

            # check if we've run out of digits, carry the one
            need_to_backtrack = False
            while octal_digits[i] == 8:
                need_to_backtrack = True
                i -= 1
                if i < 0:
                    raise AssertionError('Ran out of digits during backtracking')
                octal_digits[i] += 1
                for j in range(i + 1, len(octal_digits)):
                    octal_digits[j] = 0

            if need_to_backtrack:
                # reset digit pointer because we could've messed up earlier digits
                i = 0
                break

    A = sum(value * 8**i for i, value in enumerate(octal_digits[::-1]))
    part2 = A
    return part2


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    testinp2 = open('day17.testinp2').read()
    print(day17(testinp, only_part1=True)[0], day17(testinp2)[1])
    inp = open('day17.inp').read()
    print(day17(inp, only_part1=True)[0], day17_special(inp))
