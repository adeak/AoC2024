def day17(inp):
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

    def execute_program(skip_jump=False):
        ip = 0
        while 0 <= ip < len(program) - 1:
            instr, op = program[ip], program[ip + 1]
            fun = instructions[instr]
            jmp_target = fun(op)

            # advance instruction pointer
            if skip_jump:
                ip += 2
            else:
                ip = jmp_target if jmp_target is not None else ip + 2

    # part 1: execute with given A value
    original_registers = registers.copy()
    execute_program()
    part1 = ','.join(map(str, outputs))

    # partially generalized hand-crafted part 2

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

    # try to make some assumptions that might work for other inputs
    no_B_C = original_registers[1] == original_registers[2] == 0
    single_out = program[::2].count(5) == 1
    loop_while_A = program[-2:] == [3, 0]
    A_div_const = program[::2].count(0) == 1 and program[2*program[::2].index(0) + 1] < 4
    if not (no_B_C and single_out and loop_while_A and A_div_const):
        # slim chance of the solution working for this input
        return part1, None
    divisor = 2**program[2*program[::2].index(0) + 1]  # base for digits of A

    digits = [0] * len(program)
    digits[0] = 1
    i = 0
    while i < len(digits):
        output = program[::-1][i]
        while True:
            A = sum(value * divisor**i for i, value in enumerate(digits[: i+1][::-1]))
            registers = [A, 0, 0]
            outputs = []
            execute_program(skip_jump=True)
            if outputs[-1] == output:
                # we have a hit, advance to next digit
                i += 1
                break

            # we missed, increment digits
            digits[i] += 1

            # check if we've run out of digits, carry the one
            need_to_backtrack = False
            while digits[i] == divisor:
                need_to_backtrack = True
                i -= 1
                if i < 0:
                    # no solution with this input and heuristic
                    return part1, None

                digits[i] += 1
                for j in range(i + 1, len(digits)):
                    digits[j] = 0

            if need_to_backtrack:
                # reset digit pointer because we could've messed up earlier digits
                i = 0
                break

    A = sum(value * divisor**i for i, value in enumerate(digits[::-1]))
    part2 = A
    return part1, part2


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    print(day17(testinp))
    testinp2 = open('day17.testinp2').read()
    print(day17(testinp2))
    inp = open('day17.inp').read()
    print(day17(inp))
