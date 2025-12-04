import path
import sys

# setting path for reading input files
directory = path.Path(__file__).parent
sample_input = directory / "sample_input"
problem_input = directory / "input"


def get_lines(file_path):
    """Read input file"""
    out = []
    with open(file_path) as f:
        line = f.readline().strip()
        while line:
            out.append(line)
            line = f.readline().strip()
    return out


def biggest_joltage(battery_line, n_digits):
    """Finds the biggest joltage with n_digits in the given battery_line, which is a string of digits."""

    # Find the biggest digit, leaving room for the remaining digits.
    dig = 0
    dig_i = 0
    for i in range(len(battery_line) - (n_digits - 1)):
        dig_val = int(battery_line[i])
        if dig_val == 9:
            dig = 9
            dig_i = i
            break
            # The left most 9 is the biggest possible
        if dig_val > dig:
            dig = dig_val
            dig_i = i

    rem_digits = n_digits - 1
    joltage = dig * 10 ** (n_digits - 1)
    if rem_digits > 0:
        joltage += biggest_joltage(battery_line[dig_i + 1:], rem_digits)
    return joltage


if __name__ == "__main__":

    print("AoC Day 03.")

    input_file = problem_input
    if len(sys.argv) == 2:
        if '-sample' in sys.argv:
            input_file = sample_input
        else:
            print(f"'{sys.argv[1]}' not recognized.")
    elif len(sys.argv) > 2:
        print("Too many arguments. Use: python D03 [-sample]")

    lines = get_lines(input_file)

    ans1 = 0
    for line in lines:
        ans1 += biggest_joltage(line, 2)
    print(f"Part 1: {ans1}")

    ans2 = 0
    for line in lines:
        ans2 += biggest_joltage(line, 12)
    print(f"Part 2: {ans2}")


