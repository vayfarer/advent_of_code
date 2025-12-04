from utility import get_lines, input_arg_parse


def biggest_joltage(battery_line, n_digits):
    """Finds the biggest joltage with n_digits in the given battery_line, which is a string of digits."""

    # Find the leftmost biggest digit, leaving room for the remaining digits.
    dig = 0
    dig_i = 0
    rem_digits = n_digits - 1
    for i in range(len(battery_line) - rem_digits):
        dig_val = int(battery_line[i])
        if dig_val > dig:
            dig = dig_val
            dig_i = i

    joltage = dig * 10 ** rem_digits
    if rem_digits > 0:
        joltage += biggest_joltage(battery_line[dig_i + 1:], rem_digits)
    return joltage


if __name__ == "__main__":
    print("AoC Day 03.")
    input_file = input_arg_parse()
    lines = get_lines(input_file)

    ans1 = 0
    for line in lines:
        ans1 += biggest_joltage(line, 2)
    print(f"Part 1: {ans1}")

    ans2 = 0
    for line in lines:
        ans2 += biggest_joltage(line, 12)
    print(f"Part 2: {ans2}")


