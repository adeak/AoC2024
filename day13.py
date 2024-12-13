def day13(inp, part2=False):
    blocks = inp.strip().split('\n\n')

    result = 0
    for block in blocks:
        *button_lines, prize_line = block.splitlines()
        # not using numpy because native ints are safest (and things like np.linalg.det return doubles)
        button_matrix =[
            [int(item.removesuffix(', Y')) for item in line.split('+')[-2:]]
            for line in button_lines
        ]
        target = [int(item.removesuffix(', Y')) for item in prize_line.split('=')[-2:]]
        if part2:
            target = [value + 1000_000_000_0000 for value in target]

        # Cramer's rule, need transpose of button matrix
        a_numerator = target[0]*button_matrix[1][1] - button_matrix[1][0] * target[1]
        b_numerator = button_matrix[0][0] * target[1] - target[0]*button_matrix[0][1]
        denominator = button_matrix[0][0] * button_matrix[1][1] - button_matrix[0][1] * button_matrix[1][0]

        a_press, a_rem = divmod(a_numerator, denominator)
        b_press, b_rem = divmod(b_numerator, denominator)
        if a_rem != 0 or b_rem != 0:
            continue
        result += 3*a_press + b_press

    return result

if __name__ == "__main__":
    testinp = open('day13.testinp').read()
    print(day13(testinp), day13(testinp, part2=True))
    inp = open('day13.inp').read()
    print(day13(inp), day13(inp, part2=True))
