from utility import get_lines, input_arg_parse


def operate(op, num_list):
    """Runs an addition or multiplication operation across all members of a list"""
    if len(num_list) == 0:
        return 0

    subtotal = num_list[0]
    if op == "*":
        for i in range(1, len(num_list)):
            subtotal *= num_list[i]
    elif op == "+":
        for i in range(1, len(num_list)):
            subtotal += num_list[i]
    return subtotal


if __name__ == "__main__":
    print("AoC Day 06.")
    input_file = input_arg_parse()
    lines = get_lines(input_file)

    ops = lines[-1].split()

    num_lists = [[] for _ in range(len(ops))]
    for line in lines[0:-1]:
        for i, num in enumerate(line.split()):
            num_lists[i].append(int(num))

    ans1 = 0
    for i in range(len(num_lists)):
        ans1 += operate(ops[i], num_lists[i])
    print(f"Part 1: {ans1}")

    ans2 = 0
    op_line = lines[-1]
    op_idx_list = []
    num_lines = lines[:-1]

    for idx, op in enumerate(op_line):
        if op != ' ':
            op_idx_list.append((idx, op))

    for i, idx_op in enumerate(op_idx_list):
        first_idx, op = idx_op
        if i < len(op_idx_list) - 1:
            next_idx = op_idx_list[i + 1][0] - 1
        else:
            next_idx = len(op_line)

        num_list = []
        for num_idx in range(first_idx, next_idx):
            num_str = ''.join([line[num_idx] for line in num_lines])
            num_list.append(int(num_str))

        ans2 += operate(op, num_list)

    print(f"Part 2: {ans2}")
